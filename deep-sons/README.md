# Deep Sons — look book website

A static, self-contained website for **Deep Sons**, tailors and cloth merchants.
It is a *look book*, not a shop: customers browse photographs by section, and no
prices, MSRPs or currency figures appear anywhere on the site.

## Pages

`index.html` (Home), `men.html` (Men), `lookbook.html` (Lookbook), `about.html` (About Us), and `collection.html` for every section.

## Sections

Each of these is its own section with its own page and occasion filters:

| Section | Group | URL |
| --- | --- | --- |
| Suiting | men | `collection.html?c=suiting` |
| Shirting | men | `collection.html?c=shirting` |
| Wedding Designer Sherwani | men | `collection.html?c=sherwani` |
| Indo-Western | men | `collection.html?c=indo-western` |
| Kurta Jacket Set | men | `collection.html?c=kurta-jacket` |
| Jodhpuri | men | `collection.html?c=jodhpuri` |
| Customized Tailoring | men | `collection.html?c=tailoring` |
| Kids | kids | `collection.html?c=kids` |

Plus `collection.html?c=all` (Lookbook) and `collection.html?c=saved` (the
visitor's own shortlist, kept in their browser only).

Kids items carry `kid: True` in the generator, which draws the figure shorter
with a proportionally larger head. Every item also carries a `type` (Sherwani,
Jodhpuri, Kurta Jacket Set …), which drives `?type=` filtering and the Kids
dropdown.

## About the images — no copyright risk

**Every image on this site is original artwork, drawn from scratch as SVG by
`tools/generate_art.py`.** There is no stock photography, no scraped product
shot, no third-party illustration and no borrowed brand asset anywhere in this
repository. Nothing needs a licence, an attribution or a takedown check.

The generator draws each garment from vector primitives — silhouettes, woven
fabric patterns (herringbone, pinstripe, jaal, paisley, bandhani, brocade …) and
a shared studio backdrop — and writes both the `.svg` files and the catalogue
data the site reads.

To change, add or restyle designs, edit the `PALETTE`, `pattern_def`, garment
functions or the `ITEMS` list in `tools/generate_art.py`, then run:

```sh
python3 tools/generate_art.py
```

That rewrites `assets/img/*.svg` and regenerates `assets/js/catalogue.js`. Do not
hand-edit `catalogue.js` — it is overwritten on every run.

When real photographs of the shop's own garments are available, drop them into
`assets/img/` and point the matching `img` field in `catalogue.js` at them (or,
better, add them to the generator's item list so the data stays in one place).
Only use photographs the shop itself owns.

## Shop details — edit these

Business details live in **one** place: the `CONFIG` object at the top of
`assets/js/app.js`.

```js
var CONFIG = window.DS_CONFIG = {
  address: ['Deep Sons', 'Main Market Road', 'City — PIN'],  // TODO: confirm
  phone: '',        // e.g. '+91 98765 43210'  (leave '' to hide the row)
  whatsapp: '',     // digits only, e.g. '919876543210'
  email: '',
  mapsUrl: 'https://maps.app.goo.gl/…',
  hours: [['Monday – Saturday', '10:00 am – 8:30 pm'], ['Sunday', 'By appointment']]
};
```

The address, phone, email and hours currently shipped are **placeholders**.
Replace them with the details from the shop's Google Business listing before the
site goes live. The header, footer and Visit page all read from this object, so
one edit updates every page.

## Single-file build

`tools/build_artifact.py` folds all three pages into one self-contained HTML file
at `dist/deep-sons.html` — hash routing instead of separate pages, and the
stylesheet, scripts and all 58 artworks carried inline. Handy for sharing a
preview link or e-mailing the site to someone before it has a domain.

```sh
python3 tools/build_artifact.py
```

The multi-page site is the source of truth; rebuild after any change.

## Running it

It is plain HTML, CSS and JavaScript — no build step, no dependencies, no
external requests (no CDN, no web fonts, no analytics). Open `index.html`
directly, or serve the folder:

```sh
python3 -m http.server 8000
```

Deploy by copying this folder to any static host (GitHub Pages, Netlify, Cloudflare
Pages, or ordinary shared hosting).

## What the site does

* Section landing pages for men's and kids' wear
* Mega dropdowns on Men and Kids: the men's sections, and — since kids is a
  single section — the garment families inside it, each with a thumbnail
* Filter by occasion (Wedding Ceremony, Reception, Sangeet, Engagement,
  Mehendi, Haldi — multi-select) and by garment type; sort by name or fabric
* One-up / two-up grid toggle and a sticky sort–filter bar
* Full-screen photo viewer with keyboard arrows and swipe
* "Save" hearts that build a shortlist in the visitor's own browser
  (`localStorage`; nothing is sent anywhere)
* Works without prices by design — every call to action points at the shop

## Layout

```
index.html            home
men.html              the men's sections
lookbook.html         the picture book: pictures only, no captions
collection.html       every section, driven by ?c=<section>
about.html            who we are, address, hours, what to expect
assets/css/style.css  the whole stylesheet
assets/js/app.js      shop details + all behaviour
assets/js/catalogue.js  GENERATED — section and item data
assets/img/*.svg      GENERATED — all artwork
tools/generate_art.py the artwork generator
```
