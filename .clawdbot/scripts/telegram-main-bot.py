#!/usr/bin/env python3
"""
OpenClaw Agent Swarm - Main Control Bot
主控制 Bot，管理所有 Agent Swarm 任务
"""

import os
import sys
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
CONFIG_FILE = WORKSPACE / ".clawdbot" / "config" / "telegram-agents.json"
TASKS_FILE = WORKSPACE / ".clawdbot" / "active-tasks.json"

# 加载配置
def load_config():
    if not CONFIG_FILE.exists():
        print("Config not found. Run: telegram-agent-manager.sh init")
        sys.exit(1)
    
    with open(CONFIG_FILE) as f:
        return json.load(f)

config = load_config()
BOT_TOKEN = config.get("mainBot", {}).get("token", "")

if not BOT_TOKEN:
    print("Main bot token not configured!")
    print(f"Edit: {CONFIG_FILE}")
    sys.exit(1)

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Telegram API 函数
def send_message(chat_id, text, parse_mode="Markdown", reply_markup=None):
    """发送消息"""
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    
    try:
        resp = requests.post(url, json=data, timeout=10)
        return resp.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_updates(offset=None):
    """获取更新"""
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    
    try:
        resp = requests.get(url, params=params, timeout=35)
        return resp.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

# 工具函数
def run_command(cmd):
    """运行 shell 命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=WORKSPACE
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error: {e}"

def load_tasks():
    """加载任务列表"""
    if not TASKS_FILE.exists():
        return []
    
    try:
        with open(TASKS_FILE) as f:
            return json.load(f)
    except:
        return []

# 命令处理
def cmd_start(chat_id):
    """处理 /start 命令"""
    text = """
🤖 *OpenClaw Agent Swarm 控制中心*

欢迎！我可以帮你管理所有 AI coding agents。

*可用命令：*
• /spawn - 创建新 agent
• /status - 查看所有任务
• /list - 列出运行中的 agents
• /logs <task-id> - 查看日志
• /kill <task-id> - 杀死任务
• /cleanup - 清理完成的任务
• /help - 显示帮助

*工作流程：*
1. 用 /spawn 创建 agent
2. 系统会为任务创建专属 bot
3. 通过专属 bot 实时交互
4. 完成后收到通知

开始创建你的第一个 agent 吧！
"""
    send_message(chat_id, text)

def cmd_spawn(chat_id, args):
    """处理 /spawn 命令"""
    if not args:
        text = """
*创建新 Agent*

用法：
\`/spawn <task-id> <agent-type> <description>\`

示例：
\`/spawn feat-auth claude "实现用户认证功能"\`

Agent 类型：
• \`codex\` - 后端逻辑、复杂 bug
• \`claude\` - 前端、快速迭代
• \`gemini\` - UI 设计

或者使用工程化模式（推荐）：
\`/spawn-eng <task-id> <task-type> <description>\`

任务类型：
• \`api\` - API 开发
• \`frontend\` - 前端开发
• \`testing\` - 测试开发
• \`security\` - 安全功能
"""
        send_message(chat_id, text)
        return
    
    # 解析参数
    parts = args.split(None, 2)
    if len(parts) < 3:
        send_message(chat_id, "❌ 参数不足\n\n用法: `/spawn <task-id> <agent-type> <description>`")
        return
    
    task_id, agent_type, description = parts
    
    # 确认创建
    text = f"""
📋 *创建 Agent 确认*

任务 ID: \`{task_id}\`
Agent 类型: `{agent_type}`
描述: {description}

确认创建？发送 "确认" 或 "yes"
取消发送 "取消" 或 "no"
"""
    send_message(chat_id, text)
    
    # TODO: 保存待确认状态，等待用户回复

def cmd_status(chat_id):
    """处理 /status 命令"""
    tasks = load_tasks()
    
    if not tasks:
        send_message(chat_id, "📭 没有活动的任务")
        return
    
    # 按状态分组
    running = [t for t in tasks if t["status"] in ["running", "retrying"]]
    done = [t for t in tasks if t["status"] == "done"]
    failed = [t for t in tasks if t["status"] == "failed"]
    
    text = "*📊 任务状态总览*\n\n"
    
    if running:
        text += f"*🟢 运行中 ({len(running)})*\n"
        for task in running[:5]:
            text += f"• \`{task['id']}\` - {task['agent']} - {task['status']}\n"
        if len(running) > 5:
            text += f"  ...还有 {len(running) - 5} 个\n"
        text += "\n"
    
    if done:
        text += f"*✅ 已完成 ({len(done)})*\n"
        for task in done[:3]:
            pr = task.get('pr', 'N/A')
            text += f"• \`{task['id']}\` - PR #{pr}\n"
        if len(done) > 3:
            text += f"  ...还有 {len(done) - 3} 个\n"
        text += "\n"
    
    if failed:
        text += f"*❌ 失败 ({len(failed)})*\n"
        for task in failed[:3]:
            text += f"• \`{task['id']}\` - {task.get('retryCount', 0)} 次重试\n"
        text += "\n"
    
    text += f"\n总计: {len(tasks)} 个任务"
    
    send_message(chat_id, text)

def cmd_list(chat_id):
    """处理 /list 命令"""
    output = run_command("./swarm status")
    send_message(chat_id, f"```\n{output}\n```")

def cmd_logs(chat_id, task_id):
    """处理 /logs 命令"""
    if not task_id:
        send_message(chat_id, "用法: `/logs <task-id>`")
        return
    
    output = run_command(f"./swarm logs {task_id} | tail -50")
    
    if len(output) > 4000:
        output = output[-4000:]
    
    send_message(chat_id, f"*日志: {task_id}*\n\n```\n{output}\n```")

def cmd_kill(chat_id, task_id):
    """处理 /kill 命令"""
    if not task_id:
        send_message(chat_id, "用法: `/kill <task-id>`")
        return
    
    output = run_command(f"./swarm kill {task_id}")
    send_message(chat_id, f"🔪 *杀死任务*\n\n```\n{output}\n```")

def cmd_cleanup(chat_id):
    """处理 /cleanup 命令"""
    output = run_command("./swarm cleanup")
    send_message(chat_id, f"🧹 *清理完成*\n\n```\n{output}\n```")

def cmd_help(chat_id):
    """处理 /help 命令"""
    text = """
*🤖 命令参考*

*任务管理*
• `/spawn <id> <type> <desc>` - 创建 agent
• `/spawn-eng <id> <type> <desc>` - 创建工程化 agent
• `/status` - 查看所有任务状态
• `/list` - 列出运行中的任务
• `/logs <task-id>` - 查看任务日志
• `/kill <task-id>` - 杀死任务
• `/cleanup` - 清理完成的任务

*Agent 类型*
• `codex` - 后端、复杂逻辑
• `claude` - 前端、快速迭代
• `gemini` - UI 设计

*任务类型（工程化）*
• `api` - API 开发
• `frontend` - 前端
• `testing` - 测试
• `security` - 安全

*工作流程*
1. 创建 agent → 系统为其创建专属 bot
2. 专属 bot 加入你的对话列表
3. 通过专属 bot 实时交互
4. Plan 阶段等待你确认
5. 完成后发送 PR 链接

*提示*
• 每个任务都有独立的 Telegram bot
• 可以直接向 agent bot 发送 steering 指令
• 主控制 bot 用于管理，agent bot 用于交互
"""
    send_message(chat_id, text)

# 消息处理
def handle_message(message):
    """处理消息"""
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    
    # 命令分发
    if text.startswith("/"):
        parts = text.split(None, 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == "/start":
            cmd_start(chat_id)
        elif cmd == "/spawn":
            cmd_spawn(chat_id, args)
        elif cmd == "/status":
            cmd_status(chat_id)
        elif cmd == "/list":
            cmd_list(chat_id)
        elif cmd == "/logs":
            cmd_logs(chat_id, args)
        elif cmd == "/kill":
            cmd_kill(chat_id, args)
        elif cmd == "/cleanup":
            cmd_cleanup(chat_id)
        elif cmd == "/help":
            cmd_help(chat_id)
        else:
            send_message(chat_id, f"未知命令: {cmd}\n\n发送 /help 查看帮助")
    else:
        # 非命令消息
        send_message(chat_id, "发送 /help 查看可用命令")

# 主循环
def main():
    """主循环"""
    print("🤖 Main Control Bot Starting...")
    print(f"Workspace: {WORKSPACE}")
    print(f"Config: {CONFIG_FILE}")
    print("")
    
    offset = None
    
    while True:
        try:
            result = get_updates(offset)
            
            if result and result.get("ok"):
                for update in result.get("result", []):
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        handle_message(update["message"])
            
        except KeyboardInterrupt:
            print("\n👋 Bot stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            import time
            time.sleep(5)

if __name__ == "__main__":
    main()
