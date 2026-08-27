#!/usr/bin/env python3
"""Fold the three-page Deep Sons site into one self-contained HTML file.

The multi-page site under deep-sons/ stays the source of truth; this script
rewrites it as a single page with hash routing and every stylesheet, script and
SVG carried inline, so it can be published or e-mailed as one file.

Run:  python3 tools/build_artifact.py
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
DIST = os.path.join(ROOT, 'dist')


def datauri(relpath):
    """Inline one asset: SVG as percent-encoded text, raster as base64."""
    import base64
    from urllib.parse import quote
    full = os.path.join(ROOT, relpath)
    ext = os.path.splitext(relpath)[1].lower()
    if ext == '.svg':
        with open(full, encoding='utf-8') as f:
            return 'data:image/svg+xml,' + quote(f.read(), safe="!'()*-._~")
    mime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.webp': 'image/webp'}[ext]
    with open(full, 'rb') as f:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(f.read()).decode())


def inline_assets(text):
    """Swap every assets/img/... reference in the document for a data URI, so
    adding an image to a page never needs a matching edit here."""
    seen = {}

    def sub(m):
        rel = m.group(0)
        if rel not in seen:
            seen[rel] = datauri(rel)
        return seen[rel]

    return re.sub(r'assets/img/[A-Za-z0-9._/-]+\.(?:svg|png|jpe?g|webp)', sub, text)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding='utf-8') as f:
        return f.read()


def body_of(page):
    """The markup between the shared header and the shared footer."""
    html = read(page)
    mid = html.split('</header>', 1)[1].split('<footer', 1)[0]
    return mid.strip()


def relink(html):
    """Turn file-based navigation into hash routes."""
    html = html.replace('collection.html?c=', '#c=')
    html = html.replace('href="visit.html"', 'href="#about"')
    html = html.replace('href="about.html"', 'href="#about"')
    html = html.replace('href="men.html"', 'href="#men"')
    html = html.replace('href="lookbook.html"', 'href="#lookbook"')
    html = html.replace('href="index.html"', 'href="#"')
    return html


def sub1(text, old, new, what):
    """Replace and prove it happened. A silent no-op here ships a broken
    build, so every rewrite below is checked."""
    if old not in text:
        raise SystemExit('build_artifact: could not patch %s -- app.js has '
                         'changed under this script' % what)
    return text.replace(old, new)


def patch_app(js):
    """Rewrite app.js for a single page: hash routing and inline artwork."""

    # 1. the route is read off the hash, not the filename
    js = sub1(js, """  function currentRoute() {
    var file = (location.pathname.split('/').pop() || 'index.html');
    if (file === 'men.html') return 'men';
    if (file === 'about.html') return 'about';
    if (file === 'lookbook.html') return 'lookbook';
    if (file === 'collection.html') return 'c=' + (readQuery().get('c') || 'all');
    return '';
  }""", """  function currentRoute() {
    return location.hash.replace(/^#/, '');
  }""", 'route reader')

    # 2. every file path becomes a hash route
    js = js.replace('collection.html?c=', '#c=')
    js = js.replace('visit.html', '#about')
    js = js.replace('about.html', '#about')
    js = js.replace('men.html', '#men')
    js = js.replace('lookbook.html', '#lookbook')
    js = js.replace('index.html', '#')
    assert '.html' not in js, 'stray page link left in app.js'

    # 3. artwork comes from the inline map rather than a file path
    js = sub1(js, """  function artSrc(item) {
    return item.img;
  }""", """  var ART_CACHE = {};
  function artSrc(item) {
    if (!ART_CACHE[item.id]) {
      var raw = (window.DS_ART || {})[item.id];
      ART_CACHE[item.id] = raw ? 'data:image/svg+xml,' + encodeURIComponent(raw) : '';
    }
    return ART_CACHE[item.id];
  }""", 'artwork lookup')

    # 4. collection state lives in the hash, and is only ever written back
    #    onto a hash that is already a collection route -- otherwise the
    #    first render on the home page would navigate away from it
    js = sub1(js, """  function readQuery() {
    return new URLSearchParams(location.search);
  }""", """  function readQuery() {
    return new URLSearchParams(location.hash.replace(/^#/, ''));
  }""", 'query reader')
    js = sub1(js, """    try {
      var u = new URL(location.href);
      u.search = p.toString();
      history.replaceState(null, '', u);
    } catch (e) {""", """    if (location.hash.replace(/^#/, '').indexOf('c=') !== 0) return;
    try {
      history.replaceState(null, '', '#' + p.toString());
    } catch (e) {""", 'query writer')

    return js


ROUTER = """
/* ------------------------------------------------- single-page routing --
   Navigation is driven by the click, not by the hash. The hash is still
   updated so deep links and the back button work, but nothing depends on
   it: in a sandboxed frame the History API can be unavailable, and the
   site has to keep working there.                                        */
(function () {
  'use strict';
  var TITLES = {
    home: 'Deep Sons \\u2014 Suiting, Shirting & Wedding Wear',
    men: 'Men \\u2014 Deep Sons',
    lookbook: 'Lookbook \\u2014 Deep Sons',
    about: 'About Us \\u2014 Deep Sons'
  };

  function pages() {
    var out = {};
    [].forEach.call(document.querySelectorAll('[data-page]'), function (n) {
      out[n.getAttribute('data-page')] = n;
    });
    return out;
  }

  function dismissOverlays() {
    var drawer = document.querySelector('.drawer');
    if (drawer) { drawer.classList.remove('is-on'); drawer.setAttribute('aria-hidden', 'true'); }
    var sheet = document.querySelector('.sheet');
    if (sheet) { sheet.classList.remove('is-on'); sheet.setAttribute('aria-hidden', 'true'); }
    var lb = document.querySelector('.lb');
    if (lb) lb.classList.remove('is-on');
    [].forEach.call(document.querySelectorAll('.scrim'), function (s) { s.classList.remove('is-on'); });
    document.body.classList.remove('is-locked');
  }

  function apply(route) {
    var map = pages();
    var name = route.indexOf('c=') === 0 ? 'coll' : (map[route] ? route : 'home');
    dismissOverlays();
    for (var k in map) map[k].hidden = k !== name;
    document.body.classList.toggle('has-bar', name === 'coll');
    if (name === 'coll') {
      var root = document.querySelector('[data-collection]');
      if (root && root.__applyRoute) root.__applyRoute(new URLSearchParams(route));
    } else {
      document.title = TITLES[name] || TITLES.home;
    }
    if (window.DS_MARK_NAV) window.DS_MARK_NAV(route);
    window.scrollTo(0, 0);
  }

  function go(route) {
    apply(route);
    // best effort: keeps the address bar honest where it is allowed
    try {
      if (location.hash.replace(/^#/, '') !== route) location.hash = route;
    } catch (e) { /* sandboxed frame */ }
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a || a.hasAttribute('data-open')) return;
    e.preventDefault();
    go(a.getAttribute('href').slice(1));
  });

  window.addEventListener('hashchange', function () {
    apply(location.hash.replace(/^#/, ''));
  });

  function start() {
    var h = '';
    try { h = location.hash.replace(/^#/, ''); } catch (e) { /* sandboxed frame */ }
    apply(h);
  }

  // app.js boots on DOMContentLoaded; route after it so the title it sets for
  // a collection is not overwritten by the one this router sets for home.
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
"""


def main():
    os.makedirs(DIST, exist_ok=True)

    css = read('assets', 'css', 'style.css')

    cat = read('assets', 'js', 'catalogue.js')
    data = json.loads(cat.split('window.DS = ', 1)[1].rstrip().rstrip(';'))

    art = {}
    for item in data['items']:
        art[item['id']] = read(*item['img'].split('/'))
        del item['img']

    app = patch_app(read('assets', 'js', 'app.js'))
    about_js = read('about.html').split('<script>', 2)[-1].split('</script>')[0]

    pages = [
        ('home', relink(body_of('index.html'))),
        ('men', relink(body_of('men.html'))),
        ('lookbook', relink(body_of('lookbook.html'))),
        ('coll', relink(body_of('collection.html'))),
        ('about', relink(body_of('about.html'))),
    ]
    body = ['<div data-page="%s"%s>%s</div>' % (n, '' if n == 'home' else ' hidden', m)
            for n, m in pages]

    out = []
    out.append('<title>Deep Sons</title>')
    out.append('<meta name="description" content="Look book for Deep Sons: suiting, '
               'shirting, wedding designer sherwani, indo-western, kurta jacket sets, '
               'jodhpuri and customized tailoring.">')
    out.append('<style>\n%s\n</style>' % css.replace('../img/', 'assets/img/'))
    out.append('<header class="head" data-header></header>')
    out.extend(body)
    out.append('<footer class="foot" data-footer></footer>')
    out.append('<script>window.DS = %s;</script>' % json.dumps(data, separators=(',', ':')))
    out.append('<script>window.DS_ART = %s;</script>' % json.dumps(art, separators=(',', ':')))
    out.append('<script>\n%s\n</script>' % app)
    out.append('<script>%s</script>' % about_js)
    out.append('<script>%s</script>' % ROUTER)

    html = inline_assets('\n'.join(out))
    left = re.findall(r'assets/img/[A-Za-z0-9._/-]+', html)
    assert not left, 'un-inlined asset reference: %s' % sorted(set(left))
    path = os.path.join(DIST, 'deep-sons.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote %s  (%.0f KB, %d artworks inlined)' % (path, len(html.encode()) / 1024, len(art)))


if __name__ == '__main__':
    main()
