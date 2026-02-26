#!/bin/bash
# agent-control.sh - 小波比的 Agent Swarm 控制接口
# 让我可以直接管理 agents

WORKSPACE=~/.openclaw/workspace

case "$1" in
    create)
        # 创建新 agent
        TASK_ID="$2"
        AGENT_TYPE="$3"
        DESCRIPTION="$4"
        
        if [ -z "$TASK_ID" ] || [ -z "$AGENT_TYPE" ] || [ -z "$DESCRIPTION" ]; then
            echo "❌ 参数错误"
            echo "用法: agent-control.sh create <task-id> <type> <description>"
            exit 1
        fi
        
        cd "$WORKSPACE"
        bash ~/.openclaw/workspace/.clawdbot/scripts/spawn-for-bobi.sh "$TASK_ID" "$AGENT_TYPE" "$DESCRIPTION"
        ;;
        
    list)
        # 列出所有任务
        cd "$WORKSPACE"
        ./swarm status
        ;;
        
    logs)
        # 查看日志
        cd "$WORKSPACE"
        ./swarm logs "$2"
        ;;
        
    steer)
        # 引导 agent
        cd "$WORKSPACE"
        ./swarm steer "$2" "$3"
        ;;
        
    kill)
        # 杀死任务
        cd "$WORKSPACE"
        ./swarm kill "$2"
        ;;
        
    cleanup)
        # 清理完成的任务
        cd "$WORKSPACE"
        ./swarm cleanup
        ;;
        
    *)
        echo "小波比 Agent 控制中心"
        echo ""
        echo "命令："
        echo "  create <id> <type> <desc>  - 创建 agent (type: gemini/claude/codex)"
        echo "  list                        - 列出所有任务"
        echo "  logs <id>                   - 查看日志"
        echo "  steer <id> <msg>            - 引导 agent"
        echo "  kill <id>                   - 杀死任务"
        echo "  cleanup                     - 清理完成的任务"
        ;;
esac
