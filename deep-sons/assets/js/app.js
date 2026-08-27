/* Deep Sons — site behaviour. Vanilla JS, no dependencies. */
(function () {
  'use strict';

  /* ---------------------------------------------------------- store info --
     Everything the shop may want to change lives here.                     */
  var CONFIG = window.DS_CONFIG = {
    name: 'Deep Sons',
    tagline: 'Suiting, Shirting & Wedding Wear',
    since: 'Tailors & Cloth Merchants',
    // TODO: confirm these against the shop's Google Business listing.
    address: ['Deep Sons', 'Main Market Road', 'City — PIN'],
    phone: '',
    whatsapp: '',
    email: '',
    instagram: 'https://www.instagram.com/deep.sons/',
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
    'sherwani': 'sherwani-ivory-zardozi-sherwani',
    'indo-western': 'indo-western-emerald-cape-indo-western',
    'kurta-jacket': 'kurta-jacket-emerald-sparkle-set',
    'jodhpuri': 'jodhpuri-bottle-green-jodhpuri',
    'tailoring': 'tailoring-canvas-and-construction',
    'kids': 'kids-ivory-kurta-jacket-set'
  };

  var NAV = [
    { key: 'home', label: 'Home', href: 'index.html' },
    { key: 'men', label: 'Men', href: 'men.html', menu: 'men' },
    { key: 'kids', label: 'Kids', href: 'collection.html?c=kids', menu: 'kids' },
    { key: 'lookbook', label: 'Lookbook', href: 'lookbook.html' },
    { key: 'about', label: 'About Us', href: 'about.html' }
  ];

  // the six functions the collection filters by, in the order they read
  var OCCASIONS = ['Wedding Ceremony', 'Reception', 'Sangeet', 'Engagement',
    'Mehendi', 'Haldi'];

  var SORTS = [
    ['picked', 'Hand-picked'],
    ['az', 'Name: A to Z'],
    ['za', 'Name: Z to A'],
    ['fabric', 'Grouped by fabric']
  ];

  var ICON = {
    burger: '<path d="M3 6h18M3 12h18M3 18h18"/>',
    close: '<path d="M6 6l12 12M18 6L6 18"/>',
    chev: '<path d="M6 9l6 6 6-6"/>',
    heart: '<path d="M12 20.5S3.5 15 3.5 9.2A4.7 4.7 0 0 1 12 6.4a4.7 4.7 0 0 1 8.5 2.8c0 5.8-8.5 11.3-8.5 11.3z"/>',
    sort: '<path d="M7 4v16M7 20l-3-3M7 4l3 3M17 20V4M17 4l-3 3M17 20l3-3"/>',
    filter: '<path d="M3 5h18M6 12h12M10 19h4"/>',
    grid1: '<rect x="4" y="4" width="16" height="16" rx="1"/>',
    grid2: '<rect x="3" y="4" width="8" height="16" rx="1"/><rect x="13" y="4" width="8" height="16" rx="1"/>',
    left: '<path d="M15 5l-7 7 7 7"/>',
    right: '<path d="M9 5l7 7-7 7"/>',
    pin: '<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    insta: '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/>' +
      '<circle cx="17.2" cy="6.8" r="1.15" fill="currentColor" stroke="none"/>'
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

  /* Where a piece's artwork comes from. The single-file build replaces this
     with a lookup into its inline map. */
  function artSrc(item) {
    return item.img;
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

  function coverOf(sectionId) {
    return itemById(SECTION_COVER[sectionId]) ||
      ITEMS.filter(function (i) { return i.section === sectionId; })[0];
  }

  /* The rows of a nav dropdown: the men's sections, or — since kids is a
     single section — the garment families inside it. */
  function menuRows(kind) {
    if (kind === 'men') {
      return SECTIONS.filter(function (s) { return s.group === 'men'; })
        .map(function (s) {
          return { href: 'collection.html?c=' + s.id, label: s.name, item: coverOf(s.id) };
        });
    }
    var rows = [], seen = [];
    ITEMS.forEach(function (i) {
      if (i.section !== 'kids' || !i.type || seen.indexOf(i.type) > -1) return;
      seen.push(i.type);
      rows.push({
        href: 'collection.html?c=kids&type=' + encodeURIComponent(i.type),
        label: i.type,
        item: i
      });
    });
    return rows;
  }

  function megaHtml(n) {
    var rows = menuRows(n.menu);
    if (!rows.length) return '';
    var all = n.menu === 'men'
      ? { href: 'men.html', label: 'View all menswear' }
      : { href: 'collection.html?c=kids', label: 'View everything for kids' };
    return '<div class="mega"><div class="mega__in"><div class="mega__grid">' +
      rows.map(function (r) {
        return '<a class="mega__link" href="' + r.href + '">' +
          '<i style="background-image:url(&quot;' + (r.item ? artSrc(r.item) : '') + '&quot;)"></i>' +
          '<span>' + esc(r.label) + '</span></a>';
      }).join('') +
      '</div><a class="mega__all" href="' + all.href + '">' + esc(all.label) +
      ' &rarr;</a></div></div>';
  }

  function buildHeader() {
    var host = document.querySelector('[data-header]');
    if (!host) return;
    var links = NAV.map(function (n) {
      if (!n.menu) {
        return '<a href="' + n.href + '" data-nav="' + n.key + '">' + esc(n.label) + '</a>';
      }
      return '<span class="navitem"><a href="' + n.href + '" data-nav="' + n.key +
        '" aria-haspopup="true">' + esc(n.label) + svg('chev', 'chev') + '</a>' +
        megaHtml(n) + '</span>';
    }).join('');
    host.innerHTML =
      '<div class="head__in">' +
        '<button class="icon-btn head__burger" data-open-drawer aria-label="Open menu">' + svg('burger') + '</button>' +
        '<a class="brand" href="index.html">' +
          '<img src="assets/img/logo-mark.png" alt="" width="39" height="34">' +
          '<span class="brand__txt"><b>' + esc(CONFIG.name) + '</b>' +
          '<small>' + esc(CONFIG.since) + '</small></span>' +
        '</a>' +
        '<nav class="head__nav">' + links + '</nav>' +
        (CONFIG.instagram
          ? '<a class="icon-btn" href="' + esc(CONFIG.instagram) + '" target="_blank" ' +
            'rel="noopener" aria-label="Deep Sons on Instagram">' + svg('insta') + '</a>'
          : '') +
        '<a class="icon-btn" href="collection.html?c=saved" aria-label="Saved looks">' +
          svg('heart') + '<b class="head__count" data-saved-count hidden>0</b></a>' +
      '</div>';
    markNav();
    positionMenus();
  }

  /* Keep a dropdown inside the window: it hangs off the left edge of its nav
     item, and the nav sits at the right of the header, so a wide panel would
     otherwise run off screen. */
  function positionMenus() {
    var edge = document.documentElement.clientWidth - 14;
    [].forEach.call(document.querySelectorAll('.navitem'), function (item) {
      var m = item.querySelector('.mega');
      if (!m) return;
      m.style.left = '0px';
      var over = m.getBoundingClientRect().right - edge;
      if (over > 0) m.style.left = (-Math.ceil(over)) + 'px';
    });
  }

  function buildDrawer() {
    if (document.querySelector('.drawer')) return;
    var occasions = OCCASIONS;
    var html =
      '<div class="scrim" data-close-drawer></div>' +
      '<aside class="drawer" id="drawer" aria-label="Main menu" aria-hidden="true">' +
        '<div class="drawer__top"><span>Menu</span>' +
          '<button class="icon-btn" data-close-drawer aria-label="Close menu">' + svg('close') + '</button></div>' +
        '<div class="drawer__body">' +
          '<a class="is-lead" href="index.html">Home</a>' +
          '<h4>Men</h4>' +
          SECTIONS.filter(function (s) { return s.group === 'men'; }).map(function (s) {
            return '<a class="is-lead" href="collection.html?c=' + s.id + '">' + esc(s.name) + '</a>';
          }).join('') +
          '<a href="men.html">All menswear</a>' +
          '<h4>Kids</h4>' +
          SECTIONS.filter(function (s) { return s.group === 'kids'; }).map(function (s) {
            return '<a class="is-lead" href="collection.html?c=' + s.id + '">' + esc(s.name) + '</a>';
          }).join('') +
          '<h4>Lookbook</h4>' +
          '<a href="lookbook.html">The picture book</a>' +
          '<a href="collection.html?c=all">Everything we make</a>' +
          '<h4>Shop by occasion</h4>' +
          occasions.map(function (t) {
            return '<a href="collection.html?c=all&amp;tag=' + encodeURIComponent(t) + '">' + esc(t) + '</a>';
          }).join('') +
          '<h4>The shop</h4>' +
          '<a href="about.html">About us</a>' +
          '<a href="collection.html?c=tailoring">Customized tailoring</a>' +
          '<a href="collection.html?c=saved">Saved looks</a>' +
          (CONFIG.instagram ? '<a href="' + esc(CONFIG.instagram) + '" target="_blank" ' +
            'rel="noopener">Instagram &nearr;</a>' : '') +
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
    if (CONFIG.instagram) contact.push('<li><a href="' + esc(CONFIG.instagram) +
      '" target="_blank" rel="noopener">Instagram &nearr;</a></li>');
    host.innerHTML =
      '<div class="wrap"><div class="foot__grid">' +
        '<div><img class="foot__logo" src="assets/img/logo-full.png" alt="' +
          esc(CONFIG.name) + '" width="190">' +
          '<p>' + esc(CONFIG.tagline) + '. Cloth chosen by hand, cut on our own table ' +
          'and finished to your measurements.</p>' +
          '<p><a href="' + esc(CONFIG.mapsUrl) + '" target="_blank" rel="noopener">' +
          'Find us on the map &rarr;</a></p></div>' +
        '<div><h5>Look book</h5><ul>' +
          SECTIONS.map(function (s) {
            return '<li><a href="collection.html?c=' + s.id + '">' + esc(s.name) + '</a></li>';
          }).join('') +
          '<li><a href="lookbook.html">Lookbook</a></li>' +
          '<li><a href="collection.html?c=all">Everything we make</a></li>' +
          '<li><a href="about.html">About us</a></li></ul></div>' +
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
        '<img src="' + artSrc(item) + '" alt="' + esc(item.title) + '" loading="lazy" width="800" height="1100">' +
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

  /* ---------------------------------------------------------------- route --
     The multi-page site keeps collection state in the query string. The
     single-file build swaps these two for hash equivalents.               */

  function readQuery() {
    return new URLSearchParams(location.search);
  }

  function writeQuery(p) {
    try {
      var u = new URL(location.href);
      u.search = p.toString();
      history.replaceState(null, '', u);
    } catch (e) {
      /* opaque origin (a sandboxed frame): the view is right, the URL just
         will not update, so deep links are the only thing lost */
    }
  }

  function currentRoute() {
    var file = (location.pathname.split('/').pop() || 'index.html');
    if (file === 'men.html') return 'men';
    if (file === 'about.html') return 'about';
    if (file === 'lookbook.html') return 'lookbook';
    if (file === 'collection.html') return 'c=' + (readQuery().get('c') || 'all');
    return '';
  }

  /* Which top-level nav item owns a route. A section page belongs to the
     range it sits in, so browsing Sherwani keeps Men lit. */
  function navTarget(route) {
    if (route === 'men' || route === 'about' || route === 'lookbook') return route;
    if (route.indexOf('c=') === 0) {
      var sec = sectionById(route.slice(2).split('&')[0]);
      // "everything we make" and saved looks have no nav item of their own —
      // they hang off Home, which is where they are reached from
      if (!sec) return 'home';
      return sec.group === 'kids' ? 'kids' : 'men';
    }
    return 'home';
  }

  function markNav(route) {
    var want = navTarget(route == null ? currentRoute() : route);
    [].forEach.call(document.querySelectorAll('.head__nav [data-nav]'), function (a) {
      if (a.getAttribute('data-nav') === want) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  }

  window.DS_MARK_NAV = markNav;

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
    lb.node.querySelector('[data-lb-img]').src = artSrc(it);
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
    // a single page may carry more than one grid (the one-file build stacks
    // every page in the same document), so render all of them
    [].forEach.call(document.querySelectorAll('[data-sections]'), function (host) {
      var group = host.getAttribute('data-sections');
      var list = group ? SECTIONS.filter(function (s) { return s.group === group; }) : SECTIONS;
      host.innerHTML = list.map(function (s) {
        var cover = itemById(SECTION_COVER[s.id]) || ITEMS.filter(function (i) { return i.section === s.id; })[0];
        return '<a class="sect" href="collection.html?c=' + s.id + '">' +
          '<img src="' + artSrc(cover) + '" alt="' + esc(s.name) + '" loading="lazy">' +
          '<div class="sect__cap"><em>' + esc(s.kicker) + '</em><b>' + esc(s.name) + '</b>' +
          '<p>' + esc(s.blurb) + '</p></div></a>';
      }).join('');
    });

    initLookbook();

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

  /* -------------------------------------------------------- lookbook page -- */

  function initLookbook() {
    var grid = document.querySelector('[data-lookbook]');
    if (!grid) return;

    // deal the pictures round-robin across sections so the page does not open
    // on four fabric bolts in a row
    var bySection = {}, order = [];
    ITEMS.forEach(function (i) {
      if (isWide(i)) return;
      if (!bySection[i.section]) { bySection[i.section] = []; order.push(i.section); }
      bySection[i.section].push(i);
    });
    var shots = [], left = true;
    for (var pass = 0; left; pass++) {
      left = false;
      for (var k = 0; k < order.length; k++) {
        var q = bySection[order[k]];
        if (pass < q.length) { shots.push(q[pass]); left = true; }
      }
    }

    grid.innerHTML = shots.map(function (i) {
      return '<a class="shot" href="#" data-open="' + i.id + '">' +
        '<img src="' + artSrc(i) + '" alt="' + esc(i.title) + '" loading="lazy"></a>';
    }).join('');
    grid.addEventListener('click', function (e) {
      var a = e.target.closest('[data-open]');
      if (a) { e.preventDefault(); openLb(shots, a.getAttribute('data-open')); }
    });
  }

  /* ------------------------------------------------------ collection page -- */

  function initCollection() {
    var root = document.querySelector('[data-collection]');
    if (!root) return;

    var qs = readQuery();
    var state = {
      c: qs.get('c') || 'all',
      type: qs.get('type') || '',
      tags: (qs.get('tag') || '').split(',').filter(Boolean),
      sort: 'picked',
      view: 2
    };

    var gridEl = root.querySelector('[data-grid]');
    var countEl = root.querySelector('[data-count]');
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
      if (state.type) list = list.filter(function (i) { return i.type === state.type; });
      if (state.tags.length) {
        list = list.filter(function (i) {
          return state.tags.some(function (t) { return i.tags.indexOf(t) > -1; });
        });
      }
      if (state.sort === 'az') list.sort(function (a, b) { return a.title.localeCompare(b.title); });
      if (state.sort === 'za') list.sort(function (a, b) { return b.title.localeCompare(a.title); });
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
      if (state.type) { kicker = name; name = state.type; }
      document.title = name + ' — ' + CONFIG.name;
      headEl.innerHTML = '<p class="kicker">' + esc(kicker) + '</p><h1>' + esc(name) + '</h1>' +
        '<p>' + esc(blurb) + '</p>';
    }

    function offeredTags() {
      var here = pool();
      return OCCASIONS.filter(function (t) {
        return here.some(function (i) { return i.tags.indexOf(t) > -1; });
      });
    }

    function paintChips() {
      var tags = offeredTags();
      if (!tags.length) { chipEl.parentNode.hidden = true; return; }
      chipEl.parentNode.hidden = false;
      chipEl.innerHTML = tags.map(function (t) {
        return '<button class="chip' + (state.tags.indexOf(t) > -1 ? ' is-on' : '') +
          '" data-tag="' + esc(t) + '">' + esc(t) + '</button>';
      }).join('') +
        (state.tags.length
          ? '<button class="chip chip--clear" data-tag-clear>Clear all</button>'
          : '');
    }

    function paintGrid() {
      var list = visible();
      gridEl.className = 'grid' + (state.view === 1 ? ' is-one' : '');
      if (!list.length) {
        gridEl.className = '';
        gridEl.innerHTML = '<div class="empty"><h3>Nothing here yet</h3><p>' +
          (state.c === 'saved'
            ? 'Tap the heart on any photo to keep it here.'
            : 'Try another occasion.') + '</p></div>';
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
      var n = state.tags.length + (state.type ? 1 : 0);
      if (fl) fl.textContent = n ? n + ' applied' : 'Apply filter';
      var dot = root.querySelector('[data-filter-dot]');
      if (dot) dot.hidden = n === 0;
      [].forEach.call(root.querySelectorAll('[data-view]'), function (b) {
        b.classList.toggle('is-on', +b.getAttribute('data-view') === state.view);
      });
    }

    function sync() {
      var p = new URLSearchParams();
      p.set('c', state.c);
      if (state.type) p.set('type', state.type);
      if (state.tags.length) p.set('tag', state.tags.join(','));
      writeQuery(p);
    }

    function render() { paintHead(); paintChips(); paintGrid(); paintBar(); sync(); }

    // re-point an already-built collection at a new route without rebuilding
    // it; used by the single-file build's router
    root.__applyRoute = function (params) {
      var q = params || readQuery();
      state.c = q.get('c') || 'all';
      state.type = q.get('type') || '';
      state.tags = (q.get('tag') || '').split(',').filter(Boolean);
      render();
    };

    render();

    root.addEventListener('click', function (e) {
      if (e.target.closest('[data-tag-clear]')) { e.preventDefault(); state.tags = []; render(); return; }
      var chip = e.target.closest('[data-tag]');
      if (chip) {
        e.preventDefault();
        var t = chip.getAttribute('data-tag');
        var at = state.tags.indexOf(t);
        if (at > -1) state.tags.splice(at, 1); else state.tags.push(t);
        render();
        return;
      }
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
        var types = [];
        pool().forEach(function (i) { if (i.type && types.indexOf(i.type) < 0) types.push(i.type); });
        types.sort();
        body.innerHTML =
          (types.length > 1
            ? '<h5>Garment</h5><div class="sheet__opts">' +
                '<button class="chip' + (state.type ? '' : ' is-on') + '" data-type="">All</button>' +
                types.map(function (t) {
                  return '<button class="chip' + (state.type === t ? ' is-on' : '') +
                    '" data-type="' + esc(t) + '">' + esc(t) + '</button>';
                }).join('') + '</div>'
            : '') +
          '<h5>Occasion</h5><div class="sheet__opts">' +
            tags.map(function (t) {
              return '<button class="chip' + (state.tags.indexOf(t) > -1 ? ' is-on' : '') +
                '" data-tag="' + esc(t) + '">' + esc(t) + '</button>';
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
      if (e.target.closest('[data-sheet-clear]')) {
        state.tags = []; state.type = ''; render(); closeSheet(); return;
      }
      var s = e.target.closest('[data-sort]');
      if (s) { state.sort = s.getAttribute('data-sort'); render(); closeSheet(); return; }
      var ty = e.target.closest('[data-type]');
      if (ty) { state.type = ty.getAttribute('data-type'); render(); openSheet('filter'); return; }
      var tc = e.target.closest('[data-tag]');
      if (tc) {
        var t = tc.getAttribute('data-tag');
        var at = state.tags.indexOf(t);
        if (at > -1) state.tags.splice(at, 1); else state.tags.push(t);
        render();
        openSheet('filter');
        return;
      }
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

    window.addEventListener('resize', positionMenus);
    document.addEventListener('pointerover', function (e) {
      if (e.target.closest && e.target.closest('.navitem')) positionMenus();
    });

    document.addEventListener('click', function (e) {
      var row = e.target.closest('.mega__link, .mega__all');
      if (row) {
        var item = row.closest('.navitem');
        if (item) {
          item.classList.add('is-shut');
          item.addEventListener('mouseleave', function once() {
            item.classList.remove('is-shut');
            item.removeEventListener('mouseleave', once);
          });
        }
      }
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
