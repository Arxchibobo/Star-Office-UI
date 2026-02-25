#!/bin/bash
# spawn-agent.sh - 启动新的 coding agent
# Usage: spawn-agent.sh <task-id> <agent-type> <description> <prompt-file>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWDBOT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG="$CLAWDBOT_ROOT/config/swarm-config.json"
TASKS_JSON="$CLAWDBOT_ROOT/active-tasks.json"

# 读取参数
TASK_ID="$1"
AGENT_TYPE="$2"  # codex, claude, gemini
DESCRIPTION="$3"
PROMPT_FILE="$4"
REPO_PATH="${5:-$(jq -r '.system.workspaceRoot' "$CONFIG")}"

# 验证参数
if [ -z "$TASK_ID" ] || [ -z "$AGENT_TYPE" ] || [ -z "$DESCRIPTION" ]; then
    echo "Usage: spawn-agent.sh <task-id> <agent-type> <description> <prompt-file> [repo-path]"
    echo "Example: spawn-agent.sh feat-billing codex 'Add billing feature' /path/to/prompt.md"
    exit 1
fi

# 读取配置
WORKTREE_ROOT=$(jq -r '.system.worktreeRoot' "$CONFIG")
LOG_DIR=$(jq -r '.system.logDir' "$CONFIG")

# 创建目录
mkdir -p "$WORKTREE_ROOT"
mkdir -p "$LOG_DIR"

# 生成分支名
BRANCH="feat/$TASK_ID"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID"
TMUX_SESSION="agent-$TASK_ID"

echo "=== Spawning Agent ==="
echo "Task ID: $TASK_ID"
echo "Agent: $AGENT_TYPE"
echo "Description: $DESCRIPTION"
echo "Branch: $BRANCH"
echo "Worktree: $WORKTREE_PATH"
echo "Tmux Session: $TMUX_SESSION"
echo ""

# 1. 创建 worktree
echo "Step 1: Creating worktree..."
cd "$REPO_PATH"

# 检查分支是否已存在
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
    echo "Branch $BRANCH already exists, using existing branch"
    git worktree add "$WORKTREE_PATH" "$BRANCH" 2>/dev/null || {
        echo "Worktree already exists, reusing it"
    }
else
    git worktree add "$WORKTREE_PATH" -b "$BRANCH" 2>/dev/null || {
        echo "Worktree already exists, reusing it"
    }
fi

# 2. 安装依赖（如果需要）
echo "Step 2: Installing dependencies..."
cd "$WORKTREE_PATH"
if [ -f "package.json" ]; then
    npm install > "$LOG_DIR/$TASK_ID-install.log" 2>&1 || echo "Dependency install skipped or failed"
fi

# 3. 准备 prompt
echo "Step 3: Preparing prompt..."
if [ -n "$PROMPT_FILE" ] && [ -f "$PROMPT_FILE" ]; then
    PROMPT=$(cat "$PROMPT_FILE")
else
    PROMPT="$DESCRIPTION"
fi

# 4. 根据 agent 类型选择命令
echo "Step 4: Preparing agent command..."
case "$AGENT_TYPE" in
    codex)
        MODEL=$(jq -r '.agents.codex.model' "$CONFIG")
        REASONING=$(jq -r '.agents.codex.reasoning' "$CONFIG")
        AGENT_CMD="codex --model $MODEL -c model_reasoning_effort=$REASONING --dangerously-bypass-approvals-and-sandbox"
        ;;
    claude)
        MODEL=$(jq -r '.agents.claude.model' "$CONFIG")
        AGENT_CMD="claude --model $MODEL --dangerously-skip-permissions"
        ;;
    gemini)
        MODEL=$(jq -r '.agents.gemini.model' "$CONFIG")
        AGENT_CMD="gemini --model $MODEL"
        ;;
    *)
        echo "Unknown agent type: $AGENT_TYPE"
        exit 1
        ;;
esac

# 5. 创建 tmux 会话
echo "Step 5: Creating tmux session..."
tmux has-session -t "$TMUX_SESSION" 2>/dev/null && {
    echo "Tmux session $TMUX_SESSION already exists. Killing it."
    tmux kill-session -t "$TMUX_SESSION"
}

# 启动 tmux 会话并记录日志
tmux new-session -d -s "$TMUX_SESSION" -c "$WORKTREE_PATH"
tmux pipe-pane -t "$TMUX_SESSION" -o "cat >> $LOG_DIR/$TASK_ID.log"

# 发送命令到 tmux
sleep 1
tmux send-keys -t "$TMUX_SESSION" "echo 'Agent starting for task: $TASK_ID'" C-m
tmux send-keys -t "$TMUX_SESSION" "echo 'Agent type: $AGENT_TYPE'" C-m
tmux send-keys -t "$TMUX_SESSION" "echo 'Worktree: $WORKTREE_PATH'" C-m
tmux send-keys -t "$TMUX_SESSION" "echo '---'" C-m
tmux send-keys -t "$TMUX_SESSION" "$AGENT_CMD \"$PROMPT\"" C-m

# 6. 注册任务
echo "Step 6: Registering task..."
TIMESTAMP=$(date +%s)000

# 读取现有任务
if [ ! -f "$TASKS_JSON" ] || [ ! -s "$TASKS_JSON" ]; then
    echo "[]" > "$TASKS_JSON"
fi

# 添加新任务
TASK_ENTRY=$(cat <<EOF
{
  "id": "$TASK_ID",
  "tmuxSession": "$TMUX_SESSION",
  "agent": "$AGENT_TYPE",
  "description": "$DESCRIPTION",
  "worktree": "$WORKTREE_PATH",
  "branch": "$BRANCH",
  "startedAt": $TIMESTAMP,
  "status": "running",
  "retryCount": 0,
  "notifyOnComplete": true,
  "checks": {
    "prCreated": false,
    "branchSynced": false,
    "ciPassed": false,
    "codeReviewPassed": false,
    "screenshotsIncluded": false
  }
}
EOF
)

# 更新 JSON（移除已存在的同 ID 任务，添加新任务）
jq --argjson task "$TASK_ENTRY" 'map(select(.id != $task.id)) + [$task]' "$TASKS_JSON" > "$TASKS_JSON.tmp"
mv "$TASKS_JSON.tmp" "$TASKS_JSON"

echo ""
echo "=== Agent Spawned Successfully ==="
echo "Task registered in: $TASKS_JSON"
echo "Tmux session: $TMUX_SESSION"
echo "Log file: $LOG_DIR/$TASK_ID.log"
echo ""
echo "To attach: tmux attach -t $TMUX_SESSION"
echo "To monitor: tail -f $LOG_DIR/$TASK_ID.log"
echo ""
