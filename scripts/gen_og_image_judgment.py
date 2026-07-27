"""生成 OG 图片：1200x630，紫色调（与 japanese-judgment-expressions-summary.html 主题一致），含 logo + 标题 + 副标题。"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630
BG = (245, 247, 250)        # #f5f7fa（页面背景浅色）
DEEP = (118, 75, 162)       # #764ba2（紫色深，呼应页面页眉渐变）
MID = (161, 140, 209)       # #a18cd1（紫色中）
LIGHT = (223, 214, 235)     # 紫色浅
DARK = (44, 62, 80)         # #2c3e50（深色文本）
BODY = (73, 80, 87)         # #495057（主文本）
WHITE = (255, 255, 255)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# 顶部装饰横条
draw.rectangle([0, 0, W, 10], fill=DEEP)

# 左侧圆角矩形 logo（紫色调，呼应页眉渐变 #667eea → #764ba2）
logo_size = 240
lx, ly = 120, (H - logo_size) // 2
r = 36
draw.rounded_rectangle([lx, ly, lx + logo_size, ly + logo_size], radius=r, fill=DEEP)

# 虚线圆环
cx, cy = lx + logo_size // 2, ly + logo_size // 2
ring_r = 96
dash = 12
gap = 10
start = 0
while start < 360:
    end = start + dash
    a1 = math.radians(start - 90)
    a2 = math.radians(end - 90)
    p1 = (cx + ring_r * math.cos(a1), cy + ring_r * math.sin(a1))
    p2 = (cx + ring_r * math.cos(a2), cy + ring_r * math.sin(a2))
    draw.line([p1, p2], fill=LIGHT, width=6)
    start = end + gap

# 中央「判」字（缩小字号，与圆环保留视觉间距）
font_jp = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 96)
bbox = font_jp.getbbox("判")
gw = bbox[2] - bbox[0]
gh = bbox[3] - bbox[1]
gx = cx - gw / 2 - bbox[0]
gy = cy - gh / 2 - bbox[1]
draw.text((gx, gy), "判", font=font_jp, fill=(245, 240, 252))

# 右侧文字
tx = lx + logo_size + 60

# 主标题（两行，避免截断）
font_title = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 68)
draw.text((tx, 200), "日语表判定・", font=font_title, fill=DARK, anchor="lm")
draw.text((tx, 280), "表达方式总结", font=font_title, fill=DARK, anchor="lm")

# 副标题
font_sub = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 28)
draw.text((tx, 360), "断定 · 推量 · 样态 · 传闻 · 状况推测", font=font_sub, fill=BODY, anchor="lm")

# 第三行：词尾汇总（缩短并换行，避免截断）
font_sub2 = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 22)
draw.text((tx, 405), "だ / だろう / かもしれない", font=font_sub2, fill=BODY, anchor="lm")
draw.text((tx, 438), "はずだ / そうだ / ようだ / みたいだ / らしい", font=font_sub2, fill=BODY, anchor="lm")

# 分隔线
draw.line([(tx, 480), (tx + 600, 480)], fill=MID, width=3)

# 底部装饰横条
draw.rectangle([0, H - 10, W, H], fill=DEEP)

out = "/Users/david/i/japanese-verb-conjugation/public/og-image-judgment.jpg"
img.save(out, "JPEG", quality=88, optimize=True)
print(f"Saved: {out}")
