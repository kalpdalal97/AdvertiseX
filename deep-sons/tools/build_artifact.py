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
    """Inline one asset. SVG goes in as percent-encoded text (smaller and
    diff-able); raster formats go in as base64."""
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
    """Swap every assets/img/... reference in the document for a data URI."""
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
    html = html.replace('href="visit.html"', 'href="#visit"')
    html = html.replace('href="index.html"', 'href="#"')
    return html


def patch_app(js):
    """Rewrite app.js for a single page: hash routing and inline artwork."""

    # 1. the header no longer has a filename to mark the current page by
    #    (do these before the blanket path rewrite below)
    before = js
    js = js.replace("var here = (location.pathname.split('/').pop() || 'index.html');",
                    "var here = location.hash.replace(/^#/, '');")
    js = js.replace("(here === 'visit.html' ? ' aria-current=\"page\"' : '')",
                    "(here === 'visit' ? ' aria-current=\"page\"' : '')")
    assert js != before, 'header current-page patch did not apply'

    # 2. every remaining file path becomes a hash route
    js = js.replace('collection.html?c=', '#c=')
    js = js.replace('visit.html', '#visit')
    js = js.replace('index.html', '#')
    assert 'collection.html' not in js and '.html' not in js, 'stray page link left in app.js' 

    # 3. artwork comes from the inline map rather than a file path
    js = js.replace(
        "  function esc(s) {",
        "  var ART_CACHE = {};\n"
        "  function art(id) {\n"
        "    if (!ART_CACHE[id]) {\n"
        "      var raw = (window.DS_ART || {})[id];\n"
        "      ART_CACHE[id] = !raw ? '' : (raw.slice(0, 5) === 'data:' ? raw\n"
        "        : 'data:image/svg+xml,' + encodeURIComponent(raw));\n"
        "    }\n"
        "    return ART_CACHE[id];\n"
        "  }\n\n"
        "  function esc(s) {")
    js = js.replace("'<img src=\"' + item.img + '\"", "'<img src=\"' + art(item.id) + '\"")
    js = js.replace("lb.node.querySelector('[data-lb-img]').src = it.img;",
                    "lb.node.querySelector('[data-lb-img]').src = art(it.id);")
    js = js.replace("'<img src=\"' + cover.img + '\"", "'<img src=\"' + art(cover.id) + '\"")

    # 4. state is read from, and written back to, the hash
    js = js.replace("    var qs = new URLSearchParams(location.search);",
                    "    var qs = new URLSearchParams(location.hash.replace(/^#/, ''));")
    js = js.replace(
        """    function sync() {
      var u = new URL(location.href);
      u.searchParams.set('c', state.c);
      state.colour ? u.searchParams.set('colour', state.colour) : u.searchParams.delete('colour');
      state.tag ? u.searchParams.set('tag', state.tag) : u.searchParams.delete('tag');
      history.replaceState(null, '', u);
    }""",
        """    function sync() {
      // only ever rewrite a hash that is already a collection route, so the
      // initial render on the home page does not navigate away from it
      if (location.hash.replace(/^#/, '').indexOf('c=') !== 0) return;
      var p = new URLSearchParams();
      p.set('c', state.c);
      if (state.colour) p.set('colour', state.colour);
      if (state.tag) p.set('tag', state.tag);
      history.replaceState(null, '', '#' + p.toString());
    }""")

    # 5. let the router re-point the collection without rebuilding it
    js = js.replace(
        "    function render() { paintHead(); paintRail(); paintChips(); paintGrid(); paintBar(); sync(); }\n    render();",
        """    function render() { paintHead(); paintRail(); paintChips(); paintGrid(); paintBar(); sync(); }
    root.__applyHash = function () {
      var q = new URLSearchParams(location.hash.replace(/^#/, ''));
      state.c = q.get('c') || 'all';
      state.colour = q.get('colour') || '';
      state.tag = q.get('tag') || '';
      render();
    };
    render();""")

    return js


ROUTER = """
/* ------------------------------------------------- single-page routing -- */
(function () {
  'use strict';
  var HOME_TITLE = 'Deep Sons \\u2014 Suiting, Shirting & Wedding Wear';
  var pages = {};
  [].forEach.call(document.querySelectorAll('[data-page]'), function (n) {
    pages[n.getAttribute('data-page')] = n;
  });

  function dismissOverlays() {
    // a hash link inside the menu, the filter sheet or the viewer navigates
    // without a page load, so close whatever is covering the content
    var drawer = document.querySelector('.drawer');
    if (drawer) { drawer.classList.remove('is-on'); drawer.setAttribute('aria-hidden', 'true'); }
    var sheet = document.querySelector('.sheet');
    if (sheet) { sheet.classList.remove('is-on'); sheet.setAttribute('aria-hidden', 'true'); }
    var lb = document.querySelector('.lb');
    if (lb) lb.classList.remove('is-on');
    [].forEach.call(document.querySelectorAll('.scrim'), function (s) { s.classList.remove('is-on'); });
    document.body.classList.remove('is-locked');
  }

  function route() {
    dismissOverlays();
    var h = location.hash.replace(/^#/, '');
    var name = h === 'visit' ? 'visit' : (h.indexOf('c=') === 0 ? 'coll' : 'home');
    for (var k in pages) pages[k].hidden = k !== name;
    document.body.classList.toggle('has-bar', name === 'coll');
    if (name === 'coll') {
      var root = document.querySelector('[data-collection]');
      if (root && root.__applyHash) root.__applyHash();
    } else {
      document.title = name === 'visit' ? 'Visit Us \\u2014 Deep Sons' : HOME_TITLE;
    }
    window.scrollTo(0, 0);
  }

  window.addEventListener('hashchange', route);
  // app.js boots on DOMContentLoaded; route after it so the title it sets for a
  // collection does not overwrite the one this router sets for home or visit.
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', route);
  else route();
})();
"""


def main():
    os.makedirs(DIST, exist_ok=True)

    css = read('assets', 'css', 'style.css')
    tile = read('assets', 'img', 'tile.svg')
    from urllib.parse import quote
    tile_uri = 'data:image/svg+xml,' + quote(tile, safe="!'()*-._~ ").replace(' ', '%20')
    css = css.replace('url("../img/tile.svg")', 'url("%s")' % tile_uri)

    cat = read('assets', 'js', 'catalogue.js')
    data = json.loads(cat.split('window.DS = ', 1)[1].rstrip().rstrip(';'))

    art = {}
    for item in data['items']:
        rel = item['img']
        art[item['id']] = read(*rel.split('/')) if rel.endswith('.svg') else datauri(rel)
        del item['img']

    app = patch_app(read('assets', 'js', 'app.js'))
    visit_js = read('visit.html').split('<script>', 2)[-1].split('</script>')[0]

    pages = [
        ('home', relink(body_of('index.html'))),
        ('coll', relink(body_of('collection.html'))),
        ('visit', relink(body_of('visit.html'))),
    ]
    body = ['<div data-page="%s"%s>%s</div>' % (n, '' if n == 'home' else ' hidden', m)
            for n, m in pages]

    out = []
    out.append('<title>Deep Sons</title>')
    out.append('<meta name="description" content="Look book for Deep Sons: suiting, '
               'shirting, wedding designer sherwani, indo-western, kurta jacket sets, '
               'jodhpuri and customized tailoring.">')
    out.append('<style>\n%s\n</style>' % css)
    out.append('<header class="head" data-header></header>')
    out.extend(body)
    out.append('<footer class="foot" data-footer></footer>')
    out.append('<script>window.DS = %s;</script>' % json.dumps(data, separators=(',', ':')))
    out.append('<script>window.DS_ART = %s;</script>' % json.dumps(art, separators=(',', ':')))
    out.append('<script>\n%s\n</script>' % app)
    out.append('<script>%s</script>' % visit_js)
    out.append('<script>%s</script>' % ROUTER)

    html = inline_assets('\n'.join(out))
    left = re.findall(r'assets/img/[A-Za-z0-9._/-]+', html)
    assert not left, 'un-inlined asset reference: %s' % set(left)
    path = os.path.join(DIST, 'deep-sons.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote %s  (%.0f KB, %d artworks inlined)' % (path, len(html.encode()) / 1024, len(art)))


if __name__ == '__main__':
    main()
