# Generates the static site in docs/. Run: python3 tools/build_site.py docs
import hashlib, json, os, re, sys, urllib.parse

OUT = sys.argv[1]

def version(path):
    """Short content hash, added as ?v=... so phones fetch new CSS/JS right after each change."""
    return hashlib.md5(open(os.path.join(OUT, path), "rb").read()).hexdigest()[:8]
def check_css(path):
    """Stop the build if style.css has unbalanced braces: one stray } makes browsers drop the next rule."""
    css = re.sub(r"/\*.*?\*/", "", open(os.path.join(OUT, path), encoding="utf-8").read(), flags=re.S)
    depth = 0
    for n, line in enumerate(css.splitlines(), 1):
        for ch in line:
            depth += (ch == "{") - (ch == "}")
            if depth < 0:
                sys.exit("CSS error in %s: stray '}' near line %d" % (path, n))
    if depth:
        sys.exit("CSS error in %s: %d unclosed '{'" % (path, depth))
check_css("assets/style.css")
CSS_V = version("assets/style.css")
JS_V = version("assets/site.js")
SITE = "https://etikaf.github.io/tajbattery"  # change to the custom domain when bought
NAME = "Taj Battery Service, UPS & Solar System"
PHOTO = "assets/img/taj-battery-shop-pehlwan-goth.webp"

# Shop photos (owner's own). file, width, height, alt text, caption
IMG = {
    "front": ("taj-battery-shop-pehlwan-goth.webp", 619, 510, "Taj Battery Service, UPS & Solar System shop front in Pehlwan Goth, Karachi, with Osaka, Exide and Phoenix battery signs", "The shop today, Pehlwan Goth"),
    "front_old": ("taj-battery-shop-front-exide-sign.webp", 287, 510, "Taj Battery Service UPS & Solar System shop with Exide signboard, about four years ago", "The same shop about four years ago"),
    "inside": ("taj-battery-shop-inside-pehlwan-goth.webp", 680, 453, "Inside Taj Battery shop: shelves of Osaka, Exide, Phoenix and AGS batteries and battery chargers", "Batteries from Osaka, Exide, Phoenix and AGS"),
    "charging": ("battery-charging-service-karachi.webp", 680, 510, "Rows of customer batteries connected to chargers at Taj Battery, Karachi", "Customer batteries on charge"),
    "ups_repair": ("ups-repair-technician-karachi.webp", 680, 381, "Technician repairing a UPS circuit board at the Taj Battery repair bench", "UPS repair at our bench"),
    "bench": ("ups-repair-test-bench.webp", 680, 453, "UPS and inverter test bench with sockets, meters and a battery under test", "Every repaired unit is tested on load"),
    "exide": ("exide-n240-12v-180ah-battery.webp", 680, 453, "Exide N240 12 volt 180Ah battery box in stock", "Exide N240, 12 V 180 Ah"),
    "stock": ("solar-panel-cables-accessories-shop.webp", 680, 510, "Solar panel, rolls of electrical cable and accessories on display in the shop", "Solar panel, cable and accessories in stock"),
    "counter": ("taj-battery-shop-counter-battery-stock.webp", 680, 453, "Shop counter at Taj Battery with shelves of Exide, Osaka and AGS batteries and Osaka boxes stacked in front", "Car, UPS and solar batteries in stock"),
    "solar_batt": ("exide-solar-tubular-batteries-karachi.webp", 680, 381, "Exide Solar 100 and Exide HP150 tubular battery boxes with Osaka batteries at the shop desk", "Exide Solar and tubular batteries"),
    "street": ("taj-battery-shop-open-front-pehlwan-goth.webp", 680, 453, "Open front of Taj Battery Service, UPS and Solar System on Main Pehlwan Goth Road, with booster chargers and battery stock", "The shop front on Main Pehlwan Goth Road"),
    "boosters": ("battery-booster-chargers-tubular-stock.webp", 680, 453, "Booster battery chargers at the shop entrance with Phoenix tubular batteries and Osaka boxes inside", "Booster chargers for battery charging"),
    "team": ("taj-battery-team-pehlwan-goth.webp", 680, 453, "Two of the Taj Battery team at the shop, with AGS batteries and shelves of chargers and accessories", "The people you deal with at the shop"),
    "desk": ("solar-ups-repair-desk.webp", 680, 510, "Test board with switches and lights, UPS units and a solar panel at the repair desk", "Test board for UPS and solar units"),
}

def fig(key, cls="", eager=False, caption=True, cap_text=None, pre=""):
    f, w, h, alt, cap = IMG[key]
    cap = cap_text or cap
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    alt = alt.replace("&", "&amp;")
    fc = "<figcaption>%s</figcaption>" % cap if caption else ""
    return f'<figure class="ph {cls}"><img src="{pre}assets/img/{f}" width="{w}" height="{h}" {load} decoding="async" alt="{alt}">{fc}</figure>'
PHONE_E164 = "+923152020525"  # shop line for calls, as on the signboard
PHONE_LOCAL = "0315 2020525"
WA = "923152020525"  # WhatsApp, same as the shop line
WA_LOCAL = "0315 2020525"
MAPS = "https://share.google/svg2b4ibmyMFKSHeM"
FACEBOOK = "https://www.facebook.com/tajbatery"
ADDRESS = "Main Pehlwan Goth Road, near Saqa-e-Sakina Imambargah, Pehlwan Goth, Karachi"
ADDRESS_UR = "مین پہلوان گوٹھ روڈ، نزد سقائے سکینہ امام بارگاہ، پہلوان گوٹھ، کراچی"
HOURS = "Open every day, 9 am to 9 pm"

def wa(text):
    return "https://wa.me/" + WA + "?text=" + urllib.parse.quote(text)

ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.5-.3Z"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.2 11.4 11.4 0 0 0 3.6.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .6 3.6 1 1 0 0 1-.3 1Z"/></svg>'
ICON_PANEL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M5 4h14l3 12H2z"/><path d="M8.5 4 7 16M15.5 4 17 16M3.5 10h17M12 16v4M8 20h8"/></svg>'
ICON_METER = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M12 12l-2 4h4l-2 4"/></svg>'
ICON_PLUG = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0zM12 17v4"/></svg>'
ICON_BATT = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="3" y="7" width="16" height="11" rx="2"/><path d="M21 11v3M8 12.5h5M10.5 10v5"/></svg>'
ICON_SWAP = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h14l-4-4M20 16H6l4 4"/></svg>'
ICON_WRENCH = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8M14.7 6.3 13 4.6a4 4 0 0 0-5 5L3 14.6 6.4 18l5-5"/></svg>'

NAV = [
    ("index.html", "Home", "ہوم"),
    ("solar-packages.html", "Packages", "سولر پیکجز"),
    ("batteries.html", "Batteries", "بیٹریاں"),
    ("accessories.html", "Accessories", "سامان"),
    ("services.html", "Services", "خدمات"),
    ("our-shop.html", "Our Shop", "ہماری دکان"),
    ("contact.html", "Contact", "رابطہ"),
]

UR_PAGES = {"index.html", "solar-packages.html", "services.html", "contact.html"}  # pages that have an Urdu version in ur/

def bdi(x):
    """Keep numbers and units (5 kW, 0315 2020525) left-to-right inside Urdu text."""
    return '<bdi dir="ltr">%s</bdi>' % x

def nav_links(current, lang, home=True):
    out = []
    for href, label, ur in NAV:
        if not home and href == "index.html":
            continue
        if lang == "ur":
            target = href if href in UR_PAGES else "../" + href
            text = ur
        else:
            target, text = href, label
        cur = ' aria-current="page"' if href == current else ""
        out.append('<a href="%s"%s>%s</a>' % (target, cur, text))
    return "".join(out)

def header(current, lang="en"):
    pre = "../" if lang == "ur" else ""
    links = nav_links(current, lang, home=False)
    menu_links = nav_links(current, lang)
    if lang == "ur":
        switch = '<a class="lang" href="../%s" hreflang="en" lang="en">English</a>' % current
        menu, skip = "مینو", "مواد پر جائیں"
        wa_text = "السلام علیکم، مجھے سولر سسٹم کے بارے میں معلومات چاہییں۔"
    else:
        switch = '<a class="lang" href="ur/%s" hreflang="ur" lang="ur">اردو</a>' % (current if current in UR_PAGES else "index.html")
        menu, skip = "Menu", "Skip to content"
        wa_text = "Assalam o Alaikum, I want information about a solar system."
    return f'''<a class="skip" href="#main">{skip}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" lang="en" dir="ltr">
      <img src="{pre}assets/logo.svg" width="44" height="44" alt="">
      <div><b>Taj Battery</b><span>UPS &amp; Solar System</span></div>
    </a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="header-cta">
      <a class="btn btn--ghost btn--sm btn--call" href="tel:{PHONE_E164}">{ICON_PHONE}<bdi dir="ltr">{PHONE_LOCAL}</bdi></a>
      <a class="btn btn--wa btn--sm" href="{wa(wa_text)}" target="_blank" rel="noopener">{ICON_WA}<span>WhatsApp</span></a>
      {switch}
      <details class="menu"><summary>{menu}</summary><nav class="nav" aria-label="Mobile">{menu_links}</nav></details>
    </div>
  </div>
</header>'''

def footer(lang="en"):
    pre = "../" if lang == "ur" else ""
    if lang == "ur":
        pages = "".join('<li><a href="%s">%s</a></li>' % (h if h in UR_PAGES else "../" + h, u) for h, _, u in NAV)
        return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="stack">
      <h2>تاج بیٹری سروس، یو پی ایس اینڈ سولر سسٹم</h2>
      <p>2012 سے گھروں، دکانوں اور دفاتر کے لیے سولر سسٹم، بیٹریاں اور سولر کا سامان۔ دکان پہلوان گوٹھ، کراچی میں ہے اور ہم پورے کراچی میں کام کرتے ہیں۔</p>
    </div>
    <div>
      <h2>ہم کیا بیچتے ہیں</h2>
      <ul>
        <li><a href="solar-packages.html">سولر سسٹم، {bdi("3 kW")} سے {bdi("20 kW")}</a></li>
        <li><a href="../batteries.html#car">گاڑی کی ڈرائی اور عام بیٹریاں</a></li>
        <li><a href="../batteries.html#solar">سولر کی lithium اور tubular بیٹریاں</a></li>
        <li><a href="../accessories.html">سولر DC کا سامان</a></li>
        <li><a href="services.html#ups-repair">UPS اور inverter کی مرمت</a></li>
      </ul>
    </div>
    <div>
      <h2>صفحات</h2>
      <ul>{pages}</ul>
    </div>
    <div>
      <h2>رابطہ</h2>
      <ul>
        <li><a href="tel:{PHONE_E164}">کال {bdi(PHONE_LOCAL)}</a></li>
        <li><a href="https://wa.me/{WA}" target="_blank" rel="noopener">واٹس ایپ {bdi(WA_LOCAL)}</a></li>
        <li><a href="{MAPS}" target="_blank" rel="noopener">گوگل میپ پر دیکھیں</a></li>
        <li><a href="{FACEBOOK}" target="_blank" rel="noopener">فیس بک پیج</a></li>
        <li>{ADDRESS_UR}</li>
        <li>ہر روز صبح {bdi("9")} بجے سے رات {bdi("9")} بجے تک</li>
      </ul>
    </div>
    <p class="legal">&copy; <span id="year">2026</span> تاج بیٹری سروس، یو پی ایس اینڈ سولر سسٹم، پہلوان گوٹھ، کراچی۔ قیمتیں اور اسٹاک اکثر بدلتے رہتے ہیں، براہِ کرم واٹس ایپ پر تصدیق کر لیں۔</p>
  </div>
</footer>
<nav class="callbar" aria-label="کال یا واٹس ایپ">
  <a class="btn btn--blue" href="tel:{PHONE_E164}">{ICON_PHONE}کال کریں</a>
  <a class="btn btn--wa" href="{wa("السلام علیکم، مجھے سولر سسٹم کے بارے میں معلومات چاہییں۔")}" target="_blank" rel="noopener">{ICON_WA}واٹس ایپ</a>
</nav>
<script src="{pre}assets/site.js?v={JS_V}" defer></script>'''
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="stack">
      <h2>Taj Battery Service, UPS &amp; Solar System</h2>
      <p>Solar systems, batteries and solar accessories for homes, shops and offices since 2012. Based in Pehlwan Goth, Karachi, and serving all of Karachi.</p>
    </div>
    <div>
      <h2>What we sell</h2>
      <ul>
        <li><a href="solar-packages.html">Solar systems, 3 kW to 20 kW</a></li>
        <li><a href="batteries.html#car">Car batteries, dry and regular</a></li>
        <li><a href="batteries.html#solar">Solar batteries, lithium and tubular</a></li>
        <li><a href="accessories.html">Solar DC accessories</a></li>
        <li><a href="services.html#ups-repair">UPS and inverter repair</a></li>
      </ul>
    </div>
    <div>
      <h2>Pages</h2>
      <ul>{"".join('<li><a href="%s">%s</a></li>' % n[:2] for n in NAV)}</ul>
    </div>
    <div>
      <h2>Contact</h2>
      <ul>
        <li><a href="tel:{PHONE_E164}">Call {PHONE_LOCAL}</a></li>
        <li><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp {WA_LOCAL}</a></li>
        <li><a href="{MAPS}" target="_blank" rel="noopener">Find us on Google Maps</a></li>
        <li><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook page</a></li>
        <li>{ADDRESS}</li>
        <li>{HOURS}</li>
        <li><a href="ur/index.html" lang="ur">اردو میں دیکھیں</a></li>
      </ul>
    </div>
    <p class="legal">&copy; <span id="year">2026</span> Taj Battery Service, UPS &amp; Solar System, Pehlwan Goth, Karachi. Prices and stock change often, so please confirm on WhatsApp.</p>
  </div>
</footer>
<nav class="callbar" aria-label="Call or WhatsApp">
  <a class="btn btn--blue" href="tel:{PHONE_E164}">{ICON_PHONE}Call</a>
  <a class="btn btn--wa" href="{wa("Assalam o Alaikum, I want information about a solar system.")}" target="_blank" rel="noopener">{ICON_WA}WhatsApp</a>
</nav>
<script src="assets/site.js?v={JS_V}" defer></script>'''

BUSINESS = {
    "@type": "Store",
    "@id": SITE + "/#business",
    "name": NAME,
    "alternateName": ["Taj Battery & Solar System", "Taj Battery Service", "Taj Battery", "تاج بیٹری سروس"],
    "image": [SITE + "/assets/img/" + IMG[k][0] for k in ("front", "inside", "charging", "ups_repair")],
    "brand": [{"@type": "Brand", "name": b} for b in ["Osaka", "Exide", "Phoenix", "AGS", "Daewoo"]],
    "description": "Solar panel installation, hybrid and on-grid solar packages, dry and regular car batteries (Osaka, Exide, Phoenix, AGS, Daewoo), UPS repair, lithium and tubular batteries, inverters and solar accessories in Pehlwan Goth, Karachi.",
    "url": SITE + "/",
    "logo": SITE + "/assets/logo.svg",
    "telephone": PHONE_E164,
    "foundingDate": "2012",
    "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+" + WA, "contactOption": "WhatsApp", "areaServed": "PK", "availableLanguage": ["en", "ur"]},
    "hasMap": MAPS,
    "sameAs": [MAPS, FACEBOOK],
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "09:00",
        "closes": "21:00",
    }],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Products and services",
        "itemListElement": [{"@type": "OfferCatalog", "name": n} for n in [
            "Solar systems 3 kW to 20 kW (hybrid, on-grid, off-grid)",
            "Car batteries: dry and regular (Osaka, Exide, Phoenix, AGS, Daewoo)",
            "Solar and UPS batteries: lithium (LiFePO4) and tubular",
            "Solar DC accessories: DC cable, MC4, DC breakers, isolators, surge protectors",
            "Solar panels, hybrid inverters, lithium and tubular batteries",
            "UPS and inverter repair, battery charging"]],
    },
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Main Pehlwan Goth Road, near Saqa-e-Sakina Imambargah, Pehlwan Goth",
        "addressLocality": "Karachi",
        "addressRegion": "Sindh",
        "addressCountry": "PK",
    },
    "areaServed": [
        {"@type": "Place", "name": "Pehlwan Goth, Karachi"},
        {"@type": "Place", "name": "Gulistan-e-Jauhar, Karachi"},
        {"@type": "City", "name": "Karachi"},
    ],
    "knowsAbout": ["Solar panel installation", "Hybrid solar inverter", "Car battery", "Solar inverter repair", "MPPT charge controller repair", "UPS repair", "Lithium battery", "Tubular battery"],
}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, indent=1) + "</script>"

def crumbs_ld(slug, label, lang="en"):
    base = SITE + ("/ur/" if lang == "ur" else "/")
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ہوم" if lang == "ur" else "Home", "item": base},
            {"@type": "ListItem", "position": 2, "name": label, "item": base + slug},
        ],
    }

def crumbs_html(label, lang="en"):
    home = "ہوم" if lang == "ur" else "Home"
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="index.html">{home}</a></li><li aria-current="page">{label}</li></ol></nav>'

def url_for(slug, lang):
    return SITE + ("/ur/" if lang == "ur" else "/") + ("" if slug == "index.html" else slug)

def page(slug, title, desc, body, jsonld=(), canonical=None, lang="en"):
    canonical = canonical or url_for(slug, lang)
    blocks = "\n".join(ld(j) for j in jsonld)
    pre = "../" if lang == "ur" else ""
    alternates = ""
    if slug in UR_PAGES:
        alternates = (f'<link rel="alternate" hreflang="en" href="{url_for(slug, "en")}">\n'
                      f'<link rel="alternate" hreflang="ur" href="{url_for(slug, "ur")}">\n'
                      f'<link rel="alternate" hreflang="x-default" href="{url_for(slug, "en")}">')
    if lang == "en":
        # English pages are English only; the one Urdu line kept is marked class="... punch"
        body = re.sub(r'\s*<(p|span|small)\b(?![^>]*\bpunch\b)[^>]*\blang="ur"[^>]*>.*?</\1>', "", body, flags=re.S)
    html = f'''<!DOCTYPE html>
<html lang="{lang}"{' dir="rtl"' if lang == "ur" else ""}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{alternates}
<meta name="robots" content="index, follow">
<meta name="google-site-verification" content="QKkEqgPDfiFzSFv9FVwdT5i00rvNvBLs32RvsZem934">
<meta name="geo.region" content="PK-SD">
<meta name="geo.placename" content="Pehlwan Goth, Karachi">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="{"ur_PK" if lang == "ur" else "en_PK"}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/{PHOTO}">
<meta property="og:image:width" content="619">
<meta property="og:image:height" content="510">
<meta property="og:image:alt" content="Taj Battery Service, UPS &amp; Solar System shop front in Pehlwan Goth, Karachi">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#12336b">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap">
<link rel="stylesheet" href="__URDU_FONT__">
<link rel="stylesheet" href="{pre}assets/style.css?v={CSS_V}">
{blocks}
</head>
<body>
{header(slug, lang)}
<main id="main">
{body}
</main>
{footer(lang)}
</body>
</html>
'''
    out_dir = os.path.join(OUT, "ur") if lang == "ur" else OUT
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, slug), "w", encoding="utf-8") as f:
        f.write(html)

CTA = f'''<section class="cta section">
  <div class="wrap">
    <div class="stack">
      <h2>Send us your electricity bill. We'll size your system.</h2>
      <p>WhatsApp a photo of your latest K-Electric bill and tell us what you want to run. We reply with a system size and today's price.</p>
      <p class="ur" lang="ur">اپنا بجلی کا بل واٹس ایپ کریں، ہم آپ کو مناسب سولر سسٹم اور آج کی قیمت بتائیں گے۔</p>
    </div>
    <div class="btn-row">
      <a class="btn btn--wa" href="{wa("Assalam o Alaikum, I am sending my electricity bill for a solar quote.")}" target="_blank" rel="noopener">{ICON_WA}WhatsApp your bill</a>
      <a class="btn btn--ghost" style="color:var(--on-panel)" href="tel:{PHONE_E164}">{ICON_PHONE}Call {PHONE_LOCAL}</a>
    </div>
  </div>
</section>'''

# ---- Packages data (shared by home and packages page) ----
# Output estimate: ~4.2 units (kWh) per kWp per day, a typical Karachi average after losses.
PACKAGES = [
    dict(key="3kW", tag="Small home", size="3", kind="Hybrid", panels="6 × 585 W", kwp="3.51 kWp", units="≈ 14–15", month="≈ 440", roof="≈ 210 sq ft",
         inverter="4 kW hybrid", battery="5 kWh lithium or 2 tubular",
         runs=["Fans, lights, LED TV", "Refrigerator", "Water motor in daytime", "Backup during load shedding"]),
    dict(key="5kW", tag="Most popular", size="5", kind="Hybrid", panels="10 × 585 W", kwp="5.85 kWp", units="≈ 24–25", month="≈ 740", roof="≈ 350 sq ft",
         inverter="6 kW hybrid", battery="5 kWh lithium",
         runs=["One 1.5-ton inverter AC in daytime", "Fridge, fans, lights, motor", "Backup during load shedding", "Monitoring on your phone"], top=True),
    dict(key="10kW", tag="Large home", size="10", kind="Hybrid / On-grid", panels="18 × 585 W", kwp="10.5 kWp", units="≈ 44", month="≈ 1,330", roof="≈ 630 sq ft",
         inverter="10 kW hybrid or on-grid", battery="Optional, 10 kWh lithium",
         runs=["Two or three inverter ACs in daytime", "Whole-house load", "Cuts most of the monthly bill", "Net metering ready (service coming soon)"]),
    dict(key="15kW", tag="Shop / office", size="15–20", kind="On-grid, 3-phase", panels="26–34 × 585 W", kwp="15–20 kWp", units="≈ 64–84", month="≈ 1,900–2,500", roof="≈ 900–1,200 sq ft",
         inverter="3-phase on-grid", battery="Optional",
         runs=["Shops, clinics, schools, offices", "Multiple ACs and machines", "Monitoring on your phone", "Net metering ready (service coming soon)"]),
]

def pkg_card(p, full):
    runs = "".join("<li>%s</li>" % r for r in (p["runs"] if full else p["runs"][:3]))
    details = ""
    if full:
        details = f'''<dl class="num">
    <dt>Panels</dt><dd>{p['panels']}</dd>
    <dt>Inverter</dt><dd>{p['inverter']}</dd>
    <dt>Battery</dt><dd>{p['battery']}</dd>
  </dl>'''
    return f'''<article class="card pkg{' pkg--top' if p.get('top') else ''}" id="pkg-{p['key']}">
  <span class="tag">{p['tag']}</span>
  <div><h3 class="size"><a href="package-{p['key'].lower()}.html">{p['size']}<small> kW</small></a></h3><p class="kind">{p['kind']}</p></div>
  <p class="units num"><b>{p['units']}</b> units a day</p>
  {details}
  <ul>{runs}</ul>
  <a class="more" href="package-{p['key'].lower()}.html">See what it runs</a>
  <a class="btn {'btn--sun' if p.get('top') else 'btn--blue'}" href="contact.html?need={p['key']}">Get price</a>
</article>'''

EST_NOTE = '<p class="note">Units per day are typical for Karachi; actual output varies by season.</p>'

# ---- FAQ (home page, with FAQPage schema) ----
FAQ = [
    ("How much does a solar system cost in Karachi?",
     "Panel, inverter and battery prices change almost every week, so we quote on the day. Send your bill and the appliances you want to run on WhatsApp at " + WA_LOCAL + " and we reply with a price for the full installed system."),
    ("What size of solar system do I need?",
     "Look at the units on your K-Electric bill. Divide your monthly units by about 125 to get the kW you need. For example, 600 units a month needs roughly a 5 kW system. We check this properly during the site visit."),
    ("Will solar work during load shedding?",
     "Only hybrid and off-grid systems keep running during load shedding, because they have a battery. A plain on-grid system switches off when K-Electric power goes, for safety. Our 3 kW and 5 kW packages are hybrid for this reason."),
    ("Do you sell car batteries?",
     "Yes. We sell Osaka, Exide, Phoenix, AGS and Daewoo car batteries for most cars, both dry (maintenance-free) and regular, and fit them at the shop in Pehlwan Goth. WhatsApp your car model for the right battery and today's price."),
    ("Do you do K-Electric net metering?",
     "Net metering is coming soon. Our on-grid and hybrid systems are net metering ready, so you can apply once the service starts. Message us on WhatsApp and we'll let you know."),
    ("Do you only work in Pehlwan Goth?",
     "Our shop is in Pehlwan Goth, near Gulistan-e-Jauhar, and we install across Karachi. Message us your area for a site visit."),
    ("What warranty do I get?",
     "Panels, inverters and batteries carry the manufacturer's warranty, and we hand over the warranty cards with the system. Ask us about the warranty of the exact brand you choose."),
]
FAQ_LD = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
}
faq_html = "".join("<details><summary>%s</summary><p>%s</p></details>" % qa for qa in FAQ)

# ================= HOME =================
SWAP_BANNER = f'''<a class="swap" href="{wa("Assalam o Alaikum, I want to exchange my old battery for a new one. My battery / car: ")}" target="_blank" rel="noopener">
  <span class="swap-icon">{ICON_SWAP}</span>
  <span class="swap-text"><b>Battery exchange:</b> give your old battery, take a new one, pay only the difference.</span>
  <span class="swap-cta">Ask the price on WhatsApp</span>
</a>'''
home = f'''{SWAP_BANNER}
<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow">Solar installation · Pehlwan Goth, Karachi</span>
      <h1>Solar systems for homes and shops in Pehlwan Goth, Karachi</h1>
      <p class="ur ur-line punch" lang="ur">بجلی کے بھاری بلوں اور لوڈ شیڈنگ سے نجات — مکمل سولر سسٹم، تنصیب کے ساتھ</p>
      <p class="lead">Cut your K-Electric bill and keep the fans on in load shedding. Hybrid and on-grid packages from 3 kW to 20 kW, installed by our own team.</p>
      <div class="btn-row">
        <a class="btn btn--sun" href="solar-packages.html">See solar packages</a>
        <a class="btn btn--wa" href="{wa("Assalam o Alaikum, I want a solar quote.")}" target="_blank" rel="noopener">{ICON_WA}Get a quote on WhatsApp</a>
      </div>
    </div>
    <aside class="spec" aria-labelledby="spec-title">
      <span class="eyebrow">Our most popular system</span>
      <h2 id="spec-title"><a href="package-5kw.html">5 kW hybrid for a family home</a></h2>
      <dl>
        <dt>Solar panels</dt><dd>10 × 585 W N-type</dd>
        <dt>Array size</dt><dd>5.85 kWp</dd>
        <dt>Inverter</dt><dd>6 kW hybrid</dd>
        <dt>Battery</dt><dd>5 kWh lithium</dd>
        <dt>Units per day</dt><dd class="big">≈ 24</dd>
        <dt>Runs</dt><dd>1.5-ton inverter AC by day</dd>
      </dl>
      <small>Estimate for Karachi sunshine. Actual output depends on season, dust and shading.</small>
    </aside>
  </div>
</section>

<div class="facts">
  <a href="solar-packages.html"><b>3 kW to 20 kW</b><span>Hybrid, on-grid and off-grid systems</span></a>
  <a href="batteries.html#car"><b>Car batteries</b><span>Dry and regular. Osaka, Exide, Phoenix, AGS, Daewoo</span></a>
  <a href="accessories.html"><b>Full accessories</b><span>Structure, cables, breakers, batteries</span></a>
  <a href="our-shop.html"><b>Since 2012</b><span>Our shop in Pehlwan Goth, Karachi</span></a>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Solar packages</span>
      <h2>Pick a system by the load you want to run</h2>
      <p>Every package includes panels, inverter, mounting structure, DC and AC wiring, breakers, surge protection, earthing and installation.</p>
      <p class="ur" lang="ur">ہر پیکج میں پینل، انورٹر، اسٹرکچر، وائرنگ، بریکر، ارتھنگ اور تنصیب شامل ہے۔</p>
    </div>
    <div class="grid grid-4 swipe">{"".join(pkg_card(p, False) for p in PACKAGES)}</div>
    <p class="note" style="margin-top:16px">Unit estimates for Karachi. <a href="solar-packages.html">Full package details and comparison</a>.</p>
  </div>
</section>

<section class="section section--alt" id="car-batteries">
  <div class="wrap media-row carbat">
    {fig("exide", caption=False)}
    <div class="stack">
      <span class="eyebrow">Car batteries</span>
      <h2>Car batteries, fitted at the shop</h2>
      <p class="ur" lang="ur">گاڑی کی بیٹری — اوساکا، ایکسائیڈ، فینکس</p>
      <p>Dry (maintenance-free) and regular batteries for most cars, from Osaka, Exide, Phoenix, AGS and Daewoo. Bring your car to our shop, or call us and we come to you. We check your old battery, fit the new one and test the charging.</p>
      <ul class="brands"><li>Osaka</li><li>Exide</li><li>Phoenix</li><li>AGS</li><li>Daewoo</li></ul>
      <div class="btn-row"><a class="btn btn--wa" href="{wa("Assalam o Alaikum, I need a car battery. My car is: ")}" target="_blank" rel="noopener">{ICON_WA}Send your car model for a price</a><a class="btn btn--blue" href="tel:{PHONE_E164}">{ICON_PHONE}Call {PHONE_LOCAL}</a></div>
      <p><a class="more" href="batteries.html">Car and solar batteries: dry vs regular, lithium vs tubular</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap shop">
    {fig("front", caption=False)}
    <div class="stack">
      <span class="eyebrow">Visit the shop</span>
      <h2>Pehlwan Goth's battery and solar shop since 2012</h2>
      <p class="visit"><b>{ADDRESS}</b><br>{HOURS}</p>
      <p>Since 2012, families and shops around Pehlwan Goth have come to us for batteries, UPS and solar systems. Come and see panels, inverters and batteries in person before you buy.</p>
      <p class="ur" lang="ur">تاج بیٹری سروس، یو پی ایس اینڈ سولر سسٹم — پہلوان گوٹھ، کراچی</p>
      <p>We sell Osaka, Exide, Phoenix, AGS and Daewoo batteries, repair UPS units, and test, charge and replace batteries at the shop. <a href="services.html#batteries">Battery and UPS services</a></p>
      <div class="btn-row"><a class="btn btn--sun btn--sm" href="our-shop.html">See inside the shop</a><a class="btn btn--ghost btn--sm" href="{MAPS}" target="_blank" rel="noopener">Get directions</a><a class="btn btn--ghost btn--sm" href="tel:{PHONE_E164}">{ICON_PHONE}Call {PHONE_LOCAL}</a></div>
    </div>
  </div>
</section>

<section class="section strip-section" aria-label="Photos from the shop">
  <div class="wrap strip swipe">{fig("inside")}{fig("charging")}{fig("ups_repair")}{fig("stock")}</div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What we do</span>
      <h2>Everything for solar, from the roof to the inverter</h2>
    </div>
    <div class="grid grid-3">
      <article class="card">
        <div class="icon">{ICON_PANEL}</div>
        <h3>Solar installation</h3>
        <p>Site visit, load calculation, raised or flat-roof structure, neat wiring and a tested handover with app monitoring.</p>
        <p class="ur" lang="ur">گھروں، دکانوں اور دفاتر کے لیے مکمل سولر تنصیب</p>
        <a class="more" href="services.html#installation">How installation works</a>
      </article>
      <article class="card card--soon">
        <div class="icon">{ICON_METER}</div>
        <h3>K-Electric net metering <span class="soon">Coming soon</span></h3>
        <p>Sell extra daytime units back to K-Electric. Our systems are net metering ready, and the application service is coming soon.</p>
        <p class="ur" lang="ur">نیٹ میٹرنگ — جلد آرہا ہے</p>
        <a class="more" href="services.html#net-metering">How it will work</a>
      </article>
      <article class="card">
        <div class="icon">{ICON_PLUG}</div>
        <h3>Solar accessories</h3>
        <p>Panels, hybrid and on-grid inverters, lithium and tubular batteries, structures, solar cable, MC4, DC breakers and surge protectors.</p>
        <p class="ur" lang="ur">سولر کا تمام سامان ایک ہی جگہ</p>
        <a class="more" href="accessories.html">Browse accessories</a>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Questions</span>
      <h2>Common questions about solar in Karachi</h2>
    </div>
    <div class="faq">{faq_html}</div>
  </div>
</section>
{CTA}'''

page("index.html",
     "Solar Systems, Inverters & Batteries in Pehlwan Goth, Karachi",
     "Solar systems 3–20 kW, solar panels, inverters and inverter repair, car and solar batteries (Osaka, Exide, AGS, Daewoo) in Pehlwan Goth, Karachi. 0315 2020525.",
     home, [dict({"@context": "https://schema.org"}, **BUSINESS), FAQ_LD])

# ================= PACKAGES =================
pk = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("Solar Packages")}
      <h1>Solar system packages for Karachi homes and shops</h1>
      <p class="ur ur-line" lang="ur">سولر پیکجز — ۳ کلوواٹ سے ۲۰ کلوواٹ تک، تنصیب کے ساتھ</p>
      <p class="lead">Four standard systems with installation included. Each one can be adjusted to your roof, your load and your budget.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Packages</span>
      <h2>Installed system packages</h2>
      <p>Included in every package: panels, inverter, galvanised mounting structure, solar DC cable, MC4 connectors, DC and AC breakers, surge protector, earthing, installation and testing.</p>
    </div>
    <div class="grid grid-2">{"".join(pkg_card(p, True) for p in PACKAGES)}</div>
    <div style="margin-top:16px">{EST_NOTE}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">System types</span>
      <h2>On-grid, hybrid or off-grid?</h2>
    </div>
    <div class="grid grid-3">
      <article class="card"><h3>On-grid</h3><p>Lowest price. Cuts the bill, but switches off in load shedding.</p></article>
      <article class="card"><h3>Hybrid</h3><p>Cuts the bill and keeps running in load shedding, with a battery.</p></article>
      <article class="card"><h3>Off-grid</h3><p>For places without a K-Electric connection.</p></article>
    </div>
  </div>
</section>

{CTA}'''

PKG_LD = {
    "@context": "https://schema.org",
    "@type": "Service",
    "serviceType": "Solar system installation",
    "provider": {"@id": SITE + "/#business"},
    "areaServed": {"@type": "City", "name": "Karachi"},
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Solar packages",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "%s kW %s solar system" % (p["size"], p["kind"]),
             "description": "%s panels (%s), %s inverter, about %s units per day in Karachi." % (p["panels"], p["kwp"], p["inverter"], p["units"].replace("≈ ", ""))}}
            for p in PACKAGES
        ],
    },
}
page("solar-packages.html",
     "Solar System Packages in Karachi: 3, 5, 10 & 15 kW | Taj Battery",
     "3 kW, 5 kW, 10 kW and 15–20 kW solar packages with installation in Karachi. Panels, hybrid inverter and lithium battery backup. Shop in Pehlwan Goth. Call 0315 2020525.",
     pk, [crumbs_ld("solar-packages.html", "Solar Packages"), PKG_LD])

# ================= ACCESSORIES =================
CATS = [
    ("panels", "Solar panels", "سولر پینل", [
        ("N-type mono panels", "580–620 W class, A-grade. Brands such as Longi, Jinko and JA Solar, depending on stock."),
        ("Bifacial panels", "Generate extra from light reflected off the roof. Best on raised structures."),
        ("Used and B-grade panels", "Lower-cost option. Ask us what's available and what warranty applies."),
    ]),
    ("inverters", "Inverters", "انورٹر", [
        ("Hybrid inverters", "Solar, battery and K-Electric together. 4 kW to 12 kW."),
        ("On-grid inverters", "For net metering systems. Single-phase and 3-phase."),
        ("Home UPS and solar UPS", "Backup for fans and lights. Sales, repair and battery pairing."),
        ("Off-grid inverters", "For places without a K-Electric connection."),
        ("Wi-Fi monitoring dongle", "See your solar production on your phone."),
    ]),
    ("batteries", "Batteries", "بیٹریاں", [
        ("Dry car batteries", "Maintenance-free car batteries, no water top-up. Osaka, Exide, Phoenix, AGS and Daewoo, fitted at the shop."),
        ("Regular car batteries", "Standard (water) car batteries for most cars, from the same brands, fitted at the shop."),
        ("Bike batteries", "Batteries for motorbikes and rickshaws."),
        ("Lithium (LiFePO4) batteries", "2.5, 5 and 10 kWh. Long life, no water top-up."),
        ("Tubular batteries", "Osaka, Exide, Phoenix, AGS and Daewoo deep-cycle batteries for UPS and solar."),
        ("Battery cables and lugs", "Copper cables and lugs to connect battery banks safely."),
    ], "exide"),
    ("structures", "Mounting structures", "اسٹرکچر", [
        ("Raised (elevated) structure", "Galvanised iron frame that keeps the roof usable underneath."),
        ("Flat-roof structure", "Standard tilted frame for rooftop installations."),
        ("Rails, clamps and bolts", "End clamps, mid clamps and fasteners for panel fitting."),
    ]),
    ("wiring", "Solar DC cables and connectors", "تار اور کنیکٹر", [
        ("Solar DC cable 4 mm² / 6 mm²", "UV-resistant cable from panels to inverter."),
        ("MC4 connectors", "Waterproof panel connectors and MC4 branch connectors."),
        ("AC cable", "Inverter to distribution board wiring."),
    ], "stock"),
    ("protection", "DC and AC protection", "حفاظتی سامان", [
        ("DC breakers and isolators", "Switch off and protect the solar side."),
        ("Surge protector (SPD)", "Protects inverter and panels from lightning and voltage spikes."),
        ("DB / combiner box", "Weather-proof box for breakers and fuses."),
        ("Earthing kit", "Copper earth rod and wire. Every system needs proper earthing."),
        ("Changeover switch", "Switch loads between solar, K-Electric and generator."),
    ]),
    ("care", "Care and extras", "دیکھ بھال", [
        ("Panel cleaning kit", "Brush and pole for washing dust off panels."),
        ("Voltage stabilisers", "For ACs and fridges on unstable supply."),
        ("Ceiling fans and LED lights", "Energy-saving fans and lights for UPS and solar homes."),
    ]),
]
cat_html = []
for cid, title, ur, items, *photo in CATS:
    lis = "".join(
        '<li><b>%s</b><span>%s</span><a href="%s" target="_blank" rel="noopener">Ask price on WhatsApp</a></li>'
        % (n, d, wa("Assalam o Alaikum, what is the price of: " + n + "?"))
        for n, d in items)
    cat_html.append(f'<section class="cat" id="{cid}" aria-labelledby="h-{cid}"><h3 id="h-{cid}">{title} <span class="ur" lang="ur">{ur}</span></h3>{('<div class="cat-media">' + fig(photo[0]) + '<ul class="items">' + lis + '</ul></div>') if photo else '<ul class="items">' + lis + '</ul>'}</section>')
jump = "".join('<a href="#%s">%s</a>' % (c[0], c[1]) for c in CATS)

acc = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("Accessories")}
      <h1>Solar panels, inverters, batteries and DC accessories in Karachi</h1>
      <p class="ur ur-line" lang="ur">سولر کا تمام سامان — پینل، انورٹر، بیٹری، اسٹرکچر اور وائرنگ</p>
      <p class="lead">Buy the full system or just the parts: solar panels (solar plates), inverters, batteries and wiring. Prices change often, so tap any item to ask today's rate on WhatsApp.</p>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Solar DC accessories</span>
      <h2>Everything between the panels and the inverter</h2>
      <p>Solar DC cable (4 mm² and 6 mm²), MC4 connectors, DC breakers, DC isolators, surge protectors (SPD), combiner boxes and earthing kits, plus panels, inverters, batteries and mounting structures. Buy single items for repairs or a full set for a new system.</p>
    </div>
    <nav class="jump" aria-label="Categories">{jump}</nav>
    <div class="stack" style="gap:44px">{"".join(cat_html)}</div>
  </div>
</section>
{CTA}'''
page("accessories.html",
     "Solar DC Accessories, Panels & Inverters in Karachi | Taj Battery",
     "Solar DC cable 4 mm² and 6 mm², MC4, DC breakers, isolators and surge protectors, plus panels, inverters and batteries. Pehlwan Goth, Karachi. 0315 2020525.",
     acc, [crumbs_ld("accessories.html", "Accessories")])

# ================= BATTERIES (car + solar) =================
BRANDS = ["Osaka", "Exide", "Phoenix", "AGS", "Daewoo"]
CARS = ["Suzuki Alto", "Suzuki Mehran", "Suzuki Cultus", "Suzuki Wagon R", "Suzuki Bolan", "Toyota Corolla", "Toyota Yaris", "Honda City", "Honda Civic", "Daihatsu Cuore", "KIA Picanto", "Hyundai, Changan and more"]
CB_FAQ = [
    ("How much is a car battery in Karachi?",
     "It depends on the battery size your car needs, the brand, and whether you choose dry or regular. Prices change often, so WhatsApp your car model and year to " + WA_LOCAL + " and we reply with today's price for each brand."),
    ("Dry or regular battery: which is better?",
     "A dry (maintenance-free) battery never needs water top-up, so it suits people who don't want to check it. A regular battery costs less but its water level should be checked regularly. Both start the car the same way; we help you choose for your budget."),
    ("Which battery fits my car?",
     "Send us your car model and year. We match the right size (Ah) and terminal layout and tell you which Osaka, Exide, Phoenix, AGS or Daewoo batteries fit."),
    ("Do you fit the battery?",
     "Yes. Bring your car to our shop in Pehlwan Goth, or call us and we come to you. We fit the new battery and check that the car's charging is working."),
    ("Do you take the old battery?",
     "Yes. Bring your old battery, take a new one and pay only the price difference. WhatsApp us your old battery's brand and size for the exact amount."),
    ("Lithium or tubular battery for solar?",
     "Lithium lasts much longer, needs no maintenance and handles daily solar charging better, but costs more. Tubular costs less and works well for UPS backup, but needs water top-up and is replaced sooner. Tell us your inverter and the backup hours you need and we suggest the right one."),
    ("Can I add a battery to my existing solar system?",
     "Yes, if your inverter is hybrid or off-grid. A plain on-grid inverter cannot use a battery, so it needs a hybrid inverter first. Send us a photo of your inverter's label on WhatsApp and we check."),
    ("My car won't start. Can you help?",
     "If you are near Pehlwan Goth, call " + PHONE_LOCAL + " for a jump start. If the battery is finished, we can fit a new one at the shop."),
]
CB_FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in CB_FAQ]}
cb = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("Batteries")}
      <h1>Car and solar batteries in Karachi</h1>
      <p class="lead">Dry and regular car batteries, and lithium and tubular batteries for solar and UPS, from our shop in Pehlwan Goth. Osaka, Exide, Phoenix, AGS and Daewoo.</p>
      <div class="btn-row">
        <a class="btn btn--sun" href="#car">Car batteries</a>
        <a class="btn btn--sun" href="#solar">Solar batteries</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="car">
  <div class="wrap media-row carbat">
    {fig("exide", caption=False)}
    <div class="stack">
      <span class="eyebrow">Car batteries</span>
      <h2>Car batteries: Osaka, Exide, Phoenix, AGS and Daewoo</h2>
      <p>Dry and regular batteries for most cars, fitted the same day at our Pehlwan Goth shop.</p>
      <ul class="brands">{"".join("<li>%s</li>" % b for b in BRANDS)}</ul>
      <div class="btn-row"><a class="btn btn--wa" href="{wa("Assalam o Alaikum, I need a car battery. My car model and year: ")}" target="_blank" rel="noopener">{ICON_WA}WhatsApp your car model</a><a class="btn btn--blue" href="tel:{PHONE_E164}">{ICON_PHONE}Call {PHONE_LOCAL}</a></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="duo">
      <article class="card"><h3>Dry (maintenance-free)</h3><p>No water top-up, ever.</p></article>
      <article class="card"><h3>Regular</h3><p>Lower price. Check the water now and then.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Your car</span>
      <h2>Batteries for popular cars in Pakistan</h2>
      <p>Tell us your car model and year. We match the right size and terminal layout.</p>
    </div>
    <ul class="brands cars">{"".join("<li>%s</li>" % c for c in CARS)}</ul>
  </div>
</section>

<section class="section section--alt" id="solar">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Solar batteries</span>
      <h2>Solar and UPS batteries: lithium and tubular</h2>
      <p>Lithium in 2.5, 5 and 10 kWh, and tubular batteries from Osaka, Exide, Phoenix, AGS and Daewoo.</p>
    </div>
    <div class="duo">
      <article class="card"><h3>Lithium (LiFePO4)</h3><p>Lasts longest, no maintenance. Best for hybrid solar.</p></article>
      <article class="card"><h3>Tubular</h3><p>Lower price. Good for UPS backup.</p></article>
    </div>
    <div class="strip strip--2" style="margin-top:20px">{fig("solar_batt")}{fig("counter")}</div>
    <div class="btn-row" style="margin-top:20px">
      <a class="btn btn--wa" href="{wa("Assalam o Alaikum, I need a solar / UPS battery. My inverter or UPS is: ")}" target="_blank" rel="noopener">{ICON_WA}Ask about solar batteries</a>
      <a class="btn btn--blue" href="solar-packages.html">See solar packages</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">At the shop</span>
      <h2>Battery check, fitting and exchange</h2>
      <p>For car, UPS and solar batteries.</p>
    </div>
    <div class="grid grid-3">
      <article class="card"><div class="icon">{ICON_BATT}</div><h3>Battery check</h3><p>We test your battery and the car's charging, so you only replace the battery if it really needs it.</p></article>
      <article class="card"><div class="icon">{ICON_WRENCH}</div><h3>Fitting and battery exchange</h3><p>Give your old battery, take a new one, pay only the difference. Fitted at the shop.</p></article>
      <article class="card"><div class="icon">{ICON_PHONE}</div><h3>Jump start nearby</h3><p>Car won't start near Pehlwan Goth? Call {PHONE_LOCAL}.</p></article>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Questions</span>
      <h2>Battery questions</h2>
    </div>
    <div class="faq">{"".join("<details><summary>%s</summary><p>%s</p></details>" % qa for qa in CB_FAQ)}</div>
  </div>
</section>
{CTA}'''
page("batteries.html",
     "Car & Solar Batteries in Karachi: Lithium, Tubular | Taj Battery",
     "Dry and regular car batteries, lithium and tubular solar batteries. Osaka, Exide, Phoenix, AGS, Daewoo. Pehlwan Goth, Karachi. WhatsApp 0315 2020525.",
     cb, [crumbs_ld("batteries.html", "Batteries"), CB_FAQ_LD])

# ================= SERVICES =================
STEPS = [
    ("Site visit and load check", "We visit your home or shop, check the roof, shading and direction, and list the appliances you want to run."),
    ("System design and quote", "You get a written quote with panel count, inverter, battery and structure, at the day's price."),
    ("Installation", "Our team fits the structure, panels, inverter, battery, wiring, breakers, surge protection and earthing."),
    ("Testing and handover", "We test the system, set up monitoring on your phone and show you how to use it."),
    ("Ready for net metering", "Your system is set up so it can be net metered later. Our net metering application service is coming soon."),
    ("After-sales support", "Call or WhatsApp us for faults, cleaning, upgrades or adding batteries later."),
]
steps_html = "".join("<li><h3>%s</h3><p>%s</p></li>" % s for s in STEPS)

svc = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("Services")}
      <h1>Solar installation, inverter and UPS repair, battery services</h1>
      <p class="ur ur-line" lang="ur">سولر تنصیب، نیٹ میٹرنگ، مینٹیننس اور بیٹری سروس</p>
      <p class="lead">From the first site visit to years of after-sales support, one team handles your system.</p>
    </div>
  </div>
</section>

<section class="section" id="installation">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Installation</span>
      <h2>How a solar installation works</h2>
      <p>A typical 5 kW home system is installed in one to two days after the order is confirmed.</p>
    </div>
    <ol class="steps">{steps_html}</ol>
  </div>
</section>

<section class="section section--alt" id="net-metering">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">K-Electric</span>
      <h2>Net metering in Karachi <span class="soon">Coming soon</span></h2>
      <p>With net metering, extra units your panels produce in the day go to K-Electric and are adjusted against your bill. We are getting ready to handle net metering applications. Here is how it will work.</p>
      <p class="ur" lang="ur">دن میں اضافی بجلی کے الیکٹرک کو دیں اور اپنے بل میں کمی لائیں۔</p>
    </div>
    <div class="grid grid-2">
      <article class="card">
        <h3>What you need</h3>
        <ul>
          <li>Copy of CNIC of the meter owner</li>
          <li>Latest K-Electric bill</li>
          <li>Proof of ownership or tenancy of the property</li>
          <li>An installed on-grid or hybrid system</li>
        </ul>
      </article>
      <article class="card">
        <h3>What we will do</h3>
        <ul>
          <li>Prepare the application and system drawings</li>
          <li>Submit the file and follow up with K-Electric</li>
          <li>Coordinate the inspection</li>
          <li>Stay with you until the green meter is fitted</li>
        </ul>
      </article>
    </div>
    <p class="note" style="margin-top:16px">Net metering rules and buy-back rates are set by NEPRA and can change. Ask us about the current rules before you decide.</p>
  </div>
</section>

<section class="section" id="maintenance">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Maintenance</span>
      <h2>Keep your system producing</h2>
      <p>Karachi dust can cut panel output noticeably within a few weeks. Regular cleaning and checks keep your units up.</p>
    </div>
    <div class="grid grid-3">
      <article class="card"><div class="icon">{ICON_PANEL}</div><h3>Panel washing</h3><p>Washing and inspection of panels, clamps and connectors.</p></article>
      <article class="card"><div class="icon">{ICON_WRENCH}</div><h3>Fault repair</h3><p>Inverter error codes, tripping breakers, low output and wiring faults.</p></article>
      <article class="card"><div class="icon">{ICON_PLUG}</div><h3>Upgrades and shifting</h3><p>Add panels or batteries, change the inverter, or move a system to a new house.</p></article>
    </div>
  </div>
</section>

<section class="section section--alt" id="ups-repair">
  <div class="wrap media-row">
    {fig("ups_repair")}
    <div class="stack">
      <span class="eyebrow">Inverter, MPPT and UPS repair</span>
      <h2>Inverter and UPS repair at our own bench</h2>
      <p>Solar inverter showing an error, MPPT controller not charging, or UPS beeping and switching off under load? Bring it to the shop. We repair the circuit boards, replace faulty parts and test every unit on load before it goes back.</p>
      <p class="ur" lang="ur">یو پی ایس اور انورٹر کی مرمت — دکان پر ٹیسٹنگ کے ساتھ</p>
      <ul>
        <li>Solar and hybrid inverter repair</li>
        <li>MPPT and solar charge controller repair</li>
        <li>Home UPS repair, charging faults and battery pairing</li>
        <li>Inverter fitting and replacement</li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="batteries">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Batteries</span>
      <h2>Battery services</h2>
      <p>Bring your battery to the shop in Pehlwan Goth, or call us.</p>
    </div>
    <div class="grid grid-3">
      <article class="card"><div class="icon">{ICON_BATT}</div><h3>Testing and charging</h3><p>Health check and charging for UPS, tubular and car batteries.</p></article>
      <article class="card"><div class="icon">{ICON_BATT}</div><h3>Replacement</h3><p>Lithium, tubular and car batteries, fitted at the shop. Give your old battery and pay only the difference.</p><a class="more" href="batteries.html">Car and solar batteries</a></article>
      <article class="card"><div class="icon">{ICON_PHONE}</div><h3>Car jump start</h3><p>Car won't start nearby? Call {PHONE_LOCAL} and we'll come to you.</p></article>
    </div>
    <div class="strip strip--2" style="margin-top:20px">{fig("charging")}{fig("boosters")}</div>
  </div>
</section>
{CTA}'''

SVC_LD = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "provider": {"@id": SITE + "/#business"}, "areaServed": "Karachi"}}
        for i, n in enumerate(["Solar system installation", "Solar panel cleaning and maintenance", "Solar inverter and MPPT repair", "UPS repair", "Battery testing, charging and replacement", "Car battery jump start"])
    ],
}
page("services.html",
     "Solar Inverter, MPPT & UPS Repair in Karachi | Taj Battery",
     "Solar inverter, MPPT and UPS repair, inverter fitting, solar installation and panel cleaning, plus battery charging. Pehlwan Goth, Karachi. 0315 2020525.",
     svc, [crumbs_ld("services.html", "Services"), SVC_LD])

# ================= OUR SHOP =================
GALLERY = ["front", "street", "team", "counter", "inside", "charging", "boosters", "ups_repair", "bench", "desk", "stock", "solar_batt", "exide", "front_old"]
shop = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("Our Shop")}
      <h1>Our shop in Pehlwan Goth, Karachi</h1>
      <p class="ur ur-line" lang="ur">تاج بیٹری سروس، یو پی ایس اینڈ سولر سسٹم</p>
      <p class="lead">Batteries, UPS repair and solar under one roof. Come in, see the stock and talk to the people who will install your system.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap media-row media-row--tall">
    {fig("front_old")}
    <div class="stack">
      <span class="eyebrow">About us</span>
      <h2>Batteries, UPS and solar in Pehlwan Goth since 2012</h2>
      <p>Taj Battery Service opened in Pehlwan Goth in 2012. Since then, families and shopkeepers have come to us for batteries, UPS units, charging and repairs, and for solar systems. We design and install complete solar systems for homes, shops and offices across Karachi.</p>
      <p>When you buy solar from us, you deal with a shop you can walk into. If something needs attention later, you know where to find us.</p>
      <ul>
        <li>Dry and regular car batteries and UPS batteries from Osaka, Exide, Phoenix, AGS and Daewoo</li>
        <li>UPS and inverter repair at our own bench</li>
        <li>Solar panels, inverters, cables and accessories</li>
        <li>Complete solar installation (net metering coming soon)</li>
      </ul>
      <div class="btn-row"><a class="btn btn--sun" href="solar-packages.html">See solar packages</a><a class="btn btn--ghost" href="{MAPS}" target="_blank" rel="noopener">Get directions</a></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Photos</span>
      <h2>Inside Taj Battery</h2>
    </div>
    <div class="gallery">{"".join(fig(k) for k in GALLERY)}</div>
  </div>
</section>
{CTA}'''
page("our-shop.html",
     "Our Shop in Pehlwan Goth, Karachi | Taj Battery Service, UPS & Solar",
     "Visit Taj Battery Service, UPS & Solar System in Pehlwan Goth, Karachi. Osaka, Exide, Phoenix, AGS and Daewoo batteries, UPS repair, battery charging, solar panels and accessories. Call 0315 2020525.",
     shop, [crumbs_ld("our-shop.html", "Our Shop")])

# ================= CONTACT =================
opts = [p["key"] + " solar system" for p in PACKAGES] + ["Accessories / parts only", "Car battery", "UPS / home batteries", "Maintenance or repair", "Not sure yet"]
opts_html = "".join("<option>%s</option>" % o for o in opts)
con = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("Contact")}
      <h1>Contact Taj Battery &amp; Solar in Pehlwan Goth</h1>
      <p class="ur ur-line" lang="ur">ہم سے رابطہ کریں — کال یا واٹس ایپ</p>
      <p class="lead">Call, WhatsApp, or visit the shop. Fill in the form and it opens WhatsApp with your details ready to send.</p>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap contact">
    <div class="stack" style="gap:24px">{fig("front", "shop-photo", caption=False)}
    <dl class="nap">
      <div><dt>Phone</dt><dd><a href="tel:{PHONE_E164}">{PHONE_LOCAL}</a></dd></div>
      <div><dt>WhatsApp</dt><dd><a href="https://wa.me/{WA}" target="_blank" rel="noopener">+92 315 2020525</a></dd></div>
      <div><dt>Shop</dt><dd>Main Pehlwan Goth Road, near Saqa-e-Sakina Imambargah, Pehlwan Goth, Karachi</dd></div>
      <div><dt>Opening hours</dt><dd>Every day, 9 am to 9 pm</dd></div>
      <div><dt>Facebook</dt><dd><a href="{FACEBOOK}" target="_blank" rel="noopener">facebook.com/tajbatery</a></dd></div>
      <div><dt>Map</dt><dd><a href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps</a></dd></div>
      <div><dt>Service area</dt><dd style="font-weight:400">Pehlwan Goth, Gulistan-e-Jauhar (Johar) and all of Karachi</dd></div>
    </dl></div>
    <form class="quote" id="quote-form">
      <h2 style="font-size:1.6rem">Request a quote</h2>
      <label for="name">Your name<input id="name" name="name" required autocomplete="name"></label>
      <label for="area">Area in Karachi<input id="area" name="area" required placeholder="e.g. Pehlwan Goth, Gulistan-e-Jauhar"></label>
      <label for="need">What do you need?<select id="need" name="need">{opts_html}</select></label>
      <label for="bill">Monthly bill or units <span class="hint">(optional)</span><input id="bill" name="bill" placeholder="e.g. 650 units or Rs 40,000"></label>
      <label for="msg">Anything else <span class="hint">(optional)</span><textarea id="msg" name="msg" placeholder="Appliances you want to run, roof type, timing"></textarea></label>
      <button class="btn btn--wa" type="submit">{ICON_WA}Send on WhatsApp</button>
    </form>
  </div>
</section>'''
page("contact.html",
     "Contact Taj Battery & Solar, Pehlwan Goth Karachi | 0315 2020525",
     "Call or WhatsApp 0315 2020525 for solar quotes, batteries and accessories. Taj Battery & Solar System, Pehlwan Goth, Karachi.",
     con, [crumbs_ld("contact.html", "Contact"), dict({"@context": "https://schema.org"}, **BUSINESS)])

# ================= 404 =================
nf = f'''<section class="hero hero-sm">
  <div class="wrap"><div class="hero-copy">
    <h1>Page not found</h1>
    <p class="lead">This page doesn't exist. Try the solar packages or contact us on WhatsApp.</p>
    <div class="btn-row"><a class="btn btn--sun" href="index.html">Go to home page</a><a class="btn btn--ghost" href="solar-packages.html">Solar packages</a></div>
  </div></div>
</section>'''
page("404.html", "Page not found | Taj Battery & Solar", "Page not found.", nf)
# 404 must not be indexed
p404 = os.path.join(OUT, "404.html")
s = open(p404, encoding="utf-8").read().replace('content="index, follow"', 'content="noindex"')
open(p404, "w", encoding="utf-8").write(s)

# ================= URDU PAGES (ur/) =================
# Home, Packages and Contact in Urdu. Technical words (kW, inverter, hybrid, on-grid, lithium) stay in English.
# Numbers with units are wrapped in bdi() so they read left to right inside Urdu sentences.
B = bdi
SOON_UR = '<span class="soon">جلد آرہا ہے</span>'
PKG_UR = {
    "3kW": dict(tag="چھوٹا گھر", inverter="4 kW hybrid", battery=B("5 kWh") + " lithium یا " + B("2") + " tubular", roof=B("≈ 210") + " مربع فٹ",
                runs=["پنکھے، لائٹیں، LED TV", "فریج", "دن میں پانی کی موٹر", "لوڈ شیڈنگ میں بیک اپ"]),
    "5kW": dict(tag="سب سے مقبول", inverter="6 kW hybrid", battery=B("5 kWh") + " lithium", roof=B("≈ 350") + " مربع فٹ",
                runs=["دن میں ایک " + B("1.5") + " ٹن inverter AC", "فریج، پنکھے، لائٹیں، موٹر", "لوڈ شیڈنگ میں بیک اپ", "فون پر مانیٹرنگ"]),
    "10kW": dict(tag="بڑا گھر", inverter=B("10 kW") + " hybrid یا on-grid", battery="اختیاری، " + B("10 kWh") + " lithium", roof=B("≈ 630") + " مربع فٹ",
                 runs=["دن میں دو یا تین inverter AC", "پورے گھر کا لوڈ", "ماہانہ بل کا بڑا حصہ کم", "net metering کے لیے تیار (سروس جلد آرہی ہے)"]),
    "15kW": dict(tag="دکان / دفتر", inverter=B("3-phase") + " on-grid", battery="اختیاری", roof=B("≈ 900–1,200") + " مربع فٹ",
                 runs=["دکانیں، کلینک، اسکول، دفاتر", "کئی AC اور مشینیں", "فون پر مانیٹرنگ", "net metering کے لیے تیار (سروس جلد آرہی ہے)"]),
}

def pkg_card_ur(p, full):
    u = PKG_UR[p["key"]]
    runs = "".join("<li>%s</li>" % r for r in (u["runs"] if full else u["runs"][:3]))
    details = ""
    if full:
        details = f'''<dl>
    <dt>پینل</dt><dd>{B(p['panels'])}</dd>
    <dt>Inverter</dt><dd>{u['inverter']}</dd>
    <dt>بیٹری</dt><dd>{u['battery']}</dd>
  </dl>'''
    return f'''<article class="card pkg{' pkg--top' if p.get('top') else ''}" id="pkg-{p['key']}">
  <span class="tag">{u['tag']}</span>
  <div><h3 class="size"><a href="package-{p['key'].lower()}.html">{B(p['size'] + '<small> kW</small>')}</a></h3><p class="kind" dir="ltr">{p['kind']}</p></div>
  <p class="units"><b>{B(p['units'])}</b> یونٹ روزانہ</p>
  {details}
  <ul>{runs}</ul>
  <a class="more" href="package-{p['key'].lower()}.html">دیکھیں کیا چلے گا</a>
  <a class="btn {'btn--sun' if p.get('top') else 'btn--blue'}" href="contact.html?need={p['key']}">قیمت معلوم کریں</a>
</article>'''

FAQ_UR = [
    ("کراچی میں سولر سسٹم کتنے کا لگتا ہے؟",
     "پینل، inverter اور بیٹری کی قیمتیں تقریباً ہر ہفتے بدلتی ہیں، اس لیے ہم اسی دن کی قیمت بتاتے ہیں۔ اپنا بجلی کا بل اور جو چیزیں چلانی ہیں، واٹس ایپ " + B(WA_LOCAL) + " پر بھیجیں۔ ہم مکمل لگے ہوئے سسٹم کی قیمت بتا دیں گے۔"),
    ("مجھے کتنے kW کا سسٹم چاہیے؟",
     "اپنے K-Electric بل پر ماہانہ یونٹ دیکھیں اور انہیں تقریباً " + B("125") + " سے تقسیم کریں۔ مثلاً " + B("600") + " یونٹ ماہانہ کے لیے تقریباً " + B("5 kW") + " کا سسٹم۔ سائٹ وزٹ پر ہم درست حساب کرتے ہیں۔"),
    ("کیا لوڈ شیڈنگ میں سولر چلے گا؟",
     "صرف hybrid اور off-grid سسٹم لوڈ شیڈنگ میں چلتے ہیں، کیونکہ ان میں بیٹری ہوتی ہے۔ عام on-grid سسٹم حفاظت کی وجہ سے بجلی جاتے ہی بند ہو جاتا ہے۔ اسی لیے ہمارے " + B("3 kW") + " اور " + B("5 kW") + " پیکج hybrid ہیں۔"),
    ("کیا آپ گاڑی کی بیٹری بھی بیچتے ہیں؟",
     "جی ہاں۔ زیادہ تر گاڑیوں کے لیے Osaka، Exide، Phoenix، AGS اور Daewoo کی ڈرائی (maintenance-free) اور عام بیٹریاں، پہلوان گوٹھ کی دکان پر فٹنگ کے ساتھ۔ صحیح بیٹری اور آج کی قیمت کے لیے اپنی گاڑی کا ماڈل واٹس ایپ کریں۔"),
    ("کیا آپ K-Electric net metering کرواتے ہیں؟",
     "Net metering کی سروس جلد شروع ہو رہی ہے۔ ہمارے on-grid اور hybrid سسٹم net metering کے لیے تیار ہوتے ہیں، اس لیے سروس شروع ہوتے ہی آپ درخواست دے سکیں گے۔ واٹس ایپ پر پیغام بھیجیں، ہم آپ کو بتا دیں گے۔"),
    ("کیا آپ صرف پہلوان گوٹھ میں کام کرتے ہیں؟",
     "ہماری دکان گلستانِ جوہر کے قریب پہلوان گوٹھ میں ہے، اور ہم پورے کراچی میں سسٹم لگاتے ہیں۔ سائٹ وزٹ کے لیے اپنا علاقہ بھیجیں۔"),
    ("وارنٹی کیا ملتی ہے؟",
     "پینل، inverter اور بیٹری پر کمپنی کی وارنٹی ہوتی ہے، اور ہم سسٹم کے ساتھ وارنٹی کارڈ دیتے ہیں۔ جو برانڈ آپ چنیں، اس کی وارنٹی کی تفصیل ہم سے پوچھ لیں۔"),
]
def strip_tags(t):
    return re.sub(r"<[^>]+>", "", t)
FAQ_UR_LD = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "inLanguage": "ur",
    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in FAQ_UR],
}
faq_ur_html = "".join("<details><summary>%s</summary><p>%s</p></details>" % qa for qa in FAQ_UR)

CTA_UR = f'''<section class="cta section">
  <div class="wrap">
    <div class="stack">
      <h2>اپنا بجلی کا بل بھیجیں، ہم سسٹم کا سائز بتائیں گے</h2>
      <p>اپنے تازہ K-Electric بل کی تصویر واٹس ایپ کریں اور بتائیں کہ کیا چلانا ہے۔ ہم سسٹم کا سائز اور آج کی قیمت بتائیں گے۔</p>
    </div>
    <div class="btn-row">
      <a class="btn btn--wa" href="{wa("السلام علیکم، میں سولر کی قیمت کے لیے اپنا بجلی کا بل بھیج رہا ہوں۔")}" target="_blank" rel="noopener">{ICON_WA}بل واٹس ایپ کریں</a>
      <a class="btn btn--ghost" style="color:var(--on-panel)" href="tel:{PHONE_E164}">{ICON_PHONE}کال کریں {B(PHONE_LOCAL)}</a>
    </div>
  </div>
</section>'''

home_ur = f'''<a class="swap" href="{wa("السلام علیکم، میں اپنی پرانی بیٹری کے بدلے نئی بیٹری لینا چاہتا ہوں۔ میری بیٹری / گاڑی: ")}" target="_blank" rel="noopener">
  <span class="swap-icon">{ICON_SWAP}</span>
  <span class="swap-text"><b>بیٹری ایکسچینج:</b> پرانی بیٹری دیں، نئی بیٹری لیں، صرف فرق کی رقم ادا کریں۔</span>
  <span class="swap-cta">واٹس ایپ پر قیمت پوچھیں</span>
</a>
<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow">سولر تنصیب · پہلوان گوٹھ، کراچی</span>
      <h1>پہلوان گوٹھ، کراچی میں گھروں اور دکانوں کے لیے سولر سسٹم</h1>
      <p class="ur-line">بجلی کے بھاری بلوں اور لوڈ شیڈنگ سے نجات</p>
      <p class="lead">K-Electric کا بل کم کریں اور لوڈ شیڈنگ میں بھی پنکھے چلتے رہیں۔ {B("3 kW")} سے {B("20 kW")} تک hybrid اور on-grid پیکجز، ہماری اپنی ٹیم کی تنصیب کے ساتھ۔</p>
      <div class="btn-row">
        <a class="btn btn--sun" href="solar-packages.html">سولر پیکجز دیکھیں</a>
        <a class="btn btn--wa" href="{wa("السلام علیکم، مجھے سولر سسٹم کی قیمت معلوم کرنی ہے۔")}" target="_blank" rel="noopener">{ICON_WA}واٹس ایپ پر قیمت پوچھیں</a>
      </div>
    </div>
    <aside class="spec" aria-labelledby="spec-title">
      <span class="eyebrow">ہمارا سب سے مقبول سسٹم</span>
      <h2 id="spec-title"><a href="package-5kw.html">گھر کے لیے {B("5 kW")} hybrid</a></h2>
      <dl>
        <dt>سولر پینل</dt><dd>{B("10 × 585 W")} N-type</dd>
        <dt>کل سائز</dt><dd>{B("5.85 kWp")}</dd>
        <dt>Inverter</dt><dd>{B("6 kW")} hybrid</dd>
        <dt>بیٹری</dt><dd>{B("5 kWh")} lithium</dd>
        <dt>روزانہ یونٹ</dt><dd class="big">{B("≈ 24")}</dd>
        <dt>کیا چلے گا</dt><dd>دن میں {B("1.5")} ٹن inverter AC</dd>
      </dl>
      <small>کراچی کی دھوپ کے حساب سے اندازہ۔ اصل پیداوار موسم، گرد اور سائے پر منحصر ہے۔</small>
    </aside>
  </div>
</section>

<div class="facts">
  <a href="solar-packages.html"><b>{B("3 kW")} سے {B("20 kW")}</b><span>hybrid، on-grid اور off-grid سسٹم</span></a>
  <a href="../batteries.html#car"><b>گاڑی کی بیٹریاں</b><span>ڈرائی اور عام۔ Osaka، Exide، Phoenix، AGS، Daewoo</span></a>
  <a href="../accessories.html"><b>مکمل سامان</b><span>اسٹرکچر، تاریں، بریکر، بیٹریاں</span></a>
  <a href="../our-shop.html"><b><bdi dir="ltr">2012</bdi> سے</b><span>ہماری دکان پہلوان گوٹھ، کراچی میں</span></a>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">سولر پیکجز</span>
      <h2>جو چلانا ہے، اس کے حساب سے سسٹم چنیں</h2>
      <p>ہر پیکج میں پینل، inverter، اسٹرکچر، DC اور AC وائرنگ، بریکر، surge protection، ارتھنگ اور تنصیب شامل ہے۔</p>
    </div>
    <div class="grid grid-4 swipe">{"".join(pkg_card_ur(p, False) for p in PACKAGES)}</div>
    <p class="note" style="margin-top:16px">کراچی کے لیے یونٹ کا اندازہ۔ <a href="solar-packages.html">تمام پیکجز کی مکمل تفصیل</a></p>
  </div>
</section>

<section class="section section--alt" id="car-batteries">
  <div class="wrap media-row carbat">
    {fig("exide", caption=False, pre="../")}
    <div class="stack">
      <span class="eyebrow">گاڑی کی بیٹریاں</span>
      <h2>گاڑی کی بیٹری، دکان پر فٹنگ کے ساتھ</h2>
      <p>زیادہ تر گاڑیوں کے لیے ڈرائی (maintenance-free) اور عام بیٹریاں، Osaka، Exide، Phoenix، AGS اور Daewoo کی۔ گاڑی ہماری دکان پر لائیں، یا کال کریں اور ہم آپ کے پاس آئیں گے۔ ہم پرانی بیٹری چیک کریں گے، نئی بیٹری لگائیں گے اور چارجنگ ٹیسٹ کریں گے۔</p>
      <ul class="brands" dir="ltr"><li>Osaka</li><li>Exide</li><li>Phoenix</li><li>AGS</li><li>Daewoo</li></ul>
      <div class="btn-row"><a class="btn btn--wa" href="{wa("السلام علیکم، مجھے گاڑی کی بیٹری چاہیے۔ میری گاڑی کا ماڈل: ")}" target="_blank" rel="noopener">{ICON_WA}گاڑی کا ماڈل بھیج کر قیمت پوچھیں</a><a class="btn btn--blue" href="tel:{PHONE_E164}">{ICON_PHONE}کال کریں {B(PHONE_LOCAL)}</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap shop">
    {fig("front", caption=False, pre="../")}
    <div class="stack">
      <span class="eyebrow">دکان پر تشریف لائیں</span>
      <h2>2012 سے پہلوان گوٹھ کی بیٹری اور سولر کی دکان</h2>
      <p class="visit"><b>{ADDRESS_UR}</b><br>ہر روز صبح {B("9")} بجے سے رات {B("9")} بجے تک</p>
      <p>2012 سے پہلوان گوٹھ کے گھرانے اور دکاندار بیٹریوں، UPS اور سولر سسٹم کے لیے ہمارے پاس آتے ہیں۔ خریدنے سے پہلے پینل، inverter اور بیٹریاں خود آ کر دیکھیں۔</p>
      <p>ہم Osaka، Exide، Phoenix، AGS اور Daewoo کی بیٹریاں بیچتے ہیں، UPS کی مرمت کرتے ہیں، اور دکان پر بیٹری چیک، چارج اور تبدیل کرتے ہیں۔</p>
      <div class="btn-row"><a class="btn btn--sun btn--sm" href="../our-shop.html">دکان کی تصاویر دیکھیں</a><a class="btn btn--ghost btn--sm" href="{MAPS}" target="_blank" rel="noopener">راستہ دیکھیں</a><a class="btn btn--ghost btn--sm" href="tel:{PHONE_E164}">{ICON_PHONE}کال کریں {B(PHONE_LOCAL)}</a></div>
    </div>
  </div>
</section>

<section class="section strip-section" aria-label="دکان کی تصاویر">
  <div class="wrap strip swipe">{fig("inside", cap_text="Osaka، Exide، Phoenix اور AGS کی بیٹریاں", pre="../")}{fig("charging", cap_text="گاہکوں کی بیٹریاں چارجنگ پر", pre="../")}{fig("ups_repair", cap_text="ہماری بینچ پر UPS کی مرمت", pre="../")}{fig("stock", cap_text="سولر پینل، تاریں اور سامان", pre="../")}</div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">ہمارا کام</span>
      <h2>سولر کا ہر کام، چھت سے inverter تک</h2>
    </div>
    <div class="grid grid-3">
      <article class="card">
        <div class="icon">{ICON_PANEL}</div>
        <h3>سولر تنصیب</h3>
        <p>سائٹ وزٹ، لوڈ کا حساب، اونچا یا عام اسٹرکچر، صاف ستھری وائرنگ، اور ٹیسٹ کے بعد حوالگی، فون پر مانیٹرنگ کے ساتھ۔</p>
        <a class="more" href="services.html#installation">تنصیب کا طریقہ</a>
      </article>
      <article class="card card--soon">
        <div class="icon">{ICON_METER}</div>
        <h3>K-Electric net metering {SOON_UR}</h3>
        <p>دن کے اضافی یونٹ K-Electric کو دیں اور بل کم کریں۔ ہمارے سسٹم net metering کے لیے تیار ہیں، درخواست کی سروس جلد شروع ہوگی۔</p>
        <a class="more" href="services.html#net-metering">مزید تفصیل</a>
      </article>
      <article class="card">
        <div class="icon">{ICON_PLUG}</div>
        <h3>سولر کا سامان</h3>
        <p>پینل، hybrid اور on-grid inverter، lithium اور tubular بیٹریاں، اسٹرکچر، سولر کیبل، MC4، DC بریکر اور surge protector۔</p>
        <a class="more" href="../accessories.html">سامان دیکھیں (English)</a>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">سوالات</span>
      <h2>کراچی میں سولر کے بارے میں عام سوالات</h2>
    </div>
    <div class="faq">{faq_ur_html}</div>
  </div>
</section>
{CTA_UR}'''

page("index.html",
     "پہلوان گوٹھ، کراچی میں سولر سسٹم، گاڑی کی بیٹریاں اور UPS | Taj Battery",
     "پہلوان گوٹھ، کراچی میں 3 kW سے 20 kW تک hybrid اور on-grid سولر پیکجز، تنصیب کے ساتھ۔ Osaka، Exide، Phoenix، AGS اور Daewoo گاڑی کی بیٹریاں اور UPS کی مرمت۔ کال یا واٹس ایپ 0315 2020525",
     home_ur, [dict({"@context": "https://schema.org"}, **BUSINESS), FAQ_UR_LD], lang="ur")

# ---- Urdu packages page ----
pk_ur = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("سولر پیکجز", "ur")}
      <h1>کراچی کے گھروں اور دکانوں کے لیے سولر پیکجز</h1>
      <p class="lead">تنصیب کے ساتھ چار معیاری سسٹم۔ ہر سسٹم آپ کی چھت، لوڈ اور بجٹ کے مطابق بدلا جا سکتا ہے۔</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">پیکجز</span>
      <h2>تنصیب کے ساتھ مکمل سسٹم</h2>
      <p>ہر پیکج میں شامل: پینل، inverter، galvanised اسٹرکچر، سولر DC کیبل، MC4 کنیکٹر، DC اور AC بریکر، surge protector، ارتھنگ، تنصیب اور ٹیسٹنگ۔</p>
    </div>
    <div class="grid grid-2">{"".join(pkg_card_ur(p, True) for p in PACKAGES)}</div>
    <p class="note" style="margin-top:16px">روزانہ یونٹ کراچی کے عام اندازے کے مطابق ہیں، موسم کے ساتھ کم یا زیادہ ہو سکتے ہیں۔</p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">سسٹم کی قسم</span>
      <h2>On-grid، hybrid یا off-grid؟</h2>
    </div>
    <div class="grid grid-3">
      <article class="card"><h3>On-grid</h3><p>سب سے کم قیمت۔ بل کم کرتا ہے، لیکن لوڈ شیڈنگ میں بند ہو جاتا ہے۔</p></article>
      <article class="card"><h3>Hybrid</h3><p>بل کم کرتا ہے اور بیٹری کے ساتھ لوڈ شیڈنگ میں بھی چلتا ہے۔</p></article>
      <article class="card"><h3>Off-grid</h3><p>جہاں K-Electric کا کنکشن نہ ہو۔</p></article>
    </div>
  </div>
</section>

{CTA_UR}'''
page("solar-packages.html",
     "کراچی میں سولر پیکجز: 3، 5، 10 اور 15 kW | Taj Battery & Solar",
     "کراچی میں 3 kW، 5 kW، 10 kW اور 15–20 kW سولر پیکجز، تنصیب کے ساتھ۔ پینل، hybrid inverter اور lithium بیٹری بیک اپ۔ دکان پہلوان گوٹھ میں۔ کال 0315 2020525",
     pk_ur, [crumbs_ld("solar-packages.html", "سولر پیکجز", "ur")], lang="ur")

# ---- Urdu contact page ----
OPTS_UR = [(p["key"] + " solar system", B(p["key"].replace("kW", " kW")) + " سولر سسٹم") for p in PACKAGES] + [
    ("Accessories / parts only", "صرف سامان / پرزے"), ("Car battery", "گاڑی کی بیٹری"), ("UPS / home batteries", "UPS / گھر کی بیٹریاں"),
    ("Maintenance or repair", "مینٹیننس یا مرمت"), ("Not sure yet", "ابھی طے نہیں کیا")]
opts_ur_html = "".join('<option value="%s">%s</option>' % (v, strip_tags(t)) for v, t in OPTS_UR)
con_ur = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("رابطہ", "ur")}
      <h1>پہلوان گوٹھ میں Taj Battery & Solar سے رابطہ کریں</h1>
      <p class="lead">کال کریں، واٹس ایپ کریں یا دکان پر آئیں۔ فارم بھریں، آپ کی تفصیل کے ساتھ واٹس ایپ کھل جائے گا۔</p>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap contact">
    <div class="stack" style="gap:24px">{fig("front", "shop-photo", caption=False, pre="../")}
    <dl class="nap">
      <div><dt>فون</dt><dd><a href="tel:{PHONE_E164}">{B(PHONE_LOCAL)}</a></dd></div>
      <div><dt>واٹس ایپ</dt><dd><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{B("+92 315 2020525")}</a></dd></div>
      <div><dt>دکان</dt><dd>{ADDRESS_UR}</dd></div>
      <div><dt>اوقات</dt><dd>ہر روز صبح {B("9")} بجے سے رات {B("9")} بجے تک</dd></div>
      <div><dt>فیس بک</dt><dd><a href="{FACEBOOK}" target="_blank" rel="noopener">{B("facebook.com/tajbatery")}</a></dd></div>
      <div><dt>نقشہ</dt><dd><a href="{MAPS}" target="_blank" rel="noopener">گوگل میپ پر کھولیں</a></dd></div>
      <div><dt>سروس کا علاقہ</dt><dd style="font-weight:400">پہلوان گوٹھ، گلستانِ جوہر اور پورا کراچی</dd></div>
    </dl></div>
    <form class="quote" id="quote-form">
      <h2 style="font-size:1.6rem">قیمت معلوم کریں</h2>
      <label for="name">آپ کا نام<input id="name" name="name" required autocomplete="name"></label>
      <label for="area">کراچی میں علاقہ<input id="area" name="area" required placeholder="مثلاً پہلوان گوٹھ، گلستانِ جوہر"></label>
      <label for="need">آپ کو کیا چاہیے؟<select id="need" name="need">{opts_ur_html}</select></label>
      <label for="bill">ماہانہ بل یا یونٹ <span class="hint">(اختیاری)</span><input id="bill" name="bill" placeholder="مثلاً 650 یونٹ یا 40,000 روپے"></label>
      <label for="msg">مزید تفصیل <span class="hint">(اختیاری)</span><textarea id="msg" name="msg" placeholder="کون سی چیزیں چلانی ہیں، چھت کیسی ہے، کب چاہیے"></textarea></label>
      <button class="btn btn--wa" type="submit">{ICON_WA}واٹس ایپ پر بھیجیں</button>
    </form>
  </div>
</section>'''
page("contact.html",
     "Taj Battery & Solar سے رابطہ، پہلوان گوٹھ کراچی | 0315 2020525",
     "سولر کی قیمت، بیٹریوں اور سامان کے لیے کال یا واٹس ایپ کریں 0315 2020525۔ Taj Battery Service, UPS & Solar System، پہلوان گوٹھ، کراچی۔",
     con_ur, [crumbs_ld("contact.html", "رابطہ", "ur")], lang="ur")


# ---- Urdu services page ----
STEPS_UR = [
    ("سائٹ وزٹ اور لوڈ کا جائزہ", "ہم آپ کے گھر یا دکان آتے ہیں، چھت، سایہ اور سمت دیکھتے ہیں، اور وہ چیزیں لکھتے ہیں جو آپ چلانا چاہتے ہیں۔"),
    ("سسٹم کا ڈیزائن اور قیمت", "آپ کو لکھی ہوئی قیمت ملتی ہے جس میں پینل کی تعداد، inverter، بیٹری اور اسٹرکچر شامل ہوتا ہے، اسی دن کے ریٹ پر۔"),
    ("تنصیب", "ہماری ٹیم اسٹرکچر، پینل، inverter، بیٹری، وائرنگ، بریکر، surge protection اور ارتھنگ لگاتی ہے۔"),
    ("ٹیسٹنگ اور حوالگی", "ہم سسٹم ٹیسٹ کرتے ہیں، آپ کے فون پر مانیٹرنگ سیٹ کرتے ہیں اور استعمال کا طریقہ سمجھاتے ہیں۔"),
    ("Net metering کے لیے تیار", "آپ کا سسٹم اس طرح لگایا جاتا ہے کہ بعد میں net metering ہو سکے۔ ہماری net metering درخواست کی سروس جلد شروع ہوگی۔"),
    ("بعد از فروخت سروس", "خرابی، صفائی، سسٹم بڑا کرنے یا بعد میں بیٹری لگوانے کے لیے کال یا واٹس ایپ کریں۔"),
]
steps_ur_html = "".join("<li><h3>%s</h3><p>%s</p></li>" % s for s in STEPS_UR)
svc_ur = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("خدمات", "ur")}
      <h1>سولر تنصیب، UPS کی مرمت اور بیٹری سروس</h1>
      <p class="lead">پہلے سائٹ وزٹ سے لے کر برسوں کی بعد از فروخت سروس تک، ایک ہی ٹیم آپ کا سسٹم سنبھالتی ہے۔</p>
    </div>
  </div>
</section>

<section class="section" id="installation">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">تنصیب</span>
      <h2>سولر تنصیب کیسے ہوتی ہے</h2>
      <p>گھر کا عام {B("5 kW")} سسٹم آرڈر کنفرم ہونے کے بعد ایک سے دو دن میں لگ جاتا ہے۔</p>
    </div>
    <ol class="steps">{steps_ur_html}</ol>
  </div>
</section>

<section class="section section--alt" id="net-metering">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">K-Electric</span>
      <h2>کراچی میں net metering {SOON_UR}</h2>
      <p>Net metering میں دن کے وقت آپ کے پینلز کی اضافی بجلی K-Electric کو جاتی ہے اور آپ کے بل میں ایڈجسٹ ہوتی ہے۔ ہم net metering کی درخواستوں کی تیاری کر رہے ہیں۔ یہ اس طرح ہوگا:</p>
    </div>
    <div class="grid grid-2">
      <article class="card">
        <h3>آپ کو کیا چاہیے</h3>
        <ul>
          <li>میٹر کے مالک کے CNIC کی کاپی</li>
          <li>تازہ K-Electric بل</li>
          <li>پراپرٹی کی ملکیت یا کرایہ داری کا ثبوت</li>
          <li>لگا ہوا on-grid یا hybrid سسٹم</li>
        </ul>
      </article>
      <article class="card">
        <h3>ہم کیا کریں گے</h3>
        <ul>
          <li>درخواست اور سسٹم کی ڈرائنگ تیار کریں گے</li>
          <li>فائل جمع کروا کر K-Electric سے پیروی کریں گے</li>
          <li>انسپیکشن کا انتظام کریں گے</li>
          <li>گرین میٹر لگنے تک آپ کے ساتھ رہیں گے</li>
        </ul>
      </article>
    </div>
    <p class="note" style="margin-top:16px">Net metering کے قوانین اور اضافی بجلی کے ریٹ NEPRA طے کرتا ہے اور یہ بدل سکتے ہیں۔ فیصلہ کرنے سے پہلے موجودہ قوانین ہم سے پوچھ لیں۔</p>
  </div>
</section>

<section class="section" id="maintenance">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">مینٹیننس</span>
      <h2>اپنے سسٹم کی پیداوار برقرار رکھیں</h2>
      <p>کراچی کی گرد چند ہفتوں میں پینل کی پیداوار کافی کم کر سکتی ہے۔ باقاعدہ صفائی اور چیکنگ سے پورے یونٹ ملتے رہتے ہیں۔</p>
    </div>
    <div class="grid grid-3">
      <article class="card"><div class="icon">{ICON_PANEL}</div><h3>پینل کی دھلائی</h3><p>پینل، کلیمپ اور کنیکٹر کی دھلائی اور جانچ۔</p></article>
      <article class="card"><div class="icon">{ICON_WRENCH}</div><h3>خرابی کی مرمت</h3><p>Inverter کے error code، بار بار ٹرپ ہوتے بریکر، کم پیداوار اور وائرنگ کی خرابیاں۔</p></article>
      <article class="card"><div class="icon">{ICON_PLUG}</div><h3>سسٹم بڑھانا اور منتقلی</h3><p>مزید پینل یا بیٹریاں لگوائیں، inverter بدلیں، یا سسٹم نئے گھر منتقل کروائیں۔</p></article>
    </div>
  </div>
</section>

<section class="section section--alt" id="ups-repair">
  <div class="wrap media-row">
    {fig("ups_repair", cap_text="ہماری بینچ پر UPS کی مرمت", pre="../")}
    <div class="stack">
      <span class="eyebrow">UPS اور inverter کی مرمت</span>
      <h2>اپنی بینچ پر UPS کی مرمت</h2>
      <p>UPS چارج نہیں ہو رہا، بیپ کر رہا ہے یا لوڈ پر بند ہو جاتا ہے؟ دکان پر لے آئیں۔ ہم سرکٹ بورڈ ٹھیک کرتے ہیں، خراب پرزے بدلتے ہیں اور واپس دینے سے پہلے ہر یونٹ لوڈ پر ٹیسٹ کرتے ہیں۔</p>
      <ul>
        <li>گھر کے UPS اور inverter کی مرمت</li>
        <li>چارجنگ کی خرابیاں اور بیٹری کا صحیح جوڑ</li>
        <li>سولر charge controller اور hybrid inverter کی جانچ</li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="batteries">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">بیٹریاں</span>
      <h2>بیٹری سروس</h2>
      <p>اپنی بیٹری پہلوان گوٹھ کی دکان پر لائیں، یا ہمیں کال کریں۔</p>
    </div>
    <div class="grid grid-3">
      <article class="card"><div class="icon">{ICON_BATT}</div><h3>ٹیسٹنگ اور چارجنگ</h3><p>UPS، tubular اور گاڑی کی بیٹریوں کا چیک اپ اور چارجنگ۔</p></article>
      <article class="card"><div class="icon">{ICON_BATT}</div><h3>بیٹری کی تبدیلی</h3><p>Lithium، tubular، اور گاڑی کی ڈرائی یا عام بیٹریاں، دکان پر فٹنگ کے ساتھ۔ پرانی بیٹری دیں اور صرف فرق کی رقم ادا کریں۔</p></article>
      <article class="card"><div class="icon">{ICON_PHONE}</div><h3>گاڑی کا جمپ اسٹارٹ</h3><p>قریب میں گاڑی اسٹارٹ نہیں ہو رہی؟ {B(PHONE_LOCAL)} پر کال کریں، ہم آپ کے پاس آئیں گے۔</p></article>
    </div>
    <div class="strip strip--2" style="margin-top:20px">{fig("charging", cap_text="گاہکوں کی بیٹریاں چارجنگ پر", pre="../")}{fig("inside", cap_text="Osaka، Exide، Phoenix اور AGS کی بیٹریاں", pre="../")}</div>
  </div>
</section>
{CTA_UR}'''
SVC_UR_LD = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "inLanguage": "ur",
    "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "provider": {"@id": SITE + "/#business"}, "areaServed": "Karachi"}}
        for i, n in enumerate(["سولر سسٹم کی تنصیب", "سولر پینل کی صفائی اور مینٹیننس", "UPS اور inverter کی مرمت", "بیٹری ٹیسٹنگ، چارجنگ اور تبدیلی", "گاڑی کا جمپ اسٹارٹ"])
    ],
}
page("services.html",
     "کراچی میں سولر تنصیب، UPS مرمت اور بیٹری سروس | Taj Battery & Solar",
     "پہلوان گوٹھ، کراچی سے سولر تنصیب، پینل کی صفائی، UPS اور inverter کی مرمت، گاڑی کی بیٹریاں اور بیٹری چارجنگ۔ کال یا واٹس ایپ 0315 2020525",
     svc_ur, [crumbs_ld("services.html", "خدمات", "ur"), SVC_UR_LD], lang="ur")


# ================= PACKAGE DETAIL PAGES (line-art "what it runs") =================
def _art(paths):
    return '<svg viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % paths
ART = {
    "fan": _art('<path d="M24 4v8"/><circle cx="24" cy="15.5" r="3.5"/><path d="M20.6 16.4 6.3 19.6a1.6 1.6 0 0 0 .4 3.1l14.6-2.8"/><path d="M27.4 16.4l14.3 3.2a1.6 1.6 0 0 1-.4 3.1l-14.6-2.8"/><path d="M21.5 19v5a2.5 2.5 0 0 0 5 0v-5"/><path d="M12 32c4 3 20 3 24 0" opacity=".5"/>'),
    "light": _art('<path d="M18 31c-3.2-2.5-5.5-6.2-5.5-10a11.5 11.5 0 0 1 23 0c0 3.8-2.3 7.5-5.5 10v4H18z"/><path d="M19 39h10M21 43h6"/><path d="M24 2v3M7 9l2.2 2.2M41 9l-2.2 2.2M3 21h3M42 21h3"/>'),
    "tv": _art('<rect x="4" y="8" width="40" height="26" rx="2.5"/><path d="M17 41h14M24 34v7"/><path d="M9 13h9" opacity=".5"/>'),
    "fridge": _art('<rect x="12" y="3" width="24" height="42" rx="3"/><path d="M12 18h24M17 8v6M17 23v8"/>'),
    "ac": _art('<rect x="3" y="10" width="42" height="16" rx="4"/><path d="M8 21h32"/><path d="M14 31c0 2-2 2.5-2 4.5s2 2.5 2 4.5M24 31c0 2-2 2.5-2 4.5s2 2.5 2 4.5M34 31c0 2-2 2.5-2 4.5s2 2.5 2 4.5"/>'),
    "motor": _art('<rect x="5" y="17" width="22" height="17" rx="3"/><path d="M10 22v7M15 22v7M20 22v7"/><path d="M27 21h8v-9h7M27 30h12"/><path d="M9 34v5h14v-5"/>'),
    "washer": _art('<rect x="8" y="4" width="32" height="40" rx="3"/><path d="M8 12h32M13 8h5"/><circle cx="34" cy="8" r="1"/><circle cx="24" cy="28" r="9"/><path d="M19 29c2-2 4 2 6 0s3-1 4 0"/>'),
    "computer": _art('<rect x="9" y="9" width="30" height="21" rx="2"/><path d="M4 37h40l-3-7H7z"/><path d="M21 34h6"/>'),
}
LOAD_LABEL = {"fan": ("Ceiling fans", "پنکھے"), "light": ("LED lights", "LED لائٹس"), "tv": ("LED TV", "LED TV"),
              "fridge": ("Fridge", "فریج"), "ac": ("Inverter AC, 1.5 ton", "inverter AC، ڈیڑھ ٹن"), "motor": ("Water motor", "پانی کی موٹر"),
              "washer": ("Washing machine", "واشنگ مشین"), "computer": ("Computers", "کمپیوٹر")}
LOADS = {
    "3kW": [("fan", 6), ("light", 10), ("tv", 1), ("fridge", 1), ("motor", 1)],
    "5kW": [("ac", 1), ("fan", 8), ("light", 15), ("tv", 2), ("fridge", 1), ("motor", 1), ("washer", 1)],
    "10kW": [("ac", 3), ("fan", 12), ("light", 25), ("tv", 3), ("fridge", 2), ("motor", 1), ("washer", 1)],
    "15kW": [("ac", 5), ("fan", 20), ("light", 40), ("computer", 10), ("fridge", 2), ("motor", 2)],
}
LOAD_NOTE = {
    "3kW": ("Typical load in daytime sun. At night the battery keeps fans, lights and TV running.", "دن کی دھوپ میں عام لوڈ۔ رات کو بیٹری پنکھے، لائٹیں اور TV چلاتی ہے۔"),
    "5kW": ("Typical load in daytime sun; the AC runs on sunshine. At night the battery keeps fans, lights and TV running.", "دن کی دھوپ میں عام لوڈ؛ AC دھوپ پر چلتا ہے۔ رات کو بیٹری پنکھے، لائٹیں اور TV چلاتی ہے۔"),
    "10kW": ("Typical load in daytime sun. Add a battery to keep running in load shedding.", "دن کی دھوپ میں عام لوڈ۔ لوڈ شیڈنگ میں چلانے کے لیے بیٹری لگوائیں۔"),
    "15kW": ("Typical daytime load for a shop, clinic, school or office.", "دکان، کلینک، اسکول یا دفتر کا دن کا عام لوڈ۔"),
}
LOAD_DESC = {"fan": "ceiling fans", "light": "LED lights", "tv": "LED TV", "fridge": "fridge", "ac": "inverter AC",
             "motor": "water motor", "washer": "washing machine", "computer": "computers"}
def pkg_slug(key):
    return "package-%s.html" % key.lower()
for _p in PACKAGES:
    UR_PAGES.add(pkg_slug(_p["key"]))

def package_page(p, lang):
    key, ur = p["key"], (lang == "ur")
    u = PKG_UR[key]
    size = p["size"] + " kW"
    cols = len(LOADS[key]) if len(LOADS[key]) <= 6 else -(-len(LOADS[key]) // 2)
    tiles = "".join(
        f'<li class="load"><span class="load-art">{ART[k]}</span><b class="load-n">{bdi("× %d" % n) if ur else "× %d" % n}</b><span>{LOAD_LABEL[k][1 if ur else 0]}</span></li>'
        for k, n in LOADS[key])
    others = "".join(
        f'<a href="{pkg_slug(q["key"])}"{" aria-current=\"page\"" if q is p else ""}>{bdi(q["size"] + " kW") if ur else q["size"] + " kW"}</a>' for q in PACKAGES)
    if ur:
        title = f"کراچی میں {size} سولر سسٹم: کیا چلے گا | Taj Battery"
        desc = f"{size} {p['kind']} سولر پیکج، کراچی: " + "، ".join("%d %s" % (n, LOAD_LABEL[k][1]) for k, n in LOADS[key]) + "۔ تنصیب Taj Battery، پہلوان گوٹھ۔ 0315 2020525"
        body = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("سولر پیکجز", "ur").replace('<li aria-current="page">سولر پیکجز</li>', '<li><a href="solar-packages.html">سولر پیکجز</a></li><li aria-current="page">' + bdi(size) + '</li>')}
      <span class="eyebrow">{u["tag"]}</span>
      <h1>{bdi(size)} سولر سسٹم <bdi dir="ltr" class="nowrap">{p["kind"]}</bdi></h1>
      <ul class="spec-chips">
        <li>روزانہ تقریباً {bdi(p["units"].replace("≈ ", ""))} یونٹ</li>
        <li>پینل: {bdi(p["panels"])}</li>
        <li>Inverter: {u["inverter"]}</li>
        <li>بیٹری: {u["battery"]}</li>
      </ul>
      <div class="btn-row">
        <a class="btn btn--sun" href="contact.html?need={key}">قیمت معلوم کریں</a>
        <a class="btn btn--wa" href="{wa("السلام علیکم، مجھے " + size + " سولر پیکج کی قیمت معلوم کرنی ہے۔")}" target="_blank" rel="noopener">{ICON_WA}واٹس ایپ پر پوچھیں</a>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">کیا چلے گا</span>
      <h2>یہ سسٹم کیا چلا سکتا ہے</h2>
    </div>
    <ul class="loads" style="--cols:{cols}">{tiles}</ul>
    <p class="note" style="margin-top:16px">{LOAD_NOTE[key][1]} ہم آپ کی اصل چیزوں کے حساب سے سسٹم بناتے ہیں۔</p>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap stack">
    <p>شامل ہے: پینل، inverter، اسٹرکچر، DC اور AC وائرنگ، بریکر، surge protection، ارتھنگ اور تنصیب۔</p>
    <nav class="jump pkg-switch" aria-label="دوسرے پیکجز">{others}</nav>
  </div>
</section>
{CTA_UR}'''
        crumb = crumbs_ld(pkg_slug(key), size + " سولر سسٹم", "ur")
    else:
        title = f"{size} Solar System in Karachi: What It Runs | Taj Battery"
        desc = f"{size} {p['kind'].lower()} solar package in Karachi runs " + ", ".join("%d %s" % (n, LOAD_DESC[k]) for k, n in LOADS[key]) + ". Installed by Taj Battery, Pehlwan Goth. 0315 2020525."
        body = f'''<section class="hero hero-sm">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs_html("Solar Packages").replace('<li aria-current="page">Solar Packages</li>', '<li><a href="solar-packages.html">Solar Packages</a></li><li aria-current="page">' + size + '</li>')}
      <span class="eyebrow">{p["tag"]}</span>
      <h1>{size} {p["kind"]} solar system</h1>
      <ul class="spec-chips">
        <li>{p["units"]} units a day</li>
        <li>Panels: {p["panels"]}</li>
        <li>Inverter: {p["inverter"]}</li>
        <li>Battery: {p["battery"]}</li>
      </ul>
      <div class="btn-row">
        <a class="btn btn--sun" href="contact.html?need={key}">Get price</a>
        <a class="btn btn--wa" href="{wa("Assalam o Alaikum, I want the price of the " + size + " solar package.")}" target="_blank" rel="noopener">{ICON_WA}Ask on WhatsApp</a>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What it runs</span>
      <h2>What a {size} system can run</h2>
    </div>
    <ul class="loads" style="--cols:{cols}">{tiles}</ul>
    <p class="note" style="margin-top:16px">{LOAD_NOTE[key][0]} We size every system to your actual appliances.</p>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap stack">
    <p>Included: panels, inverter, mounting structure, DC and AC wiring, breakers, surge protection, earthing and installation.</p>
    <nav class="jump pkg-switch" aria-label="Other packages">{others}</nav>
  </div>
</section>
{CTA}'''
        crumb = crumbs_ld(pkg_slug(key), size + " solar system")
    page(pkg_slug(key), title, desc, body, [crumb], lang=lang)

for _p in PACKAGES:
    package_page(_p, "en")
    package_page(_p, "ur")

# ================= robots / sitemap =================
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
import datetime
TODAY = datetime.date.today().isoformat()
urls = "".join("  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n" % (SITE, "" if h == "index.html" else h, TODAY) for h, *_ in NAV)
PKG_SLUGS = [pkg_slug(p["key"]) for p in PACKAGES]
urls += "".join("  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (url_for(h, "en"), TODAY) for h in PKG_SLUGS)
urls += "".join("  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (url_for(h, "ur"), TODAY) for h in [n[0] for n in NAV] + PKG_SLUGS if h in UR_PAGES)
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
open(os.path.join(OUT, ".nojekyll"), "w").write("")

# Ask Google Fonts for only the Urdu letters each set of pages uses (a few KB instead of the whole Nastaliq font).
import glob
URDU_CHARS = r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]"
for pages, family in ((glob.glob(os.path.join(OUT, "*.html")), "Noto+Nastaliq+Urdu"),
                      (glob.glob(os.path.join(OUT, "ur", "*.html")), "Noto+Nastaliq+Urdu:wght@400;700")):
    chars = set()
    for fp in pages:
        chars |= set(re.findall(URDU_CHARS, open(fp, encoding="utf-8").read()))
    font_url = "https://fonts.googleapis.com/css2?family=%s&display=swap&text=%s" % (family, urllib.parse.quote("".join(sorted(chars)) + " "))
    for fp in pages:
        t = open(fp, encoding="utf-8").read().replace("__URDU_FONT__", font_url.replace("&", "&amp;"))
        open(fp, "w", encoding="utf-8").write(t)
print("ok")
