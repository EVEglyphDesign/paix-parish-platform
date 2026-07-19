#!/usr/bin/env python3
"""
PAIX Parish Platform — build script

Generates a portal page + one mirrored parish site per PARISHES entry,
all styled with the EVE Glyph Design canon inherited from
paroisse-sainte-anne-des-pays-bas.

Design founder: Donat Omer Thériault (EVE Glyph Design).
"""

from __future__ import annotations
import os, shutil, html
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).parent
PARISHES_DIR = ROOT / "parishes"

# ---------------------------------------------------------------------------
# Parish data
# ---------------------------------------------------------------------------

PARISHES = [
    {
        "slug": "sainte-anne",
        "name": "Paroisse Sainte-Anne-des-Pays-Bas",
        "short": "Sainte-Anne-des-Pays-Bas",
        "city": "Fredericton, Nouveau-Brunswick",
        "founded": "1981",
        "lang": "fr-CA",
        "official_url": "https://www.sainte-anne-des-pays-bas.ca",
        "address": "715, rue Priestman, Fredericton (N.-B.) E3B 5W7",
        "phone": "(506) 444-6015",
        "email": "sainteannedespaysbas@gmail.com",
        "tagline": "Paroisse catholique francophone fondée en 1981",
        "diocese": "Archidiocèse de Moncton",
        "schedule": [
            ("Samedi soir", "17 h 00"),
            ("Dimanche", "11 h 00"),
            ("Lundi, mardi et vendredi", "12 h 05"),
        ],
        "crest_style": "acadian",
        "portal_blurb": "Paroisse francophone fondée en 1981. Miroir non-officiel sous la doctrine EVE Glyph.",
    },
    {
        "slug": "saint-augustine",
        "name": "Église Saint-Augustin de Paquetville",
        "short": "Saint-Augustin de Paquetville",
        "city": "Paquetville, Nouveau-Brunswick",
        "founded": "1874",
        "lang": "fr-CA",
        "official_url": "https://www.staugustineparish.ca",
        "address": "3585, rue Principale, Paquetville (N.-B.) E8R 1G7",
        "phone": "(506) 764-2823",
        "email": "paroissesaintaugustin@nb.aibn.com",
        "tagline": "Paroisse acadienne fondée en 1874 — patrimoine et famille",
        "diocese": "Diocèse de Bathurst",
        "schedule": [
            ("Samedi soir", "19 h 00"),
            ("Dimanche", "10 h 30"),
            ("Mercredi et vendredi", "9 h 00"),
        ],
        "crest_style": "shield",
        "portal_blurb": "Paroisse acadienne du village de Paquetville, patrimoine familial des Thériault.",
    },
    {
        "slug": "saint-dunstan",
        "name": "St. Dunstan's Basilica Parish",
        "short": "St. Dunstan's Basilica",
        "city": "Charlottetown, Prince Edward Island",
        "founded": "1816",
        "lang": "en-CA",
        "official_url": "https://www.stdunstanspei.com",
        "address": "45 Great George Street, Charlottetown, PE C1A 4J8",
        "phone": "(902) 894-3486",
        "email": "office@stdunstanspei.com",
        "tagline": "Mother church of the Diocese of Charlottetown — founded 1816",
        "diocese": "Diocese of Charlottetown",
        "schedule": [
            ("Saturday Vigil", "4:00 PM"),
            ("Sunday", "10:00 AM & 5:00 PM"),
            ("Tuesday – Friday", "12:05 PM"),
        ],
        "crest_style": "gothic",
        "portal_blurb": "Mother church of the Diocese of Charlottetown. Founded 1816.",
    },
    {
        "slug": "saint-catherine",
        "name": "Saint Catherine of Siena Church",
        "short": "Saint Catherine of Siena",
        "city": "Halifax, Nova Scotia",
        "founded": "1948",
        "lang": "en-CA",
        "official_url": "https://saintcatherineofsiena.ca",
        "address": "6476 Bayers Road, Halifax, NS B3L 2B4",
        "phone": "(902) 454-8221",
        "email": "office@saintcatherineofsiena.ca",
        "tagline": "Serving Halifax's West End since 1948 — home of the Franciscans of Halifax",
        "diocese": "Archdiocese of Halifax-Yarmouth · St. Francis and St. Clare of Assisi Parish",
        "schedule": [
            ("Sunday", "11:00 AM & 7:00 PM"),
            ("Tuesday – Friday", "7:00 AM"),
            ("Saturday", "9:00 AM"),
        ],
        "crest_style": "franciscan",
        "portal_blurb": "Home of the Franciscans of Halifax. West End Halifax since 1948.",
    },
    {
        "slug": "saint-mary-basilica",
        "name": "Saint Mary's Cathedral Basilica",
        "short": "St. Mary's Cathedral Basilica",
        "city": "Halifax, Nova Scotia",
        "founded": "1820",
        "lang": "en-CA",
        "official_url": "https://stmcathedral.com",
        "address": "5221 Spring Garden Road, Halifax, NS B3J 1Z3",
        "phone": "(902) 429-9800",
        "email": "cathedral@halifaxyarmouth.org",
        "tagline": "Mother church of the Archdiocese of Halifax-Yarmouth \u2014 Gothic Revival, National Historic Site",
        "diocese": "Archdiocese of Halifax-Yarmouth",
        "schedule": [
            ("Sunday", "8:00 AM \u00b7 10:30 AM \u00b7 5:00 PM"),
            ("Monday & Wednesday", "7:30 AM & 12:15 PM"),
            ("Tuesday", "12:15 PM & 6:30 PM"),
            ("Thursday \u2013 Saturday", "12:15 PM"),
        ],
        "crest_style": "cathedral",
        "portal_blurb": "Mother church of the Archdiocese of Halifax-Yarmouth. Gothic Revival, National Historic Site of Canada.",
    },
    {
        "slug": "holy-trinity",
        "name": "Holy Trinity Catholic Parish",
        "short": "Holy Trinity — Lenexa",
        "city": "Lenexa, Kansas",
        "founded": "1979",
        "lang": "en-US",
        "official_url": "https://htlenexa.org",
        "address": "13615 W 92nd Street, Lenexa, KS 66215",
        "phone": "(913) 888-2770",
        "email": "info@htlenexa.org",
        "tagline": "Parish, school & early education center — Archdiocese of Kansas City in Kansas",
        "diocese": "Archdiocese of Kansas City in Kansas · Knights of Columbus Council of Palms #6673",
        "schedule": [
            ("Saturday Vigil", "4:00 PM"),
            ("Sunday", "7:30 AM · 9:30 AM · 11:30 AM"),
            ("Monday – Friday", "6:45 AM & 8:15 AM"),
            ("Saturday", "8:00 AM"),
        ],
        "crest_style": "trinity",
        "portal_blurb": "Home parish of Knights of Columbus Council of Palms #6673.",
    },
]

# ---------------------------------------------------------------------------
# Language pack
# ---------------------------------------------------------------------------

STRINGS = {
    "fr-CA": {
        "home": "Accueil",
        "about": "Notre paroisse",
        "pastors": "Nos curés",
        "church": "Notre église",
        "mass": "Horaire des messes",
        "bulletin": "Feuillet paroissial",
        "life": "Vie paroissiale",
        "catechesis": "Catéchèse",
        "events": "Événements",
        "links": "Liens",
        "contact": "Contact",
        "welcome": "Bienvenue",
        "mass_h1": "Horaire des messes",
        "mass_day": "Jour",
        "mass_time": "Heure",
        "contact_h1": "Nous joindre",
        "about_h1": "Notre paroisse",
        "reach_us": "Nous joindre",
        "on_this_site": "Sur ce site",
        "doctrine": "Doctrine",
        "no_profile": "Aucun profilage",
        "register": "Registre de langue",
        "founder": "Crédit fondateur",
        "portal_back": "← Retour au portail",
        "official_source": "Source officielle",
        "mirror_note": "Miroir non-officiel préparé avec soin. Contenu paroissial : © la paroisse, tous droits réservés.",
        "no_tracking": "Aucun traçage. Aucun cookie. Aucune analytique. Aucun script tiers autre que la police de caractères Google Fonts.",
        "tribute_line": "Site conçu sous la doctrine EVE Glyph Design. Fondateur du design :",
        "for_people": "Pour le bien-être du peuple.",
        "welcome_lead": "Bonjour et bienvenue au site paroissial.",
    },
    "en-CA": {
        "home": "Home",
        "about": "Our parish",
        "pastors": "Clergy",
        "church": "Our church",
        "mass": "Mass schedule",
        "bulletin": "Bulletin",
        "life": "Parish life",
        "catechesis": "Faith formation",
        "events": "Events",
        "links": "Links",
        "contact": "Contact",
        "welcome": "Welcome",
        "mass_h1": "Mass schedule",
        "mass_day": "Day",
        "mass_time": "Time",
        "contact_h1": "Get in touch",
        "about_h1": "Our parish",
        "reach_us": "Reach us",
        "on_this_site": "On this site",
        "doctrine": "Doctrine",
        "no_profile": "No profiling",
        "register": "Language register",
        "founder": "Founder credit",
        "portal_back": "← Back to the portal",
        "official_source": "Official source",
        "mirror_note": "Non-official mirror, prepared with care. Parish content: © the parish, all rights reserved.",
        "no_tracking": "No tracking. No cookies. No analytics. No third-party scripts other than Google Fonts.",
        "tribute_line": "Site built under the EVE Glyph Design doctrine. Design founder:",
        "for_people": "For the good of the people.",
        "welcome_lead": "Welcome to the parish website.",
    },
    "en-US": {
        "home": "Home",
        "about": "Our parish",
        "pastors": "Clergy",
        "church": "Our church",
        "mass": "Mass schedule",
        "bulletin": "Bulletin",
        "life": "Parish life",
        "catechesis": "Faith formation",
        "events": "Events",
        "links": "Links",
        "contact": "Contact",
        "welcome": "Welcome",
        "mass_h1": "Mass schedule",
        "mass_day": "Day",
        "mass_time": "Time",
        "contact_h1": "Get in touch",
        "about_h1": "Our parish",
        "reach_us": "Reach us",
        "on_this_site": "On this site",
        "doctrine": "Doctrine",
        "no_profile": "No profiling",
        "register": "Language register",
        "founder": "Founder credit",
        "portal_back": "← Back to the portal",
        "official_source": "Official source",
        "mirror_note": "Non-official mirror, prepared with care. Parish content: © the parish, all rights reserved.",
        "no_tracking": "No tracking. No cookies. No analytics. No third-party scripts other than Google Fonts.",
        "tribute_line": "Site built under the EVE Glyph Design doctrine. Design founder:",
        "for_people": "For the good of the people.",
        "welcome_lead": "Welcome to the parish website.",
    },
}

FOUNDER = "Donat Omer Thériault"

# ---------------------------------------------------------------------------
# Crest generator — one per style, all in the same marine + stella-gold canon
# ---------------------------------------------------------------------------

def crest_svg(style: str) -> str:
    """Return an inline-safe SVG crest in the EVE Glyph marine + stella-gold canon."""
    shield = '''<defs>
    <linearGradient id="marine" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1a5578"/>
      <stop offset="1" stop-color="#0b3b5c"/>
    </linearGradient>
  </defs>
  <path d="M50 6 C 74 6 88 12 88 12 L 88 46 C 88 70 68 88 50 94 C 32 88 12 70 12 46 L 12 12 C 12 12 26 6 50 6 Z"
        fill="url(#marine)" stroke="#b8892b" stroke-width="1.5"/>'''
    star = '''<g transform="translate(50 42)">
    <polygon points="0,-16 4.7,-4.9 16.2,-4.9 6.7,1.9 10.6,13 0,6.2 -10.6,13 -6.7,1.9 -16.2,-4.9 -4.7,-4.9"
             fill="#d4a94a"/>
  </g>'''
    if style == "acadian":
        motif = '''<path d="M18 68 Q 30 60, 42 68 T 66 68 T 82 66" fill="none" stroke="#f5efe1" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M18 76 Q 30 68, 42 76 T 66 76 T 82 74" fill="none" stroke="#d4a94a" stroke-width="1.8" stroke-linecap="round" opacity="0.85"/>'''
    elif style == "shield":
        motif = '''<path d="M32 66 L 68 66 M 32 74 L 68 74" stroke="#f5efe1" stroke-width="2" stroke-linecap="round"/>
  <path d="M50 60 L 50 80" stroke="#d4a94a" stroke-width="2" stroke-linecap="round"/>'''
    elif style == "gothic":
        motif = '''<path d="M40 82 L 40 66 Q 40 58 50 58 Q 60 58 60 66 L 60 82 Z" fill="#f5efe1" opacity="0.9"/>
  <path d="M50 58 L 50 82" stroke="#0b3b5c" stroke-width="1.2"/>
  <path d="M40 70 L 60 70" stroke="#0b3b5c" stroke-width="1.2"/>'''
    elif style == "franciscan":
        motif = '''<path d="M35 72 L 65 72 M 50 62 L 50 82" stroke="#f5efe1" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="50" cy="72" r="3.5" fill="#d4a94a"/>'''
    elif style == "cathedral":
        # Twin gothic spires with a central cross — for St. Mary's Basilica
        motif = '''<path d="M38 82 L 38 70 L 34 70 L 42 60 L 42 82 Z" fill="#f5efe1" opacity="0.92"/>
  <path d="M62 82 L 62 70 L 58 70 L 66 60 L 66 82 Z" fill="#f5efe1" opacity="0.92"/>
  <path d="M50 62 L 50 78 M 44 68 L 56 68" stroke="#d4a94a" stroke-width="2" stroke-linecap="round"/>'''
    else:  # trinity
        motif = '''<circle cx="50" cy="70" r="4" fill="none" stroke="#f5efe1" stroke-width="2"/>
  <circle cx="42" cy="78" r="4" fill="none" stroke="#f5efe1" stroke-width="2"/>
  <circle cx="58" cy="78" r="4" fill="none" stroke="#f5efe1" stroke-width="2"/>'''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Crest">\n  {shield}\n  {star}\n  {motif}\n</svg>\n'


# ---------------------------------------------------------------------------
# Page skeleton
# ---------------------------------------------------------------------------

def head(parish, page_title, css_prefix="assets/") -> str:
    return f'''<!DOCTYPE html>
<html lang="{parish['lang']}">
<head>
<meta charset="utf-8">
<title>{html.escape(page_title)} — {html.escape(parish['short'])}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(parish['tagline'])}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_prefix}style.css">
<link rel="icon" type="image/svg+xml" href="{css_prefix}crest.svg">
</head>
<body>
'''

def header(parish, css_prefix="assets/") -> str:
    return f'''<header class="site-header">
  <div class="container">
    <img src="{css_prefix}crest.svg" alt="" class="crest" aria-hidden="true">
    <div class="site-title">
      <h1>{html.escape(parish['name'])}</h1>
      <div class="sub">{html.escape(parish['city'])} — {html.escape(parish['tagline'])}</div>
    </div>
  </div>
</header>
'''

def nav(parish, active) -> str:
    s = STRINGS[parish['lang']]
    items = [
        ("index.html", s["home"]),
        ("about.html", s["about"]),
        ("mass.html", s["mass"]),
        ("life.html", s["life"]),
        ("contact.html", s["contact"]),
    ]
    links = []
    for href, label in items:
        cls = ' class="active"' if href == active else ''
        links.append(f'    <a href="{href}"{cls}>{html.escape(label)}</a>')
    portal_back = "../../index.html"
    return f'''<nav class="site-nav" aria-label="Navigation">
  <div class="container">
{chr(10).join(links)}
    <a href="{portal_back}" style="margin-left:auto; color: var(--stella-gold-light);">{html.escape(s["portal_back"])}</a>
  </div>
</nav>
'''

def footer(parish) -> str:
    s = STRINGS[parish['lang']]
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-cols">
      <div>
        <h4>{html.escape(s["reach_us"])}</h4>
        <p>{html.escape(parish['address'])}<br>
        {html.escape("Tel." if parish['lang'].startswith('en') else "Tél.")} : {html.escape(parish['phone'])}<br>
        <a href="mailto:{parish['email']}">{parish['email']}</a></p>
      </div>
      <div>
        <h4>{html.escape(s["on_this_site"])}</h4>
        <p><a href="mass.html">{html.escape(s["mass"])}</a><br>
        <a href="life.html">{html.escape(s["life"])}</a><br>
        <a href="contact.html">{html.escape(s["contact"])}</a></p>
      </div>
      <div>
        <h4>{html.escape(s["official_source"])}</h4>
        <p><a href="{parish['official_url']}">{html.escape(parish['official_url'].replace('https://', ''))}</a><br>
        {html.escape(parish['diocese'])}</p>
      </div>
    </div>
    <div class="tribute">
      <p>{html.escape(s["tribute_line"])} <span class="name">{html.escape(FOUNDER)}</span>.</p>
      <p>{html.escape(s["mirror_note"])}</p>
      <p style="margin-top:0.8rem; font-size:0.78rem;">{html.escape(s["no_tracking"])} <em>{html.escape(s["for_people"])}</em></p>
    </div>
  </div>
</footer>
</body>
</html>
'''

# ---------------------------------------------------------------------------
# Parish pages
# ---------------------------------------------------------------------------

def page_index(parish) -> str:
    s = STRINGS[parish['lang']]
    if parish['lang'] == 'fr-CA':
        blurb = f"""<p>La {parish['name']}, fondée en {parish['founded']}, est située à {parish['city']}. Ce site est un miroir non-officiel préparé sous la doctrine <em>EVE Glyph Design</em>, avec le même soin éditorial que le site officiel de la paroisse. La source officielle demeure <a href="{parish['official_url']}">{parish['official_url'].replace('https://', '')}</a>.</p>"""
        card_title = "Une paroisse, un peuple"
        card_body = "La foi vécue localement, avec la communauté qui prie, célèbre et prend soin les uns des autres."
        h1 = s["welcome"]
    else:
        blurb = f"""<p>{parish['name']}, founded in {parish['founded']}, is located in {parish['city']}. This site is a non-official mirror prepared under the <em>EVE Glyph Design</em> doctrine, with the same editorial care as the parish's official site. The official source remains <a href="{parish['official_url']}">{parish['official_url'].replace('https://', '')}</a>.</p>"""
        card_title = "One parish, one people"
        card_body = "Faith lived locally, with a community that prays, celebrates and cares for one another."
        h1 = s["welcome"]

    body = f'''<main>
  <div class="container">
    <h1>{h1}</h1>
    <p class="lead">{s["welcome_lead"]}</p>
    {blurb}
    <div class="card">
      <h3>{card_title}</h3>
      <p>{card_body}</p>
    </div>

    <h2>{s["mass"]}</h2>
    <table class="schedule">
      <thead><tr><th>{s["mass_day"]}</th><th>{s["mass_time"]}</th></tr></thead>
      <tbody>
{chr(10).join(f'        <tr><td>{html.escape(d)}</td><td>{html.escape(t)}</td></tr>' for d, t in parish["schedule"])}
      </tbody>
    </table>
  </div>
</main>
'''
    return head(parish, s["welcome"]) + header(parish) + nav(parish, "index.html") + body + footer(parish)


def page_about(parish) -> str:
    s = STRINGS[parish['lang']]
    if parish['lang'] == 'fr-CA':
        body = f"""<main><div class="container">
<h1>{s['about_h1']}</h1>
<p class="lead">{parish['tagline']}.</p>
<p>Fondée en {parish['founded']}, la {parish['name']} sert la communauté de {parish['city']}. Elle fait partie de {parish['diocese']}.</p>
<p>Cette page est un espace de présentation. Pour l'historique complet, la biographie des curés et le récit de l'église, consultez le site officiel de la paroisse : <a href="{parish['official_url']}">{parish['official_url'].replace('https://', '')}</a>.</p>
<div class="card">
  <h3>Notre engagement</h3>
  <p>Site local, hébergement libre, aucun traçage, aucune publicité. La paroisse reste propriétaire de son contenu et peut reprendre ce miroir à tout moment.</p>
</div>
</div></main>"""
    else:
        body = f"""<main><div class="container">
<h1>{s['about_h1']}</h1>
<p class="lead">{parish['tagline']}.</p>
<p>Founded in {parish['founded']}, {parish['name']} serves the community of {parish['city']}. It is part of {parish['diocese']}.</p>
<p>This page introduces the parish. For the full history, clergy biographies, and church story, please visit the parish's official site: <a href="{parish['official_url']}">{parish['official_url'].replace('https://', '')}</a>.</p>
<div class="card">
  <h3>Our commitment</h3>
  <p>Locally hosted, no tracking, no ads. The parish owns its content and may take over this mirror at any time.</p>
</div>
</div></main>"""
    return head(parish, s["about_h1"]) + header(parish) + nav(parish, "about.html") + body + footer(parish)


def page_mass(parish) -> str:
    s = STRINGS[parish['lang']]
    body = f'''<main><div class="container">
<h1>{s["mass_h1"]}</h1>
<table class="schedule">
  <thead><tr><th>{s["mass_day"]}</th><th>{s["mass_time"]}</th></tr></thead>
  <tbody>
{chr(10).join(f'    <tr><td>{html.escape(d)}</td><td>{html.escape(t)}</td></tr>' for d, t in parish["schedule"])}
  </tbody>
</table>
<p><a href="{parish['official_url']}">{html.escape(s["official_source"])}</a></p>
</div></main>'''
    return head(parish, s["mass_h1"]) + header(parish) + nav(parish, "mass.html") + body + footer(parish)


def page_life(parish) -> str:
    s = STRINGS[parish['lang']]
    if parish['lang'] == 'fr-CA':
        items = ["Groupe de prières", "Adoration eucharistique", "Chorale", "Catéchèse", "Chevaliers de Colomb", "Comité de pastorale", "Aide aux personnes démunies", "Bénévolat paroissial"]
        title = "Vie paroissiale"
        intro = "Voici les groupes actifs dans la paroisse. Pour plus de détails ou pour vous joindre à un groupe, contactez le secrétariat de la paroisse."
    else:
        items = ["Prayer group", "Eucharistic adoration", "Choir", "Faith formation", "Knights of Columbus", "Parish pastoral council", "Outreach to those in need", "Parish volunteering"]
        title = "Parish life"
        intro = "The active groups in the parish. To learn more or to join a group, contact the parish office."
    body = f'''<main><div class="container">
<h1>{title}</h1>
<p class="lead">{intro}</p>
<ul class="groups">
{chr(10).join(f'  <li>{html.escape(x)}</li>' for x in items)}
</ul>
</div></main>'''
    return head(parish, title) + header(parish) + nav(parish, "life.html") + body + footer(parish)


def page_contact(parish) -> str:
    s = STRINGS[parish['lang']]
    dt_lbls = ("Adresse", "Téléphone", "Courriel", "Diocèse") if parish['lang'] == 'fr-CA' else ("Address", "Phone", "Email", "Diocese")
    body = f'''<main><div class="container">
<h1>{s["contact_h1"]}</h1>
<div class="contact-block">
  <dl>
    <dt>{dt_lbls[0]}</dt><dd>{html.escape(parish['address'])}</dd>
    <dt>{dt_lbls[1]}</dt><dd>{html.escape(parish['phone'])}</dd>
    <dt>{dt_lbls[2]}</dt><dd><a href="mailto:{parish['email']}">{parish['email']}</a></dd>
    <dt>{dt_lbls[3]}</dt><dd>{html.escape(parish['diocese'])}</dd>
  </dl>
</div>
<p><a href="{parish['official_url']}">{html.escape(s["official_source"])} → {parish['official_url'].replace('https://', '')}</a></p>
</div></main>'''
    return head(parish, s["contact_h1"]) + header(parish) + nav(parish, "contact.html") + body + footer(parish)


# ---------------------------------------------------------------------------
# Portal (front page)
# ---------------------------------------------------------------------------

def portal() -> str:
    cards = []
    for p in PARISHES:
        cards.append(f'''      <a class="parish-card" href="parishes/{p['slug']}/index.html">
        <div class="parish-card-crest"><img src="parishes/{p['slug']}/assets/crest.svg" alt=""></div>
        <div class="parish-card-body">
          <h3>{html.escape(p['short'])}</h3>
          <p class="parish-card-city">{html.escape(p['city'])}</p>
          <p class="parish-card-blurb">{html.escape(p['portal_blurb'])}</p>
          <p class="parish-card-founded">Founded {p['founded']} · {html.escape(p['diocese'])}</p>
        </div>
      </a>''')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>PAIX Parish Platform — Parish Sovereign Gateway</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A parish-owned platform template. Locally hosted, no tracking, no ads. Under the EVE Glyph Design doctrine.">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/portal.css">
<link rel="icon" type="image/svg+xml" href="assets/portal-crest.svg">
</head>
<body class="portal-body">

<header class="site-header portal-header">
  <div class="container">
    <img src="assets/portal-crest.svg" alt="" class="crest" aria-hidden="true">
    <div class="site-title">
      <h1>PAIX Parish Platform</h1>
      <div class="sub">Parish Sovereign Gateway — a community-first alternative to predatory hosting</div>
    </div>
  </div>
</header>

<nav class="site-nav">
  <div class="container">
    <a href="index.html" class="active">Parishes</a>
    <a href="#about">About the platform</a>
    <a href="#kofc">For the Knights</a>
    <a href="#doctrine">Doctrine</a>
  </div>
</nav>

<main>
  <div class="container portal-hero">
    <h1>A parish website belongs to the parish.</h1>
    <p class="lead">Six parishes, one design canon. Locally hosted. No tracking. No ads. No third-party predators. Every dollar stays in the community.</p>
    <p>Select a parish to enter its site. Every parish site shares the same EVE Glyph Design canon, so navigation and typography stay familiar. Each parish's official site remains the source of truth — this is a mirror prepared with care, ready to be handed over to the parish's existing IT volunteer whenever they want it.</p>
  </div>

  <div class="container">
    <div class="parish-grid">
{chr(10).join(cards)}
    </div>
  </div>

  <div class="container portal-section" id="about">
    <h2>What this is</h2>
    <p>Six Catholic parishes, each with a mirrored site under a shared editorial template. Same header, same footer, same navigation — but each parish keeps its own crest, mass times, contact information and diocesan link. If a parish already has an IT volunteer, this is not a replacement; it is an option they can inspect, fork, or ignore.</p>
    <div class="pillars">
      <div class="pillar">
        <h4>Locally hosted</h4>
        <p>Static site on GitHub Pages or the parish's own hosting. No third-party dashboards, no vendor lock-in.</p>
      </div>
      <div class="pillar">
        <h4>Zero surveillance</h4>
        <p>No cookies. No analytics. No third-party scripts other than Google Fonts. <em>noindex, nofollow</em> until the parish approves publication.</p>
      </div>
      <div class="pillar">
        <h4>Full parish ownership</h4>
        <p>The parish owns its content, its domain, and its exit. Fork the repository, take it home, keep going.</p>
      </div>
      <div class="pillar">
        <h4>Consistent design</h4>
        <p>Shared EVE Glyph Design canon so parishioners moving between parish sites feel at home.</p>
      </div>
    </div>
  </div>

  <div class="container portal-section" id="kofc">
    <h2>For the Knights of Columbus</h2>
    <p class="lead">This is what "scale in a week" looks like — with no hurt feelings.</p>
    <p>If the Knights want to standardize parish web presence across a diocese, this template can spin up a new parish site in about an hour. But that is not the offer. The offer is a <em>choice</em>:</p>
    <ul class="kofc-list">
      <li><strong>Existing IT volunteer stays put.</strong> If a Brother Knight or parishioner is already running the parish site, nothing is disrupted. This platform is available if they want to switch or fork; otherwise it sits alongside their existing work as a reference.</li>
      <li><strong>Money stays in the parish.</strong> No annual GoDaddy invoices, no Squarespace subscriptions, no Facebook advertising credits. Static hosting on GitHub Pages is free, and every dollar the parish saves stays in the community.</li>
      <li><strong>Parishioners stay safe.</strong> No surveillance, no engagement-optimized feeds, no algorithmic exposure of children, women, or vulnerable people. The parish site is a parish site — not a data-extraction surface for a platform in California.</li>
      <li><strong>The Knights stay in charge.</strong> Ownership, doctrine and exit rights belong to the parish and its Council. The design canon is a shared reference, not a vendor contract.</li>
    </ul>
    <p class="kofc-note">Council of Palms #6673 (Holy Trinity, Lenexa) is the reference council for this build.</p>
  </div>

  <div class="container portal-section" id="doctrine">
    <h2>Doctrine</h2>
    <div class="doctrine-grid">
      <div>
        <h4>No profiling</h4>
        <p>No parishioner is scored, categorized or targeted by this platform. Ever.</p>
      </div>
      <div>
        <h4>Safety first, betterment second</h4>
        <p>Content and identity safety comes before growth, engagement, or monetization.</p>
      </div>
      <div>
        <h4>Founder credit</h4>
        <p>Design founder: <strong>{FOUNDER}</strong>, EVE Glyph Design. This credit is irrevocable.</p>
      </div>
      <div>
        <h4>Parish sovereignty</h4>
        <p>The parish binds the platform, receives a governance receipt, and may exit with full content export at any time.</p>
      </div>
    </div>
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-cols">
      <div>
        <h4>PAIX Parish Platform</h4>
        <p>A Parish Sovereign Gateway reference build.<br>
        Under the EVE Glyph Design doctrine.<br>
        Contact the parish directly — see each parish page for details.</p>
      </div>
      <div>
        <h4>Parishes</h4>
        <p>{"<br>".join(f'<a href="parishes/{p["slug"]}/index.html">{html.escape(p["short"])}</a>' for p in PARISHES)}</p>
      </div>
      <div>
        <h4>Reference</h4>
        <p><a href="https://github.com/EVEglyphDesign/paroisse-sainte-anne-des-pays-bas">Sainte-Anne source repo</a><br>
        <a href="https://github.com/EVEglyphDesign/kofc-6673-outreach">KofC #6673 outreach</a><br>
        <a href="https://github.com/EVEglyphDesign/godaddy-killer">GoDaddy-Killer migration kit</a></p>
      </div>
    </div>
    <div class="tribute">
      <p>Platform designed under the doctrine <em>EVE Glyph Design</em>. Design founder: <span class="name">{FOUNDER}</span>.</p>
      <p>Every parish retains full ownership of its own content, domain and exit path. This is a mirror prepared with care, not a takeover.</p>
      <p style="margin-top:0.8rem; font-size:0.78rem;">No tracking. No cookies. No analytics. No third-party scripts other than Google Fonts. <em>For the good of the people. Pour le bien-être du peuple.</em></p>
    </div>
  </div>
</footer>
</body>
</html>
'''


# ---------------------------------------------------------------------------
# Extra portal CSS
# ---------------------------------------------------------------------------

PORTAL_CSS = '''/* Portal-specific extensions to the EVE Glyph canon */
.portal-body main { background: var(--white); padding: 2.5rem 0 4rem; }
.portal-header .site-title h1 { font-size: 1.85rem; }
.portal-hero { max-width: 780px; }
.portal-hero h1 { font-size: 2.7rem; margin-bottom: 0.6rem; }
.portal-hero .lead { font-size: 1.3rem; margin-bottom: 1.2rem; }

.parish-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.4rem;
  max-width: 1100px;
  margin: 2.5rem auto 3rem;
}
.parish-card {
  display: flex;
  flex-direction: column;
  background: var(--parchment);
  border: 1px solid var(--rule);
  border-left: 4px solid var(--stella-gold);
  padding: 1.4rem 1.4rem 1.2rem;
  text-decoration: none;
  color: var(--ink);
  transition: transform 0.15s, box-shadow 0.15s, border-left-color 0.15s;
}
.parish-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(11, 59, 92, 0.12);
  border-left-color: var(--marine);
  color: var(--ink);
}
.parish-card-crest {
  width: 54px; height: 54px; margin-bottom: 0.9rem;
}
.parish-card-crest img { width: 100%; height: 100%; display: block; }
.parish-card h3 {
  font-size: 1.35rem;
  color: var(--marine-deep);
  margin: 0 0 0.2rem;
}
.parish-card-city {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  color: var(--ink-soft);
  margin: 0 0 0.7rem;
  font-size: 1.02rem;
}
.parish-card-blurb {
  color: var(--ink-soft);
  font-size: 0.95rem;
  margin: 0 0 0.8rem;
  line-height: 1.55;
}
.parish-card-founded {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--marine);
  margin: auto 0 0;
  padding-top: 0.6rem;
  border-top: 1px dotted var(--rule);
}

.portal-section {
  max-width: 900px;
  margin-top: 3rem;
  padding-top: 2.4rem;
  border-top: 1px solid var(--rule);
}
.portal-section h2 {
  font-size: 2rem;
  color: var(--marine-deep);
  margin-bottom: 0.4em;
}
.pillars {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.4rem;
  margin-top: 1.4rem;
}
.pillar {
  background: var(--parchment);
  border-left: 3px solid var(--stella-gold);
  padding: 1rem 1.2rem;
}
.pillar h4 {
  color: var(--marine);
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 1.15rem;
  margin: 0 0 0.35em;
}
.pillar p { font-size: 0.94rem; margin: 0; color: var(--ink-soft); }

.kofc-list {
  list-style: none;
  padding: 0;
  margin: 1.4rem 0;
}
.kofc-list li {
  padding: 0.8rem 0 0.9rem 1.2rem;
  border-top: 1px solid var(--rule);
  position: relative;
}
.kofc-list li:last-child { border-bottom: 1px solid var(--rule); }
.kofc-list li::before {
  content: "◆";
  color: var(--stella-gold);
  position: absolute;
  left: 0;
  top: 0.85rem;
  font-size: 0.85rem;
}
.kofc-list li strong { color: var(--marine-deep); }
.kofc-note {
  font-style: italic;
  color: var(--marine);
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 1.05rem;
  margin-top: 0.8rem;
}

.doctrine-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.6rem;
  margin-top: 1.4rem;
}
.doctrine-grid h4 {
  color: var(--marine-deep);
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 1.2rem;
  margin: 0 0 0.35em;
  padding-bottom: 0.35em;
  border-bottom: 1px solid var(--rule);
}
.doctrine-grid p { color: var(--ink-soft); font-size: 0.95rem; }

@media (max-width: 600px) {
  .portal-hero h1 { font-size: 2rem; }
  .portal-hero .lead { font-size: 1.1rem; }
  .portal-section h2 { font-size: 1.6rem; }
}
'''

# Portal crest — the composite five-shield mark
PORTAL_CREST = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="PAIX Parish Platform">
  <defs>
    <linearGradient id="marine" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1a5578"/>
      <stop offset="1" stop-color="#0b3b5c"/>
    </linearGradient>
  </defs>
  <!-- Outer ring -->
  <circle cx="50" cy="50" r="44" fill="url(#marine)" stroke="#b8892b" stroke-width="1.5"/>
  <!-- Central cross -->
  <path d="M50 24 L 50 76 M 30 50 L 70 50" stroke="#d4a94a" stroke-width="3.5" stroke-linecap="round"/>
  <!-- Four cardinal dots + one center = five parishes -->
  <circle cx="50" cy="24" r="4" fill="#f5efe1"/>
  <circle cx="50" cy="76" r="4" fill="#f5efe1"/>
  <circle cx="30" cy="50" r="4" fill="#f5efe1"/>
  <circle cx="70" cy="50" r="4" fill="#f5efe1"/>
  <circle cx="50" cy="50" r="5" fill="#d4a94a" stroke="#0b3b5c" stroke-width="1"/>
</svg>
'''

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    # Portal assets
    (ROOT / "assets" / "portal.css").write_text(PORTAL_CSS)
    (ROOT / "assets" / "portal-crest.svg").write_text(PORTAL_CREST)

    # Portal front page
    (ROOT / "index.html").write_text(portal())

    # Per-parish sites
    for p in PARISHES:
        pdir = PARISHES_DIR / p["slug"]
        adir = pdir / "assets"
        adir.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / "assets" / "style.css", adir / "style.css")
        (adir / "crest.svg").write_text(crest_svg(p["crest_style"]))
        (pdir / "index.html").write_text(page_index(p))
        (pdir / "about.html").write_text(page_about(p))
        (pdir / "mass.html").write_text(page_mass(p))
        (pdir / "life.html").write_text(page_life(p))
        (pdir / "contact.html").write_text(page_contact(p))
        print(f"  ✓ {p['slug']} ({p['name']})")

    print(f"\nBuilt {len(PARISHES)} parishes + portal at {ROOT}")

if __name__ == "__main__":
    build()
