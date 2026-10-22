"""Generate assets/img/og.png (social share image). Requires Pillow."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 630
im = Image.new("RGB", (W, H), "#16233F"); d = ImageDraw.Draw(im)
d.arc((140, 170, 1060, 1090), 180, 360, fill="#2E3B57", width=26)
d.arc((140, 170, 1060, 1090), 180, 300, fill="#FFC23D", width=26)
a = math.radians(300); cx, cy = 600 + 460 * math.cos(a), 630 + 460 * math.sin(a)
d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill="#FFC23D", outline="#16233F", width=8)
def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()
for text, size, y, col in [("Simple.solar", 110, 330, "#FFFFFF"), ("Solar, without the sales pitch.", 44, 470, "#FFC23D")]:
    f = font(size); w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=col)
(ROOT / "assets/img").mkdir(parents=True, exist_ok=True)
im.save(ROOT / "assets/img/og.png", optimize=True)
print("og.png written")
