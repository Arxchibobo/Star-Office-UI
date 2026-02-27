# 🏢 Bobo的办公室 - Star-Office-UI

基于 [ringhyacinth/Star-Office-UI](https://github.com/ringhyacinth/Star-Office-UI) 的个性化版本，完整的像素风格办公室实时状态展示系统。

## ✨ 特点

### 🎨 完整的像素艺术场景
- **AI生成的办公室背景** - 使用 Gemini 3 Pro Image (nano-banana-pro) 生成的精美像素场景
- **可爱的龙虾角色** - 鲜艳的深红色像素龙虾，141px，醒目可辨识
- **流畅的动画效果** - 角色走动、眨眼（透明度变化）、气泡对话
- **实时状态同步** - 根据 OpenClaw AI 助手的工作状态实时更新

### 📱 多平台访问
- **本地浏览器** - `http://localhost:18793/` 完整体验
- **Telegram WebApp** - 通过 cloudflare tunnel 提供 HTTPS 公网访问
- **双版本支持** - 完整版（Phaser游戏引擎）+ 简化版（纯HTML）

### 🔄 智能状态映射
办公室角色会根据 AI 助手的工作状态自动移动：
- **idle/completed** → 休息区（沙发）
- **writing/executing/researching** → 工作区（办公桌）
- **error** → 警告区

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Node.js (可选，用于前端开发)
- cloudflared (Telegram 公网访问需要)

### 安装

```bash
# 克隆仓库
git clone https://github.com/Arxchibobo/Star-Office-UI.git
cd Star-Office-UI

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install pillow numpy  # 图片处理需要
```

### 启动服务

#### 方式1：一键启动（推荐）
```bash
./start_office.sh
```

#### 方式2：手动启动
```bash
# 启动办公室后端
python backend/app_telegram.py &

# 启动状态同步
python sync_openclaw_state.py &
```

访问 `http://localhost:18793/` 查看效果。

### Telegram 公网访问配置

```bash
# 自动配置（推荐）
./setup_telegram_public.sh

# 手动配置
cloudflared tunnel --url http://localhost:18793
# 然后将生成的 URL 配置到 setup_telegram_webapp.py
```

## 📂 项目结构

```
Star-Office-UI/
├── frontend/
│   ├── index.html              # 完整版（Phaser 游戏引擎）
│   ├── debug.html              # 简化版
│   ├── office_bg.png           # AI 生成的办公室背景 (1.2MB)
│   └── lobster_bright_clean.png # AI 生成的龙虾角色（透明背景）
├── backend/
│   └── app_telegram.py         # FastAPI 后端服务
├── scripts/
│   └── remove_white_bg.py      # 图片背景去除工具
├── sync_openclaw_state.py      # 实时状态同步脚本
├── start_office.sh             # 一键启动脚本
├── setup_telegram_public.sh    # Telegram 公网配置脚本
└── office-config.json          # 配置文件
```

## 🎮 技术栈

- **前端**: Phaser 3 游戏引擎 + Vanilla JavaScript
- **后端**: FastAPI + Python 3.14
- **实时通信**: WebSocket
- **图片生成**: Gemini 3 Pro Image (nano-banana-pro skill)
- **公网访问**: Cloudflare Tunnel
- **部署**: Telegram WebApp + 本地浏览器

## 🎨 自定义

### 更换角色图片

1. 生成新的角色图片（需要白色背景）
2. 使用脚本去除白色背景：
   ```bash
   python scripts/remove_white_bg.py
   ```
3. 更新 `frontend/index.html` 中的图片路径和缩放比例

### 调整状态映射

编辑 `office-config.json` 中的 `state_mapping` 和 `office_areas` 配置。

### 修改办公室背景

替换 `frontend/office_bg.png` 并在 `frontend/index.html` 中调整位置。

## 📝 开发历程

### 主要升级
1. ✅ **名称个性化** - "海辛小龙虾的办公室" → "Bobo的办公室"
2. ✅ **背景色调整** - 深黑色 (#1a1a2e) → 亮蓝色 (#2d3561)
3. ✅ **AI生成背景** - 使用 nano-banana-pro 生成完整像素办公室场景
4. ✅ **AI生成角色** - 可爱的像素龙虾替代简陋方块
5. ✅ **透明度优化** - 手动处理去除棋盘格背景伪装
6. ✅ **颜色对比度** - 调整龙虾为鲜艳深红色，增强可见性
7. ✅ **尺寸优化** - 多次调整找到最佳大小（141px）
8. ✅ **Telegram集成** - 通过 cloudflare tunnel 实现公网访问

### Git 提交历史
完整的开发历程记录在 Git 提交中，包括：
- 背景图恢复
- 龙虾角色多次迭代优化
- Telegram WebApp 配置
- 自动化脚本开发

## 📄 文档

- [背景图恢复说明](BACKGROUND_RESTORED.md)
- [龙虾角色升级](LOBSTER_UPGRADE.md)
- [Telegram 完整版访问](TELEGRAM_FULL_VERSION.md)
- [Telegram 显示问题说明](TELEGRAM_DISPLAY_ISSUE.md)
- [Telegram 设置指南](TELEGRAM_SETUP.md)

## 🙏 致谢

- 原项目: [ringhyacinth/Star-Office-UI](https://github.com/ringhyacinth/Star-Office-UI)
- AI 图片生成: Gemini 3 Pro Image via nano-banana-pro
- 游戏引擎: [Phaser 3](https://phaser.io/)

## 📜 协议

基于原项目协议。

---

**🎮 现在就试试看你的 AI 助手在像素办公室里工作吧！** ✨
