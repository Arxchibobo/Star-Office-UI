#!/bin/bash
# spawn-for-bobi.sh - 小波比专用的非交互式 spawn

if [ $# -lt 3 ]; then
    echo "用法: spawn-for-bobi.sh <task-id> <agent-type> <description>"
    exit 1
fi

TASK_ID="$1"
AGENT_TYPE="$2"
DESCRIPTION="$3"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWDBOT_ROOT="$(dirname "$SCRIPT_DIR")"
WORKSPACE="$(dirname "$CLAWDBOT_ROOT")"

# 创建临时 prompt 文件
PROMPT_FILE="$CLAWDBOT_ROOT/.prompt-$TASK_ID.txt"
echo "$DESCRIPTION" > "$PROMPT_FILE"

# 调用spawn-agent.sh
cd "$WORKSPACE"
bash "$SCRIPT_DIR/spawn-agent.sh" "$TASK_ID" "$AGENT_TYPE" "$DESCRIPTION" "$PROMPT_FILE"

# 清理
rm -f "$PROMPT_FILE"
