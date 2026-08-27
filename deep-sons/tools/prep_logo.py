"""Lift the Deep Son's monogram off the creative it was supplied on.

The mark sits on a tan gradient, so the background is modelled per column
from the clear strip above the logo and anything darker than it becomes
opaque. That keeps the dark scrollwork, the maroon DS and the brown
name plate while dropping the backdrop, so the logo works on cream and
on the dark footer alike.

Run:  python3 tools/prep_logo.py
"""

import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))

SRC = os.path.join(ROOT, 'brand-source', 'logo-source.jpg')
IMG = os.path.join(ROOT, 'assets', 'img')

# the full lockup, and the monogram alone for small sizes where the name
# plate would be illegible anyway
JOBS = [
    ('logo-full.png', (55, 84, 408, 464), 330),
    ('logo-mark.png', (55, 84, 408, 392), 190),
]
SAMPLE = 14                 # rows of clean backdrop above the mark
DEAD = 9.0                  # ignore this much variation in the backdrop itself
SPREAD = 48.0               # luminance below background at which a pixel is solid


def lum(p):
    return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]


def cut(crop, width, name):
    im = Image.open(SRC).crop(crop).convert('RGB')
    w, h = im.size
    px = im.load()

    # background luminance per column, from the strip above the mark
    bg = []
    for x in range(w):
        col = sorted(lum(px[x, y]) for y in range(SAMPLE))
        bg.append(col[len(col) // 2])
    # smooth it so a stray pixel cannot carve a stripe out of the logo
    smooth = []
    for x in range(w):
        lo, hi = max(0, x - 6), min(w, x + 7)
        smooth.append(sum(bg[lo:hi]) / (hi - lo))

    out = Image.new('RGBA', (w, h))
    op = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            a = (smooth[x] - lum((r, g, b)) - DEAD) / (SPREAD - DEAD)
            a = 0.0 if a < 0 else (1.0 if a > 1 else a)
            op[x, y] = (r, g, b, int(a * 255))

    out = out.resize((width, round(width * h / w)), Image.LANCZOS)
    path = os.path.join(IMG, name)
    out.save(path, optimize=True)
    print('  %-14s %dx%-4d %5.0f KB'
          % (name, out.width, out.height, os.path.getsize(path) / 1024))


def main():
    for name, crop, width in JOBS:
        cut(crop, width, name)


if __name__ == '__main__':
    main()
