#!/bin/bash
# check-agents.sh - 监控所有运行中的 agents
# 这个脚本实现了 Ralph Loop V2 逻辑

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWDBOT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG="$CLAWDBOT_ROOT/config/swarm-config.json"
TASKS_JSON="$CLAWDBOT_ROOT/active-tasks.json"
LOG_DIR="$CLAWDBOT_ROOT/logs"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/monitor.log"
}

log_success() {
    log "${GREEN}✓ $1${NC}"
}

log_error() {
    log "${RED}✗ $1${NC}"
}

log_warning() {
    log "${YELLOW}⚠ $1${NC}"
}

# 通知 Telegram（通过 OpenClaw）
notify_telegram() {
    local message="$1"
    log "Sending Telegram notification: $message"
    # 通过 OpenClaw 的 message tool 发送
    # 这里我们创建一个临时文件，让 OpenClaw 读取
    echo "$message" > "$CLAWDBOT_ROOT/.notify-pending.txt"
}

# 检查 GitHub PR 状态
check_pr_status() {
    local branch="$1"
    local pr_number=""
    local ci_status=""
    
    # 检查是否有 PR
    pr_number=$(gh pr list --head "$branch" --json number --jq '.[0].number' 2>/dev/null || echo "")
    
    if [ -z "$pr_number" ]; then
        echo "none"
        return
    fi
    
    # 检查 CI 状态
    ci_status=$(gh pr view "$pr_number" --json statusCheckRollup --jq '.statusCheckRollup[] | select(.conclusion != null) | .conclusion' 2>/dev/null | sort -u)
    
    # 返回: pr_number:ci_status
    echo "$pr_number:$ci_status"
}

# 分析失败原因并生成改进的 prompt (Ralph Loop V2)
generate_retry_prompt() {
    local task_id="$1"
    local failure_reason="$2"
    local original_prompt="$3"
    local log_file="$LOG_DIR/$task_id.log"
    
    log "Analyzing failure for task $task_id: $failure_reason"
    
    # 读取最后100行日志
    local recent_log=$(tail -n 100 "$log_file" 2>/dev/null || echo "No log available")
    
    # 根据失败原因生成不同的改进策略
    case "$failure_reason" in
        "ci_failed")
            # CI 失败 - 提供更多测试和错误处理指导
            cat <<EOF
The previous attempt failed CI checks. Here's what went wrong:

RECENT LOG OUTPUT:
$recent_log

IMPROVED INSTRUCTIONS:
1. Focus on making tests pass first
2. Add proper error handling
3. Check TypeScript types carefully
4. Run tests locally before committing: npm test
5. Check lint: npm run lint

ORIGINAL TASK:
$original_prompt

Please fix the CI failures and ensure all checks pass.
EOF
            ;;
            
        "context_overflow")
            # 上下文太多 - 缩小范围
            cat <<EOF
The previous attempt tried to handle too many files at once.

IMPROVED INSTRUCTIONS:
1. Focus ONLY on these specific files (not the entire codebase)
2. Ignore unrelated files
3. Make minimal, targeted changes
4. Don't refactor unless specifically asked

ORIGINAL TASK:
$original_prompt

Please focus narrowly on the specific task without expanding scope.
EOF
            ;;
            
        "wrong_direction")
            # 方向错误 - 重新对齐
            cat <<EOF
The previous attempt went in the wrong direction.

ANALYSIS OF WHAT WENT WRONG:
$recent_log

CORRECT APPROACH:
$original_prompt

Please re-read the requirements carefully and follow them exactly.
EOF
            ;;
            
        *)
            # 通用重试 - 添加更多上下文
            cat <<EOF
The previous attempt failed. Let's try again with more context.

WHAT HAPPENED:
$recent_log

ORIGINAL TASK:
$original_prompt

Please try a different approach. If you're stuck, break the problem into smaller steps.
EOF
            ;;
    esac
}

# 重启 agent
respawn_agent() {
    local task_id="$1"
    local retry_count="$2"
    local failure_reason="$3"
    
    log "Respawning agent for task $task_id (retry $retry_count/3)"
    
    # 读取任务信息
    local task_json=$(jq --arg id "$task_id" '.[] | select(.id == $id)' "$TASKS_JSON")
    local agent_type=$(echo "$task_json" | jq -r '.agent')
    local description=$(echo "$task_json" | jq -r '.description')
    local original_prompt="$description"
    
    # 生成改进的 prompt (Ralph Loop V2)
    local improved_prompt=$(generate_retry_prompt "$task_id" "$failure_reason" "$original_prompt")
    
    # 保存 prompt 到临时文件
    local prompt_file="$CLAWDBOT_ROOT/.retry-prompt-$task_id.txt"
    echo "$improved_prompt" > "$prompt_file"
    
    # 更新重试次数
    jq --arg id "$task_id" --argjson count "$retry_count" \
        'map(if .id == $id then .retryCount = $count | .status = "retrying" else . end)' \
        "$TASKS_JSON" > "$TASKS_JSON.tmp"
    mv "$TASKS_JSON.tmp" "$TASKS_JSON"
    
    # 重启 agent
    "$SCRIPT_DIR/spawn-agent.sh" "$task_id" "$agent_type" "$description" "$prompt_file"
    
    log_success "Agent respawned with improved prompt"
}

# 检查单个任务
check_task() {
    local task_json="$1"
    
    local task_id=$(echo "$task_json" | jq -r '.id')
    local tmux_session=$(echo "$task_json" | jq -r '.tmuxSession')
    local branch=$(echo "$task_json" | jq -r '.branch')
    local status=$(echo "$task_json" | jq -r '.status')
    local retry_count=$(echo "$task_json" | jq -r '.retryCount // 0')
    local worktree=$(echo "$task_json" | jq -r '.worktree')
    
    log "Checking task: $task_id (status: $status, retries: $retry_count)"
    
    # 1. 检查 tmux 会话是否存活
    if ! tmux has-session -t "$tmux_session" 2>/dev/null; then
        log_warning "Tmux session $tmux_session is dead"
        
        # 检查是否有 PR（agent 可能完成了）
        pr_status=$(check_pr_status "$branch")
        
        if [ "$pr_status" != "none" ]; then
            log "Found PR for $branch, checking if it's done..."
            # 继续检查 PR 状态
        else
            log_error "No PR found and tmux dead - agent likely crashed"
            
            if [ "$retry_count" -lt 3 ]; then
                respawn_agent "$task_id" $((retry_count + 1)) "agent_crashed"
            else
                log_error "Max retries reached for $task_id"
                notify_telegram "🚨 Task $task_id failed after 3 attempts. Manual intervention needed."
                
                # 标记为失败
                jq --arg id "$task_id" \
                    'map(if .id == $id then .status = "failed" | .failedAt = now else . end)' \
                    "$TASKS_JSON" > "$TASKS_JSON.tmp"
                mv "$TASKS_JSON.tmp" "$TASKS_JSON"
            fi
            return
        fi
    fi
    
    # 2. 检查 PR 状态
    pr_status=$(check_pr_status "$branch")
    
    if [ "$pr_status" = "none" ]; then
        log "No PR yet for $task_id, agent still working..."
        return
    fi
    
    # 解析 PR 信息
    pr_number=$(echo "$pr_status" | cut -d: -f1)
    ci_status=$(echo "$pr_status" | cut -d: -f2-)
    
    log "Found PR #$pr_number for $task_id, CI status: $ci_status"
    
    # 更新 PR 信息
    jq --arg id "$task_id" --argjson pr "$pr_number" \
        'map(if .id == $id then .pr = $pr | .checks.prCreated = true else . end)' \
        "$TASKS_JSON" > "$TASKS_JSON.tmp"
    mv "$TASKS_JSON.tmp" "$TASKS_JSON"
    
    # 3. 检查 CI 状态
    if echo "$ci_status" | grep -q "FAILURE"; then
        log_error "CI failed for PR #$pr_number"
        
        if [ "$retry_count" -lt 3 ]; then
            log "Will respawn agent to fix CI failures"
            respawn_agent "$task_id" $((retry_count + 1)) "ci_failed"
        else
            log_error "Max retries reached for $task_id"
            notify_telegram "🚨 Task $task_id: CI failed after 3 attempts. Manual review needed. PR: #$pr_number"
        fi
        return
    fi
    
    # 4. 检查 CI 是否全部通过
    if echo "$ci_status" | grep -qE "^(SUCCESS|NEUTRAL)$"; then
        log_success "CI passed for PR #$pr_number"
        
        # 更新 CI 状态
        jq --arg id "$task_id" \
            'map(if .id == $id then .checks.ciPassed = true else . end)' \
            "$TASKS_JSON" > "$TASKS_JSON.tmp"
        mv "$TASKS_JSON.tmp" "$TASKS_JSON"
        
        # 5. 检查是否需要 code review
        code_review_enabled=$(jq -r '.codeReview.enabled' "$CONFIG")
        
        if [ "$code_review_enabled" = "true" ]; then
            # 触发 code review（通过另一个脚本）
            "$SCRIPT_DIR/run-code-review.sh" "$task_id" "$pr_number"
        else
            # 直接标记为完成
            mark_task_done "$task_id" "$pr_number"
        fi
    else
        log "CI still running for PR #$pr_number..."
    fi
}

# 标记任务完成
mark_task_done() {
    local task_id="$1"
    local pr_number="$2"
    
    log_success "Task $task_id is DONE!"
    
    # 更新状态
    jq --arg id "$task_id" --argjson pr "$pr_number" \
        'map(if .id == $id then .status = "done" | .pr = $pr | .completedAt = now | .checks.codeReviewPassed = true else . end)' \
        "$TASKS_JSON" > "$TASKS_JSON.tmp"
    mv "$TASKS_JSON.tmp" "$TASKS_JSON"
    
    # 发送通知
    local description=$(jq -r --arg id "$task_id" '.[] | select(.id == $id) | .description' "$TASKS_JSON")
    notify_telegram "✅ Task completed: $description\nPR #$pr_number is ready for review!"
}

# 主循环
main() {
    log "=== Agent Monitor Started ==="
    
    # 检查依赖
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) not found. Please install it."
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        log_error "jq not found. Please install it."
        exit 1
    fi
    
    # 读取所有运行中的任务
    if [ ! -f "$TASKS_JSON" ] || [ ! -s "$TASKS_JSON" ]; then
        log "No active tasks found"
        exit 0
    fi
    
    local running_tasks=$(jq -r '.[] | select(.status == "running" or .status == "retrying") | @json' "$TASKS_JSON")
    
    if [ -z "$running_tasks" ]; then
        log "No running tasks"
        exit 0
    fi
    
    # 检查每个任务
    echo "$running_tasks" | while IFS= read -r task; do
        check_task "$task"
        echo ""
    done
    
    log "=== Monitor Check Complete ==="
}

# 运行
main "$@"
