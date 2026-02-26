# Telegram显示问题说明

## ⚠️ 当前问题

Telegram中点击"🏢 查看办公室"按钮，显示的是：
- 简化版界面（debug.html）
- 没有像素场景
- 没有动画角色
- 有时显示"错误"状态

## 🔍 问题原因

### 技术限制
Telegram WebApp有严格要求：
1. **必须HTTPS** - 不接受http://
2. **必须公网访问** - 不接受localhost
3. **需要有效证书** - 自签名证书不行

### 当前配置
```json
"url": "https://showtimes-lyric-titanium-sale.trycloudflare.com"
```
这个cloudflare tunnel URL可能已过期或不可访问。

## ✅ 解决方案

### 方案A：浏览器访问（最佳）⭐️

**直接在电脑浏览器打开：**
```
http://localhost:18793/
```

**优势：**
- ✅ 完整像素办公室背景
- ✅ 流畅的角色动画
- ✅ 所有特效（眨眼、气泡）
- ✅ 实时状态同步
- ✅ 大屏幕更好的视觉体验

**这是推荐方式！**

---

### 方案B：配置Telegram公网访问

如果确实需要在Telegram中查看：

#### 步骤1：启动cloudflare tunnel
```bash
# 方式1：临时tunnel
cloudflared tunnel --url http://localhost:18793

# 方式2：使用ngrok
ngrok http 18793
```

#### 步骤2：复制HTTPS URL
tunnel会生成类似：
```
https://xxx-yyy-zzz.trycloudflare.com
```

#### 步骤3：更新Bot配置
编辑文件：
```bash
~/.openclaw/workspace/projects/Star-Office-UI/setup_telegram_webapp.py
```

修改：
```python
WEBAPP_URL = "https://你的tunnel地址"
```

#### 步骤4：应用配置
```bash
cd ~/.openclaw/workspace/projects/Star-Office-UI
source ../venv/bin/activate
python setup_telegram_webapp.py
```

#### 注意事项
- cloudflare免费tunnel会定期更换URL
- 需要tunnel保持运行
- 每次重启都要重新配置

---

### 方案C：简化版仍然有用

Telegram中的简化版（debug.html）虽然没有动画，但可以：
- ✅ 查看实时状态
- ✅ 看到工作/休息切换
- ✅ 手机随时随地查看

适合快速查看状态。

---

## 🎯 推荐使用场景

| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| **完整体验** | 浏览器 | 动画、背景、大屏 |
| **快速查看** | Telegram简化版 | 手机方便 |
| **演示展示** | 浏览器 | 视觉效果最佳 |
| **移动监控** | 配置公网访问 | 外出时查看 |

---

## 📊 两个版本对比

### 浏览器完整版 (index.html)
- ✅ 像素办公室背景 (800x600)
- ✅ Phaser游戏引擎
- ✅ 角色走动动画
- ✅ 眨眼特效（2.5秒/次）
- ✅ 气泡对话（8秒/次）
- ✅ 区域切换（工作区/休息区）
- ✅ 底部牌匾
- ✅ 实时状态同步

### Telegram简化版 (debug.html)
- ✅ 基本状态显示
- ✅ 进度条
- ✅ 更新时间
- ❌ 无背景图
- ❌ 无动画
- ❌ 无特效

---

## 💡 最佳实践

**日常使用：**
1. 电脑上 → 浏览器打开完整版
2. 手机上 → Telegram简化版快速查看

**如果需要在Telegram看完整版：**
- 只在需要演示时配置tunnel
- 使用完后可以关闭（节省资源）

---

## 🔧 当前服务状态

```bash
# 查看服务
ps aux | grep "app_telegram.py\|sync_openclaw_state"

# 访问完整版
http://localhost:18793/

# 访问简化版
http://localhost:18793/debug

# 查看日志
tail -f /tmp/star-office.log
tail -f /tmp/office-sync.log
```

---

**建议：先在浏览器体验完整版，如果觉得满意再考虑配置Telegram公网访问！** 🎮✨
