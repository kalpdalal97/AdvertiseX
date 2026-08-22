# Deep Sons — look book website

A static, self-contained website for **Deep Sons**, tailors and cloth merchants.
It is a *look book*, not a shop: customers browse photographs by section, and no
prices, MSRPs or currency figures appear anywhere on the site.

## Sections

Each of these is its own section with its own page, colour rail and filters:

| Section | URL |
| --- | --- |
| Suiting | `collection.html?c=suiting` |
| Shirting | `collection.html?c=shirting` |
| Wedding Designer Sherwani | `collection.html?c=sherwani` |
| Indo-Western | `collection.html?c=indo-western` |
| Kurta Jacket Set | `collection.html?c=kurta-jacket` |
| Jodhpuri | `collection.html?c=jodhpuri` |
| Customized Tailoring | `collection.html?c=tailoring` |

Plus `collection.html?c=all` (everything) and `collection.html?c=saved` (the
visitor's own shortlist, kept in their browser only).

## About the images — no copyright risk

Two kinds of image, both safe to publish:

1. **The shop's own photographs.** The originals sit in `photos-source/`;
   `tools/prep_photos.py` crops the app chrome and page furniture off them, cuts
   a portrait card and a full-size banner from each, compresses them into
   `assets/img/photo/`, and lifts the DS crown monogram out of its background
   into `assets/img/logo-mark.png` so the logo works on cream and on dark.

   ```sh
   python3 tools/prep_photos.py
   ```

2. **Original SVG artwork** for everything else, drawn from scratch by
   `tools/generate_art.py`.

There is no stock photography, no scraped product shot, no third-party
illustration and no borrowed brand asset anywhere in this repository. Nothing
needs a licence, an attribution or a takedown check.

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

To add more of the shop's photographs: drop the originals into
`photos-source/`, add a crop to `JOBS` in `tools/prep_photos.py`, then add an
entry to `PHOTOS` (product cards) or `CAMPAIGN` (home-page creatives) in
`tools/generate_art.py` and re-run both scripts. Photo entries carry
`'photo': True`, which puts the small "In store" badge on the card. Only use
photographs the shop itself owns.

## Shop details — edit these

Business details live in **one** place: the `CONFIG` object at the top of
`assets/js/app.js`.

```js
var CONFIG = window.DS_CONFIG = {
  proprietor: 'By Darshan Dalal',
  phone: '+91 98980 64134',
  whatsapp: '919898064134',      // digits only
  email: '',                     // leave '' to hide the row
  address: ['Deep Sons', 'Main Market Road', 'City — PIN'],  // TODO: confirm
  mapsUrl: 'https://maps.app.goo.gl/…',
  hours: [['Monday – Saturday', '10:00 am – 8:30 pm'], ['Sunday', 'By appointment']]
};
```

The phone number is the one from the shop's own creatives. **The street address
and the opening hours are still placeholders** — replace them with the details
from the Google Business listing before the site goes live. The header, footer
and Visit page all read from this object, so one edit updates every page.

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

* Section landing pages with a Manyavar-style circular colour rail
* Filter by colour and by occasion; sort by name, colour family or fabric
* One-up / two-up grid toggle and a sticky sort–filter bar
* Full-screen photo viewer with keyboard arrows and swipe
* "Save" hearts that build a shortlist in the visitor's own browser
  (`localStorage`; nothing is sent anywhere)
* Works without prices by design — every call to action points at the shop

## Layout

```
index.html            home
collection.html       every section, driven by ?c=<section>
visit.html            address, hours, what to expect
assets/css/style.css  the whole stylesheet
assets/js/app.js      shop details + all behaviour
assets/js/catalogue.js  GENERATED — section and item data
assets/img/*.svg      GENERATED — all artwork
tools/generate_art.py the artwork generator
```
