#!/usr/bin/env python3
"""Star Office UI - Telegram 集成版后端"""

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from datetime import datetime
import json
import os
import sys

# 动态路径解析
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
STATE_FILE = os.path.join(ROOT_DIR, "state.json")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="/static")

# ✅ 启用 CORS，允许 Telegram WebApp 访问
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://web.telegram.org",
            "https://k.tg",  # Telegram K
            "*"  # 开发模式：允许所有来源
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 默认状态
DEFAULT_STATE = {
    "state": "idle",
    "detail": "等待任务中...",
    "progress": 0,
    "updated_at": datetime.now().isoformat()
}


def load_state():
    """加载状态（支持自动超时回到 idle）"""
    state = None
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = None

    if not isinstance(state, dict):
        state = dict(DEFAULT_STATE)

    # 自动超时逻辑
    try:
        ttl = int(state.get("ttl_seconds", 25))
        updated_at = state.get("updated_at")
        s = state.get("state", "idle")
        working_states = {"writing", "researching", "executing"}
        if updated_at and s in working_states:
            dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            if dt.tzinfo:
                from datetime import timezone
                age = (datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds()
            else:
                age = (datetime.now() - dt).total_seconds()
            if age > ttl:
                state["state"] = "idle"
                state["detail"] = "待命中（自动回到休息区）"
                state["progress"] = 0
                state["updated_at"] = datetime.now().isoformat()
                try:
                    save_state(state)
                except Exception:
                    pass
    except Exception:
        pass

    return state


def save_state(state: dict):
    """保存状态到文件"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# 初始化状态
if not os.path.exists(STATE_FILE):
    save_state(DEFAULT_STATE)


@app.route("/", methods=["GET"])
def index():
    """返回像素办公室主页"""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/debug", methods=["GET"])
def debug():
    """返回简化调试版"""
    return send_from_directory(FRONTEND_DIR, "debug.html")


@app.route("/status", methods=["GET"])
def get_status():
    """获取当前状态（Telegram WebApp 会轮询此接口）"""
    state = load_state()
    
    # 添加 Telegram 用户信息（如果有）
    telegram_init_data = request.args.get('tgInitData', '')
    if telegram_init_data:
        state['telegram_user'] = True
    
    return jsonify(state)


@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "mode": "telegram_integration"
    })


@app.route("/update", methods=["POST"])
def update_state():
    """手动更新状态（供 Agent Swarm 调用）"""
    try:
        data = request.get_json()
        state = load_state()
        
        if "state" in data:
            state["state"] = data["state"]
        if "detail" in data:
            state["detail"] = data["detail"]
        if "progress" in data:
            state["progress"] = data["progress"]
        
        state["updated_at"] = datetime.now().isoformat()
        save_state(state)
        
        return jsonify({"success": True, "state": state})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("🏢 Star Office UI - Telegram 集成版后端")
    print("=" * 60)
    print(f"📂 State file: {STATE_FILE}")
    print(f"📁 Frontend: {FRONTEND_DIR}")
    print(f"🌐 Listening on: http://0.0.0.0:18793")
    print(f"🔗 Telegram WebApp 已启用 CORS")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=18793, debug=False)
