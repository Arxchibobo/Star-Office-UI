#!/usr/bin/env python3
"""Remove white background from lobster image"""
from PIL import Image
import numpy as np

# 加载图片
input_path = '/home/arxchibo/.openclaw/workspace/projects/Star-Office-UI/frontend/lobster_white_bg.png'
output_path = '/home/arxchibo/.openclaw/workspace/projects/Star-Office-UI/frontend/lobster_final.png'

img = Image.open(input_path).convert('RGBA')
data = np.array(img)

# 获取RGB通道
rgb = data[:, :, :3]
# 创建alpha通道：白色(接近255,255,255)变透明
threshold = 240
mask = np.all(rgb > threshold, axis=2)
data[:, :, 3] = np.where(mask, 0, 255)

# 保存
result = Image.fromarray(data)
result.save(output_path)
print(f"✅ 已去除白色背景: {output_path}")
print(f"📏 图片大小: {result.size}")
