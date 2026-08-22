/* Deep Sons — site behaviour. Vanilla JS, no dependencies. */
(function () {
  'use strict';

  /* ---------------------------------------------------------- store info --
     Everything the shop may want to change lives here.                     */
  var CONFIG = window.DS_CONFIG = {
    name: 'Deep Sons',
    tagline: 'Ethnic Wear, Suiting & Shirting',
    since: 'Ethnic Wear',
    proprietor: 'By Darshan Dalal',
    // TODO: confirm the street address against the shop's Google listing.
    address: ['Deep Sons', 'Main Market Road', 'City — PIN'],
    phone: '+91 98980 64134',
    whatsapp: '919898064134',
    email: '',
    mapsUrl: 'https://maps.app.goo.gl/EVc7AHxfjvW4ctP49?g_st=ic',
    hours: [
      ['Monday – Saturday', '10:00 am – 8:30 pm'],
      ['Sunday', 'By appointment']
    ]
  };

  var DS = window.DS || { sections: [], items: [], colours: {} };
  var SECTIONS = DS.sections, ITEMS = DS.items, COLOURS = DS.colours;

  var SECTION_COVER = {
    'suiting': 'suiting-charcoal-formal-suit',
    'shirting': 'shirting-powder-blue-fine-stripe',
    'sherwani': 'photo-blue-sherwani',
    'indo-western': 'photo-cream-indowestern',
    'kurta-jacket': 'photo-mustard-kurta',
    'jodhpuri': 'photo-ivory-bandhgala',
    'tailoring': 'tailoring-canvas-and-construction'
  };

  var SORTS = [
    ['picked', 'Hand-picked'],
    ['az', 'Name: A to Z'],
    ['za', 'Name: Z to A'],
    ['colour', 'Grouped by colour'],
    ['fabric', 'Grouped by fabric']
  ];

  var ICON = {
    burger: '<path d="M3 6h18M3 12h18M3 18h18"/>',
    close: '<path d="M6 6l12 12M18 6L6 18"/>',
    heart: '<path d="M12 20.5S3.5 15 3.5 9.2A4.7 4.7 0 0 1 12 6.4a4.7 4.7 0 0 1 8.5 2.8c0 5.8-8.5 11.3-8.5 11.3z"/>',
    sort: '<path d="M7 4v16M7 20l-3-3M7 4l3 3M17 20V4M17 4l-3 3M17 20l3-3"/>',
    filter: '<path d="M3 5h18M6 12h12M10 19h4"/>',
    grid1: '<rect x="4" y="4" width="16" height="16" rx="1"/>',
    grid2: '<rect x="3" y="4" width="8" height="16" rx="1"/><rect x="13" y="4" width="8" height="16" rx="1"/>',
    left: '<path d="M15 5l-7 7 7 7"/>',
    right: '<path d="M9 5l7 7-7 7"/>',
    pin: '<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>'
  };

  function svg(name, cls) {
    return '<svg class="' + (cls || '') + '" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" ' +
      'stroke-linejoin="round" aria-hidden="true">' + ICON[name] + '</svg>';
  }

  function el(html) {
    var t = document.createElement('template');
    t.innerHTML = html.trim();
    return t.content.firstElementChild;
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (m) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m];
    });
  }

  function sectionById(id) {
    for (var i = 0; i < SECTIONS.length; i++) if (SECTIONS[i].id === id) return SECTIONS[i];
    return null;
  }

  function itemById(id) {
    for (var i = 0; i < ITEMS.length; i++) if (ITEMS[i].id === id) return ITEMS[i];
    return null;
  }

  function isWide(item) {
    return item.id.indexOf('tailoring-measure') === 0 ||
      item.id.indexOf('tailoring-the-cutting') === 0 ||
      item.id.indexOf('tailoring-hand-finished') === 0;
  }

  /* ------------------------------------------------------------ wishlist -- */

  var KEY = 'deepsons.saved';

  function saved() {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; }
  }

  function isSaved(id) { return saved().indexOf(id) > -1; }

  function toggleSaved(id) {
    var list = saved(), i = list.indexOf(id);
    if (i > -1) list.splice(i, 1); else list.push(id);
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* private mode */ }
    paintCount();
    return i === -1;
  }

  function paintCount() {
    var n = saved().length;
    [].forEach.call(document.querySelectorAll('[data-saved-count]'), function (b) {
      b.textContent = n;
      b.hidden = n === 0;
    });
  }

  /* -------------------------------------------------------------- chrome -- */

  function buildHeader() {
    var host = document.querySelector('[data-header]');
    if (!host) return;
    var here = (location.pathname.split('/').pop() || 'index.html');
    var links = SECTIONS.slice(0, 6).map(function (s) {
      return '<a href="collection.html?c=' + s.id + '">' + esc(s.name.replace('Wedding Designer ', '')) + '</a>';
    }).join('');
    host.innerHTML =
      '<div class="head__in">' +
        '<button class="icon-btn head__burger" data-open-drawer aria-label="Open menu">' + svg('burger') + '</button>' +
        '<a class="brand" href="index.html">' +
          '<img src="assets/img/logo-mark.png" alt="" width="30" height="37">' +
          '<b>' + esc(CONFIG.name) + '</b><small>' + esc(CONFIG.since) + '</small>' +
        '</a>' +
        '<nav class="head__nav">' + links + '<a href="visit.html"' +
          (here === 'visit.html' ? ' aria-current="page"' : '') + '>Visit</a></nav>' +
        '<a class="icon-btn" href="collection.html?c=saved" aria-label="Saved looks">' +
          svg('heart') + '<b class="head__count" data-saved-count hidden>0</b></a>' +
      '</div>';
  }

  function buildDrawer() {
    if (document.querySelector('.drawer')) return;
    var occasions = ['Wedding', 'Reception', 'Sangeet', 'Mehendi', 'Formal', 'Office', 'Daytime', 'Evening'];
    var html =
      '<div class="scrim" data-close-drawer></div>' +
      '<aside class="drawer" id="drawer" aria-label="Main menu" aria-hidden="true">' +
        '<div class="drawer__top"><span>Menu<u>' + esc(CONFIG.proprietor) + '</u></span>' +
          '<button class="icon-btn" data-close-drawer aria-label="Close menu">' + svg('close') + '</button></div>' +
        '<div class="drawer__body">' +
          '<h4>Shop by product</h4>' +
          SECTIONS.map(function (s) {
            return '<a class="is-lead" href="collection.html?c=' + s.id + '">' + esc(s.name) + '</a>';
          }).join('') +
          '<a href="collection.html?c=all">View all</a>' +
          '<h4>Shop by occasion</h4>' +
          occasions.map(function (t) {
            return '<a href="collection.html?c=all&amp;tag=' + encodeURIComponent(t) + '">' + esc(t) + '</a>';
          }).join('') +
          '<h4>The shop</h4>' +
          '<a href="visit.html">Visit us</a>' +
          '<a href="collection.html?c=tailoring">Customized tailoring</a>' +
          '<a href="collection.html?c=saved">Saved looks</a>' +
          '<div class="drawer__note">This is a look-book, not a shop. Nothing here is ' +
          'priced or sold online — come in and we will show you the cloth, take your ' +
          'measurements and talk it through.</div>' +
        '</div>' +
      '</aside>';
    document.body.insertAdjacentHTML('beforeend', html);

    var drawer = document.querySelector('.drawer'), scrim = document.querySelector('.scrim');
    function open() {
      drawer.classList.add('is-on'); scrim.classList.add('is-on');
      drawer.setAttribute('aria-hidden', 'false'); document.body.classList.add('is-locked');
    }
    function close() {
      drawer.classList.remove('is-on'); scrim.classList.remove('is-on');
      drawer.setAttribute('aria-hidden', 'true'); document.body.classList.remove('is-locked');
    }
    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-open-drawer]')) { e.preventDefault(); open(); }
      else if (e.target.closest('[data-close-drawer]')) { e.preventDefault(); close(); }
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  function buildFooter() {
    var host = document.querySelector('[data-footer]');
    if (!host) return;
    var addr = CONFIG.address.map(esc).join('<br>');
    var contact = [];
    if (CONFIG.phone) contact.push('<li><a href="tel:' + esc(CONFIG.phone.replace(/\s/g, '')) + '">' + esc(CONFIG.phone) + '</a></li>');
    if (CONFIG.whatsapp) contact.push('<li><a href="https://wa.me/' + esc(CONFIG.whatsapp) + '">WhatsApp</a></li>');
    if (CONFIG.email) contact.push('<li><a href="mailto:' + esc(CONFIG.email) + '">' + esc(CONFIG.email) + '</a></li>');
    host.innerHTML =
      '<div class="wrap"><div class="foot__grid">' +
        '<div><div class="foot__brand">' + esc(CONFIG.name) + '</div>' +
          '<p class="foot__by">' + esc(CONFIG.since) + ' &middot; ' + esc(CONFIG.proprietor) + '</p>' +
          '<p>' + esc(CONFIG.tagline) + '. Cloth chosen by hand, cut on our own table ' +
          'and finished to your measurements.</p>' +
          '<p><a href="' + esc(CONFIG.mapsUrl) + '" target="_blank" rel="noopener">' +
          'Find us on the map &rarr;</a></p></div>' +
        '<div><h5>Look book</h5><ul>' +
          SECTIONS.map(function (s) {
            return '<li><a href="collection.html?c=' + s.id + '">' + esc(s.name) + '</a></li>';
          }).join('') + '</ul></div>' +
        '<div><h5>The shop</h5><p>' + addr + '</p><ul>' + contact.join('') + '</ul>' +
          '<p style="margin-top:14px">' + CONFIG.hours.map(function (h) {
            return esc(h[0]) + '<br><span style="color:#94836c">' + esc(h[1]) + '</span>';
          }).join('<br>') + '</p></div>' +
      '</div><div class="foot__base">' +
        '<span>&copy; ' + new Date().getFullYear() + ' ' + esc(CONFIG.name) + '. All artwork on this site is our own.</span>' +
        '<span>Look book only — no prices are published online.</span>' +
      '</div></div>';
  }

  /* ------------------------------------------------------------ fragments -- */

  function dotsHtml(item, limit) {
    var out = item.colours.slice(0, limit || 4).map(function (k) {
      var c = COLOURS[k];
      if (!c) return '';
      return '<i title="' + esc(c.label) + '" style="background:' + c.base + '"></i>';
    }).join('');
    var extra = item.colours.length - (limit || 4);
    if (extra > 0) out += '<u>+' + extra + '</u>';
    return '<div class="dots">' + out + '</div>';
  }

  function cardHtml(item) {
    return '<article class="card' + (isWide(item) ? ' is-wide' : '') + '" data-id="' + item.id + '">' +
      '<a class="card__shot" href="#" data-open="' + item.id + '">' +
        '<img src="' + item.img + '" alt="' + esc(item.title) + '" loading="lazy" width="800" height="1100">' +
        (item.photo ? '<em class="shot-tag">In store</em>' : '') +
      '</a>' +
      '<button class="heart' + (isSaved(item.id) ? ' is-on' : '') + '" data-save="' + item.id + '" ' +
        'aria-pressed="' + isSaved(item.id) + '" aria-label="Save ' + esc(item.title) + '">' +
        svg('heart') + '</button>' +
      '<div class="card__body">' +
        '<h3>' + esc(item.title) + '</h3>' +
        '<p class="card__meta">' + esc(item.fabric) + (item.weave ? ' &middot; ' + esc(item.weave) : '') + '</p>' +
        dotsHtml(item) +
      '</div></article>';
  }

  function swatchHtml(key, active, href) {
    var c = COLOURS[key];
    if (!c) return '';
    var bg = 'background:linear-gradient(145deg,' + c.light + ',' + c.base + ' 55%,' + c.dark + ')';
    return '<a class="swatch' + (active ? ' is-on' : '') + '" href="' + href + '">' +
      '<i style="' + bg + '"></i>' + esc(c.label) + '</a>';
  }

  /* ------------------------------------------------------------- lightbox -- */

  var lb = { list: [], i: 0, node: null };

  function buildLightbox() {
    if (lb.node) return;
    lb.node = el(
      '<div class="lb" role="dialog" aria-modal="true" aria-label="Photo viewer">' +
        '<div class="lb__top"><span data-lb-count></span>' +
          '<button class="icon-btn" data-lb-close aria-label="Close">' + svg('close') + '</button></div>' +
        '<div class="lb__stage">' +
          '<button class="lb__nav lb__nav--prev" data-lb-prev aria-label="Previous">' + svg('left') + '</button>' +
          '<img data-lb-img src="" alt="">' +
          '<button class="lb__nav lb__nav--next" data-lb-next aria-label="Next">' + svg('right') + '</button>' +
        '</div>' +
        '<div class="lb__info" data-lb-info></div>' +
      '</div>');
    document.body.appendChild(lb.node);

    lb.node.addEventListener('click', function (e) {
      if (e.target.closest('[data-lb-close]')) closeLb();
      else if (e.target.closest('[data-lb-prev]')) step(-1);
      else if (e.target.closest('[data-lb-next]')) step(1);
    });
    document.addEventListener('keydown', function (e) {
      if (!lb.node.classList.contains('is-on')) return;
      if (e.key === 'Escape') closeLb();
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
    var x0 = null;
    lb.node.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.node.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
      x0 = null;
    });
  }

  function paintLb() {
    var it = lb.list[lb.i];
    if (!it) return;
    lb.node.querySelector('[data-lb-img]').src = it.img;
    lb.node.querySelector('[data-lb-img]').alt = it.title;
    lb.node.querySelector('[data-lb-count]').textContent = (lb.i + 1) + ' / ' + lb.list.length;
    var sec = sectionById(it.section);
    lb.node.querySelector('[data-lb-info]').innerHTML =
      '<h3>' + esc(it.title) + '</h3>' +
      '<p>' + esc(it.detail) + '</p>' +
      '<p>' + esc(it.fabric) + (it.weave ? ' &middot; ' + esc(it.weave) : '') +
        (sec ? ' &middot; ' + esc(sec.name) : '') + '</p>' +
      dotsHtml(it, 6) +
      '<div class="lb__tags">' + it.tags.map(function (t) { return '<span>' + esc(t) + '</span>'; }).join('') + '</div>' +
      '<p class="lb__note">Shown for reference. Cut and finished to your own measurements ' +
      '&mdash; ask us in store.</p>';
  }

  function step(d) {
    lb.i = (lb.i + d + lb.list.length) % lb.list.length;
    paintLb();
  }

  function openLb(list, id) {
    buildLightbox();
    lb.list = list;
    lb.i = Math.max(0, list.map(function (x) { return x.id; }).indexOf(id));
    lb.node.classList.add('is-on');
    document.body.classList.add('is-locked');
    paintLb();
  }

  function closeLb() {
    lb.node.classList.remove('is-on');
    document.body.classList.remove('is-locked');
  }

  /* ------------------------------------------------------------ home page -- */

  function initHome() {
    var host = document.querySelector('[data-sections]');
    if (host) {
      host.innerHTML = SECTIONS.map(function (s) {
        var cover = itemById(SECTION_COVER[s.id]) || ITEMS.filter(function (i) { return i.section === s.id; })[0];
        return '<a class="sect" href="collection.html?c=' + s.id + '">' +
          '<img src="' + cover.img + '" alt="' + esc(s.name) + '" loading="lazy">' +
          '<div class="sect__cap"><em>' + esc(s.kicker) + '</em><b>' + esc(s.name) + '</b>' +
          '<p>' + esc(s.blurb) + '</p></div></a>';
      }).join('');
    }

    var rail = document.querySelector('[data-rail]');
    if (rail) {
      var keys = ['ivory', 'cream', 'beige', 'gold', 'mustard', 'rust', 'maroon', 'wine',
        'rose', 'peach', 'sage', 'olive', 'emerald', 'bottle', 'teal', 'powder',
        'royal', 'navy', 'indigo', 'charcoal', 'grey', 'black'];
      rail.innerHTML = keys.map(function (k) {
        return swatchHtml(k, false, 'collection.html?c=all&colour=' + k);
      }).join('');
    }

    var camp = document.querySelector('[data-campaign]');
    if (camp && DS.campaign) {
      camp.innerHTML = DS.campaign.map(function (c) {
        return '<figure class="promo">' +
          '<img src="' + c.img + '" alt="' + esc(c.title) + ' \u2014 ' + esc(c.line) + '" loading="lazy">' +
          '</figure>';
      }).join('');
    }

    var strip = document.querySelector('[data-strip]');
    if (strip) {
      var picks = ['sherwani-gold-brocade-sherwani', 'kurta-jacket-radiant-mustard-set',
        'indo-western-wine-drape-indo-western', 'jodhpuri-black-bandhgala',
        'suiting-bottle-green-glen-check-suit', 'sherwani-maroon-jaal-sherwani',
        'shirting-sky-blue-dobby', 'kurta-jacket-powder-bandhani-set'];
      var list = picks.map(itemById).filter(Boolean);
      strip.innerHTML = list.map(cardHtml).join('');
      strip.addEventListener('click', function (e) {
        var a = e.target.closest('[data-open]');
        if (a) { e.preventDefault(); openLb(list, a.getAttribute('data-open')); }
      });
    }
  }

  /* ------------------------------------------------------ collection page -- */

  function initCollection() {
    var root = document.querySelector('[data-collection]');
    if (!root) return;

    var qs = new URLSearchParams(location.search);
    var state = {
      c: qs.get('c') || 'all',
      colour: qs.get('colour') || '',
      tag: qs.get('tag') || '',
      sort: 'picked',
      view: 2
    };

    var gridEl = root.querySelector('[data-grid]');
    var countEl = root.querySelector('[data-count]');
    var railEl = root.querySelector('[data-rail]');
    var chipEl = root.querySelector('[data-chips]');
    var headEl = root.querySelector('[data-sect-head]');

    function pool() {
      if (state.c === 'saved') {
        var ids = saved();
        return ITEMS.filter(function (i) { return ids.indexOf(i.id) > -1; });
      }
      if (state.c === 'all') return ITEMS.slice();
      return ITEMS.filter(function (i) { return i.section === state.c; });
    }

    function visible() {
      var list = pool();
      if (state.colour) list = list.filter(function (i) { return i.colours.indexOf(state.colour) > -1; });
      if (state.tag) list = list.filter(function (i) { return i.tags.indexOf(state.tag) > -1; });
      if (state.sort === 'az') list.sort(function (a, b) { return a.title.localeCompare(b.title); });
      if (state.sort === 'za') list.sort(function (a, b) { return b.title.localeCompare(a.title); });
      if (state.sort === 'colour') list.sort(function (a, b) { return a.colours[0].localeCompare(b.colours[0]); });
      if (state.sort === 'fabric') list.sort(function (a, b) { return a.fabric.localeCompare(b.fabric); });
      return list;
    }

    function paintHead() {
      var s = sectionById(state.c);
      var name, kicker, blurb;
      if (state.c === 'saved') {
        name = 'Saved Looks'; kicker = 'Your shortlist';
        blurb = 'The pieces you tapped the heart on. Kept in this browser only — ' +
          'show us the list when you visit.';
      } else if (state.c === 'all' || !s) {
        name = 'The Full Look Book'; kicker = 'Everything we make';
        blurb = 'Every section in one place — cloth, stitched menswear and wedding wear.';
      } else {
        name = s.name; kicker = s.kicker; blurb = s.blurb;
      }
      document.title = name + ' — ' + CONFIG.name;
      headEl.innerHTML = '<p class="kicker">' + esc(kicker) + '</p><h1>' + esc(name) + '</h1>' +
        '<p>' + esc(blurb) + '</p>';
    }

    function paintRail() {
      var seen = [], list = pool();
      list.forEach(function (i) {
        i.colours.forEach(function (k) { if (seen.indexOf(k) < 0) seen.push(k); });
      });
      seen.sort();
      if (seen.length < 2) { railEl.parentNode.hidden = true; return; }
      railEl.parentNode.hidden = false;
      railEl.innerHTML =
        '<a class="swatch' + (state.colour ? '' : ' is-on') + '" href="#" data-colour="">' +
          '<i style="background:linear-gradient(145deg,#fdf9f0,#e3d6bf 55%,#b9a888)"></i>All</a>' +
        seen.map(function (k) {
          var c = COLOURS[k];
          if (!c) return '';
          return '<a class="swatch' + (state.colour === k ? ' is-on' : '') + '" href="#" data-colour="' + k + '">' +
            '<i style="background:linear-gradient(145deg,' + c.light + ',' + c.base + ' 55%,' + c.dark + ')"></i>' +
            esc(c.label) + '</a>';
        }).join('');
    }

    function paintChips() {
      var tags = [];
      pool().forEach(function (i) {
        i.tags.forEach(function (t) { if (tags.indexOf(t) < 0) tags.push(t); });
      });
      tags.sort();
      chipEl.innerHTML = '<button class="chip' + (state.tag ? '' : ' is-on') + '" data-tag="">All occasions</button>' +
        tags.map(function (t) {
          return '<button class="chip' + (state.tag === t ? ' is-on' : '') + '" data-tag="' + esc(t) + '">' + esc(t) + '</button>';
        }).join('');
    }

    function paintGrid() {
      var list = visible();
      gridEl.className = 'grid' + (state.view === 1 ? ' is-one' : '');
      if (!list.length) {
        gridEl.className = '';
        gridEl.innerHTML = '<div class="empty"><h3>Nothing here yet</h3><p>' +
          (state.c === 'saved'
            ? 'Tap the heart on any photo to keep it here.'
            : 'Try another colour or occasion.') + '</p></div>';
      } else {
        gridEl.innerHTML = list.map(cardHtml).join('');
      }
      countEl.textContent = list.length + (list.length === 1 ? ' design' : ' designs');
      root.__list = list;
    }

    function paintBar() {
      var s = SORTS.filter(function (x) { return x[0] === state.sort; })[0];
      var lab = root.querySelector('[data-sort-label]');
      if (lab) lab.textContent = s ? s[1] : 'Hand-picked';
      var fl = root.querySelector('[data-filter-label]');
      var n = (state.colour ? 1 : 0) + (state.tag ? 1 : 0);
      if (fl) fl.textContent = n ? n + ' applied' : 'Apply filter';
      var dot = root.querySelector('[data-filter-dot]');
      if (dot) dot.hidden = n === 0;
      [].forEach.call(root.querySelectorAll('[data-view]'), function (b) {
        b.classList.toggle('is-on', +b.getAttribute('data-view') === state.view);
      });
    }

    function sync() {
      var u = new URL(location.href);
      u.searchParams.set('c', state.c);
      state.colour ? u.searchParams.set('colour', state.colour) : u.searchParams.delete('colour');
      state.tag ? u.searchParams.set('tag', state.tag) : u.searchParams.delete('tag');
      history.replaceState(null, '', u);
    }

    function render() { paintHead(); paintRail(); paintChips(); paintGrid(); paintBar(); sync(); }
    render();

    root.addEventListener('click', function (e) {
      var sw = e.target.closest('[data-colour]');
      if (sw) {
        e.preventDefault();
        state.colour = sw.getAttribute('data-colour');
        render();
        return;
      }
      var chip = e.target.closest('[data-tag]');
      if (chip) { e.preventDefault(); state.tag = chip.getAttribute('data-tag'); render(); return; }
      var v = e.target.closest('[data-view]');
      if (v) { state.view = +v.getAttribute('data-view'); paintGrid(); paintBar(); return; }
      var open = e.target.closest('[data-open]');
      if (open) { e.preventDefault(); openLb(root.__list, open.getAttribute('data-open')); return; }
    });

    /* sort + filter sheets */
    var sheet = el(
      '<div class="sheet" role="dialog" aria-modal="true" aria-hidden="true">' +
        '<div class="sheet__top"><b data-sheet-title>Sort by</b>' +
          '<button class="icon-btn" data-sheet-close aria-label="Close">' + svg('close') + '</button></div>' +
        '<div class="sheet__body" data-sheet-body></div>' +
        '<div class="sheet__foot"><button class="btn btn--ink" data-sheet-clear hidden>Clear all</button>' +
          '<button class="btn btn--solid" data-sheet-close>Show designs</button></div>' +
      '</div>');
    document.body.appendChild(sheet);
    var sheetScrim = el('<div class="scrim" data-sheet-close></div>');
    document.body.appendChild(sheetScrim);

    function openSheet(kind) {
      var body = sheet.querySelector('[data-sheet-body]');
      sheet.querySelector('[data-sheet-title]').textContent = kind === 'sort' ? 'Sort by' : 'Filter';
      sheet.querySelector('[data-sheet-clear]').hidden = kind === 'sort';
      if (kind === 'sort') {
        body.innerHTML = SORTS.map(function (s) {
          return '<button class="radio' + (state.sort === s[0] ? ' is-on' : '') +
            '" data-sort="' + s[0] + '"><i></i>' + s[1] + '</button>';
        }).join('');
      } else {
        var tags = [];
        pool().forEach(function (i) { i.tags.forEach(function (t) { if (tags.indexOf(t) < 0) tags.push(t); }); });
        var cols = [];
        pool().forEach(function (i) { i.colours.forEach(function (k) { if (cols.indexOf(k) < 0) cols.push(k); }); });
        tags.sort(); cols.sort();
        body.innerHTML =
          '<h5>Occasion &amp; use</h5><div class="sheet__opts">' +
            '<button class="chip' + (state.tag ? '' : ' is-on') + '" data-tag="">All</button>' +
            tags.map(function (t) {
              return '<button class="chip' + (state.tag === t ? ' is-on' : '') + '" data-tag="' + esc(t) + '">' + esc(t) + '</button>';
            }).join('') + '</div>' +
          '<h5>Colour</h5><div class="sheet__opts">' +
            '<button class="chip' + (state.colour ? '' : ' is-on') + '" data-colour="">All</button>' +
            cols.map(function (k) {
              var c = COLOURS[k];
              return c ? '<button class="chip' + (state.colour === k ? ' is-on' : '') + '" data-colour="' + k + '">' +
                '<span style="display:inline-block;width:11px;height:11px;border-radius:50%;background:' +
                c.base + ';margin-right:7px;vertical-align:-1px;border:1px solid rgba(0,0,0,.15)"></span>' +
                esc(c.label) + '</button>' : '';
            }).join('') + '</div>';
      }
      sheet.classList.add('is-on'); sheetScrim.classList.add('is-on');
      sheet.setAttribute('aria-hidden', 'false'); document.body.classList.add('is-locked');
    }

    function closeSheet() {
      sheet.classList.remove('is-on'); sheetScrim.classList.remove('is-on');
      sheet.setAttribute('aria-hidden', 'true'); document.body.classList.remove('is-locked');
    }

    sheet.addEventListener('click', function (e) {
      if (e.target.closest('[data-sheet-close]')) { closeSheet(); return; }
      if (e.target.closest('[data-sheet-clear]')) { state.colour = ''; state.tag = ''; render(); closeSheet(); return; }
      var s = e.target.closest('[data-sort]');
      if (s) { state.sort = s.getAttribute('data-sort'); render(); closeSheet(); return; }
      var t = e.target.closest('[data-tag]');
      if (t) { state.tag = t.getAttribute('data-tag'); render(); openSheet('filter'); return; }
      var c = e.target.closest('[data-colour]');
      if (c) { state.colour = c.getAttribute('data-colour'); render(); openSheet('filter'); return; }
    });
    sheetScrim.addEventListener('click', closeSheet);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeSheet(); });
    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-sheet]');
      if (b) { e.preventDefault(); openSheet(b.getAttribute('data-sheet')); }
    });
  }

  /* ---------------------------------------------------------------- boot -- */

  function boot() {
    buildHeader();
    buildDrawer();
    buildFooter();
    paintCount();
    initHome();
    initCollection();

    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-save]');
      if (!b) return;
      e.preventDefault();
      var on = toggleSaved(b.getAttribute('data-save'));
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', String(on));
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
