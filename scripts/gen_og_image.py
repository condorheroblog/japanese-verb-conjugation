"""生成 OG 图片：1200x630，橙色调，含 logo + 标题 + 副标题。"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (253, 246, 236)        # #fdf6ec
DEEP = (233, 122, 48)       # #e97a30
MID = (250, 199, 166)       # #fac7a6
LIGHT = (253, 224, 200)     # #fde0c8
DARK = (90, 48, 24)         # #5a3018
BODY = (107, 68, 35)        # #6b4423

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# 顶部装饰横条
draw.rectangle([0, 0, W, 10], fill=DEEP)

# 左侧圆形 logo（与 logo.svg 风格一致）
logo_size = 240
lx, ly = 120, (H - logo_size) // 2
# 圆角矩形背景
r = 36
draw.rounded_rectangle([lx, ly, lx + logo_size, ly + logo_size], radius=r, fill=DEEP)

# 虚线圆环
cx, cy = lx + logo_size // 2, ly + logo_size // 2
ring_r = 96
dash = 12
gap = 10
# 手动绘制虚线
import math
start = 0
while start < 360:
    end = start + dash
    a1 = math.radians(start - 90)
    a2 = math.radians(end - 90)
    p1 = (cx + ring_r * math.cos(a1), cy + ring_r * math.sin(a1))
    p2 = (cx + ring_r * math.cos(a2), cy + ring_r * math.sin(a2))
    draw.line([p1, p2], fill=LIGHT, width=6)
    start = end + gap

# 中央「う」字（以字形包围盒中心对齐 logo 中心，避免 baseline/字身偏移）
# 字号需保证字形半径 < 圆环半径 - 间隙，留约 14px 视觉间距
font_jp = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 160)
bbox = font_jp.getbbox("う")           # (l, t, r, b)
gw = bbox[2] - bbox[0]
gh = bbox[3] - bbox[1]
# 将 glyph 的中心对齐到 (cx, cy)
gx = cx - gw / 2 - bbox[0]
gy = cy - gh / 2 - bbox[1]
draw.text((gx, gy), "う", font=font_jp, fill=(253, 241, 227))

# 右侧文字
tx = lx + logo_size + 60
# 主标题
font_title = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 78)
draw.text((tx, 230), "日语动词活用表", font=font_title, fill=DARK, anchor="lm")

# 副标题
font_sub = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 30)
draw.text((tx, 310), "五段 · 一段 · サ変 · カ変 · 特殊变化", font=font_sub, fill=BODY, anchor="lm")

# 分隔线
draw.line([(tx, 370), (tx + 520, 370)], fill=MID, width=3)

# 版权来源
font_cr = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 24)
draw.text((tx, 410), "圆圆的日语教室", font=font_cr, fill=DEEP, anchor="lm")
font_url = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 20)
draw.text((tx, 446), "space.bilibili.com/453272233", font=font_url, fill=BODY, anchor="lm")

# 底部装饰横条
draw.rectangle([0, H - 10, W, H], fill=DEEP)

out = "/Users/david/i/japanese-verb-conjugation/public/og-image.jpg"
img.save(out, "JPEG", quality=88, optimize=True)
print(f"Saved: {out}")
