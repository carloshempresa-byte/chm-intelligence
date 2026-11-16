"""Aplica textos grandes (estilo Short viral) sobre os quadros de teste, para mostrar o padrão final.
Uso: python3 textos_teste.py <pasta_testes>
Os textos e números seguem o roteiro aprovado (rev. 2)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '..', '..', 'identidade-visual', 'assets', 'Montserrat-Black.ttf')
INK = (22, 22, 22)
COL = dict(white=(255, 255, 255), yellow=(255, 210, 63), orange=(255, 122, 31), green=(63, 191, 111), red=(229, 72, 77))


def f(s):
    return ImageFont.truetype(FONT, s)


def big(img, xy, text, size, fill, stroke=None, rot=0):
    stroke = stroke or max(8, size // 9)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((xy[0] + 6, xy[1] + 12), text, font=f(size), fill=(0, 0, 0, 130), stroke_width=stroke, stroke_fill=(0, 0, 0, 130), anchor='mm')
    lay = lay.filter(ImageFilter.GaussianBlur(5))
    d = ImageDraw.Draw(lay)
    d.text(xy, text, font=f(size), fill=fill, stroke_width=stroke, stroke_fill=INK, anchor='mm')
    if rot:
        lay = lay.rotate(rot, center=xy, resample=Image.BICUBIC)
    img.alpha_composite(lay)


def pill(img, xy, text, size, bg, fg=INK):
    fo = f(size); bb = fo.getbbox(text)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    px, py, ol = int(size * 0.55), int(size * 0.34), max(5, size // 9)
    w, h = tw + 2 * px + 2 * ol, th + 2 * py + 2 * ol
    x0, y0 = int(xy[0] - w / 2), int(xy[1] - h / 2)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x0 + 6, y0 + 10, x0 + w + 6, y0 + h + 10), radius=h // 2, fill=(0, 0, 0, 100))
    lay = lay.filter(ImageFilter.GaussianBlur(3)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=h // 2, fill=INK)
    d.rounded_rectangle((x0 + ol, y0 + ol, x0 + w - ol, y0 + h - ol), radius=(h - 2 * ol) // 2, fill=bg)
    d.text(xy, text, font=fo, fill=fg, anchor='mm')
    img.alpha_composite(lay)


def caption(img, words, hl=()):
    x = 540; y = 1330
    txt = ' '.join(words)
    col = COL['yellow'] if any(w in hl for w in words) else COL['white']
    big(img, (x, y), txt, 96, col, 12)


PLAN = {
    '01_gancho_engole_montanhas': lambda im: (big(im, (540, 330), 'ENGOLE', 150, COL['yellow'], rot=4), big(im, (540, 500), 'MONTANHAS', 150, COL['white'], rot=-3),
                                              caption(im, ['MONTANHAS'], ('MONTANHAS',))),
    '02_roda_cavando_close': lambda im: (pill(im, (540, 300), '21,6 m', 110, COL['yellow']), pill(im, (540, 450), '18 CAÇAMBAS', 70, COL['white']),
                                         caption(im, ['18', 'CAÇAMBAS'], ('CAÇAMBAS',))),
    '03_escala_dois_cristos': lambda im: (big(im, (540, 300), '96 m', 190, COL['yellow']), pill(im, (540, 480), '2 × CRISTO (38 m) = 76 m', 52, COL['white']),
                                          caption(im, ['CRISTOS'], ('CRISTOS',))),
    '04_drone_dois_campos': lambda im: (big(im, (540, 260), '225 m', 170, COL['yellow']), pill(im, (540, 420), 'MAIS DE 2 CAMPOS', 64, COL['green']),
                                        caption(im, ['CAMPOS', 'DE'], ('CAMPOS',))),
    '05_esteiras_camera_baixa': lambda im: (pill(im, (540, 300), '12 ESTEIRAS', 84, COL['yellow']), pill(im, (540, 440), '3,8 m CADA', 64, COL['white']),
                                            caption(im, ['ESTEIRAS'], ('ESTEIRAS',))),
    '06_mudanca_rodovia': lambda im: (big(im, (540, 270), '2001', 160, COL['yellow'], rot=-3), pill(im, (540, 430), '22 km EM 3 SEMANAS', 60, COL['white']),
                                      pill(im, (540, 545), 'ATRAVESSANDO A RODOVIA', 48, COL['orange']), caption(im, ['RODOVIA'], ('RODOVIA',))),
}
os.makedirs(os.path.join(D, 'com_texto'), exist_ok=True)
for name, fn in PLAN.items():
    p = os.path.join(D, name + '.png')
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert('RGBA')
    fn(im)
    im.convert('RGB').save(os.path.join(D, 'com_texto', name + '_texto.jpg'), quality=92)
    print('ok', name)
