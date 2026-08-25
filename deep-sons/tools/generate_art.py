#!/usr/bin/env python3
"""Generate the original artwork used across the Deep Sons website.

Every image on the site is drawn here from vector primitives, so the whole
gallery is original work that belongs to Deep Sons: no stock photography,
no third-party licences, nothing to attribute and nothing to take down.

Run:  python3 tools/generate_art.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'assets', 'img')
JS = os.path.join(ROOT, 'assets', 'js')

W, H = 800, 1100

# ---------------------------------------------------------------- colour ---

def _hex(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    """Blend a towards b by t (0..1)."""
    ra, ga, ba = _hex(a)
    rb, gb, bb = _hex(b)
    return '#%02x%02x%02x' % (
        round(ra + (rb - ra) * t),
        round(ga + (gb - ga) * t),
        round(ba + (bb - ba) * t),
    )


RAW = {
    'ivory':    ('Ivory',        '#efe6d3', '#cbbc9e', '#fbf6ea', '#c8a02f'),
    'cream':    ('Cream',        '#f5ecd9', '#d6c6a5', '#fffaf0', '#b98f3a'),
    'beige':    ('Beige',        '#ded0b6', '#b9a888', '#f2e8d5', '#8c6f43'),
    'gold':     ('Gold',         '#d9b45a', '#a8842f', '#f0d68f', '#6d4f16'),
    'mustard':  ('Mustard',      '#d99a1f', '#a56d0b', '#f0bd57', '#5c3d06'),
    'copper':   ('Copper',       '#b5673a', '#8a4726', '#d78f61', '#f2c98a'),
    'rust':     ('Rust',         '#a8482c', '#7d301b', '#c86f4f', '#edc178'),
    'maroon':   ('Maroon',       '#6e1f2b', '#4b101a', '#92384a', '#d9b25c'),
    'wine':     ('Wine',         '#59243b', '#3b1427', '#7c3d56', '#cba55f'),
    'rose':     ('Rose',         '#d98a95', '#b0636f', '#f0b3ba', '#8a3f4c'),
    'pink':     ('Pink',         '#e8a7b4', '#c47f8e', '#f7c9d1', '#8e4a58'),
    'peach':    ('Peach',        '#e8b48d', '#c08a63', '#f7d2b4', '#91572e'),
    'lavender': ('Lavender',     '#a89ac9', '#7d6ea3', '#c7bce0', '#4b3d73'),
    'sage':     ('Sage Green',   '#9aa885', '#74815f', '#bcc7a8', '#4e5a3a'),
    'olive':    ('Olive',        '#6f7a44', '#4e5729', '#94a066', '#d6c07a'),
    'emerald':  ('Emerald',      '#1f6b52', '#124534', '#3d9375', '#d8b45e'),
    'bottle':   ('Bottle Green', '#14483a', '#0a2d23', '#2c6d5a', '#cba24f'),
    'teal':     ('Teal',         '#1d6470', '#0f424c', '#3a8b98', '#d8b45e'),
    'powder':   ('Powder Blue',  '#a9c3d9', '#7f9cb5', '#cbdcea', '#35566e'),
    'royal':    ('Royal Blue',   '#24478f', '#142c62', '#4a6cb5', '#d3b158'),
    'navy':     ('Navy',         '#1b2a4a', '#0e1a30', '#364a72', '#c9a95c'),
    'indigo':   ('Indigo',       '#33306b', '#201d47', '#55518f', '#cdae62'),
    'charcoal': ('Charcoal',     '#3a3d42', '#232529', '#5a5e66', '#b9bcc2'),
    'grey':     ('Grey',         '#8e9299', '#6a6e75', '#b2b6bd', '#3c3f45'),
    'black':    ('Black',        '#23242a', '#121317', '#414349', '#c6a95f'),
    'white':    ('White',        '#f4f4f2', '#d5d5d1', '#ffffff', '#9aa0a6'),
    'skyblue':  ('Sky Blue',     '#bcd3e6', '#93b0c8', '#dcebf6', '#3f6682'),
    'lilac':    ('Lilac',        '#c9b7d9', '#a08fb3', '#e3d7ee', '#5b4670'),
}

PALETTE = {}
for key, (label, base, dark, light, accent) in RAW.items():
    PALETTE[key] = {
        'key': key,
        'label': label,
        'base': base,
        'dark': dark,
        'light': light,
        'accent': accent,
        'bg1': mix(base, '#f6f0e5', 0.82),
        'bg2': mix(base, '#d8cec0', 0.60),
    }

SKIN = '#c08a5e'
SKIN_D = '#a06f47'
HAIR = '#241a15'
SHOE = '#3a2b20'

# --------------------------------------------------------------- patterns ---


def pattern_def(pid, kind, c):
    """Return an SVG <pattern> that paints one fabric."""
    base, dark, light, acc = c['base'], c['dark'], c['light'], c['accent']

    def wrap(w, h, inner):
        return ('<pattern id="%s" patternUnits="userSpaceOnUse" width="%s" '
                'height="%s"><rect width="%s" height="%s" fill="%s"/>%s'
                '</pattern>' % (pid, w, h, w, h, base, inner))

    if kind == 'plain':
        return wrap(16, 16, '<path d="M0,16 L16,0" stroke="%s" stroke-width="1" '
                            'opacity=".10"/>' % light)

    if kind == 'twill':
        return wrap(12, 12, '<path d="M-3,3 L3,-3 M0,12 L12,0 M9,15 L15,9" '
                            'stroke="%s" stroke-width="2.2" opacity=".22"/>' % dark)

    if kind == 'pinstripe':
        return wrap(20, 20, '<path d="M5,0 L5,20" stroke="%s" stroke-width="1.6" '
                            'opacity=".55"/><path d="M15,0 L15,20" stroke="%s" '
                            'stroke-width="1" opacity=".18"/>' % (light, dark))

    if kind == 'herringbone':
        return wrap(24, 24, '<path d="M0,12 L6,6 L12,12 L18,6 L24,12" fill="none" '
                            'stroke="%s" stroke-width="2.4" opacity=".28"/>'
                            '<path d="M0,24 L6,18 L12,24 L18,18 L24,24" fill="none" '
                            'stroke="%s" stroke-width="2.4" opacity=".16"/>' % (dark, light))

    if kind == 'windowpane':
        return wrap(72, 72, '<path d="M0,0 L0,72 M0,0 L72,0" stroke="%s" '
                            'stroke-width="2.6" opacity=".45"/>'
                            '<path d="M36,0 L36,72 M0,36 L72,36" stroke="%s" '
                            'stroke-width="1" opacity=".20"/>' % (light, dark))

    if kind == 'glencheck':
        return wrap(40, 40, '<path d="M0,0 L0,40 M20,0 L20,40" stroke="%s" '
                            'stroke-width="1.6" opacity=".30"/>'
                            '<path d="M0,0 L40,0 M0,20 L40,20" stroke="%s" '
                            'stroke-width="1.6" opacity=".30"/>'
                            '<path d="M0,10 L40,10 M10,0 L10,40" stroke="%s" '
                            'stroke-width="4" opacity=".14"/>' % (dark, dark, light))

    if kind == 'check':
        return wrap(44, 44, '<rect width="22" height="22" fill="%s" opacity=".38"/>'
                            '<rect x="22" y="22" width="22" height="22" fill="%s" '
                            'opacity=".38"/><path d="M22,0 L22,44 M0,22 L44,22" '
                            'stroke="%s" stroke-width="1" opacity=".25"/>'
                            % (light, dark, dark))

    if kind == 'dobby':
        return wrap(22, 22, '<circle cx="5.5" cy="5.5" r="2" fill="%s" opacity=".45"/>'
                            '<circle cx="16.5" cy="16.5" r="2" fill="%s" opacity=".45"/>'
                            '<circle cx="16.5" cy="5.5" r="1.2" fill="%s" opacity=".28"/>'
                            '<circle cx="5.5" cy="16.5" r="1.2" fill="%s" opacity=".28"/>'
                            % (light, light, dark, dark))

    if kind == 'bandhani':
        return wrap(30, 30, '<circle cx="8" cy="8" r="3.4" fill="none" stroke="%s" '
                            'stroke-width="1.6" opacity=".7"/>'
                            '<circle cx="8" cy="8" r="1.1" fill="%s" opacity=".8"/>'
                            '<circle cx="23" cy="23" r="3.4" fill="none" stroke="%s" '
                            'stroke-width="1.6" opacity=".7"/>'
                            '<circle cx="23" cy="23" r="1.1" fill="%s" opacity=".8"/>'
                            % (light, acc, light, acc))

    if kind == 'zari':
        return wrap(18, 18, '<path d="M0,4 L18,4" stroke="%s" stroke-width="2.4" '
                            'opacity=".65"/><path d="M0,11 L18,11" stroke="%s" '
                            'stroke-width="1" opacity=".3"/>' % (acc, light))

    if kind == 'chevron':
        return wrap(32, 28, '<path d="M0,20 L8,8 L16,20 L24,8 L32,20" fill="none" '
                            'stroke="%s" stroke-width="3" opacity=".55"/>'
                            '<path d="M0,6 L8,-6 L16,6 L24,-6 L32,6" fill="none" '
                            'stroke="%s" stroke-width="3" opacity=".25"/>' % (acc, light))

    if kind == 'lattice':
        return wrap(54, 54, '<path d="M27,2 L52,27 L27,52 L2,27 Z" fill="none" '
                            'stroke="%s" stroke-width="2" opacity=".55"/>'
                            '<path d="M27,14 L40,27 L27,40 L14,27 Z" fill="%s" '
                            'opacity=".18"/><circle cx="27" cy="27" r="3.2" fill="%s" '
                            'opacity=".8"/><circle cx="0" cy="0" r="2.4" fill="%s" '
                            'opacity=".6"/><circle cx="54" cy="54" r="2.4" fill="%s" '
                            'opacity=".6"/><circle cx="0" cy="54" r="2.4" fill="%s" '
                            'opacity=".6"/><circle cx="54" cy="0" r="2.4" fill="%s" '
                            'opacity=".6"/>' % (acc, light, acc, acc, acc, acc, acc))

    if kind == 'paisley':
        m = ('<path d="M18,54 C4,48 4,26 20,17 C38,7 56,18 52,35 C49,48 35,52 29,43 '
             'C24,35 30,26 38,28" fill="none" stroke="%s" stroke-width="2.6" '
             'opacity=".8" stroke-linecap="round"/>'
             '<circle cx="24" cy="30" r="2.6" fill="%s" opacity=".7"/>'
             '<circle cx="43" cy="46" r="2" fill="%s" opacity=".55"/>'
             '<path d="M60,62 C66,58 72,62 70,68" fill="none" stroke="%s" '
             'stroke-width="2" opacity=".5"/>' % (acc, light, acc, light))
        return wrap(76, 76, m)

    if kind == 'floral':
        petals = ''.join(
            '<ellipse cx="30" cy="30" rx="6" ry="13" fill="%s" opacity=".62" '
            'transform="rotate(%d 30 30)"/>' % (acc, a) for a in (0, 45, 90, 135))
        m = (petals + '<circle cx="30" cy="30" r="4.2" fill="%s" opacity=".9"/>'
             '<path d="M30,44 C34,52 44,54 50,52" fill="none" stroke="%s" '
             'stroke-width="2" opacity=".45"/>'
             '<ellipse cx="52" cy="50" rx="7" ry="3.4" fill="%s" opacity=".45" '
             'transform="rotate(-25 52 50)"/>' % (light, light, acc))
        return wrap(62, 62, m)

    if kind == 'scroll':
        m = ('<path d="M4,44 C14,20 34,20 40,36 C45,48 60,48 64,32" fill="none" '
             'stroke="%s" stroke-width="2.6" opacity=".75" stroke-linecap="round"/>'
             '<path d="M8,58 C22,50 30,58 38,56" fill="none" stroke="%s" '
             'stroke-width="1.8" opacity=".4"/>'
             '<circle cx="20" cy="28" r="2.4" fill="%s" opacity=".85"/>'
             '<circle cx="52" cy="42" r="2.4" fill="%s" opacity=".85"/>'
             '<circle cx="60" cy="14" r="1.8" fill="%s" opacity=".6"/>'
             % (acc, light, acc, acc, light))
        return wrap(68, 68, m)

    if kind == 'buti':
        m = ('<path d="M20,10 L26,20 L20,30 L14,20 Z" fill="%s" opacity=".7"/>'
             '<circle cx="20" cy="20" r="2" fill="%s" opacity=".8"/>'
             '<path d="M0,40 L6,50 L0,60 L-6,50 Z" fill="%s" opacity=".45"/>'
             '<path d="M40,40 L46,50 L40,60 L34,50 Z" fill="%s" opacity=".45"/>'
             % (acc, light, acc, acc))
        return wrap(40, 60, m)

    if kind == 'brocade':
        m = ('<path d="M0,24 C12,10 36,10 48,24 C36,38 12,38 0,24 Z" fill="none" '
             'stroke="%s" stroke-width="2.2" opacity=".6"/>'
             '<circle cx="24" cy="24" r="4" fill="%s" opacity=".55"/>'
             '<path d="M24,0 L24,8 M24,40 L24,48" stroke="%s" stroke-width="2" '
             'opacity=".45"/>' % (acc, light, acc))
        return wrap(48, 48, m)

    return wrap(16, 16, '')


PATTERN_LABEL = {
    'plain': 'Plain weave', 'twill': 'Twill weave', 'pinstripe': 'Pinstripe',
    'herringbone': 'Herringbone', 'windowpane': 'Windowpane check',
    'glencheck': 'Glen check', 'check': 'Gingham check', 'dobby': 'Dobby dot',
    'bandhani': 'Bandhani', 'zari': 'Zari stripe', 'chevron': 'Chevron',
    'lattice': 'Jaal lattice', 'paisley': 'Paisley buta', 'floral': 'Floral vine',
    'scroll': 'Threadwork scroll', 'buti': 'Buti motif', 'brocade': 'Brocade',
}

# ------------------------------------------------------------------ parts ---


def defs(c, fab_kind, second=None, bgc=None, span=(252, 552)):
    d = ['<defs>']
    d.append(pattern_def('fab', fab_kind, c))
    if second:
        d.append(pattern_def('fab2', second[1], second[0]))
    d.append('<linearGradient id="sheen" gradientUnits="userSpaceOnUse" '
             'x1="%d" y1="0" x2="%d" y2="0">'
             '<stop offset="0" stop-color="#000" stop-opacity=".22"/>'
             '<stop offset=".26" stop-color="#fff" stop-opacity=".16"/>'
             '<stop offset=".55" stop-color="#fff" stop-opacity="0"/>'
             '<stop offset="1" stop-color="#000" stop-opacity=".26"/>'
             '</linearGradient>' % span)
    b = bgc or c
    d.append('<radialGradient id="bg" cx=".5" cy=".38" r=".78">'
             '<stop offset="0" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></radialGradient>' % (b['bg1'], b['bg2']))
    d.append('<radialGradient id="floor" cx=".5" cy=".5" r=".5">'
             '<stop offset="0" stop-color="#000" stop-opacity=".26"/>'
             '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>')
    d.append('</defs>')
    return ''.join(d)


def backdrop():
    return ('<rect width="%d" height="%d" fill="url(#bg)"/>'
            '<ellipse cx="400" cy="1035" rx="235" ry="46" fill="url(#floor)"/>' % (W, H))


def head():
    return (
        '<path d="M378,232 L422,232 L424,296 L376,296 Z" fill="%s"/>'
        '<path d="M378,232 L422,232 L422,258 C410,268 390,268 378,258 Z" fill="%s" opacity=".55"/>'
        '<ellipse cx="348" cy="196" rx="8" ry="12" fill="%s"/>'
        '<ellipse cx="452" cy="196" rx="8" ry="12" fill="%s"/>'
        '<ellipse cx="400" cy="188" rx="53" ry="63" fill="%s"/>'
        '<path d="M347,186 C341,130 378,113 400,113 C422,113 459,130 453,186 '
        'C449,158 438,144 400,144 C362,144 351,158 347,186 Z" fill="%s"/>'
        % (SKIN, SKIN_D, SKIN, SKIN, SKIN, HAIR))


def hands(lx=282, ly=584, rx=518, ry=584):
    return ('<ellipse cx="%d" cy="%d" rx="19" ry="25" fill="%s" '
            'transform="rotate(-8 %d %d)"/>'
            '<ellipse cx="%d" cy="%d" rx="19" ry="25" fill="%s" '
            'transform="rotate(8 %d %d)"/>' % (lx, ly, SKIN, lx, ly, rx, ry, SKIN, rx, ry))


def legs(fill, stroke, top=596):
    d = ('M344,%d L456,%d L452,1006 L410,1006 L400,720 L390,1006 L348,1006 Z'
         % (top, top))
    return ('<path d="%s" fill="%s"/><path d="%s" fill="url(#sheen)" opacity=".5"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="2" opacity=".35"/>'
            % (d, fill, d, d, stroke))


def shoes():
    return ('<path d="M330,1000 L396,1000 L396,1022 C396,1032 388,1036 378,1036 '
            'L338,1036 C328,1036 322,1030 324,1020 Z" fill="%s"/>'
            '<path d="M404,1000 L470,1000 L476,1020 C478,1030 472,1036 462,1036 '
            'L422,1036 C412,1036 404,1032 404,1022 Z" fill="%s"/>'
            '<path d="M330,1010 L396,1010 M404,1010 L472,1010" stroke="#fff" '
            'stroke-width="1.6" opacity=".2"/>' % (SHOE, SHOE))


def cloth(paths, fill='url(#fab)', stroke=None, shade=True):
    out = []
    for d in paths:
        out.append('<path d="%s" fill="%s"/>' % (d, fill))
    if shade:
        for d in paths:
            out.append('<path d="%s" fill="url(#sheen)"/>' % d)
    if stroke:
        for d in paths:
            out.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.4" '
                       'opacity=".45"/>' % (d, stroke))
    return ''.join(out)


def buttons(n, x, y0, step, c, r=6):
    return ''.join('<circle cx="%d" cy="%d" r="%s" fill="%s" stroke="%s" '
                   'stroke-width="1.4"/>' % (x, y0 + i * step, r, c['accent'], c['dark'])
                   for i in range(n))


def mandarin(c, tall=False):
    if tall:
        return ('<path d="M370,276 C386,264 414,264 430,276 L424,306 L400,328 '
                'L376,306 Z" fill="%s"/>'
                '<path d="M374,282 C388,272 412,272 426,282" fill="none" '
                'stroke="%s" stroke-width="2" opacity=".7"/>' % (c['dark'], c['accent']))
    return ('<path d="M372,284 C386,274 414,274 428,284 L422,304 L400,326 L378,304 Z" '
            'fill="%s"/>' % c['dark'])


SLEEVE_L = 'M294,336 C278,372 266,442 256,548 L300,558 C310,452 318,390 330,342 Z'
SLEEVE_R = 'M506,336 C522,372 534,442 544,548 L500,558 C490,452 482,390 470,342 Z'
SLEEVE_L_LONG = 'M290,334 C272,372 258,452 246,578 L292,590 C304,470 312,392 326,340 Z'
SLEEVE_R_LONG = 'M510,334 C528,372 542,452 554,578 L508,590 C496,470 488,392 474,340 Z'

# --------------------------------------------------------------- garments ---


def g_kurta(c):
    torso = ('M292,340 C296,314 312,300 336,296 L378,292 L400,328 L422,292 L464,296 '
             'C488,300 504,314 508,340 L526,798 Q400,822 274,798 Z')
    body = legs(c['light'], c['dark'])
    body += cloth([torso, SLEEVE_L, SLEEVE_R], stroke=c['dark'])
    body += mandarin(c)
    body += ('<path d="M392,330 L408,330 L408,790 L392,790 Z" fill="%s" opacity=".35"/>'
             % c['dark'])
    body += buttons(6, 400, 352, 56, c, r=5)
    body += ('<path d="M256,548 L300,558 M544,548 L500,558" stroke="%s" '
             'stroke-width="4" opacity=".5"/>' % c['dark'])
    return body, hands()


def g_kurta_jacket(c, jc, jkind):
    torso = ('M296,340 C300,314 316,300 340,296 L380,292 L400,328 L420,292 L460,296 '
             'C484,300 500,314 504,340 L520,796 Q400,818 280,796 Z')
    body = legs(c['light'], c['dark'])
    body += cloth([torso, SLEEVE_L, SLEEVE_R], stroke=c['dark'])
    body += mandarin(c)
    jacket = ('M322,340 C326,314 340,300 360,296 L384,294 L400,334 L416,294 L440,296 '
              'C460,300 474,314 478,340 L500,652 Q400,668 300,652 Z')
    body += cloth([jacket], fill='url(#fab2)', stroke=jc['dark'])
    body += ('<path d="M400,334 L400,662" stroke="%s" stroke-width="2.6" '
             'opacity=".55"/>' % jc['dark'])
    body += ('<path d="M386,292 C393,306 407,306 414,292" fill="none" stroke="%s" '
             'stroke-width="2.4" opacity=".7"/>' % jc['accent'])
    body += buttons(5, 400, 376, 58, jc, r=6)
    body += ('<path d="M338,414 L372,408 L360,436 Z" fill="%s" opacity=".9"/>'
             % jc['accent'])
    body += ('<path d="M256,548 L300,558 M544,548 L500,558" stroke="%s" '
             'stroke-width="4" opacity=".5"/>' % c['dark'])
    return body, hands()


def g_sherwani(c):
    coat = ('M288,338 C292,312 308,298 334,294 L376,292 L400,330 L424,292 L466,296 '
            'C492,300 508,312 512,338 L548,876 Q400,902 252,876 Z')
    body = legs(c['light'], c['dark'])
    body += cloth([coat, SLEEVE_L_LONG, SLEEVE_R_LONG], stroke=c['dark'])
    body += mandarin(c, tall=True)
    body += ('<path d="M388,330 L412,330 L420,868 L380,868 Z" fill="%s" opacity=".9"/>'
             '<path d="M388,330 L412,330 L420,868 L380,868 Z" fill="none" stroke="%s" '
             'stroke-width="2" opacity=".85"/>' % (c['dark'], c['accent']))
    body += ''.join('<circle cx="400" cy="%d" r="5.6" fill="%s"/>'
                    '<circle cx="400" cy="%d" r="2" fill="%s" opacity=".8"/>'
                    % (356 + i * 62, c['accent'], 356 + i * 62, c['light'])
                    for i in range(8))
    body += ('<path d="M256,842 Q400,868 544,842" fill="none" stroke="%s" '
             'stroke-width="7" opacity=".85"/>' % c['accent'])
    body += ('<path d="M248,566 L292,578 M552,566 L508,578" stroke="%s" '
             'stroke-width="5" opacity=".8"/>' % c['accent'])
    return body, hands(280, 604, 520, 604)


def g_jodhpuri(c):
    coat = ('M296,338 C300,312 316,298 340,294 L378,292 L400,326 L422,292 L460,294 '
            'C484,298 500,312 504,338 L518,702 L282,702 Z')
    body = legs(c['base'], c['dark'])
    body += ('<path d="M344,596 L456,596 L452,1006 L410,1006 L400,720 L390,1006 '
             'L348,1006 Z" fill="url(#fab)"/>')
    body += cloth([coat, SLEEVE_L, SLEEVE_R], stroke=c['dark'])
    body += ('<path d="M366,272 C384,258 416,258 434,272 L428,304 L400,322 L372,304 Z" '
             'fill="%s"/><path d="M370,280 C386,268 414,268 430,280" fill="none" '
             'stroke="%s" stroke-width="2.2" opacity=".8"/>' % (c['dark'], c['accent']))
    body += ('<path d="M400,322 L400,698" stroke="%s" stroke-width="2.2" '
             'opacity=".5"/>' % c['dark'])
    body += buttons(5, 400, 356, 66, c, r=6)
    body += ('<path d="M318,412 L372,404" stroke="%s" stroke-width="3" opacity=".5"/>'
             '<path d="M330,406 L366,400 L354,428 Z" fill="%s"/>' % (c['dark'], c['accent']))
    body += ('<circle cx="424" cy="300" r="7" fill="%s"/>'
             '<circle cx="424" cy="300" r="2.6" fill="%s"/>' % (c['accent'], c['light']))
    body += ('<path d="M330,560 L344,556 M456,556 L470,560" stroke="%s" '
             'stroke-width="3" opacity=".45"/>' % c['dark'])
    return body, hands()


def g_indowestern(c, jc, jkind):
    tunic = ('M296,340 C300,314 316,300 340,296 L380,292 L400,328 L420,292 L460,296 '
             'C484,300 500,314 504,340 L516,760 Q400,782 284,760 Z')
    body = legs(c['light'], c['dark'])
    body += cloth([tunic, SLEEVE_L, SLEEVE_R], stroke=c['dark'])
    drape = ('M300,332 C304,310 318,298 342,294 L382,292 L400,330 L418,292 L458,294 '
             'C482,298 496,310 500,332 L542,886 L488,898 L272,656 Z')
    body += cloth([drape], fill='url(#fab2)', stroke=jc['dark'])
    body += ('<path d="M272,656 L488,898" stroke="%s" stroke-width="8" '
             'opacity=".95" stroke-linecap="round"/>' % jc['accent'])
    body += ('<path d="M400,330 L400,470 L360,530" fill="none" stroke="%s" '
             'stroke-width="2.6" opacity=".6"/>' % jc['dark'])
    body += ('<circle cx="400" cy="360" r="6" fill="%s"/>'
             '<circle cx="388" cy="412" r="6" fill="%s"/>'
             '<circle cx="374" cy="466" r="6" fill="%s"/>'
             % (jc['accent'], jc['accent'], jc['accent']))
    body += ('<path d="M386,292 C393,306 407,306 414,292" fill="none" stroke="%s" '
             'stroke-width="2.4" opacity=".7"/>' % jc['accent'])
    return body, hands()


def g_suit(c):
    body = ('<path d="M344,596 L456,596 L452,1006 L410,1006 L400,720 L390,1006 '
            'L348,1006 Z" fill="url(#fab)"/>'
            '<path d="M344,596 L456,596 L452,1006 L410,1006 L400,720 L390,1006 '
            'L348,1006 Z" fill="url(#sheen)" opacity=".5"/>')
    body += ('<path d="M340,296 L460,296 L460,600 L340,600 Z" fill="#f7f5f0"/>'
             '<path d="M372,288 L400,320 L428,288 L432,306 L400,336 L368,306 Z" '
             'fill="#ffffff"/>')
    body += ('<path d="M394,318 L406,318 L416,342 L408,516 L392,516 L384,342 Z" '
             'fill="%s"/><path d="M394,318 L406,318 L416,342 L400,352 L384,342 Z" '
             'fill="%s" opacity=".55"/>' % (c['accent'], c['dark']))
    jacket = ('M294,340 C298,314 314,300 338,296 L382,290 L400,472 L418,290 L462,296 '
              'C486,300 502,314 506,340 L520,706 L280,706 Z')
    body += cloth([jacket, SLEEVE_L, SLEEVE_R], stroke=c['dark'])
    body += ('<path d="M382,290 L400,472 L366,436 L344,300 Z" fill="url(#fab)"/>'
             '<path d="M382,290 L400,472 L366,436 L344,300 Z" fill="#000" opacity=".16"/>'
             '<path d="M418,290 L400,472 L434,436 L456,300 Z" fill="url(#fab)"/>'
             '<path d="M418,290 L400,472 L434,436 L456,300 Z" fill="#fff" opacity=".10"/>')
    body += ('<path d="M382,290 L400,472 L366,436 L344,300 Z M418,290 L400,472 '
             'L434,436 L456,300 Z" fill="none" stroke="%s" stroke-width="2" '
             'opacity=".55"/>' % c['dark'])
    body += buttons(2, 400, 496, 52, c, r=7)
    body += ('<path d="M318,470 L352,464" stroke="%s" stroke-width="2.4" '
             'opacity=".55"/>'
             '<path d="M320,462 L348,457 L336,442 Z" fill="#fff" opacity=".95"/>'
             % c['dark'])
    body += ('<path d="M300,540 L318,546 M500,540 L482,546" stroke="%s" '
             'stroke-width="2" opacity=".4"/>' % c['dark'])
    return body, hands()


def g_shirt(c, trouser='charcoal'):
    t = PALETTE[trouser]
    shirt = ('M300,338 C304,312 320,298 344,294 L384,292 L400,332 L416,292 L456,294 '
             'C480,298 496,312 500,338 L510,664 L290,664 Z')
    body = legs(t['base'], t['dark'], top=618)
    body += cloth([shirt, SLEEVE_L, SLEEVE_R], stroke=c['dark'])
    body += ('<path d="M376,286 L400,330 L366,318 L358,294 Z" fill="%s"/>'
             '<path d="M424,286 L400,330 L434,318 L442,294 Z" fill="%s"/>'
             '<path d="M372,282 C386,272 414,272 428,282 L424,296 L400,318 L376,296 Z" '
             'fill="%s" opacity=".85"/>' % (c['light'], c['light'], c['light']))
    body += ('<path d="M392,326 L410,326 L410,660 L392,660 Z" fill="%s" opacity=".3"/>'
             % c['dark'])
    body += ''.join('<circle cx="401" cy="%d" r="4.4" fill="%s" opacity=".9"/>'
                    % (356 + i * 58, c['light']) for i in range(5))
    body += ('<path d="M336,404 L376,398 L376,446 L336,452 Z" fill="%s" opacity=".25"/>'
             % c['dark'])
    body += ('<path d="M254,540 L302,552 L298,572 L250,560 Z" fill="%s"/>'
             '<path d="M546,540 L498,552 L502,572 L550,560 Z" fill="%s"/>'
             % (c['light'], c['light']))
    body += ('<path d="M344,614 L456,614" stroke="%s" stroke-width="10" opacity=".9"/>'
             '<rect x="384" y="606" width="32" height="18" rx="4" fill="%s"/>'
             % (t['dark'], t['accent']))
    return body, hands()


def g_bolt(c):
    """Folded lengths of cloth stacked on the shop counter."""
    out = ['<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H)]
    out.append('<rect x="0" y="852" width="800" height="248" fill="#8a6a45" '
               'opacity=".30"/>')
    out.append('<path d="M0,852 L800,852" stroke="#5e4526" stroke-width="4" '
               'opacity=".32"/>')
    out.append('<ellipse cx="400" cy="866" rx="300" ry="34" fill="url(#floor)"/>')

    # a rolled bolt standing at the back
    out.append('<path d="M600,236 L700,236 L700,846 L600,846 Z" fill="url(#fab)"/>')
    out.append('<path d="M600,236 L700,236 L700,846 L600,846 Z" fill="url(#sheen)" '
               'opacity=".45"/>')
    out.append('<ellipse cx="650" cy="236" rx="50" ry="17" fill="%s"/>' % c['light'])
    out.append('<ellipse cx="650" cy="236" rx="50" ry="17" fill="none" stroke="%s" '
               'stroke-width="2" opacity=".5"/>' % c['dark'])
    out.append('<path d="M650,236 C672,244 676,252 650,253" fill="none" stroke="%s" '
               'stroke-width="2" opacity=".55"/>' % c['dark'])
    out.append('<path d="M600,236 L600,846 M700,236 L700,846" stroke="%s" '
               'stroke-width="2" opacity=".35"/>' % c['dark'])

    # folded lengths stacked in front
    for i in range(5):
        y0 = 366 + i * 100
        left = i % 2 == 0
        if left:
            d = ('M132,%d C96,%d 96,%d 132,%d L560,%d L560,%d Z'
                 % (y0, y0 + 32, y0 + 60, y0 + 92, y0 + 62, y0 - 24))
            fold = 'M132,%d C102,%d 102,%d 132,%d' % (y0 + 5, y0 + 34, y0 + 58, y0 + 87)
        else:
            d = ('M560,%d C596,%d 596,%d 560,%d L132,%d L132,%d Z'
                 % (y0 - 20, y0 + 12, y0 + 44, y0 + 76, y0 + 92, y0))
            fold = 'M560,%d C590,%d 590,%d 560,%d' % (y0 - 15, y0 + 14, y0 + 42, y0 + 71)
        out.append('<path d="%s" fill="url(#fab)"/>' % d)
        out.append('<path d="%s" fill="url(#sheen)" opacity=".45"/>' % d)
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.4" '
                   'opacity=".55"/>' % (d, c['dark']))
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" '
                   'opacity=".6"/>' % (fold, c['light']))
        out.append('<path d="%s" fill="none" stroke="#000" stroke-width="10" '
                   'opacity=".07" transform="translate(0,8)"/>' % fold)

    # the shop's own tag on the top length
    out.append('<g transform="rotate(-7 512 352)">'
               '<path d="M486,336 L540,326 L548,366 L494,376 Z" fill="#fffdf6"/>'
               '<path d="M486,336 L540,326 L548,366 L494,376 Z" fill="none" '
               'stroke="%s" stroke-width="1.6" opacity=".5"/>'
               '<path d="M496,346 L536,338 M496,356 L530,349" stroke="%s" '
               'stroke-width="2.6" opacity=".65"/></g>' % (c['dark'], c['dark']))
    return ''.join(out), ''


def g_tools(c):
    """Atelier still life: cloth on the counter with shears, tape, spools and pins."""
    out = ['<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H)]
    out.append('<rect x="0" y="600" width="800" height="500" fill="#8a6a45" '
               'opacity=".30"/>')
    out.append('<path d="M0,600 L800,600" stroke="#5e4526" stroke-width="4" '
               'opacity=".35"/>')
    out.append('<ellipse cx="400" cy="906" rx="316" ry="48" fill="url(#floor)"/>')

    # measuring tape, draped across the upper third
    tape = 'M36,384 C176,286 296,486 424,438 C556,388 658,470 772,398'
    out.append('<path d="%s" fill="none" stroke="#c68f18" stroke-width="30" '
               'stroke-linecap="round" transform="translate(0,9)" opacity=".45"/>' % tape)
    out.append('<path d="%s" fill="none" stroke="#eab93f" stroke-width="30" '
               'stroke-linecap="round"/>' % tape)
    out.append('<path d="%s" fill="none" stroke="#4a3312" stroke-width="26" '
               'stroke-dasharray="2.5 24" opacity=".85" '
               'transform="translate(0,-7)"/>' % tape)
    out.append('<path d="%s" fill="none" stroke="#4a3312" stroke-width="10" '
               'stroke-dasharray="2.5 24" opacity=".6" '
               'transform="translate(0,9)"/>' % tape)

    # length of cloth on the counter
    d = ('M62,470 C214,398 322,536 470,478 C596,428 700,486 742,522 L742,858 '
         'C656,906 534,818 420,868 C300,920 140,884 62,842 Z')
    out.append('<path d="%s" fill="url(#fab)"/><path d="%s" fill="url(#sheen)"/>'
               '<path d="%s" fill="none" stroke="%s" stroke-width="2.6" '
               'opacity=".5"/>' % (d, d, d, c['dark']))
    out.append('<path d="M104,568 C246,506 336,626 474,566 C592,514 682,556 726,586" '
               'fill="none" stroke="%s" stroke-width="3" opacity=".22"/>' % c['dark'])
    out.append('<path d="M92,712 C242,652 334,780 466,714 C580,658 680,700 728,730" '
               'fill="none" stroke="%s" stroke-width="3" opacity=".16"/>' % c['light'])

    # tailor's shears
    out.append('<g transform="translate(474,700) rotate(-17)">'
               '<path d="M4,-5 L188,-44 L196,-18 L10,5 Z" fill="#b6bec7"/>'
               '<path d="M4,5 L188,44 L196,18 L10,-5 Z" fill="#8e97a1"/>'
               '<path d="M10,-5 L188,-44 M10,5 L188,44" stroke="#616a74" '
               'stroke-width="2"/>'
               '<path d="M0,-3 L-30,-18 M0,3 L-30,18" stroke="#2c2f35" '
               'stroke-width="15" stroke-linecap="round"/>'
               '<ellipse cx="-66" cy="-30" rx="42" ry="23" fill="none" '
               'stroke="#2c2f35" stroke-width="15" transform="rotate(-22 -66 -30)"/>'
               '<ellipse cx="-66" cy="30" rx="42" ry="23" fill="none" '
               'stroke="#2c2f35" stroke-width="15" transform="rotate(22 -66 30)"/>'
               '<circle cx="2" cy="0" r="9" fill="#5c6169"/>'
               '<circle cx="2" cy="0" r="3.4" fill="#9aa0a6"/></g>')

    # spools of thread
    for cx, col in ((156, c['accent']), (252, c['light']), (348, c['dark'])):
        out.append('<g transform="translate(%d,760) scale(1.3)">'
                   '<rect x="-28" y="-98" width="56" height="15" rx="6" fill="#8a6a45"/>'
                   '<rect x="-28" y="-12" width="56" height="15" rx="6" fill="#8a6a45"/>'
                   '<rect x="-22" y="-86" width="44" height="76" fill="%s"/>'
                   '<path d="M-22,-74 L22,-66 M-22,-52 L22,-44 M-22,-30 L22,-22" '
                   'stroke="#000" stroke-width="2.4" opacity=".20"/>'
                   '<path d="M-22,-86 L-22,-10 M22,-86 L22,-10" stroke="#000" '
                   'stroke-width="2" opacity=".18"/>'
                   '<path d="M20,-24 C64,-12 74,20 42,36" fill="none" stroke="%s" '
                   'stroke-width="4.5" stroke-linecap="round"/></g>' % (cx, col, col))

    # tailor's chalk and pins
    out.append('<path d="M540,822 L598,800 L620,842 L562,864 Z" fill="#f4f4ef" '
               'stroke="#c9c9c2" stroke-width="2.4"/>')
    out.append('<path d="M540,822 L598,800" stroke="#d8d8d0" stroke-width="3"/>')
    for px, py, rot in ((652, 720, 18), (686, 762, -6), (630, 784, 34)):
        out.append('<g transform="rotate(%d %d %d)">'
                   '<path d="M%d,%d L%d,%d" stroke="#9aa0a6" stroke-width="3.4" '
                   'stroke-linecap="round"/>'
                   '<circle cx="%d" cy="%d" r="7.5" fill="%s"/>'
                   '<circle cx="%d" cy="%d" r="2.6" fill="#fff" opacity=".5"/></g>'
                   % (rot, px, py, px + 6, py + 3, px + 46, py + 26,
                      px, py, c['accent'], px - 2, py - 2))
    return ''.join(out), ''


def g_atelier(c):
    """A finished jacket on the stand with a tape measure over the shoulder."""
    body, hd = g_suit(c)
    tape = ('<path d="M330,300 C300,420 330,560 352,650 M470,300 C500,420 470,560 '
            '448,650" fill="none" stroke="#e8b53a" stroke-width="20" '
            'stroke-linecap="round"/>'
            '<path d="M330,300 C300,420 330,560 352,650 M470,300 C500,420 470,560 '
            '448,650" fill="none" stroke="#4a3312" stroke-width="18" '
            'stroke-dasharray="2 22" opacity=".75"/>')
    return body + tape, hd


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


# ------------------------------------------------------------------ build ---


def build(item):
    c = PALETTE[item['color']]
    kind = item['pattern']
    second = None
    if item.get('color2'):
        second = (PALETTE[item['color2']], item.get('pattern2', 'lattice'))

    g = item['garment']
    if g == 'kurta':
        body, hd = g_kurta(c)
    elif g == 'kurta_jacket':
        body, hd = g_kurta_jacket(c, second[0], second[1])
    elif g == 'sherwani':
        body, hd = g_sherwani(c)
    elif g == 'jodhpuri':
        body, hd = g_jodhpuri(c)
    elif g == 'indowestern':
        body, hd = g_indowestern(c, second[0], second[1])
    elif g == 'suit':
        body, hd = g_suit(c)
    elif g == 'shirt':
        body, hd = g_shirt(c, item.get('trouser', 'charcoal'))
    elif g == 'atelier':
        body, hd = g_atelier(c)
    elif g == 'bolt':
        body, hd = g_bolt(c)
    elif g == 'tools':
        body, hd = g_tools(c)
    else:
        raise SystemExit('unknown garment %s' % g)

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
             'width="%d" height="%d" role="img" aria-label="%s">'
             % (W, H, W, H, esc(item['title']))]
    parts.append('<title>%s</title>' % esc(item['title']))
    span = (110, 700) if g in ('bolt', 'tools') else (252, 552)
    parts.append(defs(c, kind, second, PALETTE[item['bg']] if item.get('bg') else None, span))
    if g in ('bolt', 'tools'):
        parts.append(body)
    elif item.get('kid'):
        # shrink the body about the shoulder line and drop it so the feet still
        # meet the floor, then set a proportionally larger head on top of it
        parts.append(backdrop())
        parts.append('<g transform="translate(400,455) scale(1.06) '
                     'translate(-400,-296)">%s</g>' % head())
        parts.append('<g transform="translate(400,455) scale(0.86,0.78) '
                     'translate(-400,-300)">%s%s%s</g>' % (body, hd, shoes()))
    else:
        parts.append(backdrop())
        parts.append(head())
        parts.append(body)
        parts.append(hd)
        parts.append(shoes())
    parts.append('</svg>')
    return ''.join(parts)


# -------------------------------------------------------------- catalogue ---

SECTIONS = [
    {
        'group': 'men',
        'id': 'suiting',
        'name': 'Suiting',
        'kicker': 'Cloth & Two-Piece',
        'blurb': 'All-season wools, wool blends and travel-friendly weaves — seen as '
                 'lengths on the counter and as finished two-piece suits.',
    },
    {
        'group': 'men',
        'id': 'shirting',
        'name': 'Shirting',
        'kicker': 'Cloth & Stitched',
        'blurb': 'Poplins, dobbies, twills and soft checks, cut to your collar, cuff '
                 'and shoulder rather than to a size label.',
    },
    {
        'group': 'men',
        'id': 'sherwani',
        'name': 'Wedding Designer Sherwani',
        'kicker': 'Occasion',
        'blurb': 'Full-length ceremonial sherwanis with hand-guided threadwork, '
                 'zari plackets and matched inner kurta and churidar.',
    },
    {
        'group': 'men',
        'id': 'indo-western',
        'name': 'Indo-Western',
        'kicker': 'Occasion',
        'blurb': 'Draped and asymmetric silhouettes — cowls, capes and angled hems '
                 'layered over a clean tunic base.',
    },
    {
        'group': 'men',
        'id': 'kurta-jacket',
        'name': 'Kurta Jacket Set',
        'kicker': 'Festive',
        'blurb': 'Kurta, churidar and a Nehru jacket, worked as a set so the jacket '
                 'motif and the kurta ground read together.',
    },
    {
        'group': 'men',
        'id': 'jodhpuri',
        'name': 'Jodhpuri',
        'kicker': 'Formal',
        'blurb': 'The bandhgala — closed collar, clean chest, structured shoulder — '
                 'in self-textures and ceremonial weaves.',
    },
    {
        'group': 'men',
        'id': 'tailoring',
        'name': 'Customized Tailoring',
        'kicker': 'Made to Measure',
        'blurb': 'Everything above can be cut to your own measurements: your cloth or '
                 'ours, your collar, your length, your finish.',
    },
    {
        'group': 'kids',
        'id': 'kids',
        'name': 'Kids',
        'kicker': 'Little Occasion',
        'blurb': 'Sherwanis, kurta sets and bandhgalas cut small \u2014 the same cloth '
                 'and the same finish as the grown-up rail, sized for the ring bearer.',
    },
]


def I(sec, title, garment, color, pattern, fabric, detail, tags,
      color2=None, pattern2=None, bg=None, trouser=None, also=(), kid=False):
    d = {
        'id': '%s-%s' % (sec, title.lower().replace(' ', '-').replace('&', 'and')
                         .replace('--', '-')),
        'section': sec, 'title': title, 'garment': garment, 'color': color,
        'pattern': pattern, 'fabric': fabric, 'detail': detail,
        'tags': list(tags), 'also': list(also),
    }
    if color2:
        d['color2'] = color2
        d['pattern2'] = pattern2 or 'lattice'
    if bg:
        d['bg'] = bg
    if trouser:
        d['trouser'] = trouser
    if kid:
        d['kid'] = True
    return d


ITEMS = [
    # ------------------------------------------------------------- suiting --
    I('suiting', 'Charcoal Herringbone Length', 'bolt', 'charcoal', 'herringbone',
      'All-season wool blend', 'Classic herringbone that reads plain from a distance.',
      ['Formal', 'Office', 'Cloth'], also=['grey', 'black']),
    I('suiting', 'Midnight Navy Pinstripe', 'bolt', 'navy', 'pinstripe',
      'Fine worsted blend', 'Chalk-fine stripe on a deep navy ground.',
      ['Formal', 'Cloth'], also=['navy', 'indigo', 'charcoal']),
    I('suiting', 'Slate Windowpane Length', 'bolt', 'grey', 'windowpane',
      'Wool-rich suiting', 'Wide windowpane for a relaxed business look.',
      ['Office', 'Cloth'], also=['grey', 'beige']),
    I('suiting', 'Ink Black Twill', 'bolt', 'black', 'twill',
      'Matte twill weave', 'Deep, even black with a dry finish.',
      ['Formal', 'Evening', 'Cloth'], also=['black', 'charcoal']),
    I('suiting', 'Bottle Green Glen Check Suit', 'suit', 'bottle', 'glencheck',
      'Wool blend, half-canvas', 'Notch lapel, two-button front, side vents.',
      ['Reception', 'Two-Piece'], also=['bottle', 'olive']),
    I('suiting', 'Royal Blue Two-Piece', 'suit', 'royal', 'plain',
      'Smooth worsted finish', 'Clean-front jacket with a soft shoulder.',
      ['Reception', 'Two-Piece'], also=['royal', 'navy', 'powder']),
    I('suiting', 'Beige Summer Two-Piece', 'suit', 'beige', 'twill',
      'Light open weave', 'Unlined body for warm-weather day functions.',
      ['Daytime', 'Two-Piece'], also=['beige', 'cream']),
    I('suiting', 'Charcoal Formal Suit', 'suit', 'charcoal', 'pinstripe',
      'Worsted blend', 'Structured chest, full-canvas front, working cuffs.',
      ['Formal', 'Two-Piece'], also=['charcoal', 'black', 'grey']),

    # ------------------------------------------------------------ shirting --
    I('shirting', 'Pure White Poplin', 'bolt', 'white', 'plain',
      '2-ply cotton poplin', 'The one length that goes with everything above.',
      ['Formal', 'Cloth'], also=['white', 'ivory']),
    I('shirting', 'Sky Blue Dobby', 'bolt', 'skyblue', 'dobby',
      'Cotton dobby', 'Self-textured dot that catches light at the collar.',
      ['Office', 'Cloth'], also=['skyblue', 'powder']),
    I('shirting', 'Powder Blue Fine Stripe', 'shirt', 'powder', 'pinstripe',
      'Cotton shirting', 'Cutaway collar, single-button barrel cuff.',
      ['Office', 'Stitched'], also=['powder', 'skyblue'], trouser='charcoal'),
    I('shirting', 'Ivory Textured Weave', 'shirt', 'ivory', 'dobby',
      'Cotton-linen mix', 'Soft-roll collar with a lightly fused placket.',
      ['Daytime', 'Stitched'], also=['ivory', 'cream'], trouser='beige'),
    I('shirting', 'Lilac Micro Check', 'bolt', 'lilac', 'check',
      'Yarn-dyed cotton', 'Small check that stays quiet under a jacket.',
      ['Office', 'Cloth'], also=['lilac', 'lavender']),
    I('shirting', 'Sage Cotton Check', 'shirt', 'sage', 'check',
      'Yarn-dyed cotton', 'Button-down collar, patch chest pocket.',
      ['Casual', 'Stitched'], also=['sage', 'olive'], trouser='beige'),
    I('shirting', 'Charcoal Twill Shirt', 'shirt', 'charcoal', 'twill',
      'Brushed cotton twill', 'Hidden placket and a slightly longer point collar.',
      ['Evening', 'Stitched'], also=['charcoal', 'black'], trouser='black'),
    I('shirting', 'Cream Linen-Look Shirt', 'shirt', 'cream', 'plain',
      'Linen-blend shirting', 'Relaxed body, mother-of-pearl style buttons.',
      ['Daytime', 'Stitched'], also=['cream', 'beige'], trouser='beige'),

    # ------------------------------------------------------------ sherwani --
    I('sherwani', 'Ivory Zardozi Sherwani', 'sherwani', 'ivory', 'scroll',
      'Raw-silk look base', 'Scrolling threadwork over the chest and full placket.',
      ['Wedding', 'Groom'], also=['ivory', 'cream', 'gold']),
    I('sherwani', 'Gold Brocade Sherwani', 'sherwani', 'gold', 'brocade',
      'Brocade weave', 'All-over brocade with a plain contrast churidar.',
      ['Wedding', 'Groom'], also=['gold', 'mustard']),
    I('sherwani', 'Maroon Jaal Sherwani', 'sherwani', 'maroon', 'lattice',
      'Silk-blend base', 'Jaal lattice ground with a zari hem border.',
      ['Wedding', 'Reception'], also=['maroon', 'wine']),
    I('sherwani', 'Bottle Green Threadwork', 'sherwani', 'bottle', 'scroll',
      'Silk-blend base', 'Tonal threadwork with an antique-gold placket.',
      ['Wedding', 'Groom'], also=['bottle', 'emerald']),
    I('sherwani', 'Wine Paisley Sherwani', 'sherwani', 'wine', 'paisley',
      'Textured silk look', 'Paisley buta placed across the body and sleeve.',
      ['Reception', 'Sangeet'], also=['wine', 'maroon']),
    I('sherwani', 'Cream Floral Sherwani', 'sherwani', 'cream', 'floral',
      'Matte silk look', 'Soft floral vine, ideal for a daytime ceremony.',
      ['Wedding', 'Daytime'], also=['cream', 'ivory', 'peach']),
    I('sherwani', 'Navy Zari Sherwani', 'sherwani', 'navy', 'zari',
      'Silk-blend base', 'Fine zari striping with a high mandarin collar.',
      ['Reception', 'Evening'], also=['navy', 'indigo']),
    I('sherwani', 'Rose Gold Buti Sherwani', 'sherwani', 'peach', 'buti',
      'Tissue-look blend', 'Scattered buti motif with a tonal hem band.',
      ['Wedding', 'Daytime'], also=['peach', 'rose', 'gold']),

    # -------------------------------------------------------- indo-western --
    I('indo-western', 'Emerald Cape Indo-Western', 'indowestern', 'cream', 'plain',
      'Silk-blend drape', 'Cape-cut overlay pinned at the shoulder.',
      ['Sangeet', 'Cocktail'], color2='emerald', pattern2='scroll', bg='emerald',
      also=['emerald', 'bottle']),
    I('indo-western', 'Ink Black Asymmetric', 'indowestern', 'black', 'plain',
      'Matte blend', 'Angled hem with a tonal trim along the fall.',
      ['Cocktail', 'Evening'], color2='charcoal', pattern2='lattice', bg='charcoal',
      also=['black', 'charcoal']),
    I('indo-western', 'Wine Drape Indo-Western', 'indowestern', 'ivory', 'plain',
      'Silk-blend drape', 'Floral drape over an ivory tunic base.',
      ['Sangeet', 'Reception'], color2='wine', pattern2='floral', bg='wine',
      also=['wine', 'maroon']),
    I('indo-western', 'Teal Layered Indo-Western', 'indowestern', 'cream', 'plain',
      'Brocade overlay', 'Long brocade panel layered to one side.',
      ['Cocktail', 'Reception'], color2='teal', pattern2='brocade', bg='teal',
      also=['teal', 'powder']),
    I('indo-western', 'Copper Cowl Indo-Western', 'indowestern', 'beige', 'plain',
      'Textured blend', 'Chevron-worked cowl drape with a soft fall.',
      ['Sangeet', 'Cocktail'], color2='copper', pattern2='chevron', bg='copper',
      also=['copper', 'rust']),
    I('indo-western', 'Indigo Angled Indo-Western', 'indowestern', 'ivory', 'plain',
      'Silk-blend drape', 'Buti-worked overlay with a sharp diagonal hem.',
      ['Cocktail', 'Evening'], color2='indigo', pattern2='buti', bg='indigo',
      also=['indigo', 'navy']),
    I('indo-western', 'Sage Overlay Indo-Western', 'indowestern', 'cream', 'plain',
      'Matte silk look', 'Paisley overlay in a muted sage for daytime.',
      ['Daytime', 'Mehendi'], color2='sage', pattern2='paisley', bg='sage',
      also=['sage', 'olive']),
    I('indo-western', 'Rust Panelled Indo-Western', 'indowestern', 'ivory', 'plain',
      'Silk-blend drape', 'Panelled front with a jaal-worked overlay.',
      ['Mehendi', 'Sangeet'], color2='rust', pattern2='lattice', bg='rust',
      also=['rust', 'copper']),

    # -------------------------------------------------------- kurta-jacket --
    I('kurta-jacket', 'Emerald Sparkle Set', 'kurta_jacket', 'emerald', 'plain',
      'Silk-blend kurta', 'Plain emerald kurta under a lattice-worked jacket.',
      ['Festive', 'Set'], color2='gold', pattern2='lattice', also=['emerald', 'gold']),
    I('kurta-jacket', 'Radiant Mustard Set', 'kurta_jacket', 'mustard', 'floral',
      'Printed kurta', 'Floral kurta matched to a tonal jacket.',
      ['Festive', 'Haldi'], color2='mustard', pattern2='lattice',
      also=['mustard', 'gold', 'rust']),
    I('kurta-jacket', 'Beige Patchwork Set', 'kurta_jacket', 'beige', 'plain',
      'Cotton-silk kurta', 'Patch-effect jacket over a plain beige kurta.',
      ['Daytime', 'Set'], color2='cream', pattern2='lattice', also=['beige', 'cream']),
    I('kurta-jacket', 'Sage Jaal Set', 'kurta_jacket', 'sage', 'plain',
      'Silk-blend kurta', 'Jaal-worked jacket in a deeper olive.',
      ['Mehendi', 'Festive'], color2='olive', pattern2='lattice', also=['sage', 'olive']),
    I('kurta-jacket', 'Ivory Motif Set', 'kurta_jacket', 'ivory', 'plain',
      'Matte silk look', 'Buti-worked jacket with a fine tonal border.',
      ['Wedding', 'Daytime'], color2='cream', pattern2='buti', also=['ivory', 'cream']),
    I('kurta-jacket', 'Navy Brocade Set', 'kurta_jacket', 'navy', 'plain',
      'Silk-blend kurta', 'Brocade jacket, plain navy kurta and churidar.',
      ['Evening', 'Festive'], color2='navy', pattern2='brocade', also=['navy', 'indigo']),
    I('kurta-jacket', 'Maroon Paisley Set', 'kurta_jacket', 'maroon', 'plain',
      'Silk-blend kurta', 'Paisley jacket worked in matching thread.',
      ['Festive', 'Sangeet'], color2='maroon', pattern2='paisley', also=['maroon', 'wine']),
    I('kurta-jacket', 'Powder Bandhani Set', 'kurta_jacket', 'powder', 'plain',
      'Cotton-silk kurta', 'Bandhani-effect jacket over a powder blue kurta.',
      ['Daytime', 'Festive'], color2='royal', pattern2='bandhani',
      also=['powder', 'royal', 'skyblue']),

    # ------------------------------------------------------------ jodhpuri --
    I('jodhpuri', 'Black Bandhgala', 'jodhpuri', 'black', 'plain',
      'Matte wool blend', 'Closed collar, five-button front, matching trouser.',
      ['Formal', 'Evening'], also=['black', 'charcoal']),
    I('jodhpuri', 'Ink Navy Bandhgala', 'jodhpuri', 'navy', 'twill',
      'Twill wool blend', 'Self-twill ground with a lightly padded shoulder.',
      ['Formal', 'Reception'], also=['navy', 'indigo']),
    I('jodhpuri', 'Bottle Green Jodhpuri', 'jodhpuri', 'bottle', 'brocade',
      'Brocade weave', 'Ceremonial brocade with a plain collar band.',
      ['Wedding', 'Reception'], also=['bottle', 'emerald']),
    I('jodhpuri', 'Wine Textured Jodhpuri', 'jodhpuri', 'wine', 'scroll',
      'Textured silk look', 'Tonal threadwork across the chest and collar.',
      ['Reception', 'Evening'], also=['wine', 'maroon']),
    I('jodhpuri', 'Charcoal Self-Check Jodhpuri', 'jodhpuri', 'charcoal', 'glencheck',
      'Wool blend', 'Quiet self-check for formal daytime wear.',
      ['Office', 'Formal'], also=['charcoal', 'grey']),
    I('jodhpuri', 'Ivory Ceremonial Jodhpuri', 'jodhpuri', 'ivory', 'buti',
      'Raw-silk look', 'Scattered buti with a contrast collar brooch.',
      ['Wedding', 'Daytime'], also=['ivory', 'cream']),
    I('jodhpuri', 'Maroon Zari Jodhpuri', 'jodhpuri', 'maroon', 'zari',
      'Silk-blend base', 'Fine zari striping, ceremonial finish.',
      ['Wedding', 'Evening'], also=['maroon', 'wine']),
    I('jodhpuri', 'Teal Jaal Jodhpuri', 'jodhpuri', 'teal', 'lattice',
      'Silk-blend base', 'Jaal lattice ground with a tonal button set.',
      ['Reception', 'Sangeet'], also=['teal', 'powder']),

    # ---------------------------------------------------------------- kids --
    I('kids', 'Ivory Kurta Jacket Set', 'kurta_jacket', 'ivory', 'plain',
      'Cotton-silk kurta', 'Lattice-worked jacket over a plain ivory kurta.',
      ['Wedding', 'Festive'], color2='gold', pattern2='lattice', kid=True,
      also=['ivory', 'gold']),
    I('kids', 'Royal Blue Jodhpuri', 'jodhpuri', 'royal', 'plain',
      'Soft wool blend', 'A proper bandhgala with a closed collar and five buttons.',
      ['Wedding', 'Formal'], kid=True, also=['royal', 'navy']),
    I('kids', 'Maroon Brocade Sherwani', 'sherwani', 'maroon', 'brocade',
      'Brocade weave', 'Full-length sherwani with a zari placket and hem band.',
      ['Wedding', 'Groom'], kid=True, also=['maroon', 'wine']),
    I('kids', 'Mustard Floral Kurta', 'kurta', 'mustard', 'floral',
      'Printed cotton-silk', 'Light printed kurta and churidar for a daytime function.',
      ['Haldi', 'Daytime'], kid=True, also=['mustard', 'gold']),
    I('kids', 'Bottle Green Jacket Set', 'kurta_jacket', 'bottle', 'plain',
      'Silk-blend kurta', 'Buti-worked jacket over a deep green kurta.',
      ['Festive', 'Evening'], color2='gold', pattern2='buti', kid=True,
      also=['bottle', 'gold']),
    I('kids', 'Peach Indo-Western', 'indowestern', 'cream', 'plain',
      'Silk-blend drape', 'A small draped overlay with an angled hem.',
      ['Sangeet', 'Daytime'], color2='peach', pattern2='floral', bg='peach', kid=True,
      also=['peach', 'rose']),
    I('kids', 'Navy Bandhgala', 'jodhpuri', 'navy', 'twill',
      'Twill wool blend', 'Self-twill bandhgala with matching trousers.',
      ['Formal', 'Reception'], kid=True, also=['navy', 'indigo']),
    I('kids', 'Cream Threadwork Sherwani', 'sherwani', 'cream', 'scroll',
      'Matte silk look', 'Tonal threadwork, cut short and easy to move in.',
      ['Wedding', 'Daytime'], kid=True, also=['cream', 'ivory']),

    # ----------------------------------------------------------- tailoring --
    I('tailoring', 'Measure & Fit', 'tools', 'beige', 'plain',
      'Your measurements', 'Sixteen measurements taken by hand, kept on file for '
      'every future order.', ['Made to Measure']),
    I('tailoring', 'The Cutting Table', 'tools', 'teal', 'twill',
      'Cut in house', 'Every length is chalked and cut on our own table, never '
      'sub-contracted.', ['Made to Measure']),
    I('tailoring', 'Canvas & Construction', 'atelier', 'charcoal', 'herringbone',
      'Half and full canvas', 'Choose the internal construction that suits how you '
      'wear the jacket.', ['Suiting', 'Made to Measure']),
    I('tailoring', 'Bespoke Suit Trial', 'atelier', 'navy', 'pinstripe',
      'Two fittings included', 'A basted trial before finishing, so the shoulder and '
      'the sleeve pitch are yours.', ['Suiting', 'Made to Measure']),
    I('tailoring', 'Hand-Finished Details', 'tools', 'maroon', 'scroll',
      'Hand finishing', 'Buttonholes, hems and linings finished by hand where it '
      'shows and where it matters.', ['Made to Measure']),
    I('tailoring', 'Made-to-Measure Sherwani', 'sherwani', 'ivory', 'brocade',
      'Your cloth or ours', 'Wedding wear cut to your own length, collar height and '
      'placket.', ['Wedding', 'Made to Measure'], also=['ivory', 'cream', 'gold']),
]


# ------------------------------------------------------------ decorative ---

def arch(x, y, w, h):
    hw = w / 2.0
    return ('M%s,%s L%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s L%s,%s Z'
            % (x, y + h, x, y + h * 0.42,
               x, y + h * 0.14, x + hw * 0.55, y + h * 0.10, x + hw, y,
               x + w - hw * 0.55, y + h * 0.10, x + w, y + h * 0.14, x + w, y + h * 0.42,
               x + w, y + h))


def make_hero():
    cs = [PALETTE['maroon'], PALETTE['ivory'], PALETTE['bottle']]
    kinds = ['paisley', 'lattice', 'scroll']
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" '
         'height="900" role="img" aria-label="Deep Sons atelier">']
    p.append('<defs>')
    for i, (c, k) in enumerate(zip(cs, kinds)):
        p.append(pattern_def('h%d' % i, k, c))
    p.append(pattern_def('hbg', 'lattice', PALETTE['beige']))
    p.append('<linearGradient id="hg" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#241a12"/>'
             '<stop offset="1" stop-color="#120c08"/></linearGradient>')
    p.append('<linearGradient id="hfade" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#000" stop-opacity="0"/>'
             '<stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient>')
    p.append('</defs>')
    p.append('<rect width="1600" height="900" fill="url(#hg)"/>')
    p.append('<rect width="1600" height="900" fill="url(#hbg)" opacity=".12"/>')
    for i in range(3):
        x = 190 + i * 420
        d = arch(x, 150, 340, 640)
        p.append('<path d="%s" fill="url(#h%d)"/>' % (d, i))
        p.append('<path d="%s" fill="url(#hfade)"/>' % d)
        p.append('<path d="%s" fill="none" stroke="#c9a227" stroke-width="4" '
                 'opacity=".85"/>' % d)
        inner = arch(x + 26, 178, 288, 584)
        p.append('<path d="%s" fill="none" stroke="#c9a227" stroke-width="1.6" '
                 'opacity=".45"/>' % inner)
    p.append('<path d="M120,96 L1480,96 M120,836 L1480,836" stroke="#c9a227" '
             'stroke-width="2" opacity=".55"/>')
    for x in range(140, 1481, 40):
        p.append('<circle cx="%d" cy="96" r="3" fill="#c9a227" opacity=".5"/>'
                 '<circle cx="%d" cy="836" r="3" fill="#c9a227" opacity=".5"/>' % (x, x))
    p.append('</svg>')
    return ''.join(p)


def make_logo():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" '
            'height="120" role="img" aria-label="Deep Sons"><defs>'
            '<linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#e0bd63"/>'
            '<stop offset="1" stop-color="#a97f26"/></linearGradient></defs>'
            '<path d="%s" fill="none" stroke="url(#lg)" stroke-width="5"/>'
            '<path d="%s" fill="none" stroke="url(#lg)" stroke-width="2" opacity=".6"/>'
            '<text x="60" y="76" text-anchor="middle" font-family="Georgia,serif" '
            'font-size="40" font-weight="700" fill="url(#lg)">DS</text>'
            '<path d="M60,88 C46,94 44,104 52,108" fill="none" stroke="url(#lg)" '
            'stroke-width="2.4"/>'
            '<circle cx="52" cy="108" r="2.6" fill="url(#lg)"/></svg>'
            % (arch(14, 10, 92, 100), arch(23, 20, 74, 82)))


def make_tile():
    """A transparent jaal tile used as a whisper-quiet page texture."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" width="60" '
            'height="60"><g fill="none" stroke="#a9802a" stroke-width="1.1" '
            'opacity=".16"><path d="M30,2 L58,30 L30,58 L2,30 Z"/>'
            '<path d="M30,16 L44,30 L30,44 L16,30 Z"/></g>'
            '<g fill="#a9802a" opacity=".2"><circle cx="30" cy="30" r="1.8"/>'
            '<circle cx="0" cy="0" r="1.4"/><circle cx="60" cy="0" r="1.4"/>'
            '<circle cx="0" cy="60" r="1.4"/><circle cx="60" cy="60" r="1.4"/>'
            '</g></svg>')


def make_favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" '
            'height="64"><rect width="64" height="64" rx="12" fill="#2b1a12"/>'
            '<text x="32" y="44" text-anchor="middle" font-family="Georgia,serif" '
            'font-size="30" font-weight="700" fill="#d9b45a">DS</text></svg>')


# ----------------------------------------------------------------- main ----

def main():
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(JS, exist_ok=True)

    seen = set()
    out_items = []
    for it in ITEMS:
        if it['id'] in seen:
            raise SystemExit('duplicate id %s' % it['id'])
        seen.add(it['id'])
        svg = build(it)
        with open(os.path.join(IMG, it['id'] + '.svg'), 'w') as f:
            f.write(svg)
        colours = [it['color']] + [a for a in it['also'] if a != it['color']]
        if it.get('color2') and it['color2'] not in colours:
            colours.append(it['color2'])
        out_items.append({
            'id': it['id'],
            'section': it['section'],
            'title': it['title'],
            'img': 'assets/img/%s.svg' % it['id'],
            'fabric': it['fabric'],
            'weave': PATTERN_LABEL.get(it['pattern'], ''),
            'detail': it['detail'],
            'tags': it['tags'],
            'colours': colours[:4],
            'kid': bool(it.get('kid')),
        })

    for name, maker in (('hero', make_hero), ('logo', make_logo),
                        ('tile', make_tile), ('favicon', make_favicon)):
        with open(os.path.join(IMG, name + '.svg'), 'w') as f:
            f.write(maker())

    swatches = {k: {'label': v['label'], 'base': v['base'], 'dark': v['dark'],
                    'light': v['light']} for k, v in PALETTE.items()}
    payload = {'sections': SECTIONS, 'items': out_items, 'colours': swatches}
    with open(os.path.join(JS, 'catalogue.js'), 'w') as f:
        f.write('/* Generated by tools/generate_art.py - do not edit by hand. */\n')
        f.write('window.DS = ')
        f.write(json.dumps(payload, indent=2))
        f.write(';\n')

    print('wrote %d product images + 4 brand assets' % len(out_items))
    for s in SECTIONS:
        n = sum(1 for i in out_items if i['section'] == s['id'])
        print('  %-14s %d' % (s['id'], n))


if __name__ == '__main__':
    main()
