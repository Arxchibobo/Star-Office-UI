# Star Office UI - Telegram 集成指南

## 🎯 概述

将像素办公室（Star Office UI）集成到 OpenClaw Agent Swarm 系统，让用户可以在 Telegram 中实时查看 AI 助手的工作状态。

### 集成方案

本项目采用 **方案1（主）+ 方案3（辅）** 的组合方案：

1. **Telegram WebApp 集成**（主要）- 实时交互，在 Telegram 内直接打开像素办公室
2. **截图推送**（辅助）- 定期推送办公室快照到 Telegram 群组

---

## 📁 项目结构

```
Star-Office-UI/
├── backend/
│   ├── app.py              # 原始后端（保留）
│   └── app_telegram.py     # ✨ Telegram 集成版后端（新增 CORS）
├── frontend/
│   └── index.html          # 前端界面
├── sync_agent_state.py     # ✨ Agent Swarm 状态同步器
├── screenshot_to_telegram.py # ✨ 截图推送工具
├── deploy.sh               # ✨ 一键部署脚本
├── office-config.json      # ✨ 配置文件
├── state.json              # 运行时状态（自动生成）
└── STAR_OFFICE_INTEGRATION.md # 本文档
```

---

## 🚀 快速开始

### 1. 一键部署

```bash
cd ~/.openclaw/workspace/projects/Star-Office-UI
chmod +x deploy.sh
./deploy.sh
```

部署脚本会自动完成：
- ✅ 创建 Python 虚拟环境
- ✅ 安装依赖（Flask、Flask-CORS、Playwright）
- ✅ 安装 Playwright Chromium（用于截图）
- ✅ 创建启动脚本
- ✅ 初始化配置文件

### 2. 启动服务

#### 方式 A：直接启动（测试用）

```bash
# 终端1：启动后端服务
./start.sh

# 终端2：启动状态同步（可选）
./start_sync.sh
```

#### 方式 B：使用 systemd（生产环境）

```bash
# 创建 systemd 服务
sudo tee /etc/systemd/system/star-office.service > /dev/null <<EOF
[Unit]
Description=Star Office UI Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/.openclaw/workspace/projects/Star-Office-UI
ExecStart=$HOME/.openclaw/workspace/projects/Star-Office-UI/start.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 创建状态同步服务
sudo tee /etc/systemd/system/star-office-sync.service > /dev/null <<EOF
[Unit]
Description=Star Office State Sync
After=star-office.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/.openclaw/workspace/projects/Star-Office-UI
ExecStart=$HOME/.openclaw/workspace/projects/Star-Office-UI/start_sync.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable star-office.service star-office-sync.service
sudo systemctl start star-office.service star-office-sync.service

# 查看状态
sudo systemctl status star-office.service
sudo systemctl status star-office-sync.service
```

### 3. 暴露到公网（Cloudflare Tunnel）

```bash
# 安装 cloudflared（如果未安装）
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# 启动快速隧道
cloudflared tunnel --url http://localhost:18791
```

**输出示例：**
```
2026-02-26T16:45:00Z INF +--------------------------------------------------------------------------------------------+
2026-02-26T16:45:00Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2026-02-26T16:45:00Z INF |  https://abc123xyz.trycloudflare.com                                                        |
2026-02-26T16:45:00Z INF +--------------------------------------------------------------------------------------------+
```

**保存这个 URL！** 你需要在下一步配置 Telegram WebApp。

---

## 🤖 Telegram 集成配置

### 方案 1：Telegram WebApp 按钮（推荐）⭐

#### 步骤 1：配置 BotFather

1. 找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/setmenubutton`
3. 选择你的 Bot
4. 选择 `Edit menu button URL`
5. 输入你的 Cloudflare Tunnel URL：
   ```
   https://your-tunnel-url.trycloudflare.com
   ```
6. 按钮文本输入：`🏢 查看办公室`

#### 步骤 2：测试 WebApp

1. 打开你的 Bot
2. 点击左下角的 `🏢 查看办公室` 按钮
3. 应该会在 Telegram 内打开像素办公室界面

#### 步骤 3：配置权限

编辑 `~/.openclaw/workspace/.clawdbot/config/telegram-agents.json`：

```json
{
  "mainBot": {
    "token": "your-bot-token",
    "authorizedChatIds": ["-1003850977818"],
    "authorizedUserIds": ["7744442092"],
    "webAppUrl": "https://your-tunnel-url.trycloudflare.com"
  }
}
```

---

### 方案 3：截图推送（辅助）

#### 手动推送

```bash
./screenshot.sh
```

#### 定时推送（cron）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每5分钟推送一次）
*/5 * * * * /home/your-user/.openclaw/workspace/projects/Star-Office-UI/screenshot.sh >> /tmp/star-office-screenshot.log 2>&1
```

---

## ⚙️ 配置说明

### office-config.json

```json
{
  "telegram_webapp": {
    "enabled": true,
    "url": "https://your-tunnel-url.trycloudflare.com",
    "button_text": "🏢 查看办公室"
  },
  "state_sync": {
    "enabled": true,
    "source": "agent_swarm",
    "interval_seconds": 5
  },
  "screenshot": {
    "enabled": false,
    "interval_minutes": 5
  }
}
```

### 状态映射

| Agent Swarm 状态 | 办公室状态 | Emoji | 位置 |
|-----------------|----------|-------|------|
| `pending` | `idle` | 🛋️ | 休息区 |
| `running` | `executing` | ⚙️ | 办公桌 |
| `writing` | `writing` | ✍️ | 办公桌 |
| `researching` | `researching` | 🔍 | 办公桌 |
| `completed` | `idle` | ✅ | 休息区 |
| `failed` | `error` | ❌ | 休息区 |

---

## 🔧 使用方法

### 手动更新状态

```bash
cd ~/.openclaw/workspace/projects/Star-Office-UI
python set_state.py writing "正在写代码..."
python set_state.py idle "待命中"
```

### API 调用

```bash
# 获取当前状态
curl http://localhost:18791/status

# 手动更新状态
curl -X POST http://localhost:18791/update \
  -H "Content-Type: application/json" \
  -d '{"state": "writing", "detail": "正在处理任务...", "progress": 50}'
```

---

## 🐛 故障排除

### 问题 1：Telegram WebApp 无法加载

**症状：** 点击按钮后白屏或加载失败

**解决方案：**
1. 检查 Cloudflare Tunnel 是否运行：
   ```bash
   ps aux | grep cloudflared
   ```
2. 检查后端是否启动：
   ```bash
   curl http://localhost:18791/health
   ```
3. 检查 CORS 配置：
   ```bash
   curl -H "Origin: https://web.telegram.org" http://localhost:18791/status
   ```

### 问题 2：状态不同步

**症状：** 办公室状态与实际 Agent 状态不一致

**解决方案：**
1. 检查状态同步脚本是否运行：
   ```bash
   ps aux | grep sync_agent_state
   ```
2. 手动触发同步：
   ```bash
   python sync_agent_state.py
   ```
3. 检查 `active-tasks.json`：
   ```bash
   cat ~/.openclaw/workspace/.clawdbot/active-tasks.json
   ```

### 问题 3：截图失败

**症状：** `screenshot.sh` 报错

**解决方案：**
1. 确认 Playwright 已安装：
   ```bash
   playwright --version
   ```
2. 重新安装 Chromium：
   ```bash
   source venv/bin/activate
   playwright install chromium
   ```
3. 检查后端是否可访问：
   ```bash
   curl http://localhost:18791/
   ```

### 问题 4：权限问题

**症状：** "⛔️ 抱歉，你没有权限使用此Bot"

**解决方案：**
1. 确认你的用户ID在授权列表中
2. 编辑配置文件添加你的用户ID：
   ```json
   {
     "mainBot": {
       "authorizedUserIds": ["your-user-id"]
     }
   }
   ```
3. 获取你的用户ID（发送 `/start` 给 @userinfobot）

---

## 📊 监控与日志

### 查看日志

```bash
# 后端日志
journalctl -u star-office.service -f

# 同步日志
journalctl -u star-office-sync.service -f

# 截图日志
tail -f /tmp/star-office-screenshot.log
```

### 健康检查

```bash
# 后端健康检查
curl http://localhost:18791/health

# 状态检查
curl http://localhost:18791/status
```

---

## 🎨 自定义

### 修改办公室背景

1. 替换 `frontend/office_bg.png`（推荐尺寸：800×600）
2. 重启服务

### 修改状态映射

编辑 `office-config.json` 中的 `state_mapping`。

### 修改更新频率

编辑 `sync_agent_state.py`：
```python
# 默认 5 秒
watch_mode(interval=5)
```

---

## 🔐 安全注意事项

1. **不要在 `detail` 字段中放敏感信息**
   - 任何有 Tunnel URL 的人都能看到状态

2. **Cloudflare Tunnel 是临时的**
   - 每次重启会生成新 URL
   - 生产环境建议使用固定域名

3. **限制访问**
   - 使用 Telegram 的授权机制
   - 考虑添加 API Token 验证

4. **定期检查日志**
   - 监控异常访问
   - 检查错误日志

---

## 📈 性能优化

### 减少轮询频率

如果服务器资源有限，可以增加更新间隔：

```bash
# 从 5 秒改为 10 秒
./start_sync.sh 10
```

### 禁用截图功能

如果不需要截图推送，可以不运行 `screenshot.sh`。

### 使用 Redis 缓存

对于高并发场景，可以考虑使用 Redis 缓存状态：

```python
# 在 app_telegram.py 中添加 Redis 支持
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
```

---

## 🧪 测试报告

### 测试环境

- **OS:** Ubuntu 22.04 LTS (WSL2)
- **Python:** 3.10.12
- **Node.js:** v22.22.0
- **Agent Swarm:** v1.0
- **Telegram Bot API:** 7.0

### 测试用例

| 测试项 | 状态 | 说明 |
|-------|------|------|
| ✅ 后端启动 | 通过 | Flask 在 18791 端口启动成功 |
| ✅ CORS 配置 | 通过 | Telegram WebApp 可正常访问 |
| ✅ 状态同步 | 通过 | Agent 状态成功映射到办公室状态 |
| ✅ 截图功能 | 通过 | Playwright 截图正常 |
| ✅ Telegram 推送 | 通过 | 图片成功发送到授权聊天 |
| ✅ 自动超时 | 通过 | 30秒无更新自动回到 idle |
| ✅ 多 Agent 支持 | 通过 | 显示当前活跃 Agent 数量 |
| ⚠️ Cloudflare Tunnel | 部分通过 | URL 是临时的，需要手动更新 |

### 已知限制

1. **Cloudflare 快速隧道不稳定**
   - 每次重启会生成新 URL
   - 建议：使用固定域名或 Cloudflare Tunnel 命名隧道

2. **截图性能开销**
   - Playwright 需要 Chromium 浏览器
   - 建议：按需触发，不要频繁截图

3. **单一状态显示**
   - 当前只显示第一个活跃 Agent
   - 改进：显示多个小人代表多个 Agent

---

## 🎯 后续改进计划

### 短期（1-2周）

- [ ] 固定域名支持（Cloudflare Tunnel Named Tunnel）
- [ ] 多 Agent 多小人显示
- [ ] 添加任务进度条
- [ ] 性能监控面板

### 中期（1-2月）

- [ ] AgentHub 前端集成（方案2）
- [ ] 状态历史记录
- [ ] 实时 WebSocket 推送（替代轮询）
- [ ] 移动端优化

### 长期（3-6月）

- [ ] 3D 办公室场景
- [ ] Agent 角色自定义（不同服装、外观）
- [ ] 交互功能（点击小人查看详情）
- [ ] 数据可视化（任务统计、时间线）

---

## 📚 参考资料

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram WebApps](https://core.telegram.org/bots/webapps)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [Playwright Python](https://playwright.dev/python/)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

---

## 🤝 贡献

如有问题或改进建议，请联系项目维护者或提交 Issue。

---

## 📄 许可证

MIT License - 与 Star-Office-UI 原项目保持一致

---

**集成完成！🎉**

现在你可以在 Telegram 中实时查看 AI 助手的工作状态了！
