#!/bin/bash
# run-code-review.sh - 自动化代码审查（Gemini + Codex）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWDBOT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG="$CLAWDBOT_ROOT/config/swarm-config.json"
TASKS_JSON="$CLAWDBOT_ROOT/active-tasks.json"
LOG_DIR="$CLAWDBOT_ROOT/logs"

TASK_ID="$1"
PR_NUMBER="$2"

if [ -z "$TASK_ID" ] || [ -z "$PR_NUMBER" ]; then
    echo "Usage: run-code-review.sh <task-id> <pr-number>"
    exit 1
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/code-review.log"
}

log "=== Starting Code Review for PR #$PR_NUMBER (task: $TASK_ID) ==="

# 读取配置
REVIEWERS=$(jq -r '.codeReview.reviewers[]' "$CONFIG")
CRITICAL_ONLY=$(jq -r '.codeReview.criticalOnly' "$CONFIG")

# 获取 PR 信息
PR_DIFF=$(gh pr diff "$PR_NUMBER")
PR_FILES=$(gh pr view "$PR_NUMBER" --json files --jq '.files[].path' | tr '\n' ',' | sed 's/,$//')

log "PR Files: $PR_FILES"
log "Reviewers: $REVIEWERS"

# 创建 review prompt
REVIEW_PROMPT="You are an expert code reviewer. Review this Pull Request carefully.

PR #$PR_NUMBER
Files changed: $PR_FILES

DIFF:
\`\`\`
$PR_DIFF
\`\`\`

Please review for:
1. Logic errors and bugs
2. Security vulnerabilities
3. Performance issues
4. Code quality and best practices
5. Missing error handling
6. Edge cases

${CRITICAL_ONLY:+IMPORTANT: Only flag CRITICAL issues. Skip minor style or preference suggestions.}

Format your response as:
- ✅ LGTM (looks good to me) - if no issues
- ⚠️ ISSUES FOUND - list each issue with severity (CRITICAL/MAJOR/MINOR)

Be specific about file:line when pointing out issues.
"

# 保存 prompt 到文件
PROMPT_FILE="$CLAWDBOT_ROOT/.review-prompt-$PR_NUMBER.txt"
echo "$REVIEW_PROMPT" > "$PROMPT_FILE"

REVIEW_RESULTS="$LOG_DIR/review-$PR_NUMBER.txt"
echo "=== Code Review Results for PR #$PR_NUMBER ===" > "$REVIEW_RESULTS"
echo "" >> "$REVIEW_RESULTS"

# 对每个 reviewer 运行审查
ALL_PASSED=true

for reviewer in $REVIEWERS; do
    log "Running $reviewer review..."
    
    case "$reviewer" in
        gemini)
            log "Gemini Code Assist review..."
            # 使用 Gemini (免费！)
            RESPONSE=$(GEMINI_API_KEY="${GEMINI_API_KEY}" python3 <<EOF
import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.0-flash-exp')

with open('$PROMPT_FILE', 'r') as f:
    prompt = f.read()

response = model.generate_content(prompt)
print(response.text)
EOF
            )
            
            echo "## Gemini Review:" >> "$REVIEW_RESULTS"
            echo "$RESPONSE" >> "$REVIEW_RESULTS"
            echo "" >> "$REVIEW_RESULTS"
            
            # 检查是否发现 critical 问题
            if echo "$RESPONSE" | grep -qi "CRITICAL"; then
                log "⚠️ Gemini found CRITICAL issues"
                ALL_PASSED=false
            fi
            ;;
            
        codex)
            log "Codex review..."
            # 使用 OpenClaw 的方式调用 Codex
            # 这里简化处理，实际应该通过 OpenClaw API
            log "Codex review via OpenClaw - skipped in this prototype"
            # TODO: 实现通过 OpenClaw 调用 Codex review
            ;;
            
        claude)
            log "Claude review..."
            # 类似地实现 Claude review
            log "Claude review - skipped in this prototype"
            ;;
    esac
done

# 将结果发布到 PR 评论
log "Posting review results to PR..."
gh pr comment "$PR_NUMBER" --body "$(cat $REVIEW_RESULTS)"

# 更新任务状态
if [ "$ALL_PASSED" = true ]; then
    log "✅ All reviews passed!"
    
    jq --arg id "$TASK_ID" \
        'map(if .id == $id then .checks.codeReviewPassed = true | .status = "review_passed" else . end)' \
        "$TASKS_JSON" > "$TASKS_JSON.tmp"
    mv "$TASKS_JSON.tmp" "$TASKS_JSON"
    
    # 标记为完成
    "$SCRIPT_DIR/check-agents.sh"  # 触发下一轮检查，会标记为 done
else
    log "⚠️ Reviews found issues, agent may need to fix them"
    
    jq --arg id "$TASK_ID" \
        'map(if .id == $id then .status = "review_failed" else . end)' \
        "$TASKS_JSON" > "$TASKS_JSON.tmp"
    mv "$TASKS_JSON.tmp" "$TASKS_JSON"
    
    # TODO: 可以选择自动 respawn agent 去修复 review 发现的问题
fi

log "=== Code Review Complete ==="
