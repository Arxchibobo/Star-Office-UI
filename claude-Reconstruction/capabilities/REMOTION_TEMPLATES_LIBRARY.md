# Remotion 模板库

> **来源**: [React Video Editor - Remotion Templates](https://www.reactvideoeditor.com/remotion-templates)
> **仓库**: https://github.com/reactvideoeditor/remotion-templates
> **许可**: MIT License（可用于个人和商业项目）

---

## 📚 模板总览

### 本地模板库（15个核心模板）

| 模板名称                 | 类型       | 适用场景             | 技术特点             | 视觉效果            |
| ------------------------ | ---------- | -------------------- | -------------------- | ------------------- |
| **animated-list**        | 列表动画   | 特性展示、步骤说明   | Spring动画、延迟入场 | 从左滑入+缩放+渐显  |
| **animated-text**        | 文字动画   | 标题、口号           | 逐字动画、旋转入场   | 字符下落旋转        |
| **bounce-text**          | 标题卡片   | 开场、章节分隔       | 渐变背景、弹性缩放   | 弹跳式入场+渐变卡片 |
| **bubble-pop-text**      | 气泡文字   | 趣味标题、品牌展示   | 圆形气泡、弹性缩放   | 气泡依次弹出        |
| **card-flip**            | 卡片翻转   | 信息切换、产品展示   | 3D翻转、透视效果     | 360度翻转           |
| **floating-bubble-text** | 悬浮气泡   | 强调文字、焦点展示   | 浮动动画、霓虹边框   | 上下浮动+霓虹效果   |
| **geometric-patterns**   | 几何背景   | 科技感背景、过渡场景 | 多层旋转、缩放       | 几何图形旋转        |
| **glitch-text**          | 故障文字   | 赛博朋克、科技主题   | RGB偏移、抖动效果    | 三色分离抖动        |
| **liquid-wave**          | 液态波浪   | 背景效果、过渡动画   | SVG路径、正弦波      | 流动的液态波浪      |
| **matrix-rain**          | 矩阵雨     | 科技主题、黑客风格   | 随机字符、下落动画   | 绿色/蓝色字符雨     |
| **particle-explosion**   | 粒子爆炸   | 爆炸效果、强调时刻   | 粒子系统、径向扩散   | 粒子旋转爆炸        |
| **pulsing-text**         | 脉冲文字   | 节奏感强调、音乐视频 | 周期缩放、光晕效果   | 逐字脉冲闪烁        |
| **slide-text**           | 滑动文字   | 简单标题、字幕       | 平滑滑入、渐显       | 从右滑入            |
| **sound-wave**           | 声波可视化 | 音乐视频、音频展示   | 动态柱状图、音频同步 | 律动的声波条        |
| **typewriter-subtitle**  | 打字机字幕 | 字幕、对话、旁白     | 逐字显示、光标闪烁   | 打字机效果+闪烁光标 |

---

## 🎨 按场景分类

### 1. 标题和开场（6个）

#### **animated-text** - 动态标题

```typescript
// 适用场景：视频开场、章节标题
// 效果：字符逐个从上下落并旋转入场
// 配色：白色文字
// 时长建议：2-3秒

const text = 'Hello Remotion'.split('');
// 每个字符延迟 5 帧入场
// Spring动画：从-50px下落，旋转-180度到0度
```

**最佳实践**：

- 文字长度：6-15个字符
- 适合：科技、现代、活力风格
- 搭配：深色背景

---

#### **bounce-text** - 弹跳标题卡片

```typescript
// 适用场景：产品介绍、宣传视频
// 效果：渐变卡片+弹性入场+字幕淡入
// 配色：蓝色渐变（#1e3a8a → #3b82f6）
// 时长建议：3-5秒

// 主标题：slideIn + scaleIn
// 副标题：延迟15帧淡入
```

**最佳实践**：

- 主标题：3-8个字
- 副标题：10-20个字
- 适合：专业、商务、科技风格

---

#### **bubble-pop-text** - 气泡弹出

```typescript
// 适用场景：趣味视频、儿童内容、品牌展示
// 效果：圆形气泡依次弹出
// 配色：蓝色渐变+半透明边框
// 时长建议：1-2秒

// 每个字符延迟 5 帧
// 弹性缩放：从0到1，damping=8, stiffness=100
```

**最佳实践**：

- 文字长度：3-6个字符
- 适合：活泼、有趣、年轻风格
- 配色可调：修改 background gradient

---

#### **slide-text** - 简单滑入

```typescript
// 适用场景：简洁字幕、快速切换
// 效果：从右滑入+渐显
// 配色：白色文字
// 时长建议：1秒

// Spring动画：从200px滑入到0
// 30帧完成动画
```

**最佳实践**：

- 最简洁的文字入场
- 适合：极简风格、快节奏视频

---

#### **pulsing-text** - 脉冲闪烁

```typescript
// 适用场景：音乐视频、节奏感强的内容
// 效果：逐字脉冲+光晕效果
// 配色：白色文字+白色光晕
// 时长建议：持续循环

// 每个字符延迟 6 帧
// 30帧为一个周期，缩放 1 → 1.2 → 1
```

**最佳实践**：

- 适合：EDM、电子音乐、派对视频
- 可配合音频：使用 useAudioData

---

#### **glitch-text** - 故障效果

```typescript
// 适用场景：赛博朋克、黑客主题、科技视频
// 效果：RGB分离+抖动
// 配色：青色(cyan) + 品红(magenta) + 白色
// 时长建议：持续循环

// 三层文字：青色偏移、品红偏移、白色主体
// mixBlendMode: 'screen'
```

**最佳实践**：

- 适合：Cyberpunk、Synthwave风格
- 不宜过长使用：容易视觉疲劳
- 搭配：深色背景

---

### 2. 列表和信息展示（1个）

#### **animated-list** - 动画列表

```typescript
// 适用场景：功能特性、步骤说明、数据展示
// 效果：列表项依次从左滑入+缩放+圆形图标
// 配色：蓝色系（可自定义）
// 时长建议：每项1秒，总3-5秒

const items = [
  { name: '特性一', color: '#3b82f6' },
  { name: '特性二', color: '#60a5fa' },
  { name: '特性三', color: '#93c5fd' },
];

// 每项延迟 5 帧
// 三重动画：slideX、opacity、scale
```

**最佳实践**：

- 列表项数量：3-5项
- 适合：产品功能、步骤教程、优势展示
- 自定义：修改 items 数组的颜色和名称

---

### 3. 特效和背景（6个）

#### **card-flip** - 3D卡片翻转

```typescript
// 适用场景：产品展示、信息切换
// 效果：360度翻转，正反两面
// 配色：蓝色渐变
// 时长建议：2-3秒

// 3D透视：perspective: "1000px"
// 正反面：backfaceVisibility: "hidden"
// 旋转：rotateY(0 → 360deg)
```

**最佳实践**：

- 正面：品牌/产品图
- 反面：详细信息/CTA
- 适合：产品对比、前后对比

---

#### **floating-bubble-text** - 悬浮气泡

```typescript
// 适用场景：强调文字、焦点展示
// 效果：上下浮动+霓虹边框
// 配色：蓝色渐变+青品渐变边框
// 时长建议：持续循环

// 浮动：Math.sin(frame / 30) * 20
// 霓虹边框：gradient(45deg, cyan, magenta)
```

**最佳实践**：

- 适合：关键信息、CTA、强调内容
- 搭配：深色背景

---

#### **geometric-patterns** - 几何图案背景

```typescript
// 适用场景：科技感背景、过渡场景
// 效果：20个几何图形旋转+缩放
// 配色：深色渐变（#0f172a → #1e293b）
// 时长建议：持续循环

// 20个图形，每个延迟 3 帧
// 旋转：0 → 360度
// 边框圆角：index * 5%（渐变形状）
```

**最佳实践**：

- 作为背景层使用
- 适合：科技、现代、极简风格
- 可调整：图形数量、颜色、旋转速度

---

#### **liquid-wave** - 液态波浪

```typescript
// 适用场景：背景效果、过渡动画
// 效果：流动的液态波浪
// 配色：蓝色渐变（#1e3a8a → #3b82f6）
// 时长建议：持续循环

// SVG路径动画
// 50个控制点
// 正弦波：Math.sin(frame / 20 + i / 5) * 50
```

**最佳实践**：

- 作为背景层或过渡效果
- 适合：水、流体、自然主题
- 可调整：波浪高度、速度

---

#### **matrix-rain** - 矩阵雨

```typescript
// 适用场景：科技主题、黑客风格
// 效果：随机字符下落
// 配色：蓝色系（可改为绿色）
// 时长建议：持续循环

const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*';
// 每列独立速度
// 文字阴影：glow效果
```

**最佳实践**：

- 作为背景层
- 适合：Cyberpunk、科技、编程主题
- 经典绿色：改为 #00ff00

---

#### **particle-explosion** - 粒子爆炸

```typescript
// 适用场景：爆炸效果、强调时刻、转场
// 效果：150个粒子径向旋转扩散
// 配色：蓝色系渐变（HSL动态）
// 时长建议：3-4秒

// 粒子数：150
// 旋转角度：baseAngle + frame * 0.02
// 距离：0 → 180-220px
```

**最佳实践**：

- 适合：产品发布、重要时刻、转场
- 中心文字：可自定义
- 性能：粒子数量可调

---

### 4. 字幕和文字效果（2个）

#### **typewriter-subtitle** - 打字机字幕

```typescript
// 适用场景：字幕、对话、旁白
// 效果：逐字显示+闪烁光标
// 配色：白色文字+蓝色光标
// 时长建议：根据文字长度自动

const text = 'I like typing...';
// 45帧显示完整文字
// 光标闪烁：15帧周期
```

**最佳实践**：

- 适合：教程、采访、对话
- 字体：等宽字体（Courier New）
- 速度：可调整帧数比例

---

#### **sound-wave** - 声波可视化

```typescript
// 适用场景：音乐视频、音频展示、播客
// 效果：40个律动的声波柱
// 配色：白色柱状+蓝色阴影
// 时长建议：持续循环

// 40个柱状图
// 高度：Math.sin(frame / 10 + i / 2) * 100
// 可配合：useAudioData() 实现真实音频同步
```

**最佳实践**：

- 适合：音乐、播客、音频内容
- 进阶：使用 useAudioData 同步真实音频
- 颜色：可改为彩虹渐变

---

## 🚀 快速使用指南

### 1. 复制模板到项目

```bash
# 克隆模板库
git clone https://github.com/reactvideoeditor/remotion-templates.git

# 复制需要的模板到你的项目
cp remotion-templates/templates/animated-text.tsx ./src/components/
```

### 2. 集成到 Remotion

```tsx
// src/Root.tsx
import { Composition } from 'remotion';
import AnimatedText from './components/animated-text';

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="AnimatedText"
        component={AnimatedText}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
```

### 3. 自定义模板

```tsx
// 修改文字内容
const text = '你的标题'.split('');

// 修改配色
background: 'linear-gradient(45deg, #your-color-1, #your-color-2)';

// 修改动画参数
const slideX = spring({
  frame: frame - delay,
  fps,
  from: -100,
  to: 0,
  config: {
    damping: 12, // 阻尼（越大越稳定）
    mass: 0.5, // 质量（越大越缓慢）
    stiffness: 100, // 刚度（越大越快）
  },
});
```

---

## 📖 进阶技巧

### 1. 组合多个模板

```tsx
// 开场：animated-text (0-90帧)
// 列表：animated-list (90-240帧)
// 结尾：particle-explosion (240-330帧)

export const MyVideo = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill>
      {frame < 90 && <AnimatedText />}
      {frame >= 90 && frame < 240 && <AnimatedList />}
      {frame >= 240 && <ParticleExplosion />}
    </AbsoluteFill>
  );
};
```

### 2. 背景+前景叠加

```tsx
<AbsoluteFill>
  {/* 背景层 */}
  <GeometricPatterns />

  {/* 内容层 */}
  <div style={{ position: 'relative', zIndex: 10 }}>
    <AnimatedText />
  </div>
</AbsoluteFill>
```

### 3. 动态数据驱动

```tsx
// 从API获取数据
const items = props.features.map((feature, i) => ({
  name: feature.title,
  color: feature.color,
}));

// 渲染列表
<AnimatedList items={items} />;
```

### 4. 音频同步

```tsx
import { useAudioData, Audio } from 'remotion';

export const SyncedSoundWave = () => {
  const audioData = useAudioData('./audio.mp3');

  // 使用真实音频数据驱动声波
  const amplitude = audioData?.getAmplitude(frame) || 0;
  const height = amplitude * 200;

  return <div style={{ height: `${height}px` }} />;
};
```

---

## 🎨 配色方案参考

### 科技/现代风格

```typescript
primary: '#0066ff';
secondary: '#00ffff';
background: '#1e1e1e';
accent: '#FFFFFF';
```

### Cyberpunk/赛博朋克

```typescript
primary: '#00FFFF';
secondary: '#FF00FF';
background: '#0A0E27';
accent: '#FFFF00';
```

### 专业/商务

```typescript
primary: '#2C3E50';
secondary: '#34495E';
background: '#ECF0F1';
accent: '#E74C3C';
```

### 温暖/友好

```typescript
primary: '#E76F51';
secondary: '#F4A261';
background: '#FFFBF7';
accent: '#2A9D8F';
```

---

## 🔗 扩展资源

### 官方资源

- **官网模板库**: https://www.reactvideoeditor.com/remotion-templates
- **GitHub仓库**: https://github.com/reactvideoeditor/remotion-templates
- **Remotion文档**: https://www.remotion.dev/docs/

### 学习资源

- **Spring动画**: https://www.remotion.dev/docs/spring
- **Interpolate**: https://www.remotion.dev/docs/interpolate
- **useAudioData**: https://www.remotion.dev/docs/use-audio-data

---

## 📝 模板选择决策树

```
用户需求 → 场景类型 → 推荐模板

标题展示 →
  ├─ 简洁现代 → slide-text
  ├─ 动感活力 → animated-text
  ├─ 专业商务 → bounce-text
  └─ 趣味可爱 → bubble-pop-text

信息展示 →
  ├─ 功能列表 → animated-list
  ├─ 步骤说明 → animated-list
  └─ 产品切换 → card-flip

字幕效果 →
  ├─ 对话/旁白 → typewriter-subtitle
  └─ 音频展示 → sound-wave

背景/特效 →
  ├─ 科技背景 → geometric-patterns
  ├─ 流体效果 → liquid-wave
  ├─ 赛博朋克 → matrix-rain / glitch-text
  ├─ 悬浮强调 → floating-bubble-text
  └─ 爆炸转场 → particle-explosion

节奏感内容 →
  ├─ 音乐视频 → pulsing-text / sound-wave
  └─ 电子音乐 → pulsing-text + particle-explosion
```

---

## 🤖 自动匹配逻辑（供 AI 使用）

当检测到 Remotion 视频制作需求时：

1. **分析场景类型**
   - 关键词：标题、列表、字幕、背景、爆炸、音乐

2. **匹配模板**
   - 标题 → animated-text / bounce-text
   - 列表 → animated-list
   - 字幕 → typewriter-subtitle
   - 背景 → geometric-patterns / liquid-wave
   - 特效 → particle-explosion / glitch-text
   - 音乐 → sound-wave / pulsing-text

3. **组合建议**
   - 开场：animated-text / bounce-text
   - 主体：animated-list / card-flip
   - 背景：geometric-patterns / matrix-rain
   - 转场：particle-explosion
   - 结尾：floating-bubble-text + particle-explosion

4. **技术栈选择**
   - 简单动画：Spring
   - 复杂插值：Interpolate
   - 音频同步：useAudioData
   - 背景效果：SVG / Canvas

---

**最后更新**: 2026-02-03
**模板数量**: 15个核心模板
**状态**: 生产就绪 ✅
