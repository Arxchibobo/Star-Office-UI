#!/bin/bash
# spawn-agent-noninteractive.sh
# 非交互式spawn agent wrapper

if [ $# -lt 3 ]; then
    echo "Error: Missing arguments"
    echo "Usage: spawn-agent-noninteractive.sh <task-id> <agent-type> <description>"
    exit 1
fi

TASK_ID="$1"
AGENT_TYPE="$2"
DESCRIPTION="$3"

WORKSPACE_ROOT=~/.openclaw/workspace
WORKTREE_ROOT=~/.openclaw/worktrees
TASK_DIR="$WORKTREE_ROOT/$TASK_ID"

# 创建任务目录
mkdir -p "$TASK_DIR"

# 创建worktree
cd "$WORKSPACE_ROOT"
git worktree add "$TASK_DIR" main 2>/dev/null || true

# 启动agent
cd "$TASK_DIR"

# 根据agent类型选择模型
case "$AGENT_TYPE" in
    gemini)
        MODEL="gemini-2.5-pro"
        ;;
    claude)
        MODEL="claude-sonnet-4.5"
        ;;
    codex)
        MODEL="gpt-5.1-codex"
        ;;
    *)
        MODEL="gemini-2.5-pro"
        ;;
esac

# 启动tmux session
tmux new-session -d -s "$TASK_ID" "cd '$TASK_DIR' && claude --model $MODEL --message '$DESCRIPTION'"

echo "✅ Agent spawned successfully!"
echo "Task ID: $TASK_ID"
echo "Agent Type: $AGENT_TYPE"
echo "Model: $MODEL"
echo ""
echo "Use './swarm logs $TASK_ID' to view progress"
echo "Use './swarm attach $TASK_ID' to interact"
