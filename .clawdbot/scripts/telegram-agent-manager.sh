#!/bin/bash
# telegram-agent-manager.sh - Telegram Agent Swarm 管理器
# 为每个 agent 任务创建独立的 Telegram bot 进行实时交互

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWDBOT_ROOT="$(dirname "$SCRIPT_DIR")"
TG_CONFIG="$CLAWDBOT_ROOT/config/telegram-agents.json"

# 初始化配置文件
init_config() {
    if [ ! -f "$TG_CONFIG" ]; then
        cat > "$TG_CONFIG" <<'EOF'
{
  "mainBot": {
    "enabled": false,
    "token": "",
    "chatId": "",
    "description": "Main control bot for managing all agents"
  },
  "agentBots": {},
  "botFatherToken": "",
  "autoCreateBots": false,
  "useTopics": true
}
EOF
        echo "Created config: $TG_CONFIG"
        echo "Please configure Telegram bot tokens."
        return 1
    fi
    return 0
}

# 创建 agent bot（通过 BotFather API 或配置）
create_agent_bot() {
    local task_id="$1"
    local description="$2"
    
    echo "Creating Telegram bot for task: $task_id"
    
    # 检查是否启用自动创建
    local auto_create=$(jq -r '.autoCreateBots' "$TG_CONFIG")
    
    if [ "$auto_create" = "true" ]; then
        # TODO: 通过 BotFather API 自动创建（需要特殊权限）
        echo "Auto-create not yet implemented"
        echo "Please create bot manually via @BotFather:"
        echo "  /newbot"
        echo "  Name: Agent - $task_id"
        echo "  Username: agent_${task_id}_bot"
        return 1
    else
        # 手动配置模式
        echo ""
        echo "═══════════════════════════════════════"
        echo "Create a new bot via @BotFather:"
        echo ""
        echo "1. Chat with @BotFather"
        echo "2. Send: /newbot"
        echo "3. Bot name: Agent - $task_id"
        echo "4. Bot username: agent_${task_id}_bot"
        echo "5. Copy the token"
        echo "═══════════════════════════════════════"
        echo ""
        read -p "Enter bot token: " bot_token
        
        if [ -z "$bot_token" ]; then
            echo "No token provided, skipping bot creation"
            return 1
        fi
        
        # 保存到配置
        local bot_config=$(cat <<EOF
{
  "taskId": "$task_id",
  "token": "$bot_token",
  "username": "agent_${task_id}_bot",
  "description": "$description",
  "createdAt": $(date +%s),
  "status": "active"
}
EOF
)
        
        # 更新配置文件
        jq --argjson bot "$bot_config" \
           --arg id "$task_id" \
           '.agentBots[$id] = $bot' \
           "$TG_CONFIG" > "$TG_CONFIG.tmp"
        mv "$TG_CONFIG.tmp" "$TG_CONFIG"
        
        echo "✓ Bot registered: @agent_${task_id}_bot"
        return 0
    fi
}

# 启动 agent bot 监听器
start_agent_bot_listener() {
    local task_id="$1"
    local bot_token=$(jq -r --arg id "$task_id" '.agentBots[$id].token' "$TG_CONFIG")
    
    if [ -z "$bot_token" ] || [ "$bot_token" = "null" ]; then
        echo "No bot token found for $task_id"
        return 1
    fi
    
    echo "Starting bot listener for $task_id..."
    
    # 创建 bot 脚本
    local bot_script="$CLAWDBOT_ROOT/.bot-$task_id.py"
    
    cat > "$bot_script" <<EOF
#!/usr/bin/env python3
"""
Telegram Bot for Agent Swarm Task: $task_id
Auto-generated bot listener
"""
import os
import sys
import json
import time
import requests
from datetime import datetime

BOT_TOKEN = "$bot_token"
TASK_ID = "$task_id"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, parse_mode="Markdown"):
    """Send message to Telegram"""
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    try:
        resp = requests.post(url, json=data, timeout=10)
        return resp.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def get_updates(offset=None):
    """Get updates from Telegram"""
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    
    try:
        resp = requests.get(url, params=params, timeout=35)
        return resp.json()
    except Exception as e:
        print(f"Error getting updates: {e}")
        return None

def handle_message(message):
    """Handle incoming message"""
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    
    # 基础命令
    if text == "/start":
        send_message(
            chat_id,
            f"🤖 *Agent Swarm Task: {TASK_ID}*\n\n"
            f"I'm monitoring this task. You can:\n"
            f"• Send steering messages\n"
            f"• Ask for status updates\n"
            f"• Confirm plans\n\n"
            f"Task logs: \`./swarm logs {TASK_ID}\`"
        )
    elif text == "/status":
        # 读取任务状态
        status_file = f"{os.path.dirname(__file__)}/active-tasks.json"
        try:
            with open(status_file) as f:
                tasks = json.load(f)
                task = next((t for t in tasks if t["id"] == TASK_ID), None)
                if task:
                    send_message(
                        chat_id,
                        f"📊 *Task Status*\n\n"
                        f"ID: \`{task['id']}\`\n"
                        f"Agent: {task['agent']}\n"
                        f"Status: {task['status']}\n"
                        f"Retries: {task.get('retryCount', 0)}\n"
                        f"Started: {datetime.fromtimestamp(task['startedAt']/1000).strftime('%Y-%m-%d %H:%M')}"
                    )
                else:
                    send_message(chat_id, "Task not found")
        except Exception as e:
            send_message(chat_id, f"Error reading status: {e}")
    
    elif text.startswith("/steer "):
        # Steering 命令
        steer_msg = text[7:]
        send_message(
            chat_id,
            f"🎯 *Steering Message Sent*\n\n\`{steer_msg}\`\n\n"
            f"The agent will receive this guidance."
        )
        # TODO: 实际发送到 agent（通过 tmux）
        os.system(f"./swarm steer {TASK_ID} '{steer_msg}'")
    
    elif text in ["确认", "confirm", "OK", "ok", "yes"]:
        # 确认消息
        send_message(
            chat_id,
            "✅ *Confirmed*\n\nAgent will proceed with the plan."
        )
        # TODO: 发送确认信号到 agent
    
    else:
        # 其他消息作为 steering
        send_message(
            chat_id,
            f"📝 *Message Received*\n\n"
            f"Treating as steering guidance:\n"
            f"\`{text}\`"
        )
        os.system(f"./swarm steer {TASK_ID} '{text}'")

def main():
    """Main bot loop"""
    print(f"Bot starting for task: {TASK_ID}")
    offset = None
    
    while True:
        try:
            result = get_updates(offset)
            if result and result.get("ok"):
                for update in result.get("result", []):
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        handle_message(update["message"])
            
            time.sleep(0.5)
        
        except KeyboardInterrupt:
            print("Bot stopped")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
EOF
    
    chmod +x "$bot_script"
    
    # 在后台启动 bot
    nohup python3 "$bot_script" > "$CLAWDBOT_ROOT/logs/bot-$task_id.log" 2>&1 &
    local bot_pid=$!
    
    # 保存 PID
    jq --arg id "$task_id" --argjson pid "$bot_pid" \
       '.agentBots[$id].pid = $pid' \
       "$TG_CONFIG" > "$TG_CONFIG.tmp"
    mv "$TG_CONFIG.tmp" "$TG_CONFIG"
    
    echo "✓ Bot listener started (PID: $bot_pid)"
    echo "  Logs: $CLAWDBOT_ROOT/logs/bot-$task_id.log"
}

# 停止 agent bot
stop_agent_bot() {
    local task_id="$1"
    local pid=$(jq -r --arg id "$task_id" '.agentBots[$id].pid // empty' "$TG_CONFIG")
    
    if [ -n "$pid" ]; then
        echo "Stopping bot for $task_id (PID: $pid)..."
        kill "$pid" 2>/dev/null || echo "Process already stopped"
        
        # 更新状态
        jq --arg id "$task_id" \
           '.agentBots[$id].status = "stopped" | .agentBots[$id].pid = null' \
           "$TG_CONFIG" > "$TG_CONFIG.tmp"
        mv "$TG_CONFIG.tmp" "$TG_CONFIG"
    else
        echo "No running bot found for $task_id"
    fi
}

# 列出所有 agent bots
list_agent_bots() {
    echo "═══ Telegram Agent Bots ═══"
    echo ""
    
    if [ ! -f "$TG_CONFIG" ]; then
        echo "No bots configured"
        return
    fi
    
    jq -r '.agentBots | to_entries[] | 
        "\(.key) | @\(.value.username) | \(.value.status) | PID: \(.value.pid // "N/A")"' \
        "$TG_CONFIG" | column -t -s '|'
}

# 主命令分发
case "${1:-help}" in
    init)
        init_config
        ;;
    create)
        create_agent_bot "$2" "$3"
        ;;
    start)
        start_agent_bot_listener "$2"
        ;;
    stop)
        stop_agent_bot "$2"
        ;;
    list)
        list_agent_bots
        ;;
    *)
        cat <<EOF
Telegram Agent Manager

Usage: telegram-agent-manager.sh <command> [args]

Commands:
  init                    Initialize config
  create <task-id> <desc> Create agent bot
  start <task-id>         Start bot listener
  stop <task-id>          Stop bot listener
  list                    List all bots

Example:
  telegram-agent-manager.sh create feat-auth "User authentication"
  telegram-agent-manager.sh start feat-auth
EOF
        ;;
esac
