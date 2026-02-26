# 在 Telegram 中查看完整像素办公室

## 🎮 现在的完整功能

完整的像素办公室包括：
- **🦞 动画角色**：会在工作区和休息区之间走动
- **👁️ 眨眼动画**：每2.5秒眨一次眼
- **💬 气泡对话**：定期冒出状态气泡
- **🏢 完整场景**：
  - 📚 书架
  - 💻 工作桌和电脑
  - 🛋️ 休息沙发
  - 💡 台灯
  - 🪟 窗户
  - ⭐ Bobo的办公室牌匾

## 📱 在 Telegram 中使用

### 方案1：本地测试（推荐）

**直接在浏览器访问：**
```bash
http://localhost:18793/
```

看到角色动画、走动、眨眼等功能。

---

### 方案2：Telegram WebApp（需要公网）

**问题**：Telegram WebApp 需要HTTPS和公网访问。

**解决方案A：使用 Cloudflare Tunnel**

1. 安装cloudflared：
```bash
# 已安装，直接运行
cloudflared tunnel --url http://localhost:18793
```

2. 复制生成的公网URL（如 `https://xxx.trycloudflare.com`）

3. 更新Bot配置：
```bash
cd ~/.openclaw/workspace/projects/Star-Office-UI
# 编辑 setup_telegram_webapp.py
# 将 WEBAPP_URL 改为你的cloudflare URL
python setup_telegram_webapp.py
```

4. 在Telegram中点击Bot菜单的"🏢 查看办公室"

---

**解决方案B：使用 ngrok**

```bash
ngrok http 18793
# 复制https URL并更新setup_telegram_webapp.py
```

---

## 🖥️ 本地浏览器使用（最简单）

**完整版（推荐）：**
```
http://localhost:18793/
```
- 有完整的像素场景
- 角色会走动
- 实时状态同步

**调试版：**
```
http://localhost:18793/debug
```
- 简化界面
- 只显示状态文字

---

## 🔄 当前运行状态

```bash
# 查看服务状态
ps aux | grep "app_telegram.py\|sync_openclaw_state"

# 查看日志
tail -f /tmp/star-office.log
tail -f /tmp/office-sync.log

# 重启服务
cd ~/.openclaw/workspace/projects/Star-Office-UI
./start_office.sh
```

---

## 🎯 快速测试动画

1. 打开浏览器：http://localhost:18793/
2. 观察右上角的红色龙虾角色
3. 给我发消息，角色会移动到工作桌
4. 等一会儿，它会回到休息区
5. 注意眨眼动画和气泡

---

## 💡 提示

- **完整版需要Phaser游戏引擎加载**，可能需要2-3秒
- **角色大小**：红色方块角色（像素风格）
- **移动速度**：根据状态变化平滑移动
- **气泡**：每8秒冒一次
- **眨眼**：每2.5秒一次

现在立即在浏览器打开看效果！🚀
