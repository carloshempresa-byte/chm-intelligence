"""Compositor 2D: legendas palavra a palavra + etiquetas em pílula ancoradas nas peças 3D + títulos/CTA.
Lê os quadros do Blender, desenha por cima com PIL e envia para o ffmpeg (vídeo sem áudio).
Uso: python3 composite.py <config.json>   (ver config_ep01.json)"""
import json, sys, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont

cfg = json.load(open(sys.argv[1], encoding='utf-8'))
BASE = os.path.dirname(os.path.abspath(sys.argv[1]))
P = lambda p: p if os.path.isabs(p) else os.path.join(BASE, p)
FPS = 30
W, H = 1080, 1920
FONT = P(cfg['font'])
ONLY = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else None  # faixa de quadros (teste)


def font(size, weight='Black'):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def hexc(h, a=255):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def ease_back(x):  # 0..1 com leve overshoot
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


# ---------------------------------------------------------------- legendas
words = json.load(open(P(cfg['words']), encoding='utf-8'))
HL = set(w.upper() for w in cfg['highlight'])
chunks = []
i = 0
while i < len(words):
    w = words[i]
    txt = w['w'].strip('.,:;!?')
    t0, t1 = w['t0'], w['t1']
    if i + 1 < len(words):
        n = words[i + 1]
        nt = n['w'].strip('.,:;!?')
        punct = w['w'][-1:] in '.,:;!?'
        if not punct and (t1 - t0) < 0.32 and (n['t1'] - n['t0']) < 0.42 and len(txt) + len(nt) <= 13:
            chunks.append(([txt, nt], t0, n['t1'])); i += 2; continue
    chunks.append(([txt], t0, t1)); i += 1
for j, (ws, t0, t1) in enumerate(chunks):
    nxt = chunks[j + 1][1] if j + 1 < len(chunks) else t1 + 1.0
    chunks[j] = (ws, t0, min(nxt, t1 + 0.6))

CAP_F = font(96)
CAP_Y = cfg.get('caption_y', 1330)
_cap_cache = {}


def caption_img(ws):
    key = tuple(ws)
    if key in _cap_cache:
        return _cap_cache[key]
    parts = [(w.upper(), hexc('#ffd23f') if w.upper().strip('.,') in HL else hexc('#ffffff')) for w in ws]
    sp = 26
    widths = [CAP_F.getbbox(t, stroke_width=12)[2] for t, _ in parts]
    tw = sum(widths) + sp * (len(parts) - 1)
    img = Image.new('RGBA', (tw + 40, 150), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 20
    for (t, col), wd in zip(parts, widths):
        d.text((x + 4, 24 + 7), t, font=CAP_F, fill=(0, 0, 0, 150), stroke_width=12, stroke_fill=(0, 0, 0, 150))  # sombra
        d.text((x, 24), t, font=CAP_F, fill=col, stroke_width=12, stroke_fill=(0, 0, 0, 255))
        x += wd + sp
    if img.width > W - 60:
        r = (W - 60) / img.width
        img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    _cap_cache[key] = img
    return img


# ---------------------------------------------------------------- pílulas
STY = {
    'white': ('#ffffff', '#161616'), 'yellow': ('#ffd23f', '#161616'), 'red': ('#e5484d', '#ffffff'),
    'blue': ('#58a6d6', '#ffffff'), 'orange': ('#ff7a1f', '#ffffff'), 'green': ('#3fbf6f', '#ffffff'),
    'cyan': ('#2ee6d6', '#161616'),
}
_pill_cache = {}


def pill_img(text, style, size):
    key = (text, style, size)
    if key in _pill_cache:
        return _pill_cache[key]
    f = font(size)
    bg, fg = STY[style]
    bb = f.getbbox(text)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    padx, pady, ol = int(size * 0.55), int(size * 0.34), max(5, size // 9)
    w, h = tw + 2 * padx + 2 * ol, th + 2 * pady + 2 * ol
    img = Image.new('RGBA', (w + 10, h + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((6, 10, w + 4, h + 10), radius=h // 2, fill=(0, 0, 0, 110))  # sombra
    d.rounded_rectangle((0, 0, w, h), radius=h // 2, fill=hexc('#111111'))
    d.rounded_rectangle((ol, ol, w - ol, h - ol), radius=(h - 2 * ol) // 2, fill=hexc(bg))
    d.text((ol + padx - bb[0], ol + pady - bb[1]), text, font=f, fill=hexc(fg))
    _pill_cache[key] = img
    return img


anch = json.load(open(P(cfg['anchors'])))
A = anch['anchors']
AF0 = anch['f0']


def anchor_xy(name, fr):
    arr = A[name]
    i = max(0, min(len(arr) - 1, fr - AF0))
    return arr[i]


def paste_scaled(base, img, cx, cy, s, alpha=1.0):
    if s <= 0.02:
        return
    im = img if abs(s - 1) < 1e-3 else img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.BILINEAR)
    if alpha < 1:
        a = im.getchannel('A').point(lambda v: int(v * alpha))
        im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def anim_scale(t, t_in, t_out, din=0.22, dout=0.16):
    if t < t_in or t > t_out:
        return 0.0
    if t < t_in + din:
        return max(0.0, ease_back((t - t_in) / din))
    if t > t_out - dout:
        return max(0.0, (t_out - t) / dout)
    return 1.0


def draw_pill(base, d, p, t, fr):
    s = anim_scale(t, p['t_in'], p['t_out'])
    if s <= 0:
        return
    img = pill_img(p['text'], p.get('style', 'white'), p.get('size', 54))
    if p.get('anchor'):
        ax, ay, vis = anchor_xy(p['anchor'], fr)
        if not vis:
            return
        dx, dy = p.get('off', [0, -170])
        px, py = ax + dx, ay + dy
        m = 30
        px = min(max(px, img.width / 2 + m), W - img.width / 2 - m)
        py = min(max(py, img.height / 2 + 150), H - img.height / 2 - 420)
        # linha guia + ponto
        if s > 0.5 and p.get('line', True):
            lw = 9
            d.line((ax, ay, px, py), fill=(17, 17, 17, 255), width=lw + 6)
            d.line((ax, ay, px, py), fill=(255, 255, 255, 255), width=lw - 2)
            r = 13
            d.ellipse((ax - r - 3, ay - r - 3, ax + r + 3, ay + r + 3), fill=(17, 17, 17, 255))
            d.ellipse((ax - r + 2, ay - r + 2, ax + r - 2, ay + r - 2), fill=hexc(STY[p.get('style', 'white')][0]))
    else:
        px, py = p['pos']
    paste_scaled(base, img, px, py, s)


def draw_text_block(base, b, t):
    s = anim_scale(t, b['t_in'], b['t_out'], 0.25, 0.2)
    if s <= 0:
        return
    paste_scaled(base, pill_img(b['text'], b.get('style', 'white'), b.get('size', 60)), b['pos'][0], b['pos'][1], s)


# ---------------------------------------------------------------- loop
frames_dir = P(cfg['frames'])
n_frames = cfg['n_frames']
out = P(cfg['out_video'])
fr_range = range(ONLY[0], ONLY[1] + 1) if ONLY else range(1, n_frames + 1)
if ONLY:
    os.makedirs(out, exist_ok=True)
    proc = None
else:
    proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                             '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17',
                             '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
last = None
for fr in fr_range:
    t = (fr - 1) / FPS
    fp = os.path.join(frames_dir, f'f_{fr:04d}.png')
    if os.path.exists(fp) and os.path.getsize(fp) > 0:
        last = fp
    base = Image.open(last).convert('RGBA')
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for p in cfg['pills']:
        draw_pill(ov, d, p, t, fr)
    for b in cfg.get('blocks', []):
        draw_text_block(ov, b, t)
    # legenda atual
    for ws, t0, t1 in chunks:
        if t0 <= t < t1:
            x = (t - t0) / 0.12
            s = 0.75 + 0.25 * ease_back(min(1.0, x))
            paste_scaled(ov, caption_img(ws), W / 2, CAP_Y, s)
            break
    base.alpha_composite(ov)
    rgb = base.convert('RGB')
    if proc:
        proc.stdin.write(rgb.tobytes())
    else:
        rgb.save(os.path.join(out, f'c_{fr:04d}.jpg'), quality=92)
    if fr % 150 == 0:
        print('quadro', fr, flush=True)
if proc:
    proc.stdin.close(); proc.wait()
print('ok')
