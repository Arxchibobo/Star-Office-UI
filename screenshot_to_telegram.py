#!/usr/bin/env python3
"""Star Office 截图推送到 Telegram

使用 Playwright 截图像素办公室并发送到 Telegram
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
import requests

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ 需要安装 Playwright:")
    print("pip install playwright")
    print("playwright install chromium")
    sys.exit(1)


# 配置
STAR_OFFICE_URL = "http://localhost:18791"
SCREENSHOT_PATH = "/tmp/star_office_snapshot.png"
TELEGRAM_CONFIG = Path.home() / ".openclaw/workspace/.clawdbot/config/telegram-agents.json"


def load_telegram_config():
    """加载 Telegram Bot 配置"""
    try:
        with open(TELEGRAM_CONFIG) as f:
            config = json.load(f)
        
        bot_token = config.get("mainBot", {}).get("token")
        chat_ids = config.get("mainBot", {}).get("authorizedChatIds", [])
        
        if not bot_token:
            print("❌ 未找到 Telegram Bot Token")
            sys.exit(1)
        
        return bot_token, chat_ids
    except Exception as e:
        print(f"❌ 加载配置失败: {e}")
        sys.exit(1)


async def capture_screenshot(url=STAR_OFFICE_URL, output_path=SCREENSHOT_PATH):
    """使用 Playwright 截图"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 800, "height": 600})
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=10000)
            
            # 等待画面渲染
            await asyncio.sleep(2)
            
            # 截图
            await page.screenshot(path=output_path)
            print(f"✅ 截图已保存: {output_path}")
            
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return False
        finally:
            await browser.close()
    
    return True


def send_to_telegram(image_path, caption=""):
    """发送图片到 Telegram"""
    import json
    
    bot_token, chat_ids = load_telegram_config()
    
    if not chat_ids:
        print("⚠️ 未配置授权聊天ID，跳过发送")
        return
    
    base_url = f"https://api.telegram.org/bot{bot_token}"
    
    for chat_id in chat_ids:
        try:
            with open(image_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': chat_id,
                    'caption': caption,
                    'parse_mode': 'Markdown'
                }
                
                response = requests.post(
                    f"{base_url}/sendPhoto",
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.json().get("ok"):
                    print(f"✅ 已发送到: {chat_id}")
                else:
                    print(f"❌ 发送失败: {response.json()}")
        
        except Exception as e:
            print(f"❌ 发送到 {chat_id} 失败: {e}")


async def main():
    """主函数"""
    print("📸 Star Office 截图推送工具")
    print("-" * 50)
    
    # 检查服务是否运行
    try:
        response = requests.get(f"{STAR_OFFICE_URL}/health", timeout=5)
        if not response.json().get("status") == "ok":
            print("❌ Star Office 服务未运行！")
            print(f"请先启动: cd ~/.openclaw/workspace/projects/Star-Office-UI/backend && python app_telegram.py")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 无法连接到 Star Office: {e}")
        sys.exit(1)
    
    # 截图
    success = await capture_screenshot()
    
    if not success:
        sys.exit(1)
    
    # 生成说明
    try:
        response = requests.get(f"{STAR_OFFICE_URL}/status", timeout=5)
        state = response.json()
        caption = f"🏢 *办公室状态快照*\n\n状态: `{state.get('state', 'unknown')}`\n详情: {state.get('detail', 'N/A')}\n\n🕐 {datetime.now().strftime('%H:%M:%S')}"
    except:
        caption = f"🏢 *办公室状态快照*\n\n🕐 {datetime.now().strftime('%H:%M:%S')}"
    
    # 发送到 Telegram
    send_to_telegram(SCREENSHOT_PATH, caption)
    
    print("✅ 完成！")


if __name__ == "__main__":
    asyncio.run(main())
