# PPT 制作优化工作流

> **Version**: 1.0 | **Created**: 2026-01-21 | **优先级：Nano Banana Pro → Processing → PPT组装**

---

## 🎯 核心原则

### 工作流程

```
1️⃣ 需求分析 → 2️⃣ Nano Banana Pro 生成页面图片 → 3️⃣ Processing 生成动态效果 → 4️⃣ 组装 PPT → 5️⃣ 导出双格式（.pptx + 图片）
```

### 技术栈优先级

1. **Nano Banana Pro** - 图片生成、整体页面设计（最高优先级）
2. **Processing** - 动态效果、粒子系统、流场动画
3. **Python-pptx** - 最终组装成 PPT 文件

---

## 📋 详细步骤

### Step 1: 需求分析和规划

**输入**: 用户的 PPT 需求描述

**输出**: 结构化的 PPT 大纲

**操作**:

```markdown
# PPT 大纲

- 总页数: N 页
- 风格主题: [科技感/商务风/创意艺术/...]
- 动态效果需求: [粒子背景/流场动画/数据可视化/...]
- 配色方案: [主色调+辅助色]
```

**关键决策**:

- 哪些页面需要静态设计（Nano Banana Pro）？
- 哪些页面需要动态效果（Processing）？
- 哪些页面需要数据可视化（图表）？

---

### Step 2: Nano Banana Pro 生成页面图片

**优先使用场景**:

- ✅ 封面页、标题页
- ✅ 内容页整体设计
- ✅ 复杂布局页面
- ✅ 需要高质量视觉设计的页面

**命令模板**:

```bash
# 生成单页设计
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Professional PPT slide design: [页面主题], [风格描述], 16:9 aspect ratio, clean layout, [配色方案]" \
  --filename "$(date +%Y-%m-%d-%H-%M-%S)-slide-[N]-[描述].png" \
  --resolution 4K

# 示例：生成封面页
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Professional tech-themed PPT cover slide: 'Data Analysis Report 2024', dark background with electric blue accents, minimalist design, 16:9 format" \
  --filename "2026-01-21-10-30-00-slide-01-cover.png" \
  --resolution 4K
```

**提示词最佳实践**:

- 明确指定 16:9 宽高比
- 包含风格关键词（professional, minimalist, tech-themed）
- 描述配色方案
- 指定文字位置和大小（large title at top, bullet points on left）

**文件命名规范**:

```
YYYY-MM-DD-HH-MM-SS-slide-[序号]-[描述].png
```

---

### Step 3: Processing 生成动态效果

**适用场景**:

- ✅ 背景动画（粒子系统、流场）
- ✅ 过渡动画（章节分隔页）
- ✅ 数据可视化动画
- ✅ 装饰性图形元素

**调用 Processing Skill**:

```bash
# 生成粒子背景动画
# Processing skill 会自动激活，直接描述需求即可
"Create a particle system background with electric blue particles on dark background, 1920x1080, export as PNG"
```

**输出格式**:

- 静态图: PNG
- 动画: GIF（如果 PPT 支持）
- 帧序列: 多张 PNG（用于复杂动画）

**配色对齐**:

- 确保 Processing 生成的效果与 Nano Banana Pro 的配色方案一致
- 从 Nano Banana Pro 图片中提取主色调，传递给 Processing

---

### Step 4: 组装 PPT

**使用 Python-pptx**:

```python
from pptx import Presentation
from pptx.util import Inches
from PIL import Image

def create_presentation_from_images(image_paths, output_filename):
    """
    将图片组装成 PPT

    Args:
        image_paths: 图片路径列表 (按页面顺序)
        output_filename: 输出的 PPT 文件名
    """
    prs = Presentation()
    prs.slide_width = Inches(10)   # 16:9 宽度
    prs.slide_height = Inches(5.625)  # 16:9 高度

    for img_path in image_paths:
        # 使用空白布局
        slide_layout = prs.slide_layouts[6]
        slide = prs.slides.add_slide(slide_layout)

        # 获取图片尺寸
        img = Image.open(img_path)
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height

        # 计算适配尺寸（铺满整个幻灯片）
        slide_width = prs.slide_width.inches
        slide_height = prs.slide_height.inches

        # 添加图片（铺满背景）
        slide.shapes.add_picture(
            img_path,
            left=0,
            top=0,
            width=Inches(slide_width),
            height=Inches(slide_height)
        )

    # 保存 PPT
    prs.save(output_filename)
    print(f"✅ PPT 已生成: {output_filename}")
    return output_filename
```

**脚本位置**:

```
E:\Bobo's Coding cache\scripts\ppt\assemble_ppt_from_images.py
```

---

### Step 5: 导出双格式

**必须输出**:

1. **PPT 文件**: `output.pptx`
2. **图片文件夹**: `output_slides/`
   ```
   output_slides/
   ├── slide-01-cover.png
   ├── slide-02-agenda.png
   ├── slide-03-content.png
   └── ...
   ```

**导出脚本**:

```python
def export_slides_as_images(pptx_file, output_dir):
    """
    从 PPT 导出每一页为图片

    使用 LibreOffice 转换:
    soffice --headless --convert-to pdf output.pptx
    pdftoppm -png -r 300 output.pdf output_slides/slide
    """
    import subprocess
    import os

    os.makedirs(output_dir, exist_ok=True)

    # 转换为 PDF
    subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf', pptx_file
    ])

    pdf_file = pptx_file.replace('.pptx', '.pdf')

    # PDF 转图片
    subprocess.run([
        'pdftoppm', '-png', '-r', '300', pdf_file,
        f'{output_dir}/slide'
    ])

    print(f"✅ 图片已导出到: {output_dir}")
```

---

## 🎨 主题配色库

### Tech Innovation (科技感)

```
主色: #0066ff (Electric Blue)
辅助: #00ffff (Neon Cyan)
背景: #1e1e1e (Dark Gray)
文字: #ffffff (White)
```

### Business Professional (商务风)

```
主色: #1C2833 (Deep Navy)
辅助: #2E4053 (Slate Gray)
强调: #F39C12 (Orange)
背景: #F4F6F6 (Off-White)
```

### Creative Vibrant (创意活力)

```
主色: #E76F51 (Coral)
辅助: #F4A261 (Peach)
强调: #2A9D8F (Teal)
背景: #264653 (Charcoal)
```

---

## 📝 完整示例

### 示例需求

> "制作一个5页的产品发布会 PPT，需要科技感，包含封面、产品介绍、功能亮点、市场分析、结束页"

### 执行流程

```bash
# Step 1: 生成封面（Nano Banana Pro）
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Professional tech product launch PPT cover: 'Product X Launch 2024', dark background with electric blue gradient, modern minimalist, 16:9, large centered title" \
  --filename "2026-01-21-10-00-00-slide-01-cover.png" \
  --resolution 4K

# Step 2: 生成产品介绍页（Nano Banana Pro）
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Product introduction slide: split layout, left side product image placeholder, right side bullet points area, tech theme, electric blue accents, 16:9" \
  --filename "2026-01-21-10-05-00-slide-02-intro.png" \
  --resolution 4K

# Step 3: 生成功能亮点页（Nano Banana Pro）
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Feature highlights slide: 3-column grid layout, icon placeholders, minimal text areas, tech blue theme, 16:9" \
  --filename "2026-01-21-10-10-00-slide-03-features.png" \
  --resolution 4K

# Step 4: 生成市场分析页 + Processing 动态图表
# 先生成背景
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Market analysis slide background: clean layout with chart placeholder area, tech theme, 16:9" \
  --filename "2026-01-21-10-15-00-slide-04-market-bg.png" \
  --resolution 4K

# 使用 Processing 生成动态数据可视化（描述即可，自动激活）
"Create an animated bar chart showing growth from 2020 to 2024, electric blue bars, dark background, 800x600px, export as GIF"

# Step 5: 生成结束页（Nano Banana Pro）
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Thank you slide: centered 'Thank You' text, contact information area at bottom, tech blue accents, minimalist, 16:9" \
  --filename "2026-01-21-10-20-00-slide-05-end.png" \
  --resolution 4K

# Step 6: 组装 PPT
python scripts/ppt/assemble_ppt_from_images.py \
  --images slide-01-cover.png slide-02-intro.png slide-03-features.png slide-04-market-bg.png slide-05-end.png \
  --output "Product_X_Launch_2024.pptx"

# Step 7: 导出图片（备份）
python scripts/ppt/export_slides_as_images.py \
  --pptx "Product_X_Launch_2024.pptx" \
  --output-dir "Product_X_Launch_2024_slides"
```

---

## ⚠️ 注意事项

### Nano Banana Pro 最佳实践

1. **分辨率选择**:
   - 默认 4K（高质量）
   - 快速预览可用 2K

2. **提示词技巧**:
   - 明确 16:9 宽高比
   - 包含"PPT slide"关键词
   - 描述布局结构（left/right/center）
   - 指定配色方案

3. **文件命名**:
   - 按时间戳 + 序号 + 描述
   - 便于后续组装排序

### Processing 最佳实践

1. **导出格式**:
   - 静态效果: PNG (高分辨率)
   - 动画效果: GIF 或 PNG 序列

2. **尺寸对齐**:
   - 全屏背景: 1920x1080 (16:9)
   - 图表/元素: 根据布局自定义

3. **配色同步**:
   - 从 Nano Banana Pro 图片提取色值
   - 保持视觉一致性

### PPT 组装注意

1. **图片质量**:
   - 确保所有图片为 16:9 比例
   - 高分辨率（至少 1920x1080）

2. **排序**:
   - 按文件名排序
   - 使用序号前缀（01, 02, 03...）

3. **备份**:
   - 保留原始图片文件
   - PPT 和图片都要提供给用户

---

## 🚀 快速启动模板

```python
# 创建 PPT 制作脚本模板
# 位置: scripts/ppt/create_ppt.py

import subprocess
import os
from datetime import datetime

def create_ppt_workflow(config):
    """
    PPT 制作工作流

    config = {
        'title': 'PPT 标题',
        'pages': [
            {
                'type': 'cover',  # cover, content, data, end
                'prompt': 'Nano Banana Pro 提示词',
                'dynamic': False,  # 是否需要 Processing 动态效果
                'processing_prompt': ''  # Processing 提示词（如果需要）
            },
            ...
        ],
        'theme': 'tech',  # tech, business, creative
        'output_name': 'output.pptx'
    }
    """
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    image_paths = []

    # Step 1: 生成所有页面图片
    for i, page in enumerate(config['pages']):
        slide_num = str(i+1).zfill(2)
        filename = f"{timestamp}-slide-{slide_num}-{page['type']}.png"

        # 使用 Nano Banana Pro 生成
        subprocess.run([
            'uv', 'run',
            os.path.expanduser('~/.claude/skills/nano-banana-pro/scripts/generate_image.py'),
            '--prompt', page['prompt'],
            '--filename', filename,
            '--resolution', '4K'
        ])

        image_paths.append(filename)

        # 如果需要动态效果，调用 Processing
        if page.get('dynamic'):
            print(f"⚡ Processing 动态效果: {page['processing_prompt']}")
            # Processing skill 会自动激活

    # Step 2: 组装 PPT
    assemble_ppt_from_images(image_paths, config['output_name'])

    # Step 3: 导出图片
    export_slides_as_images(config['output_name'], f"{config['output_name']}_slides")

    print(f"✅ 完成！")
    print(f"📁 PPT: {config['output_name']}")
    print(f"📁 图片: {config['output_name']}_slides/")
```

---

## 📚 参考文档

- Nano Banana Pro Skill: `.claude/skills/nano-banana-pro/SKILL.md`
- Processing Skill: `bo-work/processing-creative-skill/skill/processing-creative.md`
- Python-pptx 文档: `.claude/skills/document-skills/pptx/SKILL.md`
- HTML2PPTX 工作流: `.claude/skills/document-skills/pptx/html2pptx.md`

---

**最后更新**: 2026-01-21 | **维护者**: Claude + User
