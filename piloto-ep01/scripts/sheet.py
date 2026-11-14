import sys, glob
from PIL import Image, ImageDraw
fs = sorted(glob.glob(sys.argv[1] + '/t*.png'))
ims = [Image.open(f) for f in fs]; w, h = ims[0].size; cols = 8; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * h), 'white'); d = ImageDraw.Draw(sheet)
for i, (im, f) in enumerate(zip(ims, fs)):
    x, y = (i % cols) * w, (i // cols) * h; sheet.paste(im, (x, y)); d.text((x + 5, y + 5), f.split('/')[-1], fill='black')
sheet.save(sys.argv[2], quality=85)
