#!/usr/bin/env python3
"""OpenClaw Gateway → Office UI 状态同步器

实时同步 OpenClaw 的工作状态到办公室UI
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
import subprocess

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
OFFICE_STATE = WORKSPACE / "projects" / "Star-Office-UI" / "state.json"

# 状态映射
STATE_MAPPING = {
    "idle": {"office_state": "idle", "emoji": "🛋️", "detail": "待命中..."},
    "thinking": {"office_state": "researching", "emoji": "🤔", "detail": "思考中..."},
    "tool_use": {"office_state": "executing", "emoji": "⚙️", "detail": "执行任务中..."},
    "writing": {"office_state": "writing", "emoji": "✍️", "detail": "整理回复中..."},
    "searching": {"office_state": "researching", "emoji": "🔍", "detail": "搜索信息中..."},
    "error": {"office_state": "error", "emoji": "❌", "detail": "出错了..."}
}

def get_gateway_status():
    """从 OpenClaw Gateway 获取状态"""
    try:
        # 检查是否有活跃的 session
        result = subprocess.run(
            ["journalctl", "--user", "-u", "openclaw-gateway", "-n", "20", "--no-pager"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return None
        
        logs = result.stdout.lower()
        
        # 分析最近的日志判断状态
        if "tool" in logs or "exec" in logs or "browser" in logs:
            return "tool_use"
        elif "thinking" in logs or "reasoning" in logs:
            return "thinking"
        elif "writing" in logs or "generating" in logs:
            return "writing"
        elif "search" in logs or "fetch" in logs:
            return "searching"
        elif "error" in logs or "failed" in logs:
            return "error"
        else:
            return "idle"
            
    except Exception as e:
        print(f"⚠️ Error getting gateway status: {e}")
        return "idle"

def get_active_agents_count():
    """获取活跃 Agent 数量"""
    try:
        agent_tasks_file = WORKSPACE / ".clawdbot" / "active-tasks.json"
        if agent_tasks_file.exists():
            with open(agent_tasks_file) as f:
                tasks = json.load(f)
                return len([t for t in tasks if t.get("status") == "running"])
    except:
        pass
    return 0

def update_office_state(gateway_state, agent_count):
    """更新办公室状态"""
    mapping = STATE_MAPPING.get(gateway_state, STATE_MAPPING["idle"])
    
    state = {
        "state": mapping["office_state"],
        "detail": mapping["detail"],
        "emoji": mapping["emoji"],
        "progress": 0,
        "agent_count": agent_count,
        "updated_at": datetime.now().isoformat(),
        "ttl_seconds": 30
    }
    
    # 保存状态
    with open(OFFICE_STATE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    return state

def main():
    """主循环"""
    print("🚀 OpenClaw → Office UI 状态同步启动")
    print(f"📁 状态文件: {OFFICE_STATE}")
    print("⏰ 同步间隔: 3秒")
    print("-" * 50)
    
    last_state = None
    
    while True:
        try:
            # 获取状态
            gateway_state = get_gateway_status()
            agent_count = get_active_agents_count()
            
            # 更新办公室
            state = update_office_state(gateway_state, agent_count)
            
            # 只在状态改变时打印
            if state != last_state:
                emoji = state["emoji"]
                detail = state["detail"]
                agents = state["agent_count"]
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {emoji} {detail} (活跃Agents: {agents})")
                last_state = state
            
            time.sleep(3)
            
        except KeyboardInterrupt:
            print("\n👋 同步器已停止")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
