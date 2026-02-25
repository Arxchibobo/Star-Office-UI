# Processing Creative Skill 详细指南

> **Version**: 1.0.0
> **GitHub**: https://github.com/Arxchibobo/Processing-skill-for-vibe
> **状态**: 已安装并激活

---

## 概述

Processing Creative Skill 是一个为 Claude Code 设计的创意编程技能，将 Processing/p5.js 的图形生成能力集成到日常开发工作流中。适用于：

- 🎨 **前端设计** - 动态背景、交互动画
- 📊 **数据可视化** - 动画图表、信息图
- 🎬 **动画制作** - GIF、视频、加载动画
- 📑 **PPT/演示** - 视觉素材、背景图

---

## 触发方式

### 自动触发关键词

技能会在对话中检测到以下关键词时自动激活：

| 关键词                | 示例                     |
| --------------------- | ------------------------ |
| `processing`          | "用 processing 创建动画" |
| `p5.js` / `p5js`      | "p5.js 粒子效果"         |
| `generative art`      | "生成艺术风格背景"       |
| `creative coding`     | "创意编码实现"           |
| `animated background` | "动画背景"               |
| `particle system`     | "粒子系统"               |
| `flow field`          | "流场效果"               |
| `perlin noise`        | "柏林噪声"               |
| `canvas animation`    | "画布动画"               |

### 手动调用

```
/skill processing-creative
```

---

## 核心功能

### 1. 输出模式

| 模式                | 说明                  | 使用场景          |
| ------------------- | --------------------- | ----------------- |
| **p5.js HTML**      | 可直接嵌入网页的代码  | Web 开发、落地页  |
| **Processing Java** | 桌面应用/高分辨率导出 | 4K 图像、视频制作 |
| **React 组件**      | TypeScript + react-p5 | React 项目        |
| **Vue 组件**        | Vue 3 Composition API | Vue 项目          |

### 2. 视觉模式库 (6种)

#### 粒子系统 (Particles)

```
"Create a particle system with connections"
```

- 交互式粒子
- 动态连线
- 鼠标跟随
- 物理模拟

#### 流场 (Flow Field)

```
"Generate a flow field with Perlin noise"
```

- Perlin 噪声驱动
- 有机流动效果
- 可配置密度和速度
- 支持颜色渐变

#### 几何网格 (Geometric Grid)

```
"Design an interactive geometric grid"
```

- 响应式形状网格
- 鼠标交互效果
- 多种形状（方形、圆形、六边形）
- 旋转和缩放动画

#### 波浪动画 (Waves)

```
"Create wave animation layers"
```

- 正弦波叠加
- 海洋效果
- 涟漪扩散
- 音频可视化风格

#### 渐变背景 (Gradients)

```
"Generate animated gradient background"
```

- 线性/径向渐变
- 网格渐变（Mesh Gradient）
- 极光效果（Aurora）
- 锥形渐变

#### 数据可视化 (Data Visualization)

```
"Create animated bar chart for [65, 59, 80, 81, 56]"
```

- 柱状图（带动画）
- 折线图（多系列）
- 饼图/环形图
- 进入动画效果

### 3. 颜色主题系统 (16种)

#### 鲜艳主题

| 主题        | 风格     | 色值                                    |
| ----------- | -------- | --------------------------------------- |
| `neonNight` | 霓虹夜   | #FF006E #FB5607 #FFBE0B #8338EC #3A86FF |
| `cyberpunk` | 赛博朋克 | #ff00ff #00ffff #ff0080 #80ff00 #0080ff |
| `synthwave` | 合成波   | #ff71ce #01cdfe #05ffa1 #b967ff #fffb96 |
| `tropical`  | 热带     | #ff6b6b #feca57 #48dbfb #ff9ff3 #54a0ff |

#### 柔和主题

| 主题           | 风格     | 色值                                    |
| -------------- | -------- | --------------------------------------- |
| `softPastel`   | 柔和粉彩 | #FFB5A7 #FCD5CE #F8EDEB #F9DCC4 #FEC89A |
| `dreamyPink`   | 梦幻粉   | #ffafcc #ffc8dd #cdb4db #a2d2ff #bde0fe |
| `mintFresh`    | 薄荷清新 | #95d5b2 #74c69d #52b788 #40916c #2d6a4f |
| `lavenderMist` | 薰衣草   | #e0aaff #c77dff #9d4edd #7b2cbf #5a189a |

#### 深色主题

| 主题        | 风格   | 色值                                    |
| ----------- | ------ | --------------------------------------- |
| `darkTech`  | 科技暗 | #1B263B #415A77 #778DA9 #E0E1DD #FFFFFF |
| `midnight`  | 午夜   | #1a1a3e #2d2d6e #4040a1 #6666cc #9999ff |
| `deepOcean` | 深海   | #112240 #1d3557 #457b9d #a8dadc #f1faee |

#### 自然主题

| 主题     | 风格 | 色值                                    |
| -------- | ---- | --------------------------------------- |
| `forest` | 森林 | #606C38 #283618 #FEFAE0 #DDA15E #BC6C25 |
| `sunset` | 日落 | #ff7e5f #feb47b #ffcc5c #ff6f61 #c94c4c |
| `ocean`  | 海洋 | #005f73 #0a9396 #94d2bd #e9d8a6 #ee9b00 |
| `autumn` | 秋日 | #d4a373 #ccd5ae #e9edc9 #fefae0 #faedcd |

---

## 使用示例

### 场景 1: 落地页动画背景

**提示词:**

```
Create an animated particle background for my landing page with neon theme
```

**输出:** 完整 HTML 文件，包含：

- p5.js CDN 引入
- 粒子系统代码
- 响应式布局
- Hero 内容层

### 场景 2: 数据可视化

**提示词:**

```
Generate an animated bar chart for weekly sales data:
Data: [65, 59, 80, 81, 56, 55, 40]
Labels: [Mon, Tue, Wed, Thu, Fri, Sat, Sun]
```

**输出:** 带动画的柱状图代码，包含：

- 进入动画（easeOutQuart）
- 颜色渐变
- 数值标签
- 响应式尺寸

### 场景 3: React 组件

**提示词:**

```
Create a p5.js React component for flow field background
```

**输出:** TypeScript React 组件，包含：

- Props 类型定义
- 响应式画布
- 生命周期管理
- 可配置参数

### 场景 4: 高分辨率导出

**提示词:**

```
Create a Processing sketch for 4K flow field art export
```

**输出:** Processing Java 代码，包含：

- 4K 分辨率设置
- 按 S 键保存
- 多种颜色调色板
- 帧率优化

### 场景 5: PPT 页面转换动画 ⭐ **重要**

**核心原则**: Processing 动画应该是**页面转换效果**，不是页面背景。

**错误做法** ❌:

```
整页动态背景（粒子/神经网络），看不到 PPT 内容
```

**正确做法** ✅:

```
1. 每页显示 PPT 图片（slide-01.png, slide-02.png...）
2. 页面切换时播放 Processing 过渡动画（0.5-1秒）
3. 动画结束后显示新页面内容
```

**提示词示例:**

```
Create an HTML slideshow that displays PPT images (slide-01.png to slide-12.png)
with p5.js transition animations between pages. Use particle connections effect
for transitions. Keep animations subtle (under 1 second).
```

**输出:** HTML 文件，包含：

- 图片幻灯片容器
- p5.js 过渡动画层（z-index: 1000，初始 opacity: 0）
- 键盘/按钮导航
- 页面切换时触发动画（fadeIn 0.5s → 粒子动画 → fadeOut 0.5s）
- 动画完成后显示新页面

**关键技术细节:**

```javascript
// 页面容器 - 显示 PPT 图片
<div class="slide active">
  <img src="slide-01.png">
</div>

// 过渡层 - Processing 动画
<canvas id="transition-canvas" style="z-index: 1000; opacity: 0"></canvas>

// 切换逻辑
function changePage() {
  transitionCanvas.style.opacity = '1';    // 显示动画层
  playTransitionAnimation();               // 播放 0.5s 动画
  setTimeout(() => {
    switchSlideContent();                  // 切换图片
    transitionCanvas.style.opacity = '0';  // 隐藏动画层
  }, 500);
}
```

**适用动画类型:**

- ✅ 粒子连线扩散（简约科技感）
- ✅ 光波扫过（数据主题）
- ✅ 方块翻转（几何风格）
- ✅ 渐变流动（柔和过渡）
- ❌ 持续的背景动画（会遮挡内容）

---

## 自动化脚本

### 运行 Processing 草图

**Windows PowerShell:**

```powershell
.\scripts\run-sketch.ps1 -SketchPath "examples\particles"
.\scripts\run-sketch.ps1 -SketchPath "examples\particles" -Export
.\scripts\run-sketch.ps1 -SketchPath "examples\particles" -Present
```

**Bash:**

```bash
./scripts/run-sketch.sh examples/particles
./scripts/run-sketch.sh examples/particles --export
./scripts/run-sketch.sh examples/particles --present
```

### 帧序列转视频

```bash
# 转 GIF
./scripts/convert-frames.sh frames/ output --gif

# 转 MP4
./scripts/convert-frames.sh frames/ output --mp4 --fps 60

# 全部格式
./scripts/convert-frames.sh frames/ output --all --quality high
```

---

## 导出选项

### 从 p5.js 导出

```javascript
// 保存 PNG
function keyPressed() {
  if (key === 's') saveCanvas('design', 'png');
}

// 保存 GIF (5秒)
function setup() {
  createCanvas(400, 400);
  saveGif('animation', 5);
}

// 保存帧序列
function draw() {
  // ... 绑制代码
  if (frameCount <= 300) {
    saveCanvas('frame-' + nf(frameCount, 4), 'png');
  }
}
```

### 从 Processing Java 导出

```java
// 保存高分辨率
void keyPressed() {
  if (key == 's') {
    save("output/design-" + frameCount + ".png");
  }
}

// 保存帧序列
void draw() {
  // ... 绘制代码
  saveFrame("frames/frame-####.png");
  if (frameCount > 300) exit();
}
```

---

## 项目文件结构

```
Processing-skill-for-vibe/
├── skill/
│   └── processing-creative.md     # Claude 技能定义
├── scripts/
│   ├── run-sketch.ps1             # Windows 运行脚本
│   ├── run-sketch.sh              # Bash 运行脚本
│   ├── convert-frames.sh          # 帧转视频
│   └── install-processing.js      # 安装检查
├── templates/
│   ├── landing-page-hero.html     # 落地页模板
│   ├── pattern-showcase.html      # 模式预览页
│   ├── react-p5-component.tsx     # React 组件
│   └── vue-p5-component.vue       # Vue 组件
├── patterns/
│   ├── flow-field.js              # 流场
│   ├── geometric-grid.js          # 几何网格
│   ├── data-visualization.js      # 数据可视化
│   ├── waves-animation.js         # 波浪动画
│   ├── gradient-backgrounds.js    # 渐变背景
│   └── color-themes.js            # 颜色主题
├── examples/
│   ├── particles/particles.pde    # 粒子示例
│   └── flowfield/flowfield.pde    # 流场示例
└── docs/
    ├── INSTALLATION.md            # 安装指南
    └── COMMANDS.md                # 命令参考
```

---

## 依赖要求

| 依赖           | 必需 | 说明                 |
| -------------- | ---- | -------------------- |
| Node.js 18+    | 是   | 运行脚本和开发服务器 |
| Processing 4.x | 可选 | Java 桌面功能        |
| FFmpeg         | 可选 | 视频导出             |

### 安装依赖

```bash
# Node 依赖
cd Processing-skill-for-vibe
npm install

# Processing (Windows)
choco install processing

# FFmpeg (Windows)
choco install ffmpeg
```

---

## 快速参考卡

```
┌────────────────────────────────────────────────────────────┐
│              PROCESSING CREATIVE SKILL                      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  触发词: processing, p5.js, generative art, particle,       │
│         flow field, animated background, creative coding    │
│                                                             │
│  输出模式:                                                   │
│    • p5.js HTML (Web)     • Processing .pde (桌面)          │
│    • React 组件           • Vue 组件                         │
│                                                             │
│  视觉模式:                                                   │
│    • 粒子系统    • 流场       • 几何网格                      │
│    • 波浪动画    • 渐变背景   • 数据图表                      │
│                                                             │
│  颜色主题: 16 种 (neon, synthwave, pastel, tech...)         │
│                                                             │
│  导出格式: PNG, GIF, MP4, WebM, 独立应用                     │
│                                                             │
│  快捷键 (草图内):                                            │
│    S - 保存图像    R - 重置    1-5 - 切换模式                │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## 灵感来源

技能设计参考了以下 Processing 艺术家的风格：

- **[@yuruyurau](https://x.com/yuruyurau)** - 几何图案、极简动画
- **[@KomaTebe](https://x.com/KomaTebe)** - 复杂生成系统、算法艺术

可在对话中指定风格：

```
"Create a geometric pattern in yuruyurau's style"
"Generate a complex generative system like KomaTebe"
```

---

## 相关资源

- [Processing 官方文档](https://processing.org/reference/)
- [p5.js 参考](https://p5js.org/reference/)
- [p5.js 在线编辑器](https://editor.p5js.org/)
- [The Coding Train 教程](https://thecodingtrain.com/)

---

## 更新日志

### v1.0.0 (2026-01-16)

- 初始发布
- 6 种视觉模式
- 16 种颜色主题
- React/Vue 组件模板
- 自动化脚本
- 完整文档
