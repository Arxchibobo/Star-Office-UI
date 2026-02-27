#!/usr/bin/env python3
"""
设置 Telegram Bot 的 WebApp 按钮
"""
import requests
import json
import sys

# Bot配置
SWARM_BOT_TOKEN = "8222373172:AAHOIrA6ujqZiCN5Pv25vOaJIKIRzaA5ifY"
BOBO_BOT_TOKEN = "8573919212:AAFSir6wFSloGUcx8doZvwwwSsQylBl0Ovk"

# WebApp URL - 完整像素版本
WEBAPP_URL = "https://sub-stainless-columnists-voters.trycloudflare.com"

def set_menu_button(bot_token, bot_name):
    """为Bot设置菜单按钮"""
    url = f"https://api.telegram.org/bot{bot_token}/setChatMenuButton"
    
    payload = {
        "menu_button": {
            "type": "web_app",
            "text": "🏢 查看办公室",
            "web_app": {
                "url": WEBAPP_URL
            }
        }
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result.get("ok"):
        print(f"✅ {bot_name}: WebApp按钮设置成功")
    else:
        print(f"❌ {bot_name}: 设置失败 - {result.get('description')}")
    
    return result

def send_webapp_message(bot_token, chat_id, bot_name):
    """发送带WebApp按钮的测试消息"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": "🏢 Star 的像素办公室已就绪！\n\n点击下方按钮查看 AI 助手的实时工作状态：",
        "reply_markup": {
            "inline_keyboard": [[
                {
                    "text": "🏢 打开办公室",
                    "web_app": {"url": WEBAPP_URL}
                }
            ]]
        }
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result.get("ok"):
        print(f"✅ {bot_name}: 测试消息已发送")
    else:
        print(f"❌ {bot_name}: 发送失败 - {result.get('description')}")
    
    return result

if __name__ == "__main__":
    print("=" * 60)
    print("📱 配置 Telegram WebApp 按钮")
    print("=" * 60)
    print()
    
    # 配置ArxchiboSwarm_bot
    print("1️⃣ ArxchiboSwarm_bot (@ArxchiboSwarm_bot)")
    set_menu_button(SWARM_BOT_TOKEN, "ArxchiboSwarm_bot")
    send_webapp_message(SWARM_BOT_TOKEN, "7744442092", "ArxchiboSwarm_bot")
    print()
    
    # 配置boboclawbot
    print("2️⃣ boboclawbot")
    set_menu_button(BOBO_BOT_TOKEN, "boboclawbot")
    send_webapp_message(BOBO_BOT_TOKEN, "7744442092", "boboclawbot")
    print()
    
    print("=" * 60)
    print("✅ 配置完成！")
    print()
    print("📝 使用说明：")
    print("  1. 打开任意Bot的对话")
    print("  2. 点击输入框旁边的菜单按钮（☰）")
    print("  3. 选择「🏢 查看办公室」")
    print("  4. 或者点击我刚发送的消息中的按钮")
    print("=" * 60)
