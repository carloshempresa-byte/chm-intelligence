"""Composição 2D (Pillow) da identidade visual do canal Engenharia Animada.
Uso: python3 compor.py <pasta_build> <pasta_saida>
  build/perfil_3d.png (1600x1600, fundo transparente) -> perfil_800x800.png
  build/banner_3d.png (2560x1440)                     -> banner_2560x1440.png (+ guia da área segura)"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BUILD, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '..', 'assets', 'Montserrat-Black.ttf')
INK = (22, 22, 22)
YEL = (255, 210, 63)      # #ffd23f
WHITE = (255, 255, 255)
BLUE_D = (47, 111, 163)   # #2f6fa3
BLUE_L = (88, 166, 214)   # #58a6d6
CRANE = (245, 194, 66)    # #f5c242
ORANGE = (255, 122, 31)   # #ff7a1f


def f(size):
    return ImageFont.truetype(FONT, size)


def outlined_text(img, xy, text, font, fill, stroke, shadow=10):
    """Texto no estilo das legendas do canal: preenchimento + contorno preto grosso + sombra."""
    d = ImageDraw.Draw(img)
    x, y = xy
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((x + shadow * 0.5, y + shadow), text, font=font, fill=(0, 0, 0, 120),
                            stroke_width=stroke, stroke_fill=(0, 0, 0, 120), anchor='mm')
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    d.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=INK, anchor='mm')


def pill(img, cx, cy, text, size, bg, fg):
    fo = f(size)
    bb = fo.getbbox(text)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    padx, pady, ol = int(size * 0.6), int(size * 0.38), max(5, size // 8)
    w, h = tw + 2 * padx + 2 * ol, th + 2 * pady + 2 * ol
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    d.rounded_rectangle((x0 + 6, y0 + 10, x0 + w + 6, y0 + h + 10), radius=h // 2, fill=(0, 0, 0, 90))
    layer = layer.filter(ImageFilter.GaussianBlur(3))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=h // 2, fill=INK)
    d.rounded_rectangle((x0 + ol, y0 + ol, x0 + w - ol, y0 + h - ol), radius=(h - 2 * ol) // 2, fill=bg)
    d.text((cx, cy), text, font=fo, fill=fg, anchor='mm')
    img.alpha_composite(layer)
    return w, h


def fit_size(text, max_w, start, stroke_ratio=0.1):
    s = start
    while s > 20:
        bb = f(s).getbbox(text, stroke_width=int(s * stroke_ratio))
        if bb[2] - bb[0] <= max_w:
            return s
        s -= 2
    return s


# ------------------------------------------------------------------ PERFIL 800x800
S = 1600
bg = Image.new('RGBA', (S, S))
px = bg.load()
cx, cy = S / 2, S * 0.46
for y in range(S):
    for x in range(S):
        r = min(1.0, ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / (S * 0.62))
        px[x, y] = tuple(int(BLUE_L[i] + (BLUE_D[i] - BLUE_L[i]) * r) for i in range(3)) + (255,)
# raios suaves (sol) atrás da cabeça
rays = Image.new('RGBA', (S, S), (0, 0, 0, 0))
dr = ImageDraw.Draw(rays)
import math
for k in range(16):
    a0 = math.radians(k * 22.5); a1 = a0 + math.radians(9)
    dr.polygon([(cx, cy), (cx + 2000 * math.cos(a0), cy + 2000 * math.sin(a0)), (cx + 2000 * math.cos(a1), cy + 2000 * math.sin(a1))],
               fill=(255, 255, 255, 22))
bg.alpha_composite(rays)
glow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse((cx - 470, cy - 470, cx + 470, cy + 470), fill=(230, 244, 251, 120))
bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
# mascote (sombra suave + render)
m = Image.open(os.path.join(BUILD, 'perfil_3d.png')).convert('RGBA')
sc = 0.98
m = m.resize((int(m.width * sc), int(m.height * sc)), Image.LANCZOS)
ox, oy = (S - m.width) // 2, S - m.height + 40
shadow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
shadow.paste((10, 30, 60, 90), (ox + 18, oy + 26), m.getchannel('A'))
bg.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)))
bg.alpha_composite(m, (ox, oy))
# anel amarelo (guindaste) na borda do círculo
ring = Image.new('RGBA', (S, S), (0, 0, 0, 0))
ImageDraw.Draw(ring).ellipse((14, 14, S - 14, S - 14), outline=CRANE + (255,), width=26)
bg.alpha_composite(ring)
perfil = bg.resize((800, 800), Image.LANCZOS).convert('RGB')
perfil.save(os.path.join(OUT, 'perfil_800x800.png'), optimize=True)
# prévia em círculo (como aparece no YouTube) em 3 tamanhos
prev = Image.new('RGB', (800 + 40 + 176 + 40 + 88 + 40 + 48 + 40, 840), (249, 249, 249))
mask = Image.new('L', (800, 800), 0); ImageDraw.Draw(mask).ellipse((0, 0, 799, 799), fill=255)
x = 20
for size in (800, 176, 88, 48):
    p = perfil.resize((size, size), Image.LANCZOS)
    prev.paste(p, (x, 20 + (800 - size) // 2), mask.resize((size, size), Image.LANCZOS))
    x += size + 40
os.makedirs(os.path.join(OUT, 'previas'), exist_ok=True)
prev.save(os.path.join(OUT, 'previas', 'perfil_em_circulo.jpg'), quality=92)

# ------------------------------------------------------------------ BANNER 2560x1440
W, H = 2560, 1440
SAFE = ((W - 1546) // 2, (H - 423) // 2, (W + 1546) // 2, (H + 423) // 2)  # 507,508 – 2053,931
b = Image.open(os.path.join(BUILD, 'banner_3d.png')).convert('RGBA').resize((W, H), Image.LANCZOS)
# área de texto entre o mascote (esq.) e a caldeira (dir.)
TX0, TX1 = 760, 1720
TCX = (TX0 + TX1) // 2
s1 = fit_size('ENGENHARIA', TX1 - TX0, 190)
st = int(s1 * 0.1)
y1 = SAFE[1] + 92
outlined_text(b, (TCX, y1), 'ENGENHARIA', f(s1), WHITE, st)
y2 = y1 + int(s1 * 0.98)
outlined_text(b, (TCX, y2), 'ANIMADA', f(s1), YEL, st)
pill(b, TCX, y2 + int(s1 * 0.82), 'GRANDES EQUIPAMENTOS EXPLICADOS EM 3D', 40, ORANGE, WHITE)
b.convert('RGB').save(os.path.join(OUT, 'banner_2560x1440.png'), optimize=True)
# guia: área segura e o que aparece em cada tela
g = b.copy()
d = ImageDraw.Draw(g)
d.rectangle(SAFE, outline=(229, 72, 77, 255), width=6)
d.rectangle((0, SAFE[1], W - 1, SAFE[3]), outline=(46, 230, 214, 255), width=4)
d.text((SAFE[0] + 14, SAFE[1] + 10), 'ÁREA SEGURA 1546x423 (todos os aparelhos)', font=f(30), fill=(229, 72, 77))
d.text((20, SAFE[3] + 12), 'faixa do desktop 2560x423', font=f(30), fill=(20, 140, 130))
d.text((20, 20), 'imagem inteira 2560x1440 (TV)', font=f(30), fill=(40, 40, 40))
g.convert('RGB').resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, 'previas', 'banner_guia_area_segura.jpg'), quality=90)
b.crop((SAFE[0], SAFE[1], SAFE[2], SAFE[3])).convert('RGB').save(os.path.join(OUT, 'previas', 'banner_celular_1546x423.jpg'), quality=92)
b.crop((0, SAFE[1], W, SAFE[3])).convert('RGB').resize((1280, 212), Image.LANCZOS).save(os.path.join(OUT, 'previas', 'banner_desktop_2560x423.jpg'), quality=92)
print('ok', s1)
