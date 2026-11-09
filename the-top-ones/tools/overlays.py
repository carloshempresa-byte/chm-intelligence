"""Render the static title layer and the ranking-list layers for the Short.

usage: python3 -I overlays.py <config.json> <outdir>

Writes (all 1080x1920 RGBA unless noted):
  title.png                 - two-line title, keywords in blue
  list_base_<k>.png         - list numbers + names already revealed before clip k,
                              plus the highlight bar on the row of clip k
  name_<k>.png              - only the name of clip k's row (cropped RGBA) + its x/y in layout.json
  list_final.png            - every name revealed, no highlight
  layout.json               - geometry used by build.py
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

cfg = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)

W, H = 1080, 1920
FONT = cfg['font']
BLUE = tuple(int(cfg['blue'].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
WHITE = (255, 255, 255)
L = cfg['layout']

def font(sz):
    return ImageFont.truetype(FONT, sz)

def shadowed_text(layer, xy, text, fnt, fill, shadow=(0, 0, 0, 200), off=4, blur=6):
    """Draw text with a soft drop shadow so it stays readable over any frame."""
    sh = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0] + off, xy[1] + off), text, font=fnt, fill=shadow)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    layer.alpha_composite(sh)
    ImageDraw.Draw(layer).text(xy, text, font=fnt, fill=fill)

# ---------------- title ----------------
title = Image.new('RGBA', (W, H), (0, 0, 0, 0))
lines = cfg['title']  # [[ [word, 'w'|'b'], ...], ...]
size = L['title_max_size']
while True:
    f = font(size)
    widths = [f.getlength(' '.join(w for w, _ in ln)) for ln in lines]
    if max(widths) <= L['title_max_width']:
        break
    size -= 2
lh = int(size * L['title_line_gap'])
y = L['title_top']
for ln, wd in zip(lines, widths):
    x = (W - wd) / 2
    for i, (word, col) in enumerate(ln):
        piece = word + (' ' if i < len(ln) - 1 else '')
        shadowed_text(title, (x, y), word, f, BLUE if col == 'b' else WHITE)
        x += f.getlength(piece)
    y += lh
title.save(f'{out}/title.png')
title_bottom = y - lh + size

# ---------------- list ----------------
order = cfg['order']                 # playback order, e.g. [4, 6, 2, 5, 3, 1]
names = {int(k): v for k, v in cfg['names'].items()}
N = len(order)
top, bottom = L['list_top'], L['list_bottom']
row_h = min(L['row_h_max'], (bottom - top) // N)
fs = int(row_h * L['list_font_ratio'])
fl = font(fs)
num_x = L['list_x']
num_w = max(fl.getlength(f'{r}.') for r in range(1, N + 1))
name_x = int(num_x + num_w + fs * 0.45)
max_name_w = L['name_max_x'] - name_x

def row_y(rank):
    return top + (rank - 1) * row_h

def fit_font(text):
    s = fs
    while font(s).getlength(text) > max_name_w and s > 20:
        s -= 1
    return font(s)

def text_y(rank, fnt):
    # vertically center the text box in the row
    bb = fnt.getbbox('0Ag')
    return row_y(rank) + (row_h - (bb[3] - bb[1])) // 2 - bb[1]

def draw_numbers(layer, highlight=None):
    for r in range(1, N + 1):
        col = BLUE if r == highlight else WHITE
        shadowed_text(layer, (num_x, text_y(r, fl)), f'{r}.', fl, col)

def draw_highlight(layer, rank):
    bar = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bar)
    pad = 6
    d.rounded_rectangle([num_x - 22, row_y(rank) + pad, L['name_max_x'] + 22, row_y(rank) + row_h - pad],
                        radius=(row_h - 2 * pad) // 2, fill=BLUE + (70,), outline=BLUE + (220,), width=4)
    layer.alpha_composite(bar)

def draw_name(layer, rank, color=WHITE):
    fnt = fit_font(names[rank])
    shadowed_text(layer, (name_x, text_y(rank, fnt)), names[rank], fnt, color)

layout = {'row_h': row_h, 'font_size': fs, 'name_x': name_x, 'rows': {}, 'title_bottom': title_bottom}
for k, rank in enumerate(order):
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_highlight(base, rank)
    draw_numbers(base, highlight=rank)
    for prev in order[:k]:
        draw_name(base, prev)
    base.save(f'{out}/list_base_{k}.png')
    # the newly revealed name, on its own layer, cropped to its bbox
    nl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_name(nl, rank)
    bb = nl.getbbox()
    nl.crop(bb).save(f'{out}/name_{k}.png')
    layout['rows'][str(k)] = {'rank': rank, 'x': bb[0], 'y': bb[1]}

final = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw_numbers(final)
for r in order:
    draw_name(final, r)
final.save(f'{out}/list_final.png')
json.dump(layout, open(f'{out}/layout.json', 'w'), indent=1)
print(json.dumps(layout))
