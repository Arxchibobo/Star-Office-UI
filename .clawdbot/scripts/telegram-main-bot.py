#!/usr/bin/env python3
"""
OpenClaw Agent Swarm - Main Control Bot (Pure Command Version)
纯命令版本 - 只执行命令，不做智能理解
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
import time

# ------------------
#  Configuration
# ------------------
WORKSPACE = Path.home() / ".openclaw" / "workspace"
CONFIG_FILE = WORKSPACE / ".clawdbot" / "config" / "telegram-agents.json"

# 全局变量
BOT_TOKEN = None
AUTHORIZED_CHAT_IDS = []
AUTHORIZED_USER_IDS = []  # 新增：授权用户列表
BASE_URL = None

# ------------------
#  Initialization
# ------------------
def load_config():
    global BOT_TOKEN, AUTHORIZED_CHAT_IDS, AUTHORIZED_USER_IDS, BASE_URL
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
        main_bot_config = config.get("mainBot", {})
        BOT_TOKEN = main_bot_config.get("token")
        
        # 加载授权聊天ID列表（私聊和群组）
        auth_chat_ids = main_bot_config.get("authorizedChatIds", [])
        if auth_chat_ids:
            AUTHORIZED_CHAT_IDS = [str(cid) for cid in auth_chat_ids]
        else:
            admin_chat_id = main_bot_config.get("chatId")
            if admin_chat_id:
                AUTHORIZED_CHAT_IDS.append(str(admin_chat_id))
        
        # 加载授权用户ID列表（只有这些用户能执行命令）
        auth_user_ids = main_bot_config.get("authorizedUserIds", [])
        if auth_user_ids:
            AUTHORIZED_USER_IDS = [str(uid) for uid in auth_user_ids]
        else:
            # 如果没有配置，默认使用chatId作为用户ID（向后兼容）
            admin_chat_id = main_bot_config.get("chatId")
            if admin_chat_id:
                AUTHORIZED_USER_IDS.append(str(admin_chat_id))
                
    except Exception as e:
        print(f"❌ FATAL: Could not load config. Error: {e}")
        sys.exit(1)

    if not BOT_TOKEN:
        print("❌ FATAL: Main bot token not found!")
        sys.exit(1)
    
    BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, parse_mode="Markdown"):
    if not BASE_URL:
        print("❌ BASE_URL not set!")
        return
    try:
        print(f"📤 Sending to {chat_id}: {text[:50]}...")
        resp = requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            timeout=10
        )
        result = resp.json()
        if result.get("ok"):
            print(f"✅ Message sent successfully")
        else:
            print(f"❌ Send failed: {result}")
        return result
    except Exception as e:
        print(f"❌ Error sending message: {e}")

def get_updates(offset=None):
    if not BASE_URL:
        return None
    params = {"timeout": 5, "allowed_updates": ["message"]}  # 减少到5秒，快速响应
    if offset:
        params["offset"] = offset
    try:
        print(f"🔍 Polling (offset={offset})...", flush=True)
        resp = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=10)
        result = resp.json()
        if result.get("ok"):
            update_count = len(result.get("result", []))
            if update_count > 0:
                print(f"📥 Got {update_count} update(s)", flush=True)
            else:
                print(f"   Empty result", flush=True)
        return result
    except Exception as e:
        print(f"❌ Error getting updates: {e}", flush=True)
        return None

def run_command(cmd):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=WORKSPACE
        )
        return result.stdout if result.returncode == 0 else f"Error:\n{result.stderr}"
    except Exception as e:
        return f"Error running command: {e}"

# ------------------
#  Command Handlers
# ------------------
def execute_command(chat_id, command, args):
    # Map commands to actual swarm operations
    if command == "help":
        help_text = """*OpenClaw Agent Swarm 控制中心*

可用命令：
• `/spawn <id> <type> <desc>` - 创建 agent
  类型: gemini, claude, codex
• `/status` - 查看任务状态
• `/logs <id>` - 查看日志
• `/kill <id>` - 杀死任务
• `/cleanup` - 清理完成的任务
• `/help` - 显示此帮助

示例:
`/spawn my-task gemini 创建一个登录页面`
"""
        send_message(chat_id, help_text)
        return
    
    if command == "start":
        send_message(chat_id, "👋 欢迎使用 Agent Swarm 控制中心！\n\n发送 /help 查看可用命令。")
        return
    
    # Special handling for spawn command
    if command == "spawn":
        # Parse spawn args: <id> <type> <desc>
        parts = args.split(None, 2)
        if len(parts) < 3:
            send_message(chat_id, "❌ 参数不足\n\n用法: `/spawn <id> <type> <desc>`\n\n示例: `/spawn my-task gemini 创建登录页面`")
            return
        
        task_id, agent_type, description = parts
        
        # Validate agent type
        if agent_type not in ['gemini', 'claude', 'codex']:
            send_message(chat_id, f"❌ 无效的agent类型: {agent_type}\n\n支持的类型: gemini, claude, codex")
            return
        
        # Use non-interactive spawn script
        spawn_script = f"{Path.home()}/.openclaw/workspace/.clawdbot/scripts/spawn-agent-noninteractive.sh"
        full_cmd = f"{spawn_script} '{task_id}' '{agent_type}' '{description}'"
        
        print(f"Executing spawn: {full_cmd}", flush=True)
        send_message(chat_id, f"🚀 正在创建 Agent...\n\nTask ID: `{task_id}`\nType: `{agent_type}`")
        
        output = run_command(full_cmd)
        send_message(chat_id, f"*结果:*\n\n```\n{output}\n```")
        return
    
    # Execute regular swarm command
    full_cmd = f"./swarm {command} {args}"
    print(f"Executing: {full_cmd}", flush=True)
    send_message(chat_id, f"⚙️ 运行中: `{full_cmd}`")
    
    output = run_command(full_cmd)
    
    # Truncate if too long
    if len(output) > 4000:
        output = output[-4000:]
    
    send_message(chat_id, f"*结果:*\n\n```\n{output}\n```")

# ------------------
#  Message Handler
# ------------------
def handle_message(message):
    chat_id = str(message["chat"]["id"])
    user_id = str(message["from"]["id"])
    text = message.get("text", "")
    username = message["from"].get("username", "Unknown")
    
    # 双重检查：聊天必须授权 AND 用户必须授权
    if chat_id not in AUTHORIZED_CHAT_IDS:
        print(f"❌ Unauthorized chat: {chat_id}")
        return
    
    if user_id not in AUTHORIZED_USER_IDS:
        print(f"❌ Unauthorized user: {user_id} (@{username}) in chat {chat_id}")
        send_message(chat_id, f"⛔️ 抱歉，你没有权限使用此Bot。")
        return
    
    print(f"✅ Authorized command from user {user_id} (@{username}) in chat {chat_id}")
    
    # Only process commands (starting with /)
    if not text.startswith("/"):
        send_message(chat_id, "请使用命令格式。发送 /help 查看可用命令。")
        return
    
    # Parse command
    command_part = text.split('@')[0]  # Handle @botname in groups
    parts = command_part.split(None, 1)
    cmd = parts[0][1:].lower()  # Remove /
    args = parts[1].strip() if len(parts) > 1 else ""
    
    print(f"📨 Command: /{cmd} {args}")
    execute_command(chat_id, cmd, args)

# ------------------
#  Main Loop
# ------------------
def main():
    load_config()
    print("🤖 Main Control Bot Starting (Pure Command Mode)...")
    print(f"✅ Authorized Chats: {AUTHORIZED_CHAT_IDS}")
    print(f"✅ Authorized Users: {AUTHORIZED_USER_IDS}")
    print("🔄 Polling for commands...")
    
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            if updates and updates.get("ok"):
                result_list = updates.get("result", [])
                for update in result_list:
                    offset = update["update_id"] + 1
                    if "message" in update:
                        handle_message(update["message"])
            time.sleep(0.1)  # 快速轮询
        except KeyboardInterrupt:
            print("\n👋 Bot stopped")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
