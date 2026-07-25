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

# Order matters: this is the on-portal display order, grouped by region.
#   1. United States  — Lenexa, Kansas, then St. Augustine, Florida
#   2. Montréal       — the one on the mountain
#   3. Atlantic Canada — New Brunswick, PEI, Nova Scotia
#   4. México          — Bahía de Banderas, Nayarit
PARISHES = [
    {
        "slug": "holy-trinity",
        "name": "Holy Trinity Catholic Parish",
        "short": "Holy Trinity \u2014 Lenexa",
        "city": "Lenexa, Kansas",
        "founded": "1979",
        "lang": "en-US",
        "official_url": "https://htlenexa.org",
        "address": "13615 W 92nd Street, Lenexa, KS 66215",
        "phone": "(913) 888-2770",
        "email": "info@htlenexa.org",
        "tagline": "Parish, school & early education center \u2014 Archdiocese of Kansas City in Kansas",
        "diocese": "Archdiocese of Kansas City in Kansas \u00b7 Knights of Columbus Council of Palms #6673",
        "schedule": [
            ("Saturday Vigil", "4:00 PM"),
            ("Sunday", "7:30 AM \u00b7 9:30 AM \u00b7 11:30 AM"),
            ("Monday \u2013 Friday", "6:45 AM & 8:15 AM"),
            ("Saturday", "8:00 AM"),
        ],
        "crest_style": "trinity",
        "portal_blurb": "Home parish of Knights of Columbus Council of Palms #6673.",
        "region": "united-states",
        "founded_line": "Founded 1979 · Archdiocese of Kansas City in Kansas · Knights of Columbus Council of Palms #6673",
        "photo_credit": None,
    },
    {
        "slug": "cathedral-basilica-st-augustine",
        "name": "Cathedral Basilica of St. Augustine",
        "short": "Cathedral Basilica of St. Augustine",
        "city": "St. Augustine, Florida",
        "founded": "1565",
        "lang": "en-US",
        "region": "united-states",
        "official_url": "https://thefirstparish.org",
        "address": "38 Cathedral Place, St. Augustine, FL 32084",
        "phone": "(904) 824-2806",
        "email": "cathparish@gmail.com",
        "tagline": "America\u2019s first parish \u2014 a congregation at Mass since 8 September 1565",
        "diocese": "Diocese of St. Augustine",
        "schedule": [
            ("Saturday Vigil", "5:00 PM"),
            ("Sunday", "7:00 AM \u00b7 9:00 AM \u00b7 11:00 AM \u00b7 5:00 PM"),
            ("Monday \u2013 Friday", "7:00 AM"),
            ("Saturday", "7:00 AM"),
            ("Reconciliation \u2014 Saturday", "after 7:00 AM Mass \u00b7 3:30 \u2013 4:30 PM"),
        ],
        "crest_style": "spanish",
        "portal_blurb": "The oldest Catholic congregation in the continental United States. Mass has been said here since 1565.",
        "founded_line": "Congregation 1565 \u00b7 Present church 1793\u20131797 \u00b7 Minor basilica 1976 \u00b7 Diocese of St. Augustine",
        "photo_credit": "Photograph: Carlstak, CC BY-SA 4.0, via Wikimedia Commons",
        "photo_credit_url": "https://commons.wikimedia.org/wiki/File:Facade_of_Cathedral_of_St._Augustine.jpg",
    },
    {
        "slug": "saint-joseph-oratory",
        "name": "Oratoire Saint-Joseph du Mont-Royal",
        "short": "Oratoire Saint-Joseph du Mont-Royal",
        "city": "Montr\u00e9al, Qu\u00e9bec",
        "founded": "1904",
        "lang": "fr-CA",
        "region": "montreal",
        "official_url": "https://saint-joseph.org",
        "address": "3800, chemin Queen Mary, Montr\u00e9al (Qu\u00e9bec) H3V 1H6",
        "phone": "(514) 733-8211",
        "email": "info@osj.qc.ca",
        "tagline": "Basilique mineure et sanctuaire national \u2014 fond\u00e9 en 1904 par saint fr\u00e8re Andr\u00e9",
        "diocese": "Archidioc\u00e8se de Montr\u00e9al \u00b7 Congr\u00e9gation de Sainte-Croix",
        "schedule": [
            ("Dimanche \u2014 crypte (fran\u00e7ais)", "7 h \u00b7 8 h \u00b7 9 h 30 \u00b7 16 h 30 \u00b7 19 h 30"),
            ("Dimanche \u2014 basilique (fran\u00e7ais)", "11 h \u00b7 12 h 30"),
            ("Dimanche \u2014 anglais / espagnol", "11 h 15 \u00b7 15 h"),
            ("Lundi \u2013 samedi \u2014 crypte", "7 h \u00b7 8 h 30 \u00b7 10 h \u00b7 11 h 30 \u00b7 16 h 30 \u00b7 19 h 30"),
            ("Lundi \u2013 samedi \u2014 anglais", "12 h 15"),
            ("Mercredi \u2014 messe pour les malades", "14 h"),
        ],
        "crest_style": "dome",
        "portal_blurb": "La plus grande \u00e9glise du Canada, sur le flanc du mont Royal. Fond\u00e9e en 1904 par un portier, saint fr\u00e8re Andr\u00e9.",
        "founded_line": "Fond\u00e9 1904 \u00b7 Basilique mineure 1955 \u00b7 Lieu historique national du Canada",
        "status_note": "Sanctuaire national et basilique mineure \u2014 non pas une paroisse territoriale.",
        "photo_credit": "Photo : Paolo Costa Baldi, GFDL / CC BY-SA 3.0, via Wikimedia Commons",
        "photo_credit_url": "https://commons.wikimedia.org/wiki/File:Oratoire_Saint-Joseph_du_Mont-Royal_-_Montreal.jpg",
    },
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
        "region": "atlantic-canada",
        "photo_alt": "Église Sainte-Anne-des-Pays-Bas, 715 rue Priestman, Fredericton",
        "city_line": "Fredericton, Nouveau-Brunswick · 715 rue Priestman",
        "portal_blurb_override": "La seule paroisse catholique francophone de Fredericton. Fondée en 1981 — église actuelle ouverte en 2001, sur un terrain défriché par la communauté acadienne.",
        "founded_line": "Paroisse fondée 1981 · Église 2001 · Archidiocèse de Moncton",
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
        "region": "atlantic-canada",
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
        "region": "atlantic-canada",
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
        "region": "atlantic-canada",
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
        "region": "atlantic-canada",
    },
    {
        "slug": "sagrada-familia-nuevo-vallarta",
        "name": "Cuasiparroquia de la Sagrada Familia",
        "short": "Sagrada Familia \u2014 Nuevo Vallarta",
        "city": "Las Jarretaderas, Nayarit",
        "founded": "",
        "lang": "es-MX",
        "region": "mexico",
        "official_url": "http://diocesisdetepic.mx/decanato-bahia-de-banderas/",
        "address": "J. Mar\u00eda Morelos e Independencia, Las Jarretaderas, C.P. 63735, Bah\u00eda de Banderas, Nayarit",
        "phone": "(322) 297-0514",
        "email": "",
        "tagline": "La cuasiparroquia de Las Jarretaderas, a la entrada de Nuevo Vallarta y su marina",
        "diocese": "Di\u00f3cesis de Tepic \u00b7 Decanato Bah\u00eda de Banderas",
        "schedule": [
            ("Domingo", "8:30 \u00b7 12:00 \u00b7 18:30"),
            ("Martes \u2013 jueves", "7:30"),
            ("Jueves", "19:00"),
            ("S\u00e1bado", "7:30"),
            ("Confesiones \u2014 domingo", "10:00 \u2013 14:00"),
        ],
        "crest_style": "sun",
        "portal_blurb": "La parroquia del pueblo de Las Jarretaderas, a la entrada de Nuevo Vallarta, la marina y el corredor hospitalario.",
        "founded_line": "Cuasiparroquia \u00b7 Di\u00f3cesis de Tepic \u00b7 Decanato Bah\u00eda de Banderas",
        "photo_status": "pending",
        "schedule_note": "Horario seg\u00fan el directorio diocesano de Tepic. Conviene confirmar por tel\u00e9fono antes de asistir.",
    },
    {
        "slug": "santa-cruz-huanacaxtle",
        "name": "Parroquia de La Santa Cruz",
        "short": "La Santa Cruz \u2014 La Cruz de Huanacaxtle",
        "city": "La Cruz de Huanacaxtle, Nayarit",
        "founded": "",
        "lang": "es-MX",
        "region": "mexico",
        "official_url": "https://www.facebook.com/p/Parroquia-de-La-Santa-Cruz-de-Huanacaxtle-Oficial-61570443480543/",
        "address": "Calle Marl\u00edn 38, La Cruz de Huanacaxtle, C.P. 63732, Bah\u00eda de Banderas, Nayarit",
        "phone": "+52 329 295 5622",
        "email": "pcruzdehuanacaxtle@gmail.com",
        "tagline": "La parroquia del pueblo pesquero y de la Marina Riviera Nayarit",
        "diocese": "Di\u00f3cesis de Tepic \u00b7 Decanato Bah\u00eda de Banderas",
        "schedule": [
            ("Domingo", "10:30 \u00b7 12:00 \u00b7 20:00"),
            ("S\u00e1bado", "20:00"),
            ("Oficina parroquial", "10:00 \u2013 13:00 \u00b7 17:00 \u2013 20:00"),
        ],
        "crest_style": "cross",
        "portal_blurb": "Parroquia de un pueblo pesquero de Nayarit convertido en puerto n\u00e1utico, junto a la Marina Riviera Nayarit.",
        "founded_line": "Di\u00f3cesis de Tepic \u00b7 Decanato Bah\u00eda de Banderas",
        "photo_status": "pending",
        "schedule_note": "Horario reportado por feligreses; algunos directorios lo publican mal. Conviene confirmar por tel\u00e9fono.",
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
    "es-MX": {
        "home": "Inicio",
        "about": "Nuestra parroquia",
        "pastors": "Clero",
        "church": "Nuestro templo",
        "mass": "Horario de misas",
        "bulletin": "Boletín",
        "life": "Vida parroquial",
        "catechesis": "Catequesis",
        "events": "Eventos",
        "links": "Enlaces",
        "contact": "Contacto",
        "welcome": "Bienvenidos",
        "mass_h1": "Horario de misas",
        "mass_day": "Día",
        "mass_time": "Hora",
        "contact_h1": "Comuníquese con nosotros",
        "about_h1": "Nuestra parroquia",
        "reach_us": "Comuníquese",
        "on_this_site": "En este sitio",
        "doctrine": "Doctrina",
        "no_profile": "Sin perfilado",
        "register": "Registro de lengua",
        "founder": "Crédito del fundador",
        "portal_back": "← Volver al portal",
        "official_source": "Fuente oficial",
        "mirror_note": "Espejo no oficial, preparado con cuidado. Contenido parroquial: © la parroquia, todos los derechos reservados.",
        "no_tracking": "Sin rastreo. Sin cookies. Sin analítica. Sin scripts de terceros salvo Google Fonts.",
        "tribute_line": "Sitio construido bajo la doctrina EVE Glyph Design. Fundador del diseño:",
        "for_people": "Por el bien del pueblo.",
        "welcome_lead": "Bienvenidos al sitio de la parroquia.",
    },
}

FOUNDER = "Donat Omer Thériault"

# Mandatory verbatim rights footer — EVE Glyph Index L0 canon, Gate 2.
# Do not reword, abbreviate, or translate this string.
ARK_FOOTER = (
    "© 2026 Dany Theriault. EVE \u201cdigital stem cell\u201d glyph and glyph-based design "
    "principles — all rights reserved. Stewardship of rights of use and assignment for "
    "large public and institutional usage rests with the Pacific Utilities Design Council. "
    "Published as a time-stamped record of authorship and intent."
)

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
    elif style == "spanish":
        # Spanish-colonial bell gable (espadaña) with a single bell — St. Augustine, Florida
        motif = '''<path d="M34 84 L 34 70 Q 50 58 66 70 L 66 84 Z" fill="#f5efe1" opacity="0.92"/>
  <path d="M50 66 L 50 78" stroke="#0b3b5c" stroke-width="1.4"/>
  <circle cx="50" cy="74" r="3.2" fill="#d4a94a"/>'''
    elif style == "dome":
        # Great dome on a drum — Oratoire Saint-Joseph du Mont-Royal
        motif = '''<path d="M34 84 L 34 74 Q 50 56 66 74 L 66 84 Z" fill="#f5efe1" opacity="0.92"/>
  <path d="M34 76 L 66 76" stroke="#0b3b5c" stroke-width="1.2"/>
  <path d="M50 56 L 50 50 M 46 53 L 54 53" stroke="#d4a94a" stroke-width="2" stroke-linecap="round"/>'''
    elif style == "sun":
        # Rayed sun over water — Sagrada Familia, Bahía de Banderas
        motif = '''<circle cx="50" cy="70" r="7" fill="#d4a94a"/>
  <g stroke="#f5efe1" stroke-width="1.8" stroke-linecap="round">
    <path d="M50 58 L 50 61"/><path d="M41.5 61.5 L 43.6 63.6"/><path d="M58.5 61.5 L 56.4 63.6"/>
    <path d="M38 70 L 41 70"/><path d="M59 70 L 62 70"/>
  </g>
  <path d="M30 82 Q 40 78, 50 82 T 70 82" fill="none" stroke="#f5efe1" stroke-width="2" stroke-linecap="round"/>'''
    elif style == "cross":
        # The standing cross the town is named for — La Cruz de Huanacaxtle
        motif = '''<path d="M50 58 L 50 84 M 40 66 L 60 66" stroke="#f5efe1" stroke-width="3" stroke-linecap="round"/>
  <circle cx="50" cy="66" r="3" fill="#d4a94a"/>'''
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

def tel_label(parish) -> str:
    if parish['lang'] == 'fr-CA':
        return "Tél."
    if parish['lang'] == 'es-MX':
        return "Tel."
    return "Tel."


def footer(parish) -> str:
    s = STRINGS[parish['lang']]
    email_line = (f'<br>\n        <a href="mailto:{parish["email"]}">{parish["email"]}</a>'
                  if parish.get('email') else '')
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-cols">
      <div>
        <h4>{html.escape(s["reach_us"])}</h4>
        <p>{html.escape(parish['address'])}<br>
        {html.escape(tel_label(parish))} : {html.escape(parish['phone'])}{email_line}</p>
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
    {photo_credit_block(parish)}
    <div class="ark-footer">
      <p>{html.escape(ARK_FOOTER)}</p>
    </div>
  </div>
</footer>
</body>
</html>
'''


def photo_credit_block(parish) -> str:
    """Photograph attribution, where a licensed photograph is in use."""
    if not parish.get('photo_credit'):
        return ''
    credit = html.escape(parish['photo_credit'])
    url = parish.get('photo_credit_url')
    if url:
        credit = f'<a href="{url}">{credit}</a>'
    return f'<div class="photo-credit"><p>{credit}</p></div>'

# ---------------------------------------------------------------------------
# Parish pages
# ---------------------------------------------------------------------------

def page_index(parish) -> str:
    s = STRINGS[parish['lang']]
    src_link = f'<a href="{parish["official_url"]}">{tidy_url(parish["official_url"])}</a>'
    if parish['lang'] == 'fr-CA':
        founded_clause = f", fondée en {parish['founded']}," if parish['founded'] else ""
        blurb = f"""<p>L'{parish['name']}{founded_clause} est située à {parish['city']}. Ce site est un miroir non-officiel préparé sous la doctrine <em>EVE Glyph Design</em>, avec le même soin éditorial que le site officiel. La source officielle demeure {src_link}.</p>"""
        card_title = "Une paroisse, un peuple"
        card_body = "La foi vécue localement, avec la communauté qui prie, célèbre et prend soin les uns des autres."
        h1 = s["welcome"]
    elif parish['lang'] == 'es-MX':
        blurb = f"""<p>La {parish['name']} se encuentra en {parish['city']}. Este sitio es un espejo no oficial preparado bajo la doctrina <em>EVE Glyph Design</em>, con el mismo cuidado editorial que una página oficial. La fuente oficial sigue siendo {src_link}.</p>"""
        card_title = "Una parroquia, un pueblo"
        card_body = "La fe vivida en el lugar, con una comunidad que reza, celebra y se cuida entre sí."
        h1 = s["welcome"]
    else:
        blurb = f"""<p>{parish['name']}, founded in {parish['founded']}, is located in {parish['city']}. This site is a non-official mirror prepared under the <em>EVE Glyph Design</em> doctrine, with the same editorial care as the parish's official site. The official source remains <a href="{parish['official_url']}">{parish['official_url'].replace('https://', '')}</a>.</p>"""
        card_title = "One parish, one people"
        card_body = "Faith lived locally, with a community that prays, celebrates and cares for one another."
        h1 = s["welcome"]

    body = f'''<main>
{hero_figure(parish)}
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
{schedule_note(parish)}
  </div>
</main>
'''
    return head(parish, s["welcome"]) + header(parish) + nav(parish, "index.html") + body + footer(parish)


def tidy_url(u: str) -> str:
    return u.replace('https://', '').replace('http://', '').rstrip('/')


def hero_figure(parish) -> str:
    """Hero photograph, or an honest placeholder where no licensed photograph exists."""
    if parish.get('photo_status') == 'pending':
        return ('  <figure class="hero-photo hero-photo-pending">\n'
                '    <div class="hero-photo-pending-inner">\n'
                f'      <img src="assets/crest.svg" alt="" aria-hidden="true">\n'
                f'      <p>{html.escape(PHOTO_PENDING[parish["lang"]])}</p>\n'
                '    </div>\n'
                '  </figure>')
    return ('  <figure class="hero-photo">\n'
            f'    <img src="assets/hero.jpg" alt="{html.escape(parish["name"])} \u2014 {html.escape(parish["city"])}" loading="eager">\n'
            '  </figure>')


def schedule_note(parish) -> str:
    if not parish.get('schedule_note'):
        return ''
    return f'    <p class="schedule-note">{html.escape(parish["schedule_note"])}</p>'


PHOTO_PENDING = {
    "fr-CA": "Photographie à venir — aucune image sous licence libre vérifiée pour cette église.",
    "en-CA": "Photograph pending — no verified freely-licensed image of this church yet.",
    "en-US": "Photograph pending — no verified freely-licensed image of this church yet.",
    "es-MX": "Fotografía pendiente — aún no hay una imagen de este templo con licencia libre verificada.",
}


def page_about(parish) -> str:
    s = STRINGS[parish['lang']]
    status = parish.get('status_note')
    if parish['lang'] == 'es-MX':
        body = f"""<main><div class="container">
<h1>{s['about_h1']}</h1>
<p class="lead">{parish['tagline']}.</p>
<p>La {parish['name']} sirve a la comunidad de {parish['city']}. Pertenece a {parish['diocese']}.</p>
<p>Esta p\u00e1gina es una presentaci\u00f3n. Para la historia completa, el clero y los avisos parroquiales, consulte la fuente oficial: <a href="{parish['official_url']}">{tidy_url(parish['official_url'])}</a>.</p>
<div class="card">
  <h3>Nuestro compromiso</h3>
  <p>Alojamiento local, sin rastreo, sin publicidad. La parroquia conserva su contenido y puede hacerse cargo de este espejo cuando quiera.</p>
</div>
</div></main>"""
        return head(parish, s["about_h1"]) + header(parish) + nav(parish, "about.html") + body + footer(parish)
    if parish['lang'] == 'fr-CA':
        body = f"""<main><div class="container">
<h1>{s['about_h1']}</h1>
<p class="lead">{parish['tagline']}.</p>
<p>Fondé{'e' if not status else ''} en {parish['founded']}, {'la' if not status else "l'"} {parish['name']} sert la communauté de {parish['city']}. Elle fait partie de {parish['diocese']}.</p>
{f'<p>{html.escape(status)}</p>' if status else ''}
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
    if parish['lang'] == 'es-MX':
        items = ["Grupo de oración", "Adoración eucarística", "Coro", "Catequesis", "Caballeros de Colón", "Consejo pastoral parroquial", "Ayuda a los necesitados", "Voluntariado parroquial"]
        title = "Vida parroquial"
        intro = "Los grupos activos en la parroquia. Para saber más o unirse a uno, comuníquese con la oficina parroquial."
    elif parish['lang'] == 'fr-CA':
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
    dt_lbls = {
        'fr-CA': ("Adresse", "Téléphone", "Courriel", "Diocèse"),
        'es-MX': ("Dirección", "Teléfono", "Correo", "Diócesis"),
    }.get(parish['lang'], ("Address", "Phone", "Email", "Diocese"))
    email_row = (f'<dt>{dt_lbls[2]}</dt><dd><a href="mailto:{parish["email"]}">{parish["email"]}</a></dd>'
                 if parish.get('email') else '')
    body = f'''<main><div class="container">
<h1>{s["contact_h1"]}</h1>
<div class="contact-block">
  <dl>
    <dt>{dt_lbls[0]}</dt><dd>{html.escape(parish['address'])}</dd>
    <dt>{dt_lbls[1]}</dt><dd>{html.escape(parish['phone'])}</dd>
    {email_row}
    <dt>{dt_lbls[3]}</dt><dd>{html.escape(parish['diocese'])}</dd>
  </dl>
</div>
<p><a href="{parish['official_url']}">{html.escape(s["official_source"])} → {tidy_url(parish['official_url'])}</a></p>
</div></main>'''
    return head(parish, s["contact_h1"]) + header(parish) + nav(parish, "contact.html") + body + footer(parish)


# ---------------------------------------------------------------------------
# Portal (front page)
# ---------------------------------------------------------------------------

REGIONS = [
    ("united-states", "United States",
     "Lenexa, Kansas and St. Augustine, Florida."),
    ("montreal", "Montréal",
     "The one on the mountain."),
    ("atlantic-canada", "Atlantic Canada",
     "New Brunswick, Prince Edward Island, Nova Scotia."),
    ("mexico", "México",
     "Bahía de Banderas, Nayarit — the marina coast."),
]

NUM_WORDS = {6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve"}


def num_word() -> str:
    return NUM_WORDS.get(len(PARISHES), str(len(PARISHES)))


def photo_credits_line() -> str:
    parts = []
    for p in PARISHES:
        if not p.get('photo_credit'):
            continue
        c = html.escape(p['photo_credit'])
        if p.get('photo_credit_url'):
            c = f'<a href="{p["photo_credit_url"]}">{c}</a>'
        parts.append(c)
    return " · ".join(parts)


def parish_card(p) -> str:
    featured_cls = ' parish-card-featured' if p['slug'] == 'holy-trinity' else ''
    blurb = p.get('portal_blurb_override', p['portal_blurb'])
    city_line = p.get('city_line', p['city'])
    founded_line = p.get('founded_line')
    if not founded_line:
        if not p['founded']:
            founded_line = p['diocese']
        elif p['lang'] == 'fr-CA':
            founded_line = f"Fondée {p['founded']} · {p['diocese']}"
        elif p['lang'] == 'es-MX':
            founded_line = f"Fundada {p['founded']} · {p['diocese']}"
        else:
            founded_line = f"Founded {p['founded']} · {p['diocese']}"

    if p.get('photo_status') == 'pending':
        photo = (f'          <div class="parish-card-nophoto">\n'
                 f'            <img src="parishes/{p["slug"]}/assets/crest.svg" alt="" aria-hidden="true">\n'
                 f'            <span>{html.escape(PHOTO_PENDING[p["lang"]])}</span>\n'
                 f'          </div>')
    else:
        alt = p.get('photo_alt', p['name'])
        photo = (f'          <img src="parishes/{p["slug"]}/assets/thumb.jpg" alt="{html.escape(alt)}" loading="lazy">\n'
                 f'          <div class="parish-card-crest-overlay"><img src="parishes/{p["slug"]}/assets/crest.svg" alt=""></div>')

    return (f'      <a class="parish-card{featured_cls}" href="parishes/{p["slug"]}/index.html">\n'
            f'        <div class="parish-card-photo">\n'
            f'{photo}\n'
            f'        </div>\n'
            f'        <div class="parish-card-body">\n'
            f'          <h3>{html.escape(p["short"])}</h3>\n'
            f'          <p class="parish-card-city">{html.escape(city_line)}</p>\n'
            f'          <p class="parish-card-blurb">{html.escape(blurb)}</p>\n'
            f'          <p class="parish-card-founded">{html.escape(founded_line)}</p>\n'
            f'        </div>\n'
            f'      </a>')


def region_blocks() -> str:
    out = []
    for key, label, sub in REGIONS:
        members = [p for p in PARISHES if p.get('region') == key]
        if not members:
            continue
        cards = chr(10).join(parish_card(p) for p in members)
        out.append(
            f'  <div class="container region-block" id="region-{key}">\n'
            f'    <div class="region-head">\n'
            f'      <h2>{html.escape(label)}</h2>\n'
            f'      <p>{html.escape(sub)}</p>\n'
            f'    </div>\n'
            f'    <div class="parish-grid">\n'
            f'{cards}\n'
            f'    </div>\n'
            f'  </div>')
    return chr(10).join(out)


def footnote_1613() -> str:
    """The bottom-of-page footnote. Deliberately light. Not a lineage claim."""
    return (
        '  <div class="container portal-section footnote-block" id="footnote">\n'
        '    <div class="footnote-rule"></div>\n'
        '    <h2>Footnote — and who were the Acadians, anyway?</h2>\n'
        '    <p class="footnote-aside">Down here at the bottom, because it is a footnote and not a sales pitch.</p>\n'
        '\n'
        '    <p>Long before any of the parishes above, there was one at Port-Royal, in what is now Nova Scotia:\n'
        '    <strong>Saint-Jean-Baptiste, founded 1613</strong>. Capuchin friars ran the mission from 1632.\n'
        '    First Catholic parish in what eventually became Canada.</p>\n'
        '\n'
        '    <p>Then most of the paperwork stopped existing. In 1654 a New England force under Robert Sedgwick\n'
        '    took Port-Royal, killed the Capuchin superior Léonard de Chartres and shipped his confrères out —\n'
        '    against the terms of the capitulation they had just signed. Two registers survive:\n'
        '    <strong>1702–1728 and 1727–1755</strong>, now at the Centre acadien of Université Sainte-Anne.\n'
        '    Everything before 1702 is gone.</p>\n'
        '\n'
        '    <p>People ask whether Rome kept a copy. Rome does governance, not sacraments — there is no central\n'
        '    baptismal register in the Vatican. Baptisms are written down in the parish, full stop.\n'
        '    When the parish burns, that is the end of it.</p>\n'
        '\n'
        '    <p>One set did travel. The Saint-Charles-des-Mines registers from Grand-Pré went with the deported\n'
        '    Acadians to Maryland, then to Louisiana, and were handed to the priest at Fort San Gabriel in 1767.\n'
        '    They sit in the Diocese of Baton Rouge vaults today.</p>\n'
        '\n'
        '    <p>And no, this is not a claim to being the oldest Catholic anything in North America.\n'
        '    St. Augustine, Florida has 1565 — it is the second card at the top of this page.\n'
        '    San Miguel Chapel in Santa Fe is around 1610. Port-Royal is just the first one that is ours,\n'
        '    and the one whose paperwork got burned.</p>\n'
        '\n'
        '    <p class="footnote-more"><a href="https://github.com/EVEglyphDesign/paix-parish-platform/blob/main/heritage/LIGNEE-ACADIENNE.md">Full write-up — the Acadian lineage page →</a></p>\n'
        '  </div>\n')


def portal() -> str:
    parish_links = "<br>".join(
        f'<a href="parishes/{p["slug"]}/index.html">{html.escape(p["short"])}</a>' for p in PARISHES)
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
    <a href="#ledger">Charitable Ledger</a>
    <a href="#about">About the platform</a>
    <a href="#kofc">For the Knights</a>
    <a href="#doctrine">Doctrine</a>
  </div>
</nav>

<main>
  <div class="container portal-hero">
    <h1>A parish website belongs to the parish.</h1>
    <p class="lead">{num_word()} parishes across three countries, one design canon. Locally hosted. No tracking. No ads. No third-party predators. Every dollar stays in the community.</p>
    <p>Select a parish to enter its site. Every parish site shares the same EVE Glyph Design canon, so navigation and typography stay familiar. Each parish's official site remains the source of truth — this is a mirror prepared with care, ready to be handed over to the parish's existing IT volunteer whenever they want it.</p>
  </div>

{region_blocks()}

  <div class="container" id="ledger">
    <div class="caisse-hero">
      <div class="caisse-hero-badge">Paired with the parish sites</div>
      <h2>The Charitable Ledger</h2>
      <p class="caisse-hero-lead">A running tally of what the men already do around here — the shopping, the hour of help, the favour from a guy with a trade — so it adds up somewhere and the parish can see it.</p>
      <div class="caisse-hero-plain">
        <ul>
          <li>Shop through the parish code, the savings go to the parish.</li>
          <li>An hour of help, one Brother signs off, it goes on the ledger.</li>
          <li>A guy with a trade — plumber, accountant, nurse — can put an hour in at his real rate.</li>
          <li>One page, the whole parish can read it.</li>
        </ul>
      </div>
      <div class="caisse-hero-cta">
        <a class="btn-primary" href="https://eveglyphdesign.github.io/holy-trinity-caisse/">See how it works →</a>
        <a class="btn-secondary" href="https://eveglyphdesign.github.io/holy-trinity-caisse/knights-letter.html">Letter to the Knights</a>
      </div>
    </div>
  </div>

  <div class="container portal-section" id="about">
    <h2>What this is</h2>
    <p>{num_word()} Catholic parishes, each with a mirrored site under a shared editorial template. Same header, same footer, same navigation — but each parish keeps its own crest, mass times, contact information and diocesan link. If a parish already has an IT volunteer, this is not a replacement; it is an option they can inspect, fork, or ignore.</p>
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

    <p class="caisse-crossref">The <a href="#ledger">Charitable Ledger</a> above pairs with the parish sites — that is the other half of what is on offer.</p>
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

  <div class="container portal-section" id="related">
    <h2>Related surface</h2>
    <div class="doctrine-grid">
      <div>
        <h4><a href="https://eveglyphdesign.github.io/paix-educational-game/">PAIX Educational Game</a></h4>
        <p>The parishioner-facing educational video game — the game surface of the EVE Glyph Design education program, distributed through the parish and Church portal. Education first; catechetical outputs stay disabled until Church review is complete. Safety first, betterment second.</p>
      </div>
      <div>
        <h4><a href="https://eveglyphdesign.github.io/holy-trinity-caisse/">Holy Trinity Charitable Ledger (Lenexa pilot)</a></h4>
        <p>The Holy Trinity Lenexa mutual-aid economy pilot. One good deed. One witness. One hour. One token.</p>
      </div>
    </div>
  </div>

{footnote_1613()}
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
        <p>{parish_links}</p>
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
    <div class="photo-credit">
      <p>Church photographs: {photo_credits_line()}</p>
    </div>
    <div class="ark-footer">
      <p>{html.escape(ARK_FOOTER)}</p>
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

/* Hero photograph on individual parish pages */
.hero-photo {
  margin: 0 0 2.2rem;
  padding: 0;
  max-height: 480px;
  overflow: hidden;
  position: relative;
}
.hero-photo::after {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(11,59,92,0) 55%, rgba(11,59,92,0.22) 100%);
  pointer-events: none;
}
.hero-photo img {
  width: 100%; height: 100%;
  max-height: 480px;
  object-fit: cover;
  display: block;
}

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
  text-decoration: none;
  color: var(--ink);
  overflow: hidden;
  transition: transform 0.15s, box-shadow 0.15s, border-left-color 0.15s;
}
.parish-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(11, 59, 92, 0.15);
  border-left-color: var(--marine);
  color: var(--ink);
}
.parish-card-photo {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: var(--marine-deep);
}
.parish-card-photo img {
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.35s ease;
}
.parish-card:hover .parish-card-photo img { transform: scale(1.03); }
.parish-card-crest-overlay {
  position: absolute;
  left: 0.9rem; bottom: 0.9rem;
  width: 46px; height: 46px;
  background: rgba(11, 59, 92, 0.92);
  padding: 5px;
  border: 1px solid rgba(212, 169, 74, 0.85);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.parish-card-crest-overlay img { width: 100%; height: 100%; display: block; }
.parish-card-body { padding: 1.2rem 1.4rem 1.4rem; display: flex; flex-direction: column; flex: 1; }
/* Featured card: Holy Trinity Lenexa — the Knights land here first */
.parish-card-featured {
  border-left-color: var(--marine);
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: minmax(300px, 1.2fr) 1fr;
  align-items: stretch;
}
.parish-card-featured .parish-card-photo {
  aspect-ratio: auto;
  height: 100%;
  min-height: 300px;
}
.parish-card-featured .parish-card-body { padding: 2rem 2rem 2rem; justify-content: center; }
.parish-card-featured h3 { font-size: 1.7rem; }
.parish-card-featured .parish-card-blurb { font-size: 1.05rem; }
@media (max-width: 720px) {
  .parish-card-featured { grid-template-columns: 1fr; }
  .parish-card-featured .parish-card-photo { min-height: 220px; }
}
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

/* Caisse callout block on the KofC section */
.caisse-callout {
  margin-top: 2rem;
  padding: 1.5rem 1.75rem;
  border-left: 4px solid #b08a3e;
  background: #fbf7ee;
  border-radius: 4px;
}
.caisse-callout h3 {
  margin-top: 0;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.35rem;
  color: #4a3820;
}
.caisse-callout .caisse-links {
  margin-top: 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}
.caisse-callout .btn-primary {
  display: inline-block;
  padding: 0.55rem 1.1rem;
  background: #4a3820;
  color: #fbf7ee;
  border-radius: 3px;
  text-decoration: none;
  font-weight: 600;
}
.caisse-callout .btn-primary:hover { background: #6a5230; }

/* Caisse hero — top-of-landing prominent block, above the parish grid */
.caisse-hero {
  margin: 2.5rem 0 3rem;
  padding: 2.25rem 2.25rem 2rem;
  background: linear-gradient(180deg, #fbf7ee 0%, #f5efe0 100%);
  border: 1px solid #d9c99d;
  border-left: 6px solid #b08a3e;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(74, 56, 32, 0.08);
}
.caisse-hero-badge {
  display: inline-block;
  padding: 0.3rem 0.75rem;
  margin-bottom: 1rem;
  background: #4a3820;
  color: #fbf7ee;
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border-radius: 2px;
}
.caisse-hero h2 {
  margin: 0 0 0.75rem;
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: #3a2a10;
  line-height: 1.15;
}
.caisse-hero-lead {
  font-size: 1.08rem;
  color: #3a2a10;
  margin-bottom: 1.5rem;
  line-height: 1.55;
}
.caisse-hero-plain {
  background: rgba(255, 255, 255, 0.55);
  border-radius: 4px;
  padding: 1.1rem 1.4rem 1.1rem 1.4rem;
  margin: 1rem 0 1.25rem;
}
.caisse-hero-plain p:first-child {
  margin-top: 0;
  color: #4a3820;
}
.caisse-hero-plain ul {
  margin: 0.75rem 0 0;
  padding-left: 1.25rem;
}
.caisse-hero-plain li {
  margin-bottom: 0.6rem;
  line-height: 1.5;
  color: #3a2a10;
}
.caisse-hero-plain li:last-child {
  margin-bottom: 0;
}
.caisse-hero-lineage {
  font-style: italic;
  color: #5a4630;
  margin: 1.25rem 0;
  padding: 0.75rem 1rem;
  border-left: 3px solid #b08a3e;
  background: rgba(255, 255, 255, 0.4);
}
.caisse-hero-lineage strong {
  font-style: normal;
  color: #3a2a10;
}
.caisse-hero-cta {
  margin-top: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  align-items: center;
}
.caisse-hero-cta .btn-primary {
  display: inline-block;
  padding: 0.7rem 1.35rem;
  background: #4a3820;
  color: #fbf7ee;
  border-radius: 3px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.98rem;
}
.caisse-hero-cta .btn-primary:hover {
  background: #6a5230;
}
.caisse-hero-cta .btn-secondary {
  display: inline-block;
  padding: 0.7rem 1.25rem;
  background: transparent;
  color: #4a3820;
  border: 1px solid #b08a3e;
  border-radius: 3px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.98rem;
}
.caisse-hero-cta .btn-secondary:hover {
  background: rgba(176, 138, 62, 0.1);
}

.parish-grid-heading {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 600;
  color: #3a2a10;
  margin: 0 0 1rem;
  font-size: 1.4rem;
}

.caisse-crossref {
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid #e5dcc2;
  font-size: 0.95rem;
  color: #5a4630;
  font-style: italic;
}
.caisse-crossref a { color: #4a3820; font-weight: 600; }

@media (max-width: 640px) {
  .caisse-hero { padding: 1.5rem 1.25rem; margin: 1.5rem 0 2rem; }
  .caisse-hero h2 { font-size: 1.55rem; }
  .caisse-hero-lead { font-size: 1rem; }
  .caisse-hero-plain { padding: 0.9rem 1rem; }
  .caisse-hero-cta { flex-direction: column; align-items: stretch; }
  .caisse-hero-cta .btn-primary,
  .caisse-hero-cta .btn-secondary { text-align: center; }
}

/* --------------------------------------------------------------------------
   v3 — regional grouping, photo-pending state, credits, rights footer, footnote
   -------------------------------------------------------------------------- */

.region-block { margin-top: 2.6rem; }
.region-block:first-of-type { margin-top: 1.4rem; }

.region-head {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 0.15rem 1rem;
  margin-bottom: 1.1rem;
  padding-bottom: 0.55rem;
  border-bottom: 1px solid #d9c99d;
}
.region-head h2 {
  margin: 0;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.55rem;
  font-weight: 600;
  color: #0b3b5c;
  letter-spacing: 0.01em;
}
.region-head p {
  margin: 0;
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 0.86rem;
  color: #6a6154;
}

/* Card state when no freely-licensed photograph of the church exists yet */
.parish-card-nophoto {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 1.1rem 1.4rem;
  text-align: center;
  background: linear-gradient(160deg, #12496c 0%, #0b3b5c 100%);
}
.parish-card-nophoto img {
  width: 56px;
  height: 56px;
  opacity: 0.95;
  position: static;
  transform: none;
}
.parish-card-nophoto span {
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 0.74rem;
  line-height: 1.4;
  color: #e8ddc4;
  max-width: 22rem;
}
.parish-card:hover .parish-card-nophoto img { transform: none; }

/* Photograph attribution */
.photo-credit {
  margin-top: 1.1rem;
  padding-top: 0.7rem;
  border-top: 1px solid rgba(216, 201, 157, 0.35);
}
.photo-credit p {
  margin: 0;
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 0.72rem;
  line-height: 1.55;
  color: #9aa7b2;
}
.photo-credit a { color: #c9b98c; text-decoration: none; }
.photo-credit a:hover { text-decoration: underline; }

/* Mandatory rights footer — EVE Glyph Index L0 canon, Gate 2 */
.ark-footer {
  margin-top: 1.1rem;
  padding-top: 0.85rem;
  border-top: 1px solid rgba(216, 201, 157, 0.35);
}
.ark-footer p {
  margin: 0;
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 0.71rem;
  line-height: 1.6;
  color: #8f9aa5;
  max-width: 74ch;
}

/* The 1613 footnote at the very bottom — deliberately quiet */
.footnote-block { margin-top: 1rem; }
.footnote-rule {
  height: 1px;
  background: linear-gradient(90deg, #d9c99d 0%, rgba(217, 201, 157, 0) 70%);
  margin-bottom: 1.6rem;
}
.footnote-block h2 {
  font-size: 1.35rem;
  color: #5a5142;
  font-weight: 500;
}
.footnote-block p {
  font-size: 0.93rem;
  line-height: 1.66;
  color: #5f5749;
  max-width: 68ch;
}
.footnote-aside {
  font-style: italic;
  color: #8a8172;
  margin-top: -0.4rem;
}
.footnote-block strong { color: #4a4234; font-weight: 600; }
.footnote-more { margin-top: 1.3rem; }
.footnote-more a {
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 0.88rem;
  color: #1a5578;
  text-decoration: none;
  border-bottom: 1px solid rgba(26, 85, 120, 0.35);
}
.footnote-more a:hover { border-bottom-color: #1a5578; }

/* Hero placeholder on a parish page with no licensed photograph */
.hero-photo-pending {
  background: linear-gradient(160deg, #12496c 0%, #0b3b5c 100%);
  min-height: 260px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-photo-pending::after { display: none; }
.hero-photo-pending-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.9rem;
  padding: 2.6rem 1.5rem;
  text-align: center;
}
.hero-photo-pending-inner img { width: 74px; height: 74px; }
.hero-photo-pending-inner p {
  margin: 0;
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 0.83rem;
  color: #e8ddc4;
  max-width: 34rem;
}

/* Schedule caveat where the published times could not be confirmed officially */
.schedule-note {
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 0.83rem;
  line-height: 1.55;
  color: #6a6154;
  font-style: italic;
  margin-top: -0.4rem;
}

@media (max-width: 640px) {
  .region-head h2 { font-size: 1.3rem; }
  .hero-photo-pending { min-height: 190px; }
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
