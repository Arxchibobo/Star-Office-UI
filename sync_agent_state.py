#!/usr/bin/env python3
"""Agent Swarm → Star Office 状态同步器

监听 Agent Swarm 的任务状态，自动更新 Star Office UI
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
import sys

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
AGENT_TASKS_FILE = WORKSPACE / ".clawdbot" / "active-tasks.json"
STAR_OFFICE_STATE = WORKSPACE / "projects" / "Star-Office-UI" / "state.json"

# 状态映射表
STATE_MAPPING = {
    "pending": "idle",
    "running": "executing",
    "writing": "writing",
    "researching": "researching",
    "testing": "executing",
    "completed": "idle",
    "failed": "error",
    "killed": "idle"
}

# Emoji 映射
EMOJI_MAP = {
    "idle": "🛋️",
    "writing": "✍️",
    "researching": "🔍",
    "executing": "⚙️",
    "syncing": "🔄",
    "error": "❌"
}


def load_agent_tasks():
    """加载当前活跃的 Agent 任务"""
    if not AGENT_TASKS_FILE.exists():
        return []
    
    try:
        with open(AGENT_TASKS_FILE, 'r') as f:
            content = f.read().strip()
            if not content or content == "[]":
                return []
            return json.loads(content)
    except Exception as e:
        print(f"⚠️ 加载任务失败: {e}")
        return []


def get_current_state():
    """根据 Agent 任务确定当前状态"""
    tasks = load_agent_tasks()
    
    if not tasks:
        return {
            "state": "idle",
            "detail": "待命中...",
            "progress": 0,
            "agent_count": 0
        }
    
    # 找到最近的活跃任务
    active_tasks = [t for t in tasks if t.get("status") not in ["completed", "failed", "killed"]]
    
    if not active_tasks:
        return {
            "state": "idle",
            "detail": "所有任务完成，待命中",
            "progress": 0,
            "agent_count": 0
        }
    
    # 取第一个活跃任务
    task = active_tasks[0]
    task_status = task.get("status", "pending")
    task_type = task.get("type", "unknown")
    task_id = task.get("id", "unknown")
    
    # 映射状态
    office_state = STATE_MAPPING.get(task_status, "executing")
    emoji = EMOJI_MAP.get(office_state, "🤖")
    
    detail = f"{emoji} {task_type.upper()} Agent 正在处理: {task_id}"
    
    return {
        "state": office_state,
        "detail": detail,
        "progress": 50,  # 可以后续改进进度追踪
        "agent_count": len(active_tasks),
        "current_task": task_id
    }


def update_star_office():
    """更新 Star Office 状态"""
    state = get_current_state()
    state["updated_at"] = datetime.now().isoformat()
    state["ttl_seconds"] = 30  # 30秒无更新自动回到 idle
    
    # 确保目录存在
    STAR_OFFICE_STATE.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(STAR_OFFICE_STATE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 状态已更新: {state['state']} - {state['detail']}")
        return True
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        return False


def watch_mode(interval=5):
    """监听模式：持续监听 Agent 变化"""
    print("🔄 启动状态同步监听...")
    print(f"📂 监听文件: {AGENT_TASKS_FILE}")
    print(f"🎯 目标文件: {STAR_OFFICE_STATE}")
    print(f"⏱️  更新间隔: {interval}秒")
    print("-" * 50)
    
    last_state = None
    
    try:
        while True:
            current_state = get_current_state()
            
            # 只有状态改变时才更新
            if current_state != last_state:
                update_star_office()
                last_state = current_state
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n👋 停止监听")
        sys.exit(0)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        watch_mode(interval)
    else:
        # 单次更新
        update_star_office()


if __name__ == "__main__":
    main()
