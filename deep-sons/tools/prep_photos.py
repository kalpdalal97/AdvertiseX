#!/usr/bin/env python3
"""Prepare the shop's own photographs for the web.

Sources live in photos-source/ (the originals Deep Sons supplied). This script
crops the app chrome and page furniture off them, cuts a portrait card and a
wide banner where each photo supports one, compresses them, and lifts the DS
crown monogram out of its background so the logo works on cream and on dark.

Run:  python3 tools/prep_photos.py
"""

import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
SRC = os.path.join(ROOT, 'photos-source')
OUT = os.path.join(ROOT, 'assets', 'img', 'photo')

CARD_RATIO = 800 / 1100.0

# name -> (source file, crop box or None, kind)
#   'card'   portrait product shot for the grid
#   'banner' wide campaign creative, branding intact
JOBS = [
    # the clean studio shot: no overlay, usable as-is
    ('white-jodhpuri-card', '01-white-jodhpuri.png', (170, 70, 1010, 1225), 'card', 1000),
    ('white-jodhpuri-wide', '01-white-jodhpuri.png', (0, 150, 1086, 1000), 'banner', 1400),

    # the three campaign creatives, kept whole as banners …
    ('cream-indowestern-banner', '02-cream-indowestern.jpg', (12, 25, 1195, 1640), 'banner', 1100),
    ('mustard-kurta-banner', '03-mustard-kurta.jpg', (0, 40, 1206, 1245), 'banner', 1200),
    ('blue-sherwani-banner', '04-blue-sherwani.jpg', (0, 55, 1105, 1660), 'banner', 1100),

    # … and cropped to the garment alone for the product grid
    ('cream-indowestern-card', '02-cream-indowestern.jpg', (450, 15, 1195, 1040), 'card', 900),
    ('mustard-kurta-card', '03-mustard-kurta.jpg', (300, 125, 1050, 1157), 'card', 900),
    ('blue-sherwani-card', '04-blue-sherwani.jpg', (480, 55, 1105, 915), 'card', 900),
]

LOGO_SRC = ('04-blue-sherwani.jpg', (118, 48, 312, 286))


def prep_photos():
    os.makedirs(OUT, exist_ok=True)
    for name, src, box, kind, width in JOBS:
        im = Image.open(os.path.join(SRC, src)).convert('RGB')
        if box:
            im = im.crop(box)
        if width < im.width:
            h = round(im.height * width / im.width)
            im = im.resize((width, h), Image.LANCZOS)
        path = os.path.join(OUT, name + '.jpg')
        im.save(path, 'JPEG', quality=82, optimize=True, progressive=True)
        ratio = im.width / im.height
        note = ''
        if kind == 'card':
            note = '  (card ratio %.3f vs %.3f)' % (ratio, CARD_RATIO)
        print('  %-26s %4dx%-4d %5.0f KB%s'
              % (name, im.width, im.height, os.path.getsize(path) / 1024, note))


def prep_logo():
    """Lift the crown monogram off its cream ground into a transparent PNG."""
    src, box = LOGO_SRC
    im = Image.open(os.path.join(SRC, src)).crop(box).convert('RGB')
    w, h = im.size
    px = im.load()
    corners = [px[2, 2], px[w - 3, 2], px[2, h - 3], px[w - 3, h - 3]]
    bg = tuple(sum(c[i] for c in corners) // len(corners) for i in range(3))

    out = Image.new('RGBA', (w, h))
    op = out.load()
    lo, hi = 14.0, 48.0
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            d = max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2]))
            a = (d - lo) / (hi - lo)
            op[x, y] = (r, g, b, int(255 * (0.0 if a < 0 else (1.0 if a > 1 else a))))

    out = out.resize((320, round(320 * h / w)), Image.LANCZOS)
    path = os.path.join(ROOT, 'assets', 'img', 'logo-mark.png')
    out.save(path, optimize=True)
    print('  %-26s %4dx%-4d %5.0f KB  (background %s keyed out)'
          % ('logo-mark', out.width, out.height, os.path.getsize(path) / 1024, bg))


if __name__ == '__main__':
    print('photographs:')
    prep_photos()
    print('logo:')
    prep_logo()
