#!/usr/bin/env python3
"""
OpenClaw Image Generation Bot - Telegram图片生成助手
基于 nano-banana-pro (Gemini 3 Pro Image) 的图片生成Bot
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
import time
import tempfile

# ------------------
#  Configuration
# ------------------
WORKSPACE = Path.home() / ".openclaw" / "workspace"
CONFIG_FILE = WORKSPACE / ".clawdbot" / "config" / "image-bot.json"
IMAGE_SCRIPT = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills" / "nano-banana-pro" / "scripts" / "generate_image.py"

BOT_TOKEN = None
AUTHORIZED_CHAT_IDS = []
AUTHORIZED_USER_IDS = []
BASE_URL = None
GEMINI_API_KEY = None

# ------------------
#  Initialization
# ------------------
def load_config():
    global BOT_TOKEN, AUTHORIZED_CHAT_IDS, AUTHORIZED_USER_IDS, BASE_URL, GEMINI_API_KEY
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
        
        BOT_TOKEN = config.get("token")
        
        auth_chat_ids = config.get("authorizedChatIds", [])
        AUTHORIZED_CHAT_IDS = [str(cid) for cid in auth_chat_ids]
        
        auth_user_ids = config.get("authorizedUserIds", [])
        AUTHORIZED_USER_IDS = [str(uid) for uid in auth_user_ids]
        
        GEMINI_API_KEY = config.get("geminiApiKey")
        
    except Exception as e:
        print(f"❌ FATAL: Could not load config. Error: {e}")
        sys.exit(1)

    if not BOT_TOKEN:
        print("❌ FATAL: Bot token not found!")
        sys.exit(1)
    
    if not GEMINI_API_KEY:
        print("🟡 WARNING: GEMINI_API_KEY not configured!")
    
    BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, parse_mode="Markdown"):
    if not BASE_URL:
        return
    try:
        print(f"📤 Sending to {chat_id}: {text[:50]}...", flush=True)
        resp = requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            timeout=10
        )
        return resp.json()
    except Exception as e:
        print(f"❌ Error sending message: {e}", flush=True)

def send_photo(chat_id, photo_path, caption=""):
    if not BASE_URL:
        return
    try:
        print(f"📤 Sending photo to {chat_id}...", flush=True)
        with open(photo_path, 'rb') as photo:
            resp = requests.post(
                f"{BASE_URL}/sendPhoto",
                data={"chat_id": chat_id, "caption": caption},
                files={"photo": photo},
                timeout=30
            )
        return resp.json()
    except Exception as e:
        print(f"❌ Error sending photo: {e}", flush=True)

def get_updates(offset=None):
    if not BASE_URL:
        return None
    params = {"timeout": 5, "allowed_updates": ["message"]}
    if offset:
        params["offset"] = offset
    try:
        resp = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=10)
        result = resp.json()
        if result.get("ok"):
            update_count = len(result.get("result", []))
            if update_count > 0:
                print(f"📥 Got {update_count} update(s)", flush=True)
        return result
    except Exception as e:
        print(f"❌ Error getting updates: {e}", flush=True)
        return None

# ------------------
#  Image Generation
# ------------------
def generate_image(prompt, resolution="1K"):
    """使用 nano-banana-pro 生成图片"""
    if not GEMINI_API_KEY:
        return None, "GEMINI_API_KEY not configured"
    
    try:
        # 创建临时输出文件
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            output_path = tmp.name
        
        # 调用生成脚本
        cmd = [
            "uv", "run",
            str(IMAGE_SCRIPT),
            "--prompt", prompt,
            "--filename", output_path,
            "--resolution", resolution
        ]
        
        env = os.environ.copy()
        env["GEMINI_API_KEY"] = GEMINI_API_KEY
        
        print(f"🎨 Generating image: {prompt[:50]}...", flush=True)
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0 and os.path.exists(output_path):
            print(f"✅ Image generated: {output_path}", flush=True)
            return output_path, None
        else:
            error_msg = result.stderr or result.stdout or "Unknown error"
            print(f"❌ Generation failed: {error_msg}", flush=True)
            return None, error_msg
            
    except subprocess.TimeoutExpired:
        return None, "Generation timeout (60s)"
    except Exception as e:
        return None, str(e)

# ------------------
#  Command Handlers
# ------------------
def handle_generate_command(chat_id, args):
    """处理 /generate 命令"""
    if not args:
        send_message(chat_id, "❌ 请提供图片描述\n\n用法: `/generate 描述`\n示例: `/generate 一只可爱的猫咪在草地上玩耍`")
        return
    
    # 解析参数（可选分辨率）
    parts = args.split()
    resolution = "1K"
    if parts[-1].upper() in ["1K", "2K", "4K"]:
        resolution = parts[-1].upper()
        prompt = " ".join(parts[:-1])
    else:
        prompt = args
    
    send_message(chat_id, f"🎨 正在生成图片...\n描述: {prompt}\n分辨率: {resolution}")
    
    image_path, error = generate_image(prompt, resolution)
    
    if image_path:
        send_photo(chat_id, image_path, caption=f"✨ {prompt}")
        # 清理临时文件
        try:
            os.unlink(image_path)
        except:
            pass
    else:
        send_message(chat_id, f"❌ 生成失败: {error}")

def execute_command(chat_id, command, args):
    """执行命令"""
    if command == "help" or command == "start":
        help_text = """*🎨 图片生成Bot*

可用命令：
• `/generate <描述> [分辨率]` - 生成图片
  分辨率: 1K (默认), 2K, 4K
  
示例:
• `/generate 一只可爱的猫咪`
• `/generate 未来城市夜景 2K`
• `/generate 水彩风格的山水画 4K`

支持中文和英文描述！"""
        send_message(chat_id, help_text)
        return
    
    if command == "generate" or command == "gen" or command == "img":
        handle_generate_command(chat_id, args)
        return
    
    send_message(chat_id, "❌ 未知命令。发送 /help 查看帮助。")

# ------------------
#  Message Handler
# ------------------
def handle_message(message):
    chat_id = str(message["chat"]["id"])
    user_id = str(message["from"]["id"])
    text = message.get("text", "")
    username = message["from"].get("username", "Unknown")
    
    # 权限检查
    if chat_id not in AUTHORIZED_CHAT_IDS:
        print(f"❌ Unauthorized chat: {chat_id}", flush=True)
        return
    
    if user_id not in AUTHORIZED_USER_IDS:
        print(f"❌ Unauthorized user: {user_id} (@{username})", flush=True)
        send_message(chat_id, "⛔️ 抱歉，你没有权限使用此Bot。")
        return
    
    print(f"✅ Command from {user_id} (@{username}) in chat {chat_id}", flush=True)
    
    # 只处理命令
    if not text.startswith("/"):
        send_message(chat_id, "请使用命令格式。发送 /help 查看帮助。")
        return
    
    # 解析命令
    command_part = text.split('@')[0]
    parts = command_part.split(None, 1)
    cmd = parts[0][1:].lower()
    args = parts[1].strip() if len(parts) > 1 else ""
    
    print(f"📨 Command: /{cmd} {args}", flush=True)
    execute_command(chat_id, cmd, args)

# ------------------
#  Main Loop
# ------------------
def main():
    load_config()
    print("🎨 Image Generation Bot Starting...")
    print(f"✅ Authorized Chats: {AUTHORIZED_CHAT_IDS}")
    print(f"✅ Authorized Users: {AUTHORIZED_USER_IDS}")
    print("🔄 Polling for commands...")
    
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            if updates and updates.get("ok"):
                for update in updates.get("result", []):
                    offset = update["update_id"] + 1
                    if "message" in update:
                        handle_message(update["message"])
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n👋 Bot stopped")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
