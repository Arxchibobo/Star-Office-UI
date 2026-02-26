# ⚠️ 缺少办公室背景图片

## 问题

`frontend/office_bg.png` 文件丢失了！这个精美的像素艺术图片是办公室场景的核心。

## 原图应该是什么样的

根据截图，原图包含：
- 🖥️ 左边：工作区（桌子 + Mac电脑 + 台灯 + 咖啡杯）
- 🛋️ 中间：休息区（沙发 + 紫色星星角色）
- 💾 右上：服务器机房（Central Perk标志 + 蓝色机柜）
- 🛏️ 右下：卧室（Friends海报 + 床）
- 📚 书架、植物、装饰画
- 🟡 棋盘格米黄色地板
- 🎨 16-bit像素艺术风格

## 解决方案

### 方案1：找回原图（推荐）

检查这些位置：
```bash
~/Downloads/office_bg.png
~/Desktop/*office*.png
~/Pictures/*office*.png
```

找到后复制到：
```bash
cp /path/to/office_bg.png ~/.openclaw/workspace/projects/Star-Office-UI/frontend/
```

### 方案2：从原作者获取

- 在线版本：https://office.hyacinth.im
- GitHub：https://github.com/ringhyacinth/Star-Office-UI

### 方案3：AI生成（备选）

如果完全找不到，可以用AI生成类似的：

```bash
cd frontend
# 使用Gemini生成像素办公室
# （需要Gemini API key）
```

### 方案4：使用占位图（临时）

当前代码已经包含了基本的图形绘制，但不如原图精美。

## 当前状态

- ✅ 代码逻辑完整
- ✅ 角色动画正常
- ✅ 状态同步工作
- ❌ **缺少精美背景图**

一旦恢复 `office_bg.png`，所有功能都能正常工作！

## 临时使用

如果想先测试功能，注释掉 index.html 中的这行：
```javascript
// this.load.image('office_bg', '/static/office_bg.png');
```

然后移除：
```javascript
// this.add.image(400, 300, 'office_bg');
```

这样至少能看到角色动画和功能，只是没有漂亮的背景。

---

**找到原图后，立即复制到 `frontend/office_bg.png` 就能恢复完整体验！** 🎨
