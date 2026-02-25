#!/bin/bash
# task-manager.sh - 管理任务的 CLI 工具

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWDBOT_ROOT="$(dirname "$SCRIPT_DIR")"
TASKS_JSON="$CLAWDBOT_ROOT/active-tasks.json"

cmd_list() {
    echo "=== Active Tasks ==="
    if [ ! -f "$TASKS_JSON" ] || [ ! -s "$TASKS_JSON" ]; then
        echo "No tasks found"
        return
    fi
    
    jq -r '.[] | "\(.id) | \(.status) | \(.agent) | \(.description) | Retries: \(.retryCount // 0)"' "$TASKS_JSON" | \
        column -t -s '|' -N "ID,Status,Agent,Description,Retries"
}

cmd_view() {
    local task_id="$1"
    if [ -z "$task_id" ]; then
        echo "Usage: task-manager.sh view <task-id>"
        exit 1
    fi
    
    jq --arg id "$task_id" '.[] | select(.id == $id)' "$TASKS_JSON"
}

cmd_logs() {
    local task_id="$1"
    if [ -z "$task_id" ]; then
        echo "Usage: task-manager.sh logs <task-id>"
        exit 1
    fi
    
    local log_file="$CLAWDBOT_ROOT/logs/$task_id.log"
    if [ -f "$log_file" ]; then
        tail -n 50 "$log_file"
    else
        echo "Log file not found: $log_file"
    fi
}

cmd_attach() {
    local task_id="$1"
    if [ -z "$task_id" ]; then
        echo "Usage: task-manager.sh attach <task-id>"
        exit 1
    fi
    
    local session=$(jq -r --arg id "$task_id" '.[] | select(.id == $id) | .tmuxSession' "$TASKS_JSON")
    
    if [ -z "$session" ]; then
        echo "Task not found: $task_id"
        exit 1
    fi
    
    echo "Attaching to tmux session: $session"
    echo "Press Ctrl+B then D to detach"
    sleep 1
    tmux attach -t "$session"
}

cmd_steer() {
    local task_id="$1"
    shift
    local message="$*"
    
    if [ -z "$task_id" ] || [ -z "$message" ]; then
        echo "Usage: task-manager.sh steer <task-id> <message>"
        echo "Example: task-manager.sh steer feat-billing 'Stop. Focus on API layer first.'"
        exit 1
    fi
    
    local session=$(jq -r --arg id "$task_id" '.[] | select(.id == $id) | .tmuxSession' "$TASKS_JSON")
    
    if [ -z "$session" ]; then
        echo "Task not found: $task_id"
        exit 1
    fi
    
    echo "Steering agent in session $session..."
    echo "Message: $message"
    tmux send-keys -t "$session" "$message" C-m
    echo "Message sent!"
}

cmd_kill() {
    local task_id="$1"
    if [ -z "$task_id" ]; then
        echo "Usage: task-manager.sh kill <task-id>"
        exit 1
    fi
    
    local session=$(jq -r --arg id "$task_id" '.[] | select(.id == $id) | .tmuxSession' "$TASKS_JSON")
    
    if [ -z "$session" ]; then
        echo "Task not found: $task_id"
        exit 1
    fi
    
    echo "Killing tmux session: $session"
    tmux kill-session -t "$session" 2>/dev/null || echo "Session already dead"
    
    # 更新状态
    jq --arg id "$task_id" \
        'map(if .id == $id then .status = "killed" | .killedAt = now else . end)' \
        "$TASKS_JSON" > "$TASKS_JSON.tmp"
    mv "$TASKS_JSON.tmp" "$TASKS_JSON"
    
    echo "Task killed"
}

cmd_cleanup() {
    echo "Cleaning up completed tasks..."
    
    # 只保留 running/retrying 的任务
    jq 'map(select(.status == "running" or .status == "retrying"))' "$TASKS_JSON" > "$TASKS_JSON.tmp"
    mv "$TASKS_JSON.tmp" "$TASKS_JSON"
    
    # 清理 worktrees
    echo "Pruning worktrees..."
    cd "$CLAWDBOT_ROOT/../.."
    git worktree prune
    
    echo "Cleanup complete"
}

cmd_help() {
    cat <<EOF
Task Manager - Manage Agent Swarm Tasks

Usage: task-manager.sh <command> [arguments]

Commands:
  list                  List all active tasks
  view <task-id>        View task details
  logs <task-id>        View task logs
  attach <task-id>      Attach to agent's tmux session
  steer <task-id> <msg> Send message to running agent (mid-task redirection)
  kill <task-id>        Kill a running task
  cleanup               Remove completed tasks and prune worktrees
  help                  Show this help

Examples:
  task-manager.sh list
  task-manager.sh logs feat-billing
  task-manager.sh steer feat-billing "Focus on the API layer first"
  task-manager.sh attach feat-billing
EOF
}

# 主命令分发
COMMAND="${1:-help}"
shift || true

case "$COMMAND" in
    list)     cmd_list "$@" ;;
    view)     cmd_view "$@" ;;
    logs)     cmd_logs "$@" ;;
    attach)   cmd_attach "$@" ;;
    steer)    cmd_steer "$@" ;;
    kill)     cmd_kill "$@" ;;
    cleanup)  cmd_cleanup "$@" ;;
    help)     cmd_help ;;
    *)
        echo "Unknown command: $COMMAND"
        cmd_help
        exit 1
        ;;
esac
