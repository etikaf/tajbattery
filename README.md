# Taj Battery Service, UPS & Solar System — website

This is a static website for the shop in Pehlwan Goth, Karachi. The published files are in `docs/`.

## Publish on GitHub Pages (free)

1. Create an empty repository on github.com, for example `taj-battery-solar`.
2. From this folder, run:
   ```sh
   git branch -M main
   git add .
   git commit -m "First version of website"
   git remote add origin https://github.com/<your-username>/taj-battery-solar.git
   git push -u origin main
   ```
3. On GitHub, go to **Settings → Pages**. Under **Source**, choose **Deploy from a branch**, then select branch `main` and folder `/docs`, and click **Save**.
4. After a minute the site is live at `https://<your-username>.github.io/taj-battery-solar/`.
5. Open `tools/build_site.py`, set `SITE = "https://<your-username>.github.io/taj-battery-solar"`, run `python3 tools/build_site.py docs`, then commit and push again.

## Use your own domain later

1. Buy the domain, for example a `.pk` from PKNIC or a cheaper `.com`.
2. In **Settings → Pages → Custom domain**, enter it. GitHub shows the DNS records to add at your domain seller.
3. Change `SITE` in `tools/build_site.py` to the new domain, rebuild, commit and push.

## Get found on Google

- Add the site to **Google Search Console** and submit `sitemap.xml`.
- Put the website link on your **Google Business Profile**. Keep the name, phone and area on the profile exactly the same as on the website.
- Ask happy customers for Google reviews. Reviews matter a lot for local "solar near me" searches.

## Editing

Edit `tools/build_site.py` (text, packages, accessories, FAQ), then run `python3 tools/build_site.py docs`. Preview with `python3 -m http.server -d docs 8000`.
