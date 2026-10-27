# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This repo holds the website for **Taj Battery Service, UPS & Solar System**, a battery and solar shop in Pehlwan Goth, Karachi. The shop's customers have so far come through walk-ins and word of mouth, and the site's purpose is to win new customers online. Solar systems, packages and accessories are the focus. Batteries are secondary, and jump start appears only as a minor service. Phone and WhatsApp: 0315 2020525 (+923152020525).

## Layout

- `docs/`: the published static site (English pages at the root; Urdu versions of Home, Packages, Services and Contact in `docs/ur/`, right-to-left, listed in `UR_PAGES`), served by GitHub Pages from `main` → `/docs`. It has no build step at serve time and no JS framework.
- `tools/build_site.py` (run it after any CSS/JS edit too: it stamps `?v=<hash>` on style.css/site.js so phones drop cached copies): generates every page (photos are registered in its `IMG` dict and placed with `fig()`) in `docs/`, along with `robots.txt` and `sitemap.xml`. The header, footer, contact details, `SITE` URL, packages, accessories and FAQ all live here.
- `docs/assets/style.css`: all styles, hand-written CSS using tokens in `:root` plus a dark-mode override. Brand chosen by the owner: signboard blue `#1e5bb8` + sun yellow `#f5b400`, Nunito for headings and body, Noto Nastaliq Urdu; logo is the crowned battery (`docs/assets/logo.svg`). `docs/assets/site.js` turns the contact form into a pre-filled WhatsApp message and pre-selects a package from `?need=`.
- `photos/`: the owner's original photos. Copy them into `docs/assets/img/` with descriptive filenames before using them.
- `gemini pages/`: old drafts kept for reference. They are not published.

## Commands

```sh
python3 tools/build_site.py docs                 # regenerate pages after editing the generator
python3 -m http.server -d docs 8000              # preview at http://localhost:8000
```

## Rules

- English pages are English only, except the Urdu tagline on the home page (marked `punch`); `page()` strips any other `lang="ur"` text from them. Urdu pages keep technical words (kW, inverter, hybrid, on-grid, lithium, K-Electric) in English and wrap numbers with units in `bdi()` so they read left to right. The owner reviews Urdu text before it goes live.
- The shop has been open since 2012 and has always done solar; don't describe solar as new.

- Edit `tools/build_site.py` and regenerate. Don't hand-edit the generated `docs/*.html`, because the next build overwrites them. Edit CSS and JS directly in `docs/assets/`.
- When the real domain is known, change `SITE` in the generator and rebuild. It feeds the canonical URLs, Open Graph, JSON-LD, the sitemap and robots.txt.
- Mobile comes first: design and check at ~360px before desktop. Keep the site light for slow mobile connections. The Urdu Nastaliq font is requested with only the letters the site uses (`text=` subset, filled in at the end of the build). Use no frameworks or icon fonts (icons are inline SVG), compress WebP images to under about 100 KB, and lazy-load anything below the fold.
- SEO depends on consistent NAP (name, area, phone) everywhere: the `BUSINESS` JSON-LD, the footer and the contact page. Each page needs a unique `<title>` and description that name Pehlwan Goth or Karachi.
- SEO targets by page: home (solar + car batteries + UPS, Pehlwan Goth), `batteries.html` (car batteries `#car`, solar/UPS batteries `#solar`), `accessories.html` (solar DC accessories), `services.html` (installation, UPS repair). Keep `<title>` near 60 characters and descriptions near 160.
- Don't publish prices. They change weekly, so every price call-to-action links to WhatsApp or `contact.html?need=…`.
