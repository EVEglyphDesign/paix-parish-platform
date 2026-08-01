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

from i18n_runtime import (LANGS, LANGS_DISPLAY, LANG_CODES, PIVOT, DEFAULT,
                          NATIVE_OF, translator, coverage)

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
        "city_line": "Lenexa, Kansas · 13615 West 92nd Street",
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
            ("Adoration — weekdays", "after 7:00 AM Mass until noon (Wed. from 10:00 AM)"),
            ("St. Benedict the Moor — Sunday", "8:00 AM"),
        ],
        "crest_style": "spanish",
        "portal_blurb": "The oldest Catholic congregation in the continental United States. Mass has been said here since 1565.",
        "city_line": "St. Augustine, Florida · 38 Cathedral Place",
        "status_note": "The parish keeps a second church, St. Benedict the Moor, at 86 M.L. King Avenue, where the 8:00 AM Sunday Mass is celebrated. Rector: Very Rev. John Tetlow. Bishop: Most Rev. Erik T. Pohlmeier. Parish mail goes to 35 Treasury Street, St. Augustine, FL 32084. The office is open Monday to Thursday 8:00 AM to 3:00 PM and Friday 8:00 AM to 2:00 PM; the cathedral itself is open weekdays 8:00 AM to 5:00 PM. The parish is served by Knights of Columbus First Florida Council 611.",
        "schedule_note": "Adoration hours follow the parish bulletin of 4 January 2026; the static website page still shows an older ending time. The 8:00 AM Sunday Mass is at St. Benedict the Moor, the second church of the parish.",
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
        "city_line": "Montr\u00e9al, Qu\u00e9bec \u00b7 3800, chemin Queen Mary",
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
        "slug": "saint-dunstan-fredericton",
        "name": "St. Dunstan's Church",
        "short": "St. Dunstan's \u2014 Fredericton",
        "city": "Fredericton, New Brunswick",
        "founded": "1827",
        "lang": "en-CA",
        "official_url": "https://stmarymagdaleneparish.ca",
        "address": "120 Regent Street, Fredericton, New Brunswick E3B 3W6",
        "phone": "(506) 444-6001",
        "email": "office@stmarymagdaleneparish.ca",
        "tagline": "The founding Catholic parish of Fredericton \u2014 first cathedral of New Brunswick",
        "diocese": "Diocese of Saint John \u00b7 St. Mary Magdalene Parish",
        "schedule": [
            ("Saturday Vigil", "4:00 PM"),
            ("Sunday", "9:00 AM & 11:30 AM"),
            ("First Saturday of the month", "9:00 AM"),
            ("Thursday", "12:05 PM"),
            ("Wednesday \u2014 Benediction, then Mass", "6:00 PM \u00b7 6:30 PM"),
            ("Friday \u2014 Rosary to St. Joseph, then Mass", "6:00 PM \u00b7 6:30 PM"),
            ("Confession \u2014 Saturday", "from 2:30 PM"),
            ("Adoration \u2014 Thursday", "1:00 \u2013 5:00 PM"),
        ],
        "schedule_note": (
            "The weekend times \u2014 Saturday 4:00 PM, Sunday 9:00 AM and 11:30 AM \u2014 agree across the "
            "diocesan parish finder, the parish's own site and third-party listings. The weekday times "
            "do not: the diocese, the parish site and the aggregators each publish a different set. "
            "The weekday rows above follow the parish's own site, which is the closest thing to a "
            "first-hand source, but call the office at (506) 444-6001 before making a weekday trip."
        ),
        "crest_style": "spire",
        "portal_blurb": (
            "The founding parish of Catholic Fredericton, and the first cathedral of New Brunswick."
        ),
        "portal_blurb_override": (
            "The founding parish of Catholic Fredericton \u2014 a resident priest from 1827, and the first "
            "cathedral of the Diocese of New Brunswick. Sainte-Anne-des-Pays-Bas grew up inside it "
            "before going out on its own in 1981."
        ),
        "region": "atlantic-canada",
        "photo_alt": (
            "St. Dunstan's Church, Fredericton \u2014 the parish sign and the stone-and-brick "
            "colonnade of the 1965 church at the corner of Regent and Brunswick Streets"
        ),
        "photo_credit": "Photograph: KartaView contributor, CC BY-SA 4.0, via KartaView (OpenStreetCam)",
        "photo_credit_url": "https://kartaview.org/details/165588/26",
        "city_line": "Fredericton, New Brunswick \u00b7 120 Regent Street",
        "status_note": (
            "St. Dunstan's is today the principal church of St. Mary Magdalene Parish, an amalgamated "
            "parish that also takes in St. Columba at Fredericton Junction and Sts. John and Paul at "
            "New Maryland. Pastor: Rev. Peter Osborne; Bishop of Saint John: Most Rev. Christian "
            "Riesbeck, C.C. Parish mail goes to PO Box 187, Fredericton, New Brunswick E3B 4Y9. "
            "A resident priest has served here since Fr. Michael McSweeney arrived in 1827, and the "
            "church built under Bishop William Dollard in the 1840s was the first Roman Catholic "
            "cathedral in New Brunswick \u2014 Dollard was consecrated in it on 11 June 1843. When the "
            "Great Fire of 11 November 1850 took more than three hundred buildings in Fredericton, "
            "St. Dunstan's was one of the few left standing; parishioners are said to have held the "
            "roof against the embers with their own bodies. The present church, with its ninety-two "
            "foot spire, was consecrated on 15 August 1965. This is the parish that carried the "
            "French-speaking Catholics of Fredericton for sixteen years \u2014 French Mass twice a month "
            "from 1965, then a curate of St. Dunstan's assigned to them from 1978 \u2014 until "
            "Sainte-Anne-des-Pays-Bas was erected as a parish in its own right on 2 September 1981."
        ),
        "founded_line": (
            "Resident priest 1827 \u00b7 First cathedral of New Brunswick 1843 \u00b7 "
            "Present church 1965 \u00b7 Diocese of Saint John"
        ),
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
        "city_line": "Paquetville, Nouveau-Brunswick \u00b7 3585, rue Principale",
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
        "address": "65 Great George Street, Charlottetown, PE C1A 4J8",
        "phone": "(902) 894-3486",
        "email": "office@stdunstanspei.com",
        "tagline": "Mother church of the Diocese of Charlottetown — founded 1816",
        "city_line": "Charlottetown, Prince Edward Island · 65 Great George Street",
        "founded_line": (
            "Parish 1816 · Cathedral 1829 · Fire 1913 · Present church 1919 · "
            "Basilica 1929 · National Historic Site 1990"
        ),
        "status_note": (
            "Four churches have stood on this corner of Great George Street since 1816: the wooden "
            "chapel of 1816, a larger wooden cathedral from 1843, the stone cathedral dedicated in "
            "1907, and the present basilica. Fire started in the sanctuary on the night of 7 March "
            "1913 and took the roof and the whole interior; the walls and façade survived, and the "
            "church was rebuilt inside its own stone shell and rededicated on 24 September 1919. "
            "Pope Pius XI granted the title of basilica, conferred at the consecration of 26 June "
            "1929 — a hundred years to the year after the diocese was created. It has been a "
            "National Historic Site of Canada since 1990. Bishop of Charlottetown: Most Rev. Joseph "
            "Dabrowski, C.S.M.A. Knights of Columbus Our Lady of Fatima Council #824, founded in "
            "1903 and the first council east of Montréal, meets here."
        ),
        "diocese": "Diocese of Charlottetown",
        "schedule": [
            ("Saturday Vigil", "4:00 PM"),
            ("Sunday", "10:00 AM & 5:00 PM"),
            ("Tuesday – Friday", "12:05 PM"),
        ],
        "crest_style": "gothic",
        "portal_blurb": "Mother church of the Diocese of Charlottetown. Founded 1816.",
        "portal_blurb_override": (
            "Mother church of the Diocese of Charlottetown. Fourth church on the same corner — "
            "rebuilt inside its own walls after the fire of 1913."
        ),
        "region": "atlantic-canada",
        "photo_alt": "St. Dunstan's Basilica, Great George Street, Charlottetown — front elevation with both spires",
        "photo_credit": "Photograph: SoftwareSimian, CC BY-SA 4.0, via Wikimedia Commons",
        "photo_credit_url": "https://commons.wikimedia.org/wiki/File:St._Dunstan%27s_Basilica_(Charlottetown_PEI)_front_2015-May-25.jpg",
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
        "city_line": "Halifax, Nova Scotia · 6476 Bayers Road",
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
        "city_line": "Halifax, Nova Scotia · 5221 Spring Garden Road",
        "region": "atlantic-canada",
    },
    {
        "slug": "sagrada-familia-nuevo-vallarta",
        "name": "Cuasiparroquia de la Sagrada Familia",
        "short": "Sagrada Familia \u2014 Nuevo Vallarta",
        "city": "Las Jarretaderas, Nayarit",
        "founded": "",
        "lang": "es-MX",
        "city_line": "Las Jarretaderas, Nayarit · J. María Morelos e Independencia",
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
        "slug": "paradise-village-mass-nuevo-vallarta",
        "name": "Paradise Village Catholic Mass",
        "short": "Paradise Village \u2014 Nuevo Vallarta",
        "city": "Nuevo Vallarta, Nayarit",
        "founded": "",
        "lang": "en-US",
        "region": "mexico",
        "official_url": "https://pvangels.com/charities/132/worship-services",
        "address": (
            "Paradise Plaza, Av. Paseo de los Cocoteros, Nuevo Vallarta, "
            "Bah\u00eda de Banderas, Nayarit, C.P. 63735, M\u00e9xico"
        ),
        "phone": "",
        "email": "",
        "tagline": "The English Sunday Mass by the marina at Nuevo Vallarta",
        "diocese": "Di\u00f3cesis de Tepic \u00b7 Decanato Bah\u00eda de Banderas",
        "schedule": [
            ("Sunday \u2014 Mass in English", "10:00 AM"),
        ],
        "crest_style": "anchor",
        "portal_blurb": (
            "The English-language Sunday Mass held inside Paradise Plaza at Nuevo Vallarta, "
            "for the people of the marina corridor."
        ),
        "founded_line": (
            "A standing Sunday Mass, not a canonically erected parish \u00b7 "
            "Di\u00f3cesis de Tepic \u00b7 Decanato Bah\u00eda de Banderas"
        ),
        "city_line": "Nuevo Vallarta, Nayarit \u00b7 Paradise Plaza, Paseo de los Cocoteros",
        "photo_status": "pending",
        "schedule_note": (
            "Sunday 10:00 AM in English is corroborated by the PVAngels worship directory, the "
            "Villa Encantada visitor pages and repeated first-hand guest reports, but no diocesan "
            "source publishes it. There is no parish office and no published telephone number. "
            "A separate interdenominational Christian service meets at 10:30 AM in the resort's "
            "Sal\u00f3n del Sol \u2014 it is not this Mass."
        ),
        "status_note": (
            "State this plainly: this is a standing Sunday Mass, not a parish. The Di\u00f3cesis de "
            "Tepic, which holds jurisdiction over Bah\u00eda de Banderas, does not list it among its "
            "parishes or quasi-parishes, and no source names the priest or the parish that supplies "
            "the celebrant. It is a long-running pastoral accommodation for English-speaking "
            "residents, condominium owners and visitors along the marina corridor, meeting inside "
            "the Paradise Plaza mall at the Paradise Village complex. The nearest canonical parishes "
            "are the Cuasiparroquia de la Sagrada Familia at Las Jarretaderas and Nuestra Se\u00f1ora "
            "Reina de la Paz at Bucer\u00edas. The Vallarta Yacht Club stands about a kilometre north "
            "on the same Paseo de los Cocoteros; no source ties the club to this Mass, and this card "
            "does not claim one. No founding date exists to give, because nothing was ever founded \u2014 "
            "the listing is traceable in worship directories from the mid-2000s onward. No free-licensed photograph of the Mass, of the Paradise Plaza interior, or of any chapel on the site could be found. The only free image of the complex is a 2005 photograph of the resort's gated-community entrance \u2014 a gate, not a church \u2014 and a gate on a church card would be a lie of composition. The card stays without a photograph until someone on the ground sends one."
        ),
    },
    {
        "slug": "santa-cruz-huanacaxtle",
        "name": "Parroquia de La Santa Cruz",
        "short": "La Santa Cruz \u2014 La Cruz de Huanacaxtle",
        "city": "La Cruz de Huanacaxtle, Nayarit",
        "founded": "",
        "lang": "es-MX",
        "city_line": "La Cruz de Huanacaxtle, Nayarit · Calle Marlín 38",
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
        "status_note": (
            "P\u00e1rroco: Pbro. Luis Alberto Moreno Mart\u00ednez, seg\u00fan el directorio del clero de la Di\u00f3cesis de Tepic. Fiesta patronal: el 3 de mayo, D\u00eda de la Santa Cruz. No se public\u00f3 en ninguna fuente primaria el a\u00f1o de fundaci\u00f3n de la parroquia; se deja el hueco abierto en lugar de inventarlo. El c\u00f3digo postal es C.P. 63732 seg\u00fan la di\u00f3cesis, aunque varios directorios tur\u00edsticos publican 63734. No existe ninguna fotograf\u00eda de la iglesia con licencia libre: se revisaron Wikimedia Commons, Wikidata, Flickr y las im\u00e1genes de calle de KartaView a menos de trescientos metros, y ninguna muestra la fachada. La tarjeta se queda sin fotograf\u00eda hasta que alguien del pueblo mande una."
        ),
        "photo_status": "pending",
        "schedule_note": "Horario reportado por feligreses; algunos directorios lo publican mal. Conviene confirmar por tel\u00e9fono.",
    },
    {
        "slug": "metamorphosis-nafplio",
        "name": "\u0399\u03b5\u03c1\u03cc\u03c2 \u039a\u03b1\u03b8\u03bf\u03bb\u03b9\u03ba\u03cc\u03c2 \u039d\u03b1\u03cc\u03c2 \u039c\u03b5\u03c4\u03b1\u03bc\u03bf\u03c1\u03c6\u03ce\u03c3\u03b5\u03c9\u03c2 \u03c4\u03bf\u03c5 \u03a3\u03c9\u03c4\u03ae\u03c1\u03bf\u03c2",
        "short": "\u039c\u03b5\u03c4\u03b1\u03bc\u03cc\u03c1\u03c6\u03c9\u03c3\u03b7 \u03c4\u03bf\u03c5 \u03a3\u03c9\u03c4\u03ae\u03c1\u03bf\u03c2 \u2014 \u039d\u03b1\u03cd\u03c0\u03bb\u03b9\u03bf",
        "city": "\u039d\u03b1\u03cd\u03c0\u03bb\u03b9\u03bf, \u0391\u03c1\u03b3\u03bf\u03bb\u03af\u03b4\u03b1",
        "founded": "1840",
        "lang": "el-GR",
        "region": "greece",
        "official_url": "https://cathecclesia.gr/",
        "address": "\u039f\u03b4\u03cc\u03c2 \u03a6\u03c9\u03c4\u03bf\u03bc\u03ac\u03c1\u03b1, \u03a0\u03b1\u03bb\u03b9\u03ac \u03a0\u03cc\u03bb\u03b7, 211 00 \u039d\u03b1\u03cd\u03c0\u03bb\u03b9\u03bf",
        "phone": "+30 27520 24568",
        "email": "",
        "tagline": "\u0397 \u00ab\u03a6\u03c1\u03b1\u03b3\u03ba\u03bf\u03ba\u03ba\u03bb\u03b7\u03c3\u03b9\u03ac\u00bb \u03c4\u03b7\u03c2 \u03a0\u03b1\u03bb\u03b9\u03ac\u03c2 \u03a0\u03cc\u03bb\u03b7\u03c2 \u2014 \u03c4\u03bf \u03b1\u03c1\u03c7\u03b1\u03b9\u03cc\u03c4\u03b5\u03c1\u03bf \u03bc\u03bd\u03b7\u03bc\u03b5\u03af\u03bf \u03c4\u03c9\u03bd \u03a6\u03b9\u03bb\u03b5\u03bb\u03bb\u03ae\u03bd\u03c9\u03bd \u03c3\u03c4\u03b7\u03bd \u0395\u03bb\u03bb\u03ac\u03b4\u03b1",
        "diocese": "\u0399\u03b5\u03c1\u03ac \u0391\u03c1\u03c7\u03b9\u03b5\u03c0\u03b9\u03c3\u03ba\u03bf\u03c0\u03ae \u039a\u03b1\u03b8\u03bf\u03bb\u03b9\u03ba\u03ce\u03bd \u0391\u03b8\u03b7\u03bd\u03ce\u03bd",
        "schedule": [
            ("\u039a\u03c5\u03c1\u03b9\u03b1\u03ba\u03ae \u03ba\u03b1\u03b9 \u03b5\u03bf\u03c1\u03c4\u03ad\u03c2", "11:00"),
            ("\u0394\u03b5\u03c5\u03c4\u03ad\u03c1\u03b1 \u2013 \u03a4\u03b5\u03c4\u03ac\u03c1\u03c4\u03b7", "08:00"),
            ("\u03a0\u03ad\u03bc\u03c0\u03c4\u03b7 \u2013 \u03a3\u03ac\u03b2\u03b2\u03b1\u03c4\u03bf", "18:00"),
        ],
        "crest_style": "philhellene",
        "portal_blurb": "\u03a4\u03b6\u03b1\u03bc\u03af \u03c0\u03bf\u03c5 \u03ad\u03b3\u03b9\u03bd\u03b5 \u03b5\u03ba\u03ba\u03bb\u03b7\u03c3\u03af\u03b1 \u03c4\u03bf 1839. \u039c\u03ad\u03c3\u03b1 \u03c3\u03c4\u03ad\u03ba\u03b5\u03b9 \u03b7 \u0391\u03c8\u03af\u03b4\u03b1 \u03c4\u03bf\u03c5 Touret, \u03bc\u03b5 \u03c4\u03b1 \u03bf\u03bd\u03cc\u03bc\u03b1\u03c4\u03b1 \u03c0\u03b5\u03c1\u03af\u03c0\u03bf\u03c5 280 \u03a6\u03b9\u03bb\u03b5\u03bb\u03bb\u03ae\u03bd\u03c9\u03bd \u03c0\u03bf\u03c5 \u03ad\u03c0\u03b5\u03c3\u03b1\u03bd \u03b3\u03b9\u03b1 \u03c4\u03b7\u03bd \u0395\u03bb\u03bb\u03ac\u03b4\u03b1.",
        "city_line": "\u039d\u03b1\u03cd\u03c0\u03bb\u03b9\u03bf, \u0391\u03c1\u03b3\u03bf\u03bb\u03af\u03b4\u03b1 \u00b7 \u03bf\u03b4\u03cc\u03c2 \u03a6\u03c9\u03c4\u03bf\u03bc\u03ac\u03c1\u03b1, \u03c3\u03c4\u03b1 \u03c3\u03ba\u03b1\u03bb\u03bf\u03c0\u03ac\u03c4\u03b9\u03b1 \u03c4\u03b7\u03c2 \u03bf\u03b4\u03bf\u03cd \u03a0\u03bf\u03c4\u03b1\u03bc\u03b9\u03ac\u03bd\u03bf\u03c5",
        "founded_line": "\u03a0\u03b1\u03c1\u03b1\u03c7\u03ce\u03c1\u03b7\u03c3\u03b7 1839 \u00b7 \u0395\u03bd\u03bf\u03c1\u03af\u03b1 1840 \u00b7 \u0399\u03b5\u03c1\u03ac \u0391\u03c1\u03c7\u03b9\u03b5\u03c0\u03b9\u03c3\u03ba\u03bf\u03c0\u03ae \u039a\u03b1\u03b8\u03bf\u03bb\u03b9\u03ba\u03ce\u03bd \u0391\u03b8\u03b7\u03bd\u03ce\u03bd",
        "status_note": "\u0394\u03b9\u03b1\u03c4\u03b7\u03c1\u03b7\u03c4\u03ad\u03bf \u03bc\u03bd\u03b7\u03bc\u03b5\u03af\u03bf \u2014 \u03b5\u03bd\u03c4\u03cc\u03c2 \u03c4\u03bf\u03c5 \u03ba\u03b7\u03c1\u03c5\u03b3\u03bc\u03ad\u03bd\u03bf\u03c5 \u03b9\u03c3\u03c4\u03bf\u03c1\u03b9\u03ba\u03bf\u03cd \u03c4\u03cc\u03c0\u03bf\u03c5 \u03c4\u03b7\u03c2 \u03a0\u03b1\u03bb\u03b9\u03ac\u03c2 \u03a0\u03cc\u03bb\u03b7\u03c2 \u039d\u03b1\u03c5\u03c0\u03bb\u03af\u03bf\u03c5.",
        "schedule_note": "\u03a4\u03bf \u03c9\u03c1\u03ac\u03c1\u03b9\u03bf \u03c0\u03c1\u03bf\u03ad\u03c1\u03c7\u03b5\u03c4\u03b1\u03b9 \u03b1\u03c0\u03cc \u03c4\u03b7\u03bd \u03b9\u03c3\u03c4\u03bf\u03c3\u03b5\u03bb\u03af\u03b4\u03b1 \u03c4\u03b7\u03c2 \u03b5\u03bd\u03bf\u03c1\u03af\u03b1\u03c2 \u03ba\u03b1\u03b9 \u03b4\u03b5\u03bd \u03ad\u03c7\u03b5\u03b9 \u03b5\u03c0\u03b9\u03b2\u03b5\u03b2\u03b1\u03b9\u03c9\u03b8\u03b5\u03af \u03c0\u03c1\u03cc\u03c3\u03c6\u03b1\u03c4\u03b1. \u03a4\u03b7\u03bb\u03b5\u03c6\u03c9\u03bd\u03ae\u03c3\u03c4\u03b5 \u03c0\u03c1\u03b9\u03bd \u03c0\u03ac\u03c4\u03b5.",
        "photo_alt": "\u039f \u03c4\u03c1\u03bf\u03cd\u03bb\u03bf\u03c2 \u03c4\u03bf\u03c5 \u03ba\u03b1\u03b8\u03bf\u03bb\u03b9\u03ba\u03bf\u03cd \u03bd\u03b1\u03bf\u03cd \u039c\u03b5\u03c4\u03b1\u03bc\u03bf\u03c1\u03c6\u03ce\u03c3\u03b5\u03c9\u03c2 \u03c4\u03bf\u03c5 \u03a3\u03c9\u03c4\u03ae\u03c1\u03bf\u03c2 \u03c3\u03c4\u03b7\u03bd \u03a0\u03b1\u03bb\u03b9\u03ac \u03a0\u03cc\u03bb\u03b7 \u03c4\u03bf\u03c5 \u039d\u03b1\u03c5\u03c0\u03bb\u03af\u03bf\u03c5",
        "photo_credit": "\u03a6\u03c9\u03c4\u03bf\u03b3\u03c1\u03b1\u03c6\u03af\u03b1: C messier, CC BY-SA 4.0, \u03bc\u03ad\u03c3\u03c9 Wikimedia Commons",
        "photo_credit_url": "https://commons.wikimedia.org/wiki/File:%CE%9A%CE%B1%CE%B8%CE%BF%CE%BB%CE%B9%CE%BA%CE%AE_%CE%B5%CE%BA%CE%BA%CE%BB%CE%B7%CF%83%CE%AF%CE%B1_%CE%9D%CE%B1%CF%85%CF%80%CE%BB%CE%AF%CE%BF%CF%85_7833.jpg",
    },
]

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
    elif style == "anchor":
        # A cross whose foot becomes an anchor - the Sunday Mass by the marina at Nuevo Vallarta
        motif = '''<path d="M50 56 L 50 82 M 41 64 L 59 64" stroke="#f5efe1" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M38 74 Q 50 90, 62 74" fill="none" stroke="#f5efe1" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="50" cy="64" r="3" fill="#d4a94a"/>'''
    elif style == "spire":
        # A single tall spire topped with a cross — St. Dunstan's, Fredericton (1965)
        motif = '''<path d="M50 54 L 60 78 L 40 78 Z" fill="#f5efe1" opacity="0.92"/>
  <path d="M36 84 L 64 84 L 64 78 L 36 78 Z" fill="#f5efe1" opacity="0.75"/>
  <path d="M50 48 L 50 56 M 46.5 51 L 53.5 51" stroke="#d4a94a" stroke-width="2" stroke-linecap="round"/>'''
    elif style == "philhellene":
        # Classical temple front — the 1841 Touret Arch inside the Nafplio church
        motif = '''<path d="M30 84 L 30 72 L 70 72 L 70 84" fill="none" stroke="#f5efe1" stroke-width="2.4" stroke-linecap="round"/>
  <path d="M26 72 L 50 58 L 74 72 Z" fill="#f5efe1" opacity="0.92"/>
  <path d="M40 84 L 40 72 M 50 84 L 50 72 M 60 84 L 60 72" stroke="#f5efe1" stroke-width="2" stroke-linecap="round"/>
  <circle cx="50" cy="68" r="2.6" fill="#d4a94a"/>'''
    else:  # trinity
        motif = '''<circle cx="50" cy="70" r="4" fill="none" stroke="#f5efe1" stroke-width="2"/>
  <circle cx="42" cy="78" r="4" fill="none" stroke="#f5efe1" stroke-width="2"/>
  <circle cx="58" cy="78" r="4" fill="none" stroke="#f5efe1" stroke-width="2"/>'''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Crest">\n  {shield}\n  {star}\n  {motif}\n</svg>\n'


# ---------------------------------------------------------------------------
# Page skeleton — every string comes from the Latin pivot via i18n_runtime
# ---------------------------------------------------------------------------

def lang_switcher(t, url_of) -> str:
    """Language menu. A globe sits in the top-right corner and costs the page
    nothing; hovering it — or clicking, for keyboard and touch — drops a
    single column of languages beneath it, read top to bottom in DISPLAY_ORDER:
    English, the living Romance languages, Latin as their common root, Greek,
    then the rest. `url_of(code)` returns the href for a language."""
    label = html.escape(t("ui.lang_label"))
    links = []
    current = t.code
    for code, endonym, _html_lang, _dir in LANGS_DISPLAY:
        cls = ' class="active"' if code == current else ''
        pivot = ' data-pivot="1"' if code == PIVOT else ''
        links.append(
            f'        <a href="{url_of(code)}" hreflang="{code}" lang="{code}"'
            f'{cls}{pivot}>{html.escape(endonym)}</a>')
    globe = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="1.7" aria-hidden="true" focusable="false">'
             '<circle cx="12" cy="12" r="9.2"/>'
             '<path d="M2.8 12h18.4M12 2.8c2.6 2.7 3.9 6 3.9 9.2s-1.3 6.5-3.9 '
             '9.2c-2.6-2.7-3.9-6-3.9-9.2S9.4 5.5 12 2.8z"/></svg>')
    return (f'  <nav class="lang-bar" aria-label="{label}">\n'
            '    <input type="checkbox" id="lang-open" class="lang-toggle">\n'
            f'    <label for="lang-open" class="lang-globe" title="{label}" '
            f'role="button" tabindex="0" aria-label="{label}">{globe}'
            f'<span class="lang-globe-code">{html.escape(current.upper())}</span>'
            '</label>\n'
            '    <div class="lang-panel">\n'
            f'      <span class="lang-bar-label">{label}</span>\n'
            '      <div class="lang-list">\n'
            + '\n'.join(links) + '\n'
            '      </div>\n'
            '    </div>\n'
            '  </nav>\n\n')

def hreflang_links(url_of) -> str:
    out = [f'<link rel="alternate" hreflang="{c}" href="{url_of(c)}">'
           for c, _, _, _ in LANGS]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{url_of(DEFAULT)}">')
    return "\n".join(out)


def head(parish, t, css_prefix, page_title, url_of=None) -> str:
    alts = ("\n" + hreflang_links(url_of)) if url_of else ""
    return f'''<!DOCTYPE html>
<html lang="{t.html_lang}">
<head>
<meta charset="utf-8">
<title>{html.escape(page_title)} — {html.escape(parish['short'])}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(t('parish.' + parish['slug'] + '.tagline'))}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_prefix}style.css">
<link rel="icon" type="image/svg+xml" href="{css_prefix}crest.svg">{alts}
</head>
<body>
{lang_switcher(t, url_of)}'''

def header(parish, t, css_prefix) -> str:
    return f'''<header class="site-header">
  <div class="container">
    <img src="{css_prefix}crest.svg" alt="" class="crest" aria-hidden="true">
    <div class="site-title">
      <h1>{html.escape(parish['name'])}</h1>
      <div class="sub">{html.escape(parish['city'])} — {html.escape(t('parish.' + parish['slug'] + '.tagline'))}</div>
    </div>
  </div>
</header>
'''

def nav(parish, t, active, portal_back) -> str:
    items = [
        ("index.html", t("ui.home")),
        ("about.html", t("ui.about")),
        ("mass.html", t("ui.mass")),
        ("life.html", t("ui.life")),
        ("contact.html", t("ui.contact")),
    ]
    links = []
    for href, label in items:
        cls = ' class="active"' if href == active else ''
        links.append(f'    <a href="{href}"{cls}>{html.escape(label)}</a>')
    return f'''<nav class="site-nav" aria-label="Navigation">
  <div class="container">
{chr(10).join(links)}
    <a href="{portal_back}" style="margin-left:auto; color: var(--stella-gold-light);">{html.escape(t("ui.portal_back"))}</a>
  </div>
</nav>
'''


def footer(parish, t) -> str:
    slug = parish['slug']
    email_line = (f'<br>\n        <a href="mailto:{parish["email"]}">{parish["email"]}</a>'
                  if parish.get('email') else '')
    tel_line = (f'<br>\n        {html.escape(t("page.tel_abbrev"))} : {html.escape(parish["phone"])}'
                if parish.get('phone') else '')
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-cols">
      <div>
        <h4>{html.escape(t("ui.reach_us"))}</h4>
        <p>{html.escape(parish['address'])}{tel_line}{email_line}</p>
      </div>
      <div>
        <h4>{html.escape(t("ui.on_this_site"))}</h4>
        <p><a href="mass.html">{html.escape(t("ui.mass"))}</a><br>
        <a href="life.html">{html.escape(t("ui.life"))}</a><br>
        <a href="contact.html">{html.escape(t("ui.contact"))}</a></p>
      </div>
      <div>
        <h4>{html.escape(t("ui.official_source"))}</h4>
        <p><a href="{parish['official_url']}">{html.escape(tidy_url(parish['official_url']))}</a><br>
        {html.escape(t("parish." + slug + ".diocese"))}</p>
      </div>
    </div>
    <div class="tribute">
      <p>{html.escape(t("ui.tribute_line"))} <span class="name">{html.escape(FOUNDER)}</span>.</p>
      <p>{html.escape(t("ui.mirror_note"))}</p>
      <p style="margin-top:0.8rem; font-size:0.78rem;">{html.escape(t("ui.no_tracking"))} <em>{html.escape(t("ui.for_people"))}</em></p>
    </div>
    {photo_credit_block(parish)}
    <div id="authorship" class="ark-footer">
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


def tidy_url(u: str) -> str:
    return u.replace('https://', '').replace('http://', '').rstrip('/')


def schedule_rows(parish, t, indent="        ") -> str:
    slug = parish['slug']
    rows = []
    for i, (_day, time) in enumerate(parish["schedule"]):
        day = t(f"parish.{slug}.sched.{i}")
        rows.append(f'{indent}<tr><td>{html.escape(day)}</td><td>{html.escape(time)}</td></tr>')
    return chr(10).join(rows)


def hero_figure(parish, t, ap="assets/") -> str:
    """Hero photograph, or an honest placeholder where no licensed photograph exists."""
    if parish.get('photo_status') == 'pending':
        return ('  <figure class="hero-photo hero-photo-pending">\n'
                '    <div class="hero-photo-pending-inner">\n'
                f'      <img src="{ap}crest.svg" alt="" aria-hidden="true">\n'
                f'      <p>{html.escape(t("ui.photo_pending"))}</p>\n'
                '    </div>\n'
                '  </figure>')
    alt = parish.get('photo_alt') or f"{parish['name']} \u2014 {parish['city']}"
    return ('  <figure class="hero-photo">\n'
            f'    <img src="{ap}hero.jpg" alt="{html.escape(alt)}" loading="eager">\n'
            '  </figure>')


def schedule_note(parish, t) -> str:
    if not parish.get('schedule_note'):
        return ''
    return f'    <p class="schedule-note">{html.escape(t("parish." + parish["slug"] + ".schedule_note"))}</p>'


# ---------------------------------------------------------------------------
# Parish pages
# ---------------------------------------------------------------------------

def page_index(parish, t, url_of, portal_back, ap="assets/") -> str:
    slug = parish['slug']
    src_link = f'<a href="{parish["official_url"]}">{tidy_url(parish["official_url"])}</a>'
    if parish['founded']:
        blurb = t("page.index_blurb", name=html.escape(parish['name']),
                  founded=parish['founded'], city=html.escape(parish['city']),
                  source_link=src_link)
    else:
        blurb = t("page.index_blurb_nofound", name=html.escape(parish['name']),
                  city=html.escape(parish['city']), source_link=src_link)

    body = f'''<main>
{hero_figure(parish, t, ap)}
  <div class="container">
    <h1>{html.escape(t("ui.welcome"))}</h1>
    <p class="lead">{html.escape(t("ui.welcome_lead"))}</p>
    <p>{blurb}</p>
    <div class="card">
      <h3>{html.escape(t("page.card_title"))}</h3>
      <p>{html.escape(t("page.card_body"))}</p>
    </div>

    <h2>{html.escape(t("ui.mass"))}</h2>
    <table class="schedule">
      <thead><tr><th>{html.escape(t("ui.mass_day"))}</th><th>{html.escape(t("ui.mass_time"))}</th></tr></thead>
      <tbody>
{schedule_rows(parish, t)}
      </tbody>
    </table>
{schedule_note(parish, t)}
  </div>
</main>
'''
    return (head(parish, t, ap, t("ui.welcome"), url_of=url_of) + header(parish, t, ap)
            + nav(parish, t, "index.html", portal_back)
            + body + footer(parish, t))


def page_about(parish, t, url_of, portal_back, ap="assets/") -> str:
    slug = parish['slug']
    status = t(f"parish.{slug}.status_note") if parish.get('status_note') else ''
    tagline = t(f"parish.{slug}.tagline")
    diocese = t(f"parish.{slug}.diocese")
    official = f'<a href="{parish["official_url"]}">{tidy_url(parish["official_url"])}</a>'

    if slug == 'nafplio-transfiguration':
        middle = f'''<p>{html.escape(t("nafplio.location", diocese=diocese))}</p>
<p>{html.escape(t("nafplio.history"))}</p>
<div class="card">
  <h3>{html.escape(t("nafplio.arch_h"))}</h3>
  <p>{html.escape(t("nafplio.arch_p"))}</p>
</div>
<div class="card">
  <h3>{html.escape(t("nafplio.crypt_h"))}</h3>
  <p>{html.escape(t("nafplio.crypt_p"))}</p>
</div>'''
    else:
        middle = f'''<p>{html.escape(t("ui.about_founded", name=parish["name"], year=parish["founded"], city=parish["city"], diocese=diocese))}</p>'''

    body = f'''<main><div class="container">
<h1>{html.escape(t("ui.about_h1"))}</h1>
<p class="lead">{html.escape(tagline)}.</p>
{middle}
{f'<p>{html.escape(status)}</p>' if status else ''}
<p>{html.escape(t("ui.about_official"))} {official}</p>
<div class="card">
  <h3>{html.escape(t("ui.commitment_h"))}</h3>
  <p>{html.escape(t("ui.commitment_p"))}</p>
</div>
</div></main>'''
    return (head(parish, t, ap, t("ui.about_h1"), url_of=url_of) + header(parish, t, ap)
            + nav(parish, t, "about.html", portal_back)
            + body + footer(parish, t))


def page_mass(parish, t, url_of, portal_back, ap="assets/") -> str:
    body = f'''<main><div class="container">
<h1>{html.escape(t("ui.mass_h1"))}</h1>
<table class="schedule">
  <thead><tr><th>{html.escape(t("ui.mass_day"))}</th><th>{html.escape(t("ui.mass_time"))}</th></tr></thead>
  <tbody>
{schedule_rows(parish, t, indent="    ")}
  </tbody>
</table>
{schedule_note(parish, t)}
<p><a href="{parish['official_url']}">{html.escape(t("ui.official_source"))}</a></p>
</div></main>'''
    return (head(parish, t, ap, t("ui.mass_h1"), url_of=url_of) + header(parish, t, ap)
            + nav(parish, t, "mass.html", portal_back)
            + body + footer(parish, t))


def page_life(parish, t, url_of, portal_back, ap="assets/") -> str:
    items = [t(f"page.life_item.{i}") for i in range(8)]
    body = f'''<main><div class="container">
<h1>{html.escape(t("page.life_h1"))}</h1>
<p class="lead">{html.escape(t("page.life_intro"))}</p>
<ul class="groups">
{chr(10).join(f'  <li>{html.escape(x)}</li>' for x in items)}
</ul>
</div></main>'''
    return (head(parish, t, ap, t("page.life_h1"), url_of=url_of) + header(parish, t, ap)
            + nav(parish, t, "life.html", portal_back)
            + body + footer(parish, t))


def page_contact(parish, t, url_of, portal_back, ap="assets/") -> str:
    slug = parish['slug']
    email_row = (f'<dt>{html.escape(t("page.dt_email"))}</dt>'
                 f'<dd><a href="mailto:{parish["email"]}">{parish["email"]}</a></dd>'
                 if parish.get('email') else '')
    phone_row = (f'<dt>{html.escape(t("page.dt_phone"))}</dt><dd>{html.escape(parish["phone"])}</dd>'
                 if parish.get('phone') else '')
    body = f'''<main><div class="container">
<h1>{html.escape(t("ui.contact_h1"))}</h1>
<div class="contact-block">
  <dl>
    <dt>{html.escape(t("page.dt_address"))}</dt><dd>{html.escape(parish['address'])}</dd>
    {phone_row}
    {email_row}
    <dt>{html.escape(t("page.dt_diocese"))}</dt><dd>{html.escape(t("parish." + slug + ".diocese"))}</dd>
  </dl>
</div>
<p><a href="{parish['official_url']}">{html.escape(t("ui.official_source"))} → {tidy_url(parish['official_url'])}</a></p>
</div></main>'''
    return (head(parish, t, ap, t("ui.contact_h1"), url_of=url_of) + header(parish, t, ap)
            + nav(parish, t, "contact.html", portal_back)
            + body + footer(parish, t))


# ---------------------------------------------------------------------------
# Portal (front page)
# ---------------------------------------------------------------------------

REGION_ORDER = ["united-states", "montreal", "atlantic-canada", "mexico", "greece"]

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


def parish_href(p, lang, prefix) -> str:
    """Link from a portal in `lang` to that parish. Native language keeps the
    bare URL so no existing link ever breaks."""
    if lang == NATIVE_OF.get(p['lang'], DEFAULT):
        return f'{prefix}parishes/{p["slug"]}/index.html'
    return f'{prefix}parishes/{p["slug"]}/{lang}/index.html'


def parish_card(p, t, prefix) -> str:
    slug = p['slug']
    featured_cls = ' parish-card-featured' if slug == 'holy-trinity' else ''
    blurb = t(f"parish.{slug}.portal_blurb")
    city_line = t(f"parish.{slug}.city_line")
    founded_line = t(f"parish.{slug}.founded_line")

    if p.get('photo_status') == 'pending':
        photo = (f'          <div class="parish-card-nophoto">\n'
                 f'            <img src="{prefix}parishes/{slug}/assets/crest.svg" alt="" aria-hidden="true">\n'
                 f'            <span>{html.escape(t("ui.photo_pending"))}</span>\n'
                 f'          </div>')
    else:
        alt = p.get('photo_alt', p['name'])
        photo = (f'          <img src="{prefix}parishes/{slug}/assets/thumb.jpg" alt="{html.escape(alt)}" loading="lazy">\n'
                 f'          <div class="parish-card-crest-overlay"><img src="{prefix}parishes/{slug}/assets/crest.svg" alt=""></div>')

    return (f'      <a class="parish-card{featured_cls}" href="{parish_href(p, t.code, prefix)}">\n'
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


def region_blocks(t, prefix) -> str:
    out = []
    for key in REGION_ORDER:
        members = [p for p in PARISHES if p.get('region') == key]
        if not members:
            continue
        cards = chr(10).join(parish_card(p, t, prefix) for p in members)
        out.append(
            f'  <div class="container region-block" id="region-{key}">\n'
            f'    <div class="region-head">\n'
            f'      <h2>{html.escape(t("region." + key + ".name"))}</h2>\n'
            f'      <p>{html.escape(t("region." + key + ".sub"))}</p>\n'
            f'    </div>\n'
            f'    <div class="parish-grid">\n'
            f'{cards}\n'
            f'    </div>\n'
            f'  </div>')
    return chr(10).join(out)


def footnote_1613(t) -> str:
    """The bottom-of-page footnote. Deliberately light. Not a lineage claim."""
    ps = "\n\n".join(f'    <p>{html.escape(t("footnote.p" + str(i)))}</p>'
                      for i in range(1, 7))
    return (
        '  <div class="container portal-section footnote-block" id="footnote">\n'
        '    <div class="footnote-rule"></div>\n'
        f'    <h2>{html.escape(t("footnote.h2"))}</h2>\n'
        f'    <p class="footnote-aside">{html.escape(t("footnote.aside"))}</p>\n'
        '\n'
        f'{ps}\n'
        '\n'
        '    <p class="footnote-more"><a href="https://github.com/EVEglyphDesign/paix-parish-platform/blob/main/heritage/LIGNEE-ACADIENNE.md">'
        f'{html.escape(t("footnote.more"))} →</a></p>\n'
        '    <div class="footnote-credit">\n'
        f'      <p>{html.escape(t("footnote.cma"))}</p>\n'
        '      <p><a href="https://snacadie.org/nos-dossiers/promotion/congres-mondial-acadien" rel="noopener">'
        f'{html.escape(t("footnote.cma_link"))} →</a></p>\n'
        '    </div>\n'
        '  </div>\n')


POSITION_URL = "https://eveglyphdesign.github.io/eve-glyph-boot-contract/position/"
EDUCATION_URL = "https://eveglyphdesign.github.io/paix-educational-game/"


def cover(t) -> str:
    """Cover page. Churches on one side, children on the other. EgD-POS-001.

    Two panels, three points each, one shared foot. The reader chooses a side
    before the platform asks anything of them.
    """
    e = html.escape

    def side(cls, eyebrow, h2, lead, bullets, cta, href, external=False):
        items = "\n".join(
            f"          <li>{e(t(b))}</li>" for b in bullets)
        rel = ' rel="noopener"' if external else ""
        return f'''      <section class="cover-side {cls}">
        <p class="cover-eyebrow">{e(t(eyebrow))}</p>
        <h2>{e(t(h2))}</h2>
        <p class="cover-side-lead">{e(t(lead))}</p>
        <ul class="cover-points">
{items}
        </ul>
        <a class="cover-cta" href="{href}"{rel}>{e(t(cta))} <span aria-hidden="true">&#8594;</span></a>
      </section>'''

    left = side("cover-side-churches", "cover.left_eyebrow", "cover.left_h2",
                "cover.left_lead",
                ["cover.left_b1", "cover.left_b2", "cover.left_b3"],
                "cover.left_cta", "#region-united-states")
    right = side("cover-side-children", "cover.right_eyebrow", "cover.right_h2",
                 "cover.right_lead",
                 ["cover.right_b1", "cover.right_b2", "cover.right_b3"],
                 "cover.right_cta", EDUCATION_URL, external=True)

    return f'''  <div class="cover" id="cover">
    <div class="container cover-head">
      <p class="cover-kicker">{e(t("cover.kicker"))}</p>
      <h1>{e(t("cover.h1"))}</h1>
      <p class="cover-lead">{e(t("cover.lead"))}</p>
    </div>
    <div class="container cover-split">
{left}
      <div class="cover-spine" aria-hidden="true"><span>&#10011;</span></div>
{right}
    </div>
    <div class="container cover-foot">
      <p>{e(t("cover.foot"))}</p>
      <p class="cover-foot-links">
        <a href="{POSITION_URL}" rel="noopener">{e(t("cover.foot_link"))} &#8594;</a>
        <a href="#about" class="cover-foot-scroll">{e(t("cover.scroll"))} &#8595;</a>
      </p>
    </div>
  </div>
'''


def portal(t, prefix="", url_of=None) -> str:
    """`prefix` is the path back to the repository root from this page."""
    parish_links = "<br>".join(
        f'<a href="{parish_href(p, t.code, prefix)}">{html.escape(p["short"])}</a>'
        for p in PARISHES)
    n = str(len(PARISHES))
    return f'''<!DOCTYPE html>
<html lang="{t.html_lang}">
<head>
<meta charset="utf-8">
<title>{html.escape(t("portal.title"))}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(t("portal.meta_desc"))}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/style.css">
<link rel="stylesheet" href="{prefix}assets/portal.css">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/portal-crest.svg">
{hreflang_links(url_of)}
</head>
<body class="portal-body">
{lang_switcher(t, url_of)}

<header class="site-header portal-header">
  <div class="container">
    <img src="{prefix}assets/portal-crest.svg" alt="" class="crest" aria-hidden="true">
    <div class="site-title">
      <h1>PAIX Parish Platform</h1>
      <div class="sub">{html.escape(t("portal.subtitle"))}</div>
    </div>
  </div>
</header>

<nav class="site-nav">
  <div class="container">
    <a href="index.html" class="active">{html.escape(t("portal.nav_parishes"))}</a>
    <a href="#ledger">{html.escape(t("portal.nav_ledger"))}</a>
    <a href="#about">{html.escape(t("portal.nav_about"))}</a>
    <a href="#kofc">{html.escape(t("portal.nav_kofc"))}</a>
    <a href="#doctrine">{html.escape(t("portal.nav_doctrine"))}</a>
  </div>
</nav>

<main>
{cover(t)}
  <div class="container portal-hero">
    <h1>{html.escape(t("portal.hero_h1"))}</h1>
    <p class="lead">{html.escape(t("portal.hero_lead", count=n))}</p>
    <p>{html.escape(t("portal.hero_p"))}</p>
  </div>

{region_blocks(t, prefix)}

  <div class="container" id="ledger">
    <div class="caisse-hero">
      <div class="caisse-hero-badge">{html.escape(t("portal.ledger_badge"))}</div>
      <h2>{html.escape(t("portal.ledger_h2"))}</h2>
      <p class="caisse-hero-lead">{html.escape(t("portal.ledger_lead"))}</p>
      <div class="caisse-hero-plain">
        <ul>
          <li>{html.escape(t("portal.ledger_li1"))}</li>
          <li>{html.escape(t("portal.ledger_li2"))}</li>
          <li>{html.escape(t("portal.ledger_li3"))}</li>
          <li>{html.escape(t("portal.ledger_li4"))}</li>
        </ul>
      </div>
      <div class="caisse-hero-cta">
        <a class="btn-primary" href="https://eveglyphdesign.github.io/holy-trinity-caisse/">{html.escape(t("portal.ledger_cta1"))} →</a>
        <a class="btn-secondary" href="https://eveglyphdesign.github.io/holy-trinity-caisse/knights-letter.html">{html.escape(t("portal.ledger_cta2"))}</a>
      </div>
    </div>
  </div>

  <div class="container portal-section" id="about">
    <h2>{html.escape(t("portal.about_h2"))}</h2>
    <p>{html.escape(t("portal.about_p", count=n))}</p>
    <div class="pillars">
      <div class="pillar">
        <h4>{html.escape(t("portal.pillar1_h"))}</h4>
        <p>{html.escape(t("portal.pillar1_p"))}</p>
      </div>
      <div class="pillar">
        <h4>{html.escape(t("portal.pillar2_h"))}</h4>
        <p>{html.escape(t("portal.pillar2_p"))}</p>
      </div>
      <div class="pillar">
        <h4>{html.escape(t("portal.pillar3_h"))}</h4>
        <p>{html.escape(t("portal.pillar3_p"))}</p>
      </div>
      <div class="pillar">
        <h4>{html.escape(t("portal.pillar4_h"))}</h4>
        <p>{html.escape(t("portal.pillar4_p"))}</p>
      </div>
    </div>
  </div>

  <div class="container portal-section" id="languages">
    <h2>{html.escape(t("portal.lang_h2"))}</h2>
    <p class="lead">{html.escape(t("portal.lang_p1"))}</p>
    <p>{html.escape(t("portal.lang_p2"))}</p>
    <p>{html.escape(t("portal.lang_p3"))}</p>
    <div class="lang-grid">
{chr(10).join(f'      <a href="{url_of(c)}" hreflang="{c}" lang="{c}"><span>{html.escape(e)}</span></a>' for c, e, _, _ in LANGS_DISPLAY)}
    </div>
  </div>

  <div class="container portal-section" id="kofc">
    <h2>{html.escape(t("portal.kofc_h2"))}</h2>
    <p class="lead">{html.escape(t("portal.kofc_lead"))}</p>
    <p>{html.escape(t("portal.kofc_p"))}</p>
    <ul class="kofc-list">
      <li><strong>{html.escape(t("portal.kofc_li1_b"))}</strong> {html.escape(t("portal.kofc_li1"))}</li>
      <li><strong>{html.escape(t("portal.kofc_li2_b"))}</strong> {html.escape(t("portal.kofc_li2"))}</li>
      <li><strong>{html.escape(t("portal.kofc_li3_b"))}</strong> {html.escape(t("portal.kofc_li3"))}</li>
      <li><strong>{html.escape(t("portal.kofc_li4_b"))}</strong> {html.escape(t("portal.kofc_li4"))}</li>
    </ul>
    <p class="kofc-note">{html.escape(t("portal.kofc_note"))}</p>

    <p class="caisse-crossref"><a href="#ledger">{html.escape(t("portal.kofc_xref"))}</a></p>
  </div>

  <div class="container portal-section" id="doctrine">
    <h2>{html.escape(t("portal.doctrine_h2"))}</h2>
    <div class="doctrine-grid">
      <div>
        <h4>{html.escape(t("portal.doc1_h"))}</h4>
        <p>{html.escape(t("portal.doc1_p"))}</p>
      </div>
      <div>
        <h4>{html.escape(t("portal.doc2_h"))}</h4>
        <p>{html.escape(t("portal.doc2_p"))}</p>
      </div>
      <div>
        <h4>{html.escape(t("portal.doc3_h"))}</h4>
        <p>{html.escape(t("portal.doc3_p", founder=FOUNDER))}</p>
      </div>
      <div>
        <h4>{html.escape(t("portal.doc4_h"))}</h4>
        <p>{html.escape(t("portal.doc4_p"))}</p>
      </div>
    </div>
  </div>

  <div class="container portal-section" id="related">
    <h2>{html.escape(t("portal.related_h2"))}</h2>
    <div class="doctrine-grid">
      <div>
        <h4><a href="https://eveglyphdesign.github.io/paix-educational-game/">{html.escape(t("portal.rel1_h"))}</a></h4>
        <p>{html.escape(t("portal.rel1_p"))}</p>
      </div>
      <div>
        <h4><a href="https://eveglyphdesign.github.io/holy-trinity-caisse/">{html.escape(t("portal.rel2_h"))}</a></h4>
        <p>{html.escape(t("portal.rel2_p"))}</p>
      </div>
    </div>
  </div>

{footnote_1613(t)}
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-cols">
      <div>
        <h4>{html.escape(t("portal.foot_col1_h"))}</h4>
        <p>{html.escape(t("portal.foot_col1_p"))}</p>
      </div>
      <div>
        <h4>{html.escape(t("portal.foot_col2_h"))}</h4>
        <p>{parish_links}</p>
      </div>
      <div>
        <h4>{html.escape(t("portal.foot_col3_h"))}</h4>
        <p><a href="https://github.com/EVEglyphDesign/paroisse-sainte-anne-des-pays-bas">{html.escape(t("portal.foot_ref1"))}</a><br>
        <a href="https://github.com/EVEglyphDesign/kofc-6673-outreach">{html.escape(t("portal.foot_ref2"))}</a><br>
        <a href="https://github.com/EVEglyphDesign/godaddy-killer">{html.escape(t("portal.foot_ref3"))}</a></p>
      </div>
    </div>
    <div class="tribute">
      <p>{html.escape(t("portal.foot_tribute1"))} <span class="name">{html.escape(FOUNDER)}</span>.</p>
      <p>{html.escape(t("portal.foot_tribute2"))}</p>
      <p style="margin-top:0.8rem; font-size:0.78rem;">{html.escape(t("ui.no_tracking"))} <em>{html.escape(t("ui.for_people"))}</em></p>
    </div>
    <div class="photo-credit">
      <p>{html.escape(t("portal.foot_photos"))} {photo_credits_line()}</p>
    </div>
    <div id="authorship" class="ark-footer">
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

/* A region with a single parish should not stretch one card across the page */
.parish-grid:has(> .parish-card:only-child) {
  grid-template-columns: minmax(280px, 520px);
  justify-content: start;
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
.footnote-credit {
  margin-top: 1.8rem;
  padding: 1rem 1.15rem;
  border-left: 3px solid var(--stella-gold);
  background: #fbf6ea;
  max-width: 68ch;
}
.footnote-credit p { margin: 0; font-size: 0.92rem; color: #5a5142; }
.footnote-credit p + p { margin-top: 0.6rem; }
.footnote-credit a {
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-weight: 600;
  color: #8a6416;
  text-decoration: none;
  border-bottom: 1px solid #ddc98f;
}
.footnote-credit a:hover { color: var(--ink); border-bottom-color: var(--stella-gold); }
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

/* ---- Cover page — EgD-POS-001. Churches one side, children the other ---- */
.cover {
  background: linear-gradient(180deg, var(--marine-deep) 0%, var(--marine) 62%, var(--marine-light) 100%);
  color: #f3ede0;
  margin: -2.5rem 0 3.2rem;
  padding: 3.4rem 0 2.6rem;
  border-bottom: 3px solid var(--stella-gold);
}
.cover .container { max-width: 960px; }
.cover-head { max-width: 860px; }
.cover-kicker {
  font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase;
  font-weight: 600; color: var(--stella-gold-light); margin: 0 0 0.7rem;
}
.cover-head h1 {
  font-size: clamp(2.1rem, 5.2vw, 3.3rem); line-height: 1.08;
  color: #fffdf7; margin: 0 0 0.85rem;
}
.cover-lead {
  font-size: clamp(1.02rem, 2.1vw, 1.2rem); line-height: 1.6;
  color: #e6dcc6; margin: 0; max-width: 46rem;
}
.cover-split {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 0 2.4rem;
  align-items: stretch;
  margin-top: 2.9rem;
}
.cover-side {
  display: flex; flex-direction: column;
  background: rgba(255, 253, 247, 0.055);
  border: 1px solid rgba(216, 199, 160, 0.28);
  border-top: 3px solid var(--stella-gold);
  padding: 1.7rem 1.7rem 1.5rem;
}
.cover-eyebrow {
  font-size: 0.68rem; letter-spacing: 0.15em; text-transform: uppercase;
  font-weight: 600; color: var(--stella-gold-light); margin: 0 0 0.45rem;
}
.cover-side h2 {
  font-size: clamp(1.7rem, 3.4vw, 2.15rem); line-height: 1.12;
  color: #fffdf7; margin: 0 0 0.55rem;
}
.cover-side-lead {
  font-size: 1.02rem; line-height: 1.58; color: #e6dcc6; margin: 0 0 1.15rem;
}
.cover-points { list-style: none; margin: 0 0 1.5rem; padding: 0; }
.cover-points li {
  position: relative; padding-left: 1.15rem; margin-bottom: 0.8rem;
  font-size: 0.94rem; line-height: 1.58; color: #ddd3bd;
}
.cover-points li::before {
  content: ""; position: absolute; left: 0; top: 0.62em;
  width: 6px; height: 6px; background: var(--stella-gold); border-radius: 50%;
}
.cover-cta {
  margin-top: auto; align-self: flex-start;
  font-size: 0.86rem; font-weight: 600; letter-spacing: 0.06em;
  text-transform: uppercase; text-decoration: none;
  color: #08283f; background: var(--stella-gold-light);
  padding: 0.68rem 1.25rem; border: 1px solid var(--stella-gold-light);
  white-space: nowrap; text-align: center;
  transition: background 0.18s ease, color 0.18s ease;
}
.cover-cta:hover, .cover-cta:focus {
  background: transparent; color: var(--stella-gold-light);
}
.cover-spine {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; width: 1px; background: rgba(216, 199, 160, 0.3);
}
.cover-spine span {
  font-size: 1.45rem; color: var(--stella-gold);
  background: #0e4468; padding: 0.75rem 0.1rem;
  line-height: 1;
}
.cover-foot {
  margin-top: 2.6rem; padding-top: 1.4rem;
  border-top: 1px solid rgba(216, 199, 160, 0.28);
  max-width: 880px;
}
.cover-foot p {
  margin: 0 0 0.9rem; font-size: 0.97rem; line-height: 1.62; color: #d8cdb5;
  max-width: 52rem;
}
.cover-foot-links {
  display: flex; flex-wrap: wrap; gap: 0.6rem 1.9rem; margin: 0 !important;
}
.cover-foot-links a {
  color: var(--stella-gold-light); text-decoration: none;
  font-size: 0.9rem; font-weight: 600;
  border-bottom: 1px solid rgba(212, 169, 74, 0.45); padding-bottom: 1px;
}
.cover-foot-links a:hover, .cover-foot-links a:focus { border-bottom-color: var(--stella-gold-light); }

@media (max-width: 820px) {
  .cover { padding: 2.5rem 0 2rem; margin-bottom: 2.4rem; }
  .cover-split { grid-template-columns: 1fr; gap: 1.5rem; margin-top: 2.1rem; }
  .cover-spine { width: auto; height: 1px; background: rgba(216, 199, 160, 0.3); }
  .cover-spine span { padding: 0 0.7rem; }
  .cover-cta { white-space: normal; }
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
    """Emit the portal and every parish site in all nine languages.

    Back-compatibility rule: the bare URL of every page keeps the language the
    parish's own community speaks, so no link that already exists anywhere in
    the world breaks. The other eight sit underneath it in /<lang>/.
    """
    (ROOT / "assets" / "portal.css").write_text(PORTAL_CSS)
    (ROOT / "assets" / "portal-crest.svg").write_text(PORTAL_CREST)

    translators = {code: translator(code) for code in LANG_CODES}

    # ---- Portal: / (English, back-compatible) and /<lang>/ ----------------
    def portal_url(from_prefix):
        def url_of(code):
            return f"{from_prefix}{code}/index.html"
        return url_of

    (ROOT / "index.html").write_text(
        portal(translators[DEFAULT], prefix="", url_of=portal_url("")))
    for code in LANG_CODES:
        d = ROOT / code
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(
            portal(translators[code], prefix="../", url_of=portal_url("../")))

    # ---- Parish sites -----------------------------------------------------
    pages = [("index.html", page_index), ("about.html", page_about),
             ("mass.html", page_mass), ("life.html", page_life),
             ("contact.html", page_contact)]

    for p in PARISHES:
        native = NATIVE_OF.get(p["lang"], DEFAULT)
        pdir = PARISHES_DIR / p["slug"]
        adir = pdir / "assets"
        adir.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / "assets" / "style.css", adir / "style.css")
        (adir / "crest.svg").write_text(crest_svg(p["crest_style"]))

        for fname, fn in pages:
            # native copy at the bare URL
            def url_of(code, _f=fname, _n=native):
                return _f if code == _n else f"{code}/{_f}"
            (pdir / fname).write_text(
                fn(p, translators[native], url_of, "../../index.html", "assets/"))

            # one subdirectory per language
            for code in LANG_CODES:
                sub = pdir / code
                sub.mkdir(exist_ok=True)
                def url_of_sub(c, _f=fname, _n=native):
                    return f"../{_f}" if c == _n else f"../{c}/{_f}"
                (sub / fname).write_text(
                    fn(p, translators[code], url_of_sub,
                       f"../../../{code}/index.html", "../assets/"))

            # each language subdirectory needs the stylesheet one level up
        for code in LANG_CODES:
            sub_assets = pdir / code / "assets"
            if sub_assets.exists():
                shutil.rmtree(sub_assets)

        print(f"  \u2713 {p['slug']} ({p['name']}) \u2014 {len(LANG_CODES)} languages")

    # ---- Translation coverage report -------------------------------------
    print("\nTranslation coverage (against the source manifest):")
    for code, (done, total) in coverage().items():
        bar = "\u2588" * round(20 * done / total) if total else ""
        print(f"  {code}  {done:>3}/{total}  {bar}")

    print(f"\nBuilt {len(PARISHES)} parishes \u00d7 {len(LANG_CODES)} languages "
          f"+ portal at {ROOT}")


if __name__ == "__main__":
    build()
