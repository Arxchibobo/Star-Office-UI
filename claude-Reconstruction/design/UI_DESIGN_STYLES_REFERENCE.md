# UI/UX 设计风格完整参考指南

> **来源**: https://32kw.com/view/a2786f9 | **收录日期**: 2026-01-21 | **总计**: 30 种设计风格

---

## 📋 快速索引

| 分类         | 风格数量 | 代表风格                                                 |
| ------------ | -------- | -------------------------------------------------------- |
| **主流风格** | 6        | Minimalism, Glassmorphism, Neumorphism                   |
| **现代趋势** | 5        | Claymorphism, Aurora UI, Neubrutalism                    |
| **复古风格** | 5        | Retro-Futurism, Y2K, Vaporwave                           |
| **科技美学** | 4        | Cyberpunk UI, HUD/Sci-Fi FUI, AI-Native UI               |
| **自然风格** | 3        | Organic Biophilic, Biomimetic, E-Ink/Paper               |
| **动效驱动** | 4        | Motion-Driven, Micro-interactions, Parallax              |
| **特殊风格** | 3        | Spatial UI (VisionOS), Gen Z Chaos, Dimensional Layering |

---

## 01 主流风格 (Mainstream Styles)

### 1. Minimalism (极简主义)

**特征**:

- 只关注必要元素
- 简洁线条，大量留白
- 有限的配色方案
- 有目的性的排版
- 创造平静的界面体验

**适用场景**:

- 专业工具/SaaS 平台
- 内容为主的网站
- 需要清晰信息层级的应用

**配色建议**:

```
主色: 1-2 种主色调
辅助: 灰度系统（白/灰/黑）
强调: 单一强调色
```

**Nano Banana Pro 提示词模板**:

```
"Minimalist UI design, clean lines, ample whitespace, limited color palette,
purposeful typography, calm interface, 16:9"
```

---

### 2. Glassmorphism (玻璃拟态)

**特征**:

- 磨砂玻璃效果
- 透明度和模糊
- 通过分层创造深度
- 鲜艳的背景渐变透过半透明元素

**适用场景**:

- 现代化 Web 应用
- 高端品牌展示
- iOS/macOS 风格应用

**配色建议**:

```
背景: 鲜艳渐变（如紫色到粉色）
玻璃: 半透明白色 (rgba(255,255,255,0.1-0.3))
边框: 微妙的白色描边
模糊: backdrop-filter: blur(10px)
```

**Nano Banana Pro 提示词模板**:

```
"Glassmorphism UI design, frosted glass effect, transparency and blur,
vivid gradient background, depth through layering, 16:9"
```

---

### 3. Neumorphism (新拟物化)

**特征**:

- 柔和 UI，使用挤出和内凹阴影
- 背景与元素颜色匹配
- 创造触感、可触摸的界面元素
- 元素看起来从屏幕突出

**适用场景**:

- 智能家居控制面板
- 音乐播放器
- 触摸设备应用

**配色建议**:

```
背景: 中性色（如 #e0e5ec）
阴影-明: 白色或浅色
阴影-暗: 深灰色
元素: 与背景相同或非常接近
```

**注意事项**:
⚠️ 可访问性问题：对比度可能不足
⚠️ 不适合文本密集型界面

**Nano Banana Pro 提示词模板**:

```
"Neumorphism soft UI, extruded and inset shadows, matching background colors,
tactile touchable elements, 16:9"
```

---

### 4. Brutalism (粗野主义)

**特征**:

- 粗糙、故意粗犷的美学
- 粗体排版，强烈对比
- 非常规布局
- 拒绝精致的设计原则

**适用场景**:

- 创意工作室/作品集
- 艺术/文化项目
- 前卫品牌

**配色建议**:

```
主色: 黑白或单色
强调: 高饱和度原色（红/黄/蓝）
对比: 极强对比
```

**Nano Banana Pro 提示词模板**:

```
"Brutalist design, raw harsh aesthetics, bold typography, stark contrasts,
unconventional layout, rejecting polished principles, 16:9"
```

---

### 5. Flat Design (扁平设计)

**特征**:

- 二维元素，无渐变、阴影或纹理
- 依赖简洁形状和明亮颜色
- 清晰的视觉层级
- 简化的图标

**适用场景**:

- 移动应用
- 响应式网站
- 快速加载的界面

**配色建议**:

```
主色: 明亮、饱和的颜色
辅助: 柔和的互补色
文字: 深灰色（非纯黑）
```

**Nano Banana Pro 提示词模板**:

```
"Flat design, two-dimensional elements, no gradients shadows textures,
clean shapes bright colors, clear visual hierarchy, 16:9"
```

---

### 6. Skeuomorphism (拟物化)

**特征**:

- 数字元素模仿真实世界物体
- 使用纹理、渐变和阴影
- 创造直观、熟悉的界面

**适用场景**:

- 教育应用（降低学习曲线）
- 游戏界面
- 传统行业数字化

**配色建议**:

```
材质: 真实材质颜色（木纹、皮革、金属）
光影: 自然光照效果
细节: 高度写实的纹理
```

**Nano Banana Pro 提示词模板**:

```
"Skeuomorphic design, digital elements mimicking real-world objects,
textures gradients shadows, intuitive familiar interface, 16:9"
```

---

## 02 现代趋势 (Modern Trends)

### 7. Claymorphism (黏土拟态)

**特征**:

- 3D 黏土般外观
- 柔软、蓬松的元素
- 柔和色彩、圆润形状
- 内阴影创造可亲近的玩具般美学

**适用场景**:

- 儿童应用
- 创意插画风网站
- 友好品牌形象

**配色建议**:

```
主色: 柔和粉彩色（粉/蓝/黄）
阴影: 微妙的内阴影
高光: 柔和的白色高光
```

**Nano Banana Pro 提示词模板**:

```
"Claymorphism 3D clay-like appearance, soft pillowy elements, pastel colors,
rounded shapes, inner shadows, approachable toy-like aesthetics, 16:9"
```

---

### 8. Aurora UI (极光 UI)

**特征**:

- 流动、动画化的渐变
- 灵感来自北极光
- 梦幻、空灵的氛围
- 柔和的色彩过渡

**适用场景**:

- 高端品牌网站
- 创意作品集
- 沉浸式体验

**配色建议**:

```
渐变: 紫色/粉色/蓝色/绿色流动渐变
过渡: 平滑、动态的色彩变化
背景: 深色背景衬托渐变
```

**Nano Banana Pro 提示词模板**:

```
"Aurora UI, flowing animated gradients inspired by Northern Lights,
dreamy ethereal atmosphere, soft color transitions, 16:9"
```

---

### 9. Liquid Glass (液态玻璃)

**特征**:

- 结合玻璃拟态与流体有机形状
- 动画化的气泡
- 平滑曲线和透明度
- 创造活生生的、会呼吸的界面

**适用场景**:

- 高端品牌
- 艺术/设计展示
- 前沿科技产品

**配色建议**:

```
背景: 深色或渐变
玻璃: 半透明白色带模糊
形状: 有机、流动的形状
```

**Nano Banana Pro 提示词模板**:

```
"Liquid glass design, glassmorphism with fluid organic shapes,
animated blobs, smooth curves, transparency, living breathing interface, 16:9"
```

---

### 10. Neubrutalism (新粗野主义)

**特征**:

- 更柔和的粗野主义变体
- 粗体轮廓线
- 偏移阴影
- 明亮的强调色
- 结合粗犷能量与俏皮、卡通元素

**适用场景**:

- 年轻品牌
- 创意工作室
- 现代电商

**配色建议**:

```
主色: 黑色轮廓
背景: 白色或明亮色彩
强调: 高饱和度亮色（黄/粉/绿）
阴影: 偏移的实心阴影
```

**Nano Banana Pro 提示词模板**:

```
"Neubrutalism design, softer brutalism variation, bold outlines,
offset shadows, bright accent colors, playful cartoonish elements, 16:9"
```

---

### 11. Bento Box Grid (便当盒网格)

**特征**:

- 模块化布局，灵感来自日本便当盒
- 不同尺寸的卡片和谐组织
- 高效空间利用
- 视觉平衡

**适用场景**:

- Dashboard 仪表盘
- 内容密集型网站
- 卡片式布局

**配色建议**:

```
背景: 浅色或深色统一背景
卡片: 白色或微妙色彩区分
边框: 微妙的分隔线
```

**Nano Banana Pro 提示词模板**:

```
"Bento box grid layout, modular design inspired by Japanese bento,
cards of varying sizes, harmoniously organized, efficient space use, 16:9"
```

---

## 03 复古风格 (Retro Styles)

### 12. Retro-Futurism (复古未来主义)

**特征**:

- 70/80 年代对未来的想象
- 镀铬元素、霓虹网格
- 日落渐变、透视效果
- 融合怀旧与前瞻美学

**适用场景**:

- 音乐/娱乐品牌
- 游戏界面
- 复古科技产品

**配色建议**:

```
主色: 霓虹粉/紫/青
渐变: 日落渐变（粉/橙/紫）
元素: 镀铬金属质感
网格: 霓虹网格线
```

**Nano Banana Pro 提示词模板**:

```
"Retro-futurism design, 70s 80s vision of future, chrome elements,
neon grids, sunset gradients, perspective effects, nostalgic forward-looking, 16:9"
```

---

### 13. Y2K Aesthetic (千禧年美学)

**特征**:

- 90 年代末/21 世纪初的数字乐观主义
- 气泡形状
- 金属渐变
- 科技图案
- 捕捉千禧一代怀旧

**适用场景**:

- 流行文化品牌
- 年轻受众产品
- 怀旧营销

**配色建议**:

```
主色: 银色/蓝色/紫色金属渐变
形状: 气泡、圆润形状
元素: CD 光盘效果、数字元素
```

**Nano Banana Pro 提示词模板**:

```
"Y2K aesthetic, late 90s early 2000s digital optimism,
bubbly forms, metallic gradients, tech motifs, millennial nostalgia, 16:9"
```

---

### 14. Vaporwave (蒸汽波)

**特征**:

- 80/90 年代消费文化的讽刺性庆祝
- 粉色/青色渐变
- 希腊雕像、日文文字
- 故障效果

**适用场景**:

- 艺术项目
- 音乐专辑封面
- 反主流文化品牌

**配色建议**:

```
主色: 粉色 (#FF71CE) + 青色 (#01CDFE)
背景: 紫色渐变
元素: 希腊雕像、棕榈树、网格
效果: 故障、扫描线
```

**Nano Banana Pro 提示词模板**:

```
"Vaporwave design, ironic celebration of 80s 90s consumer culture,
pink cyan gradients, Greek statues, Japanese text, glitch effects, 16:9"
```

---

### 15. Memphis Design (孟菲斯设计)

**特征**:

- 1980 年代意大利设计运动
- 大胆的几何形状
- 冲突的颜色
- 俏皮的图案
- 最大化视觉冲击

**适用场景**:

- 创意品牌
- 艺术展览
- 活力品牌

**配色建议**:

```
主色: 明亮、冲突的颜色组合
图案: 几何图案（点/线/形状）
形状: 不对称、随机
```

**Nano Banana Pro 提示词模板**:

```
"Memphis design, 1980s Italian design movement, bold geometric shapes,
clashing colors, playful patterns, maximizing visual impact, 16:9"
```

---

### 16. Pixel Art (像素艺术)

**特征**:

- 8 位和 16 位时代灵感图形
- 可见像素
- 有限的调色板
- 复古游戏怀旧

**适用场景**:

- 游戏界面
- 复古主题项目
- 极客文化产品

**配色建议**:

```
调色板: 限制为 8-16 色
像素: 清晰可见的像素网格
阴影: 简单的抖动模式
```

**Nano Banana Pro 提示词模板**:

```
"Pixel art design, 8-bit 16-bit era inspired graphics,
visible pixels, limited color palette, retro gaming nostalgia, 16:9"
```

---

## 04 科技美学 (Tech Aesthetics)

### 17. Cyberpunk UI (赛博朋克 UI)

**特征**:

- 霓虹灯照明的暗色界面
- 故障效果、科技覆盖层
- 反乌托邦美学
- 青色/洋红配色方案

**适用场景**:

- 游戏界面
- 科技品牌
- 前卫产品

**配色建议**:

```
背景: 深黑色 (#0a0a0a)
霓虹: 青色 (#00ffff) + 洋红 (#ff00ff)
效果: 故障、扫描线、噪点
文字: 霓虹绿/青色
```

**Nano Banana Pro 提示词模板**:

```
"Cyberpunk UI, neon-lit dark interface, glitch effects, tech overlays,
dystopian aesthetics, cyan magenta color scheme, 16:9"
```

---

### 18. HUD/Sci-Fi FUI (抬头显示/科幻幻想 UI)

**特征**:

- 科幻电影启发的幻想用户界面
- 圆形元素、细线
- 数据可视化
- 全息效果

**适用场景**:

- 科技演示
- 未来主义品牌
- VR/AR 界面

**配色建议**:

```
主色: 青色/蓝色/绿色
元素: 细线、圆环、六角形
效果: 全息、半透明
数据: 图表、数字、网格
```

**Nano Banana Pro 提示词模板**:

```
"HUD Sci-Fi FUI, fantasy user interface inspired by sci-fi films,
circular elements, thin lines, data visualizations, holographic effects, 16:9"
```

---

### 19. Dark Mode (OLED) (深色模式)

**特征**:

- 为 OLED 显示器优化的纯黑背景
- 高对比度
- 最小化色彩强调
- 减少眼疲劳

**适用场景**:

- 移动应用
- 生产力工具
- 长时间使用的应用

**配色建议**:

```
背景: 纯黑 (#000000) 或接近黑 (#121212)
文字: 白色或浅灰
强调: 明亮但不刺眼的色彩
```

**OLED 优化**:

- 避免大面积纯白
- 使用深灰色而非纯黑（减少涂抹效应）
- 降低强调色亮度

**Nano Banana Pro 提示词模板**:

```
"Dark mode OLED optimized, true black background, high contrast,
minimal color accents, reducing eye strain, 16:9"
```

---

### 20. AI-Native UI (AI 原生 UI)

**特征**:

- 为 AI 交互设计的对话式界面
- 聊天气泡
- 输入指示器
- 流动渐变

**适用场景**:

- AI 聊天机器人
- 虚拟助手
- 对话式应用

**配色建议**:

```
背景: 柔和的中性色或渐变
气泡: 用户（浅色） vs AI（深色或渐变）
动画: 打字动画、流动效果
```

**Nano Banana Pro 提示词模板**:

```
"AI-native UI, conversational interface designed for AI interaction,
chat bubbles, typing indicators, flowing gradients, 16:9"
```

---

## 05 自然风格 (Natural Styles)

### 21. Organic Biophilic (有机亲生物)

**特征**:

- 自然启发的设计，连接用户与自然世界
- 大地色调
- 有机形状
- 平静的视觉节奏

**适用场景**:

- 健康/健身应用
- 环保品牌
- 放松/冥想应用

**配色建议**:

```
主色: 大地色（绿/棕/米色）
形状: 有机、不对称形状
纹理: 自然纹理（木材、石头）
```

**Nano Banana Pro 提示词模板**:

```
"Organic biophilic design, nature-inspired connecting users to natural world,
earthy colors, organic shapes, calming visual rhythms, 16:9"
```

---

### 22. Biomimetic (仿生)

**特征**:

- 源自生物结构的设计模式
- 六角形网格
- 细胞图案
- 生物体启发的形式

**适用场景**:

- 科学/医疗应用
- 创新科技品牌
- 教育平台

**配色建议**:

```
主色: 自然界颜色（绿/蓝/橙）
图案: 六角形、细胞、分形
结构: 对称、有机增长
```

**Nano Banana Pro 提示词模板**:

```
"Biomimetic design, patterns derived from biological structures,
hexagonal grids, cellular patterns, organism-inspired forms, 16:9"
```

---

### 23. E-Ink/Paper (电子墨水/纸张)

**特征**:

- 模仿纸张和电子墨水显示
- 深褐色调
- 微妙的纹理
- 低对比度界面

**适用场景**:

- 阅读应用
- 笔记工具
- 文档编辑器

**配色建议**:

```
背景: 米白/深褐色 (#f4f1de)
文字: 深灰/黑色
纹理: 纸张纹理
对比: 柔和、舒适
```

**Nano Banana Pro 提示词模板**:

```
"E-ink paper design, digital designs mimicking paper and e-ink displays,
sepia tones, subtle textures, low-contrast interface, 16:9"
```

---

## 06 动效驱动 (Motion-Driven)

### 24. Motion-Driven (动效驱动)

**特征**:

- 动画作为核心设计元素而非装饰
- 引导注意力
- 创造吸引人的体验

**适用场景**:

- 高端品牌网站
- 互动体验
- 产品演示

**动效类型**:

- 页面过渡
- 滚动动画
- 元素出现动画
- 悬停效果

**Nano Banana Pro 提示词模板**:

```
"Motion-driven design, animation as core design element not decoration,
guiding attention, creating engaging experiences, 16:9"
```

---

### 25. Micro-interactions (微交互)

**特征**:

- 响应用户操作的小型、聚焦动画
- 悬停效果和按钮状态
- 使界面感觉活生生

**适用场景**:

- 所有现代 UI
- 提升用户体验
- 增加愉悦感

**微交互类型**:

- 按钮按下动画
- 加载动画
- 表单验证反馈
- 点赞/收藏动画

**Nano Banana Pro 提示词模板**:

```
"Micro-interactions design, small focused animations responding to user actions,
hover effects, button states, making interface feel alive, 16:9"
```

---

### 26. Kinetic Typography (动态排版)

**特征**:

- 排版作为动态图形
- 字母和单词移动、变形、舞蹈
- 创造动态视觉叙事

**适用场景**:

- 品牌视频
- 标题动画
- 创意展示

**Nano Banana Pro 提示词模板**:

```
"Kinetic typography, typography as motion graphics,
letters and words move morph dance, dynamic visual narratives, 16:9"
```

---

### 27. Parallax Storytelling (视差故事讲述)

**特征**:

- 分层深度，元素以不同速度移动
- 创造沉浸式、电影般的体验

**适用场景**:

- 故事讲述网站
- 品牌展示
- 作品集

**Nano Banana Pro 提示词模板**:

```
"Parallax storytelling, layered depth with elements moving at different speeds,
creating immersive cinematic experiences, 16:9"
```

---

## 07 特殊风格 (Special Styles)

### 28. Spatial UI (VisionOS) (空间 UI)

**特征**:

- Apple Vision Pro 启发的空间计算设计
- 深度模糊、透明度
- 界面漂浮在 3D 空间中

**适用场景**:

- VR/AR 应用
- 空间计算平台
- 未来主义界面

**配色建议**:

```
背景: 深度模糊效果
元素: 半透明玻璃材质
深度: Z 轴分层
阴影: 柔和的投影
```

**Nano Banana Pro 提示词模板**:

```
"Spatial UI VisionOS inspired, design for spatial computing,
deep blur, transparency, interfaces floating in 3D space, 16:9"
```

---

### 29. Gen Z Chaos/Maximalism (Z 世代混乱/极繁主义)

**特征**:

- 极繁主义拒绝设计规则
- 冲突的颜色
- 重叠的元素
- 故意的混乱

**适用场景**:

- 年轻品牌
- 反叛文化
- 创意表达

**配色建议**:

```
主色: 多种冲突的高饱和度颜色
布局: 混乱、重叠、无序
元素: 过多的视觉元素
```

**Nano Banana Pro 提示词模板**:

```
"Gen Z chaos maximalism, maximalist rejection of design rules,
clashing colors, overlapping elements, intentional disorder, 16:9"
```

---

### 30. Dimensional Layering (维度分层)

**特征**:

- 多个视觉层创造深度和层级
- 通过堆叠卡片和微妙的 3D 变换

**适用场景**:

- Dashboard 仪表盘
- 数据可视化
- 复杂信息展示

**配色建议**:

```
层级: 使用阴影和高度创造层次
深度: Z 轴分层（近 → 远）
变换: 微妙的 3D 旋转/平移
```

**Nano Banana Pro 提示词模板**:

```
"Dimensional layering design, multiple visual layers creating depth and hierarchy,
stacked cards, subtle 3D transforms, 16:9"
```

---

## 🎨 Nano Banana Pro 提示词快速参考

### 模板结构

```
"[风格名称] design, [核心特征1], [核心特征2], [配色描述], [视觉效果], 16:9"
```

### 示例组合

```bash
# 科技感 + 极简主义
"Minimalist tech design, clean lines, electric blue accents #0066ff,
dark background #1e1e1e, ample whitespace, 16:9"

# 玻璃拟态 + 赛博朋克
"Cyberpunk glassmorphism UI, frosted glass effects, neon cyan magenta gradients,
glitch overlays, dark futuristic, 16:9"

# 复古未来 + 极光渐变
"Retro-futurism with aurora gradients, chrome elements, neon grids,
flowing pink purple blue gradients, nostalgic futuristic, 16:9"
```

---

## 🔄 风格混搭建议

### 推荐组合

| 主风格         | 辅助风格      | 效果         |
| -------------- | ------------- | ------------ |
| Minimalism     | Glassmorphism | 现代、精致   |
| Dark Mode      | Cyberpunk UI  | 科技感、未来 |
| Flat Design    | Neubrutalism  | 现代、活力   |
| Aurora UI      | Liquid Glass  | 高端、流动   |
| Neumorphism    | Claymorphism  | 柔和、可爱   |
| Retro-Futurism | Vaporwave     | 复古、艺术   |

### 避免组合

| 风格 A        | 风格 B      | 原因       |
| ------------- | ----------- | ---------- |
| Neumorphism   | Flat Design | 对比度冲突 |
| Skeuomorphism | Flat Design | 哲学对立   |
| Brutalism     | Minimalism  | 视觉冲突   |
| Gen Z Chaos   | Minimalism  | 概念对立   |

---

## 📚 参考资源

- **原始来源**: https://32kw.com/view/a2786f9
- **更新日期**: 2026-01-21
- **维护者**: Claude + User
- **相关文档**:
  - `docs/capabilities/PPT_WORKFLOW.md`
  - `docs/design/DESIGN_PROMPT_TEMPLATES.md` (待创建)

---

## 🔖 快速查询

### 按场景选择风格

**商务/专业**:

- Minimalism
- Flat Design
- Dark Mode

**科技/未来**:

- Glassmorphism
- Cyberpunk UI
- HUD/Sci-Fi FUI
- AI-Native UI

**创意/艺术**:

- Brutalism
- Neubrutalism
- Memphis Design
- Gen Z Chaos

**高端/奢华**:

- Aurora UI
- Liquid Glass
- Spatial UI

**怀旧/复古**:

- Retro-Futurism
- Y2K Aesthetic
- Vaporwave
- Pixel Art

**自然/有机**:

- Organic Biophilic
- Biomimetic
- E-Ink/Paper

**可爱/友好**:

- Claymorphism
- Neumorphism
- Bento Box Grid

---

**完成收录！总计 30 种设计风格 🎉**
