<p align="center"><img src="favicons/favicon.svg" width="120" alt=""></p>

# Die Zukunft — Brand Assets

Source files and generators for the party's icon, favicons, app icons, Open Graph
images and GitHub images.

- **Icon:** "Würfelkreuz, klar", a 3D Swiss cross of seven cubes, drawn with
  hidden-line removal so it stays legible down to 16 px.
- **Wordmark:** `die zukunft.` / `le futur.` / `il futuro.` / `the future.` in Clash Display 700,
  lowercase, gradient including the full stop.
- **Palette "Alpenglühen":** rose `#f43f5e` → magenta `#c026d3` → violet `#6d28d9` →
  indigo `#4338ca` (dark-mode tints `#fb7185` `#e879f9` `#a78bfa` `#818cf8`), on a
  ceramic ground `#eef0ec` with charcoal ink `#121517`.

## Layout

```
favicons/
  favicon.svg        # source mark (hidden-line-removed 3D cross) — SOURCE OF TRUTH
  favicon.png        # 512×512 raster render of favicon.svg (convenience copy)
  favicon.params     # exact params used to generate the shipped favicon.svg
og-images/
  og-{de,fr,it,en}.png   # generic per-language OG cards (1200×630)
  cross-wireframe.svg    # dedicated wireframe cross used inside article OG cards
  cross-wireframe.params # params for cross-wireframe.svg
github/
  org-avatar.png         # 1024×1024 GitHub organisation avatar
  social-<repo>.png      # 1280×640 social preview per repository
scripts/
  gen_favicon.py      # favicon SVG generator (shared renderer with the studio)
  render_brand.mjs    # renders app icons, org avatar, social previews, OG cards (Playwright)
  favicon_studio.html # interactive tuning tool (live sliders, size previews)
  gen_article_og.py   # per-article OG card generator
```

## Where these are consumed

- **Favicon** ships to the theme: `avenir/static/favicon.svg` and the vendored
  submodule `die-zukunft.ch/themes/avenir/static/favicon.svg` (what Zola reads).
  The site's own `static/` intentionally holds only the multi-size `favicon.ico`
  fallback — no `favicon.svg` override.
- **Generic OG images** are mirrored into `die-zukunft.ch/static/og-{lang}.png`.
- **Per-article OG images** live only in `die-zukunft.ch/static/og/aktuelles/<slug>.<lang>.png`.

## Regeneration

### Favicon (wireframe mark)
```bash
python3 scripts/gen_favicon.py "$(cat favicons/favicon.params)"
```
`gen_favicon.py` and `favicon_studio.html` share the same renderer, so a params
line copied from the studio (open it via `python3 -m http.server` in `scripts/`)
reproduces the SVG 1:1. After regenerating, sync the SVG to all four locations
listed above and refresh `favicon.png`.

> The PWA/iOS icons (`apple-touch-icon.png`, `icon-192/512.png` in the site
> `static/`) are a **solid flat** cross by design — a different design language
> for app tiles — and are **not** regenerated from this wireframe mark.

### Per-article OG cards
```bash
python3 scripts/gen_article_og.py   # see --help for slug/title/lang args
```
**Environment dependency:** requires `inkscape` on PATH and the **Clash Display**
and **Switzer** fonts installed locally (`~/Library/Fonts/`) with patched family
names — Fontshare web fonts report a family name of `"false"` and must be patched
with `fonttools` first. Without these the text renders with fallback fonts.

## Known gaps (follow-ups)

- **No generator for the generic `og-{lang}.png` cards.** The four root OG images
  cannot currently be reproduced from anything in this repo — only the per-article
  generator is committed. Add/commit the generic-OG script.
- **Per-article OG PNGs are not backed up here.** Unlike the generic OGs, they
  exist only in the site's `static/og/aktuelles/`. Consider mirroring them.
- **`abstimmung-14-juni-2026` has no bespoke article OG** and falls back to the
  generic card; generate one with `gen_article_og.py` if a custom card is wanted.
