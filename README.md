# Taj Battery Service, UPS & Solar System — website

This is the website for the shop in Pehlwan Goth, Karachi, which has been open since 2012. Phone and WhatsApp: 0315 2020525.

- **Live site:** https://etikaf.github.io/tajbattery/
- **Urdu pages:** https://etikaf.github.io/tajbattery/ur/
- **Repository:** https://github.com/etikaf/tajbattery

The published files are in `docs/`. GitHub Pages serves them from branch `main`, folder `/docs`, as set in **Settings → Pages**.

## Making changes

1. Edit `tools/build_site.py` to change text, packages, accessories, the FAQ or the Urdu pages. Styles are in `docs/assets/style.css`.
2. Rebuild the pages:
   ```sh
   python3 tools/build_site.py docs
   ```
3. Preview locally at http://localhost:8000:
   ```sh
   python3 -m http.server -d docs 8000
   ```
4. Commit and push. The live site updates about two minutes later:
   ```sh
   git add -A
   git commit -m "Describe the change"
   git push
   ```

Always rebuild after editing `style.css` too. The build stamps a version on the stylesheet so phones and PCs load the new one, and it stops with an error if the CSS has an unbalanced bracket.

## Photos

Put new photos in `photos/`. Before they're used on the site, they're copied to `docs/assets/img/` with descriptive filenames and added to the `IMG` list in `tools/build_site.py`.

## Google

- **Search Console:** the property is `https://etikaf.github.io/tajbattery/`, verified with the HTML tag already in the site. The sitemap at `https://etikaf.github.io/tajbattery/sitemap.xml` has been submitted.
- **Google Business Profile:** keep the name, phone (0315 2020525) and area exactly the same as on the website.

## Moving to your own domain later

1. Buy the domain, for example from PKNIC (`.pk`) or a `.com` seller.
2. In the repository, go to **Settings → Pages → Custom domain**, enter the domain, and add the DNS records GitHub shows at your domain seller.
3. In `tools/build_site.py`, change `SITE = "https://etikaf.github.io/tajbattery"` to the new address, rebuild, commit and push.
4. In Search Console, add the new domain as a property and submit its sitemap.
