# -*- coding: utf-8 -*-
"""Generates the Uni-Verse Cardiff site pages with a shared shell."""
import os
import json

OUT = os.path.dirname(os.path.abspath(__file__))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Archivo:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')

# ---- verify tick svg ----
VERIFY = ('<svg class="verify" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l2.4 1.8 3-.3 1 2.8 2.8 1-.3 3L23 12l-1.8 2.4.3 3-2.8 1-1 2.8-3-.3L12 22l-2.4-1.8-3 .3-1-2.8-2.8-1 .3-3L1 12l1.8-2.4-.3-3 2.8-1 1-2.8 3 .3L12 2zm-1.2 13.2l5.5-5.5-1.4-1.4-4.1 4.1-2-2L7.4 12l3.4 3.2z"/></svg>')

ICONS = {
    'feed': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l9-9 9 9M5 10v10h5v-6h4v6h5V10"/></svg>',
    'events': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path stroke-linecap="round" d="M3 10h18M8 2v4M16 2v4"/></svg>',
    'opps': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/><path stroke-linecap="round" d="M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>',
    'discounts': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z"/><circle cx="7" cy="7" r="1.2" fill="currentColor"/></svg>',
    'societies': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8zM23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>',
    'ai': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3l1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3zM19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8L19 15z"/></svg>',
    'profile': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path stroke-linecap="round" d="M4 21v-1a6 6 0 016-6h4a6 6 0 016 6v1"/></svg>',
    'bell': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M18 8a6 6 0 10-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 01-3.4 0"/></svg>',
    'chat': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>',
    'search': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path stroke-linecap="round" d="M21 21l-4-4"/></svg>',
    'cal': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path stroke-linecap="round" d="M3 10h18M8 2v4M16 2v4"/></svg>',
    'pin': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    'people': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8z"/></svg>',
    'money': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
    'clock': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" d="M12 7v5l3 2"/></svg>',
    'ext': '<svg fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M7 17L17 7M8 7h9v9"/></svg>',
    'heart': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.8 5.6a5.5 5.5 0 00-7.8 0L12 6.6l-1-1a5.5 5.5 0 10-7.8 7.8l1 1L12 22l7.8-7.6 1-1a5.5 5.5 0 000-7.8z"/></svg>',
    'send': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>',
    'spark': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3l1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3z"/></svg>',
    'arrow': '<svg fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg>',
    'palette': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="13.5" cy="6.5" r="2.5" fill="currentColor" stroke="none"/><circle cx="17.5" cy="10.5" r="2.5" fill="currentColor" stroke="none"/><circle cx="8.5" cy="7.5" r="2.5" fill="currentColor" stroke="none"/><circle cx="6.5" cy="12.5" r="2.5" fill="currentColor" stroke="none"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 2a10 10 0 000 20 2.5 2.5 0 002-4 2 2 0 011.7-3.2H18a4 4 0 004-4 10 10 0 00-10-9z"/></svg>',
    'check': '<svg fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>',
    'map': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M1 6l7-3 8 3 7-3v15l-7 3-8-3-7 3V6z"/><path stroke-linecap="round" d="M8 3v15M16 6v15"/></svg>',
    'close': '<svg fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M6 6l12 12M18 6L6 18"/></svg>',
    'bucs': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 21h8M12 17v4M7 4h10v5a5 5 0 01-10 0V4z"/><path stroke-linecap="round" d="M7 5H4a1 1 0 00-1 1v1a4 4 0 004 4M17 5h3a1 1 0 011 1v1a4 4 0 01-4 4"/></svg>',
    'flatmates': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="8" cy="15" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M10.8 12.2L21 2M21 2v5M21 2h-5M16.5 6.5L19 9"/></svg>',
    'plus': '<svg fill="none" stroke="currentColor" stroke-width="2.4" viewBox="0 0 24 24"><path stroke-linecap="round" d="M12 5v14M5 12h14"/></svg>',
    'shield': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6l8-4z"/></svg>',
    'phone': '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3.1-8.7A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.3 1.8.6 2.7a2 2 0 01-.4 2.1L8 9.9a16 16 0 006 6l1.4-1.4a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.8 2.2z"/></svg>',
}

# Pin/badge colour by exact "going" count — green under 20, orange 20-69, red 70+
def going_color(n):
    if n < 20:
        return '#2ED573'
    if n < 70:
        return '#FFA502'
    return '#FF4757'

NAV = [
    ('index.html', 'feed', 'Home'),
    ('events.html', 'events', 'Events'),
    ('societies.html', 'societies', 'Societies'),
    ('bucs.html', 'bucs', 'BUCS'),
    ('discounts.html', 'discounts', 'Discounts'),
    ('opportunities.html', 'opps', 'Opportunities'),
    ('map.html', 'map', 'Map'),
    ('flatmates.html', 'flatmates', 'Accommodation'),
    ('profile.html', 'profile', 'Account'),
    ('ai.html', 'ai', 'Ask Uni-Verse AI'),
]

# Sitewide search index — powers the live dropdown in the topbar on every page.
# t=title, c=category badge, u=target url, d=short subtitle shown under the title.
SEARCH_INDEX = [
    # Freshers Week
    {'t': 'Move-In Day & Welcome BBQ', 'c': 'Freshers Week', 'u': 'events.html', 'd': 'Mon 21 Sep · Halls of Residence'},
    {'t': 'International Students Welcome Social', 'c': 'Freshers Week', 'u': 'events.html', 'd': 'Tue 22 Sep · Y Plas'},
    {'t': 'Give It A Go: Try a Sport', 'c': 'Freshers Week', 'u': 'events.html', 'd': 'Thu 24 Sep · Sports Fields, Llanrumney'},
    {'t': 'Freshers Fair', 'c': 'Freshers Week', 'u': 'events.html', 'd': 'Mon 28 Sep · Y Plas & SU'},
    {'t': 'YOLO: Freshers Special', 'c': 'Freshers Week', 'u': 'events.html', 'd': 'Wed 30 Sep · Y Plas'},
    {'t': 'Freshers Bar Crawl: City Centre', 'c': 'Freshers Week', 'u': 'events.html', 'd': 'Fri 2 Oct · City Centre'},
    # Events
    {'t': 'Games Night + Pizza', 'c': 'Event', 'u': 'events.html', 'd': 'Thu 2 Oct · SU, Y Plas'},
    {'t': 'Open Mic Night', 'c': 'Event', 'u': 'events.html', 'd': 'Fri 3 Oct · The Taf'},
    {'t': 'CV Clinic + Networking', 'c': 'Event', 'u': 'events.html', 'd': 'Wed 8 Oct · sbarc | spark'},
    {'t': 'Give It A Go: Bouldering', 'c': 'Event', 'u': 'events.html', 'd': 'Sat 11 Oct · Boulders CDF'},
    {'t': 'Film Night: Cult Classics', 'c': 'Event', 'u': 'events.html', 'd': 'Sun 12 Oct · SU Cinema'},
    {'t': 'Careers in Sustainability', 'c': 'Event', 'u': 'events.html', 'd': 'Tue 14 Oct · Glamorgan Building'},
    # BUCS
    {'t': 'Cardiff vs Hartpury', 'c': 'BUCS', 'u': 'bucs.html', 'd': 'Wed 23 Sep · Home · Super Rugby'},
    {'t': 'Durham vs Cardiff', 'c': 'BUCS', 'u': 'bucs.html', 'd': 'Wed 30 Sep · Away · Super Rugby'},
    {'t': 'Cardiff vs Cardiff Met — The Cardiff Clash', 'c': 'BUCS', 'u': 'bucs.html', 'd': 'Wed 7 Oct · Cardiff Arms Park'},
    {'t': 'Brunel vs Cardiff', 'c': 'BUCS', 'u': 'bucs.html', 'd': 'Wed 14 Oct · Away · Super Rugby'},
    {'t': 'Cardiff vs Nottingham', 'c': 'BUCS', 'u': 'bucs.html', 'd': 'Wed 28 Oct · Home · Super Rugby'},
    {'t': 'Exeter vs Cardiff', 'c': 'BUCS', 'u': 'bucs.html', 'd': 'Wed 4 Nov · Away · Super Rugby'},
    # Societies
    {'t': 'Film Society', 'c': 'Society', 'u': 'society-film.html', 'd': '1,240 members'},
    {'t': 'Hiking & Mountaineering', 'c': 'Society', 'u': 'society-hiking.html', 'd': '860 members'},
    {'t': 'Entrepreneurs Society', 'c': 'Society', 'u': 'society-entrepreneurs.html', 'd': '1,510 members'},
    {'t': 'Drama Society', 'c': 'Society', 'u': 'society-drama.html', 'd': '740 members'},
    {'t': 'Football Club', 'c': 'Society', 'u': 'society-football.html', 'd': '2,100 members'},
    {'t': 'International Students', 'c': 'Society', 'u': 'society-international.html', 'd': '1,880 members'},
    {'t': 'Netball Club', 'c': 'Society', 'u': 'society-netball.html', 'd': '980 members'},
    {'t': 'Music Society', 'c': 'Society', 'u': 'society-music.html', 'd': '690 members'},
    {'t': 'Debate Society', 'c': 'Society', 'u': 'society-debate.html', 'd': '410 members'},
    {'t': 'RAG Society', 'c': 'Society', 'u': 'society-rag.html', 'd': '560 members'},
    {'t': 'Photography Society', 'c': 'Society', 'u': 'society-photography.html', 'd': '730 members'},
    {'t': 'Pride Society', 'c': 'Society', 'u': 'society-pride.html', 'd': '890 members'},
    # Discounts
    {'t': 'Brewhouse Coffee', 'c': 'Discount', 'u': 'discounts.html', 'd': 'Cathays · 25% off'},
    {'t': 'Got Beef', 'c': 'Discount', 'u': 'discounts.html', 'd': 'City Centre · Free side'},
    {'t': 'Sharp Cuts', 'c': 'Discount', 'u': 'discounts.html', 'd': 'Roath · £5 off'},
    {'t': 'Pulse Gym', 'c': 'Discount', 'u': 'discounts.html', 'd': 'Cathays · 50% off first month'},
    {'t': 'Inkwell Books', 'c': 'Discount', 'u': 'discounts.html', 'd': 'City Centre · 15% off'},
    {'t': 'Dough Co', 'c': 'Discount', 'u': 'discounts.html', 'd': 'Cathays · 2-for-1 pizzas'},
    # Opportunities
    {'t': 'Summer Internship — Admiral, Data Analyst', 'c': 'Opportunity', 'u': 'opportunities.html', 'd': '£24k pro-rata · Cardiff'},
    {'t': 'Graduate Scheme — GoCompare, Software Engineer', 'c': 'Opportunity', 'u': 'opportunities.html', 'd': '£30k · Newport'},
    {'t': 'Part-time — Student Brand Ambassador', 'c': 'Opportunity', 'u': 'opportunities.html', 'd': '£12/hr · On campus'},
    {'t': 'Placement Year — Principality, Marketing Assistant', 'c': 'Opportunity', 'u': 'opportunities.html', 'd': 'Paid · Cardiff'},
    # Flatmates
    {'t': "Priya's spare room", 'c': 'Flatmate', 'u': 'flatmates.html', 'd': 'Cathays · £450 pcm'},
    {'t': "Jack's spare room", 'c': 'Flatmate', 'u': 'flatmates.html', 'd': 'Roath · £480–520 pcm'},
    {'t': "Sara's spare room", 'c': 'Flatmate', 'u': 'flatmates.html', 'd': 'Heath · £520 pcm'},
    {'t': "Tom's spare room", 'c': 'Flatmate', 'u': 'flatmates.html', 'd': 'Gabalfa · £420 pcm'},
    {'t': "Elin's spare room", 'c': 'Flatmate', 'u': 'flatmates.html', 'd': 'Canton · £460 pcm'},
    {'t': "Liam's spare room", 'c': 'Flatmate', 'u': 'flatmates.html', 'd': 'Cardiff Bay · £500–540 pcm'},
    # Map venues
    {'t': 'Y Plas — Cardiff SU', 'c': 'Venue', 'u': 'map.html', 'd': 'Park Place · Student Union'},
    {'t': 'Misfits Social Club', 'c': 'Venue', 'u': 'map.html', 'd': 'Miskin Street · Club'},
    {'t': 'Clwb Ifor Bach', 'c': 'Venue', 'u': 'map.html', 'd': 'Womanby Street · Club'},
    {'t': 'Circuit', 'c': 'Venue', 'u': 'map.html', 'd': 'Greyfriars Road · Club'},
    {'t': 'Fuel Rock Club', 'c': 'Venue', 'u': 'map.html', 'd': 'Womanby Street · Club'},
    {'t': 'Metros', 'c': 'Venue', 'u': 'map.html', 'd': 'Bakers Row · Club'},
    {'t': 'Popworld Cardiff', 'c': 'Venue', 'u': 'map.html', 'd': 'St Mary Street · Club'},
    {'t': 'The Woodville', 'c': 'Venue', 'u': 'map.html', 'd': 'Cathays · Bar'},
    {'t': 'Dead Canary', 'c': 'Venue', 'u': 'map.html', 'd': 'Charles Street · Bar'},
    {'t': 'BrewDog Cardiff', 'c': 'Venue', 'u': 'map.html', 'd': 'Westgate Street · Bar'},
    {'t': 'The Owain Glyndŵr', 'c': 'Venue', 'u': 'map.html', 'd': 'St John Street · Bar'},
    {'t': 'Cardiff University Sports Fields', 'c': 'Venue', 'u': 'map.html', 'd': 'Llanrumney · BUCS'},
    {'t': 'Cardiff Arms Park', 'c': 'Venue', 'u': 'map.html', 'd': 'City Centre · BUCS'},
    # Pages
    {'t': 'Home', 'c': 'Page', 'u': 'index.html', 'd': 'Your feed'},
    {'t': 'Events', 'c': 'Page', 'u': 'events.html', 'd': "What's on"},
    {'t': 'Societies', 'c': 'Page', 'u': 'societies.html', 'd': 'Find your people'},
    {'t': 'BUCS', 'c': 'Page', 'u': 'bucs.html', 'd': 'Cardiff University sport'},
    {'t': 'Discounts', 'c': 'Page', 'u': 'discounts.html', 'd': 'Your card, your savings'},
    {'t': 'Opportunities', 'c': 'Page', 'u': 'opportunities.html', 'd': "Don't miss out"},
    {'t': 'Map', 'c': 'Page', 'u': 'map.html', 'd': 'Clubs, bars, the SU & BUCS'},
    {'t': 'Accommodation', 'c': 'Page', 'u': 'flatmates.html', 'd': 'Find a housemate'},
    {'t': 'Messages', 'c': 'Page', 'u': 'messages.html', 'd': 'Your inbox'},
    {'t': 'Staying safe', 'c': 'Page', 'u': 'safety.html', 'd': 'Night safety & taxis'},
    {'t': 'Ask Uni-Verse AI', 'c': 'Page', 'u': 'ai.html', 'd': 'Your Cardiff guide'},
]

# Leaflet (OpenStreetMap) — no API key needed, used on the venue map page
LEAFLET_CSS = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">'
LEAFLET_JS = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'

# Cardiff SU's own societies page — the official place to actually join (used on the Societies page)
SU_SOCIETIES_URL = 'https://www.cardiffstudents.com/activities/societies/'

def rail(active):
    btns = ['<div class="rail-logo">U</div>']
    for href, key, label in NAV:
        cls = 'rail-btn active' if key == active else 'rail-btn'
        btns.append('<a class="%s" href="%s"><span class="tip">%s</span>%s</a>' % (cls, href, label, ICONS[key]))
    btns.append('<div class="rail-spacer"></div>')
    btns.append('<a class="rail-avatar" href="profile.html">FW</a>')
    return '<nav class="rail">' + ''.join(btns) + '</nav>'

def topbar():
    return ('<header class="topbar">'
            '<div class="brand"><div class="name">Uni<span>-</span>Verse</div>'
            '<div class="loc">Cardiff University</div></div>'
            '<div class="search">%s<input type="text" id="topSearchInput" autocomplete="off" '
            'placeholder="Search events, societies, jobs, discounts…">'
            '<div class="search-results" id="topSearchResults" hidden></div></div>'
            '<div class="top-actions">'
            '<button class="icon-btn"><span class="dot"></span>%s</button>'
            '<a class="icon-btn" href="messages.html" aria-label="Messages">%s</a>'
            '</div></header>' % (ICONS['search'], ICONS['bell'], ICONS['chat']))

def theme_switcher():
    opts = [
        ('electric', '#0E1230', '#C8FF3D', '#5AD1FF', 'Electric', 'Bold navy &amp; lime'),
        ('cardiff', '#1A0A0C', '#E52713', '#F4C430', 'Cardiff', 'Red &amp; gold, official'),
        ('midnight', '#0B0B0D', '#ED1C24', '#4ECDC4', 'Midnight', 'Red on near-black'),
        ('daylight', '#F5F2ED', '#C8102E', '#0A7EA4', 'Daylight', 'Clean light mode'),
    ]
    rows = []
    for set_, a, b, c, name, desc in opts:
        rows.append(
            '<button class="theme-opt" data-set="%s">'
            '<span class="theme-swatch"><i style="background:%s"></i><i style="background:%s"></i><i style="background:%s"></i></span>'
            '<span class="tinfo"><span class="tname">%s</span><br><span class="tdesc">%s</span></span>'
            '%s</button>' % (set_, a, b, c, name, desc, ICONS['check'].replace('class="', 'class="tcheck ') if False else '<svg class="tcheck" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>'))
    return ('<button class="theme-fab" id="themeFab" aria-label="Change colours">%s</button>'
            '<div class="theme-panel" id="themePanel"><h4>%s Pick your colours</h4>'
            '<div class="theme-grid">%s</div></div>' % (ICONS['palette'], ICONS['spark'], ''.join(rows)))

def footer():
    return ('<footer><div class="mono-eyebrow">Uni-Verse Cardiff · Concept prototype</div>'
            '<div class="mono-eyebrow">Everything Cardiff, in one place</div></footer>')

def page(title, active, body, two_col_note='', chat=False, extra_head='', extra_scripts=''):
    shell_open = '<div class="app">' + rail(active) + '<div class="main">' + topbar()
    if chat:
        shell_open = '<div class="app">' + rail(active) + '<div class="main">' + topbar()
    doc = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
           '<title>%s · Uni-Verse Cardiff</title>%s%s'
           '<link rel="stylesheet" href="css/styles.css"></head><body>'
           '%s%s</div></div>%s%s'
           '<script src="js/search-data.js"></script>'
           '<script src="js/app.js"></script></body></html>'
           % (title, FONTS, extra_head, shell_open, body, theme_switcher(), extra_scripts))
    return doc

# ---------------- shared content bits ----------------
def sidebar_ai():
    return ('<div class="widget ai"><div class="ai-top"><div class="ai-orb">%s</div>'
            '<div><h3>Ask Uni-Verse</h3><div class="ai-sub">Your Cardiff guide</div></div></div>'
            '<p>Tell me what you want out of uni — I\'ll find the events, people and opportunities to get you there.</p>'
            '<div class="ai-prompts">'
            '<div class="ai-prompt">I want to break into tech — where do I start?%s</div>'
            '<div class="ai-prompt">Find me societies for a shy fresher%s</div>'
            '<div class="ai-prompt">What\'s on this weekend under a tenner?%s</div>'
            '</div><div class="ai-input"><input type="text" placeholder="Ask anything about Cardiff…">'
            '<button class="ai-send">%s</button></div></div>'
            % (ICONS['spark'], ICONS['arrow'], ICONS['arrow'], ICONS['arrow'], ICONS['send']))

def sidebar_journey():
    steps = [
        (True, 'Join your first society'),
        (True, 'Go to a social event'),
        (True, 'Claim a discount'),
        (False, 'Attend a careers event'),
        (False, 'Save your first opportunity'),
    ]
    srows = []
    for done, txt in steps:
        cls = 'step done' if done else 'step'
        box = ('<span class="box">%s</span>' % ICONS['check']) if done else '<span class="box"></span>'
        srows.append('<div class="%s">%s<span class="txt">%s</span></div>' % (cls, box, txt))
    return ('<div class="widget"><div class="widget-head"><h3>Your uni journey</h3>'
            '<span class="mono-eyebrow">Yr 1</span></div>'
            '<div class="prog-ring"><div class="ring">'
            '<svg width="64" height="64" viewBox="0 0 64 64">'
            '<circle cx="32" cy="32" r="27" fill="none" stroke="rgba(128,128,128,.25)" stroke-width="7"/>'
            '<circle cx="32" cy="32" r="27" fill="none" stroke="var(--lime)" stroke-width="7" stroke-linecap="round" stroke-dasharray="169.6" stroke-dashoffset="68"/>'
            '</svg><div class="num">60%%</div></div>'
            '<div class="prog-txt"><div class="lbl">Nicely started 🌱</div>'
            '<div class="dsc">3 of 5 first-term goals done</div></div></div>'
            '<div class="prog-steps">%s</div></div>' % ''.join(srows))

def sidebar_week():
    items = [
        ('02', 'Oct', 'Games Night + Pizza', 'var(--coral)', 'Social · 7:00pm'),
        ('08', 'Oct', 'CV Clinic + Networking', 'var(--amber)', 'Workshop · 5:30pm'),
        ('11', 'Oct', 'Give It A Go: Bouldering', 'var(--sky)', 'Sport · 2:00pm'),
    ]
    rows = []
    for d, m, t, k, meta in items:
        rows.append('<div class="up-item"><div class="up-date"><div class="d">%s</div><div class="m">%s</div></div>'
                    '<div class="up-body"><div class="t">%s</div><div class="meta"><span class="k" style="background:%s"></span>%s</div></div></div>'
                    % (d, m, t, k, meta))
    return ('<div class="widget"><div class="widget-head"><h3>Your week</h3>'
            '<a href="events.html">Calendar →</a></div><div class="up">%s</div></div>' % ''.join(rows))

def sidebar_socs():
    socs = [
        ('🎬', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Film Society', '+180 joined this week'),
        ('🥾', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Hiking & Mountaineering', '+142 joined this week'),
        ('💼', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Entrepreneurs Society', '+119 joined this week'),
    ]
    rows = []
    for emoji, bg, name, meta in socs:
        rows.append('<div class="soc-item"><div class="soc-ava" style="background:%s">%s</div>'
                    '<div class="soc-body"><div class="n">%s</div><div class="m">%s</div></div>'
                    '<button class="soc-join">Join</button></div>' % (bg, emoji, name, meta))
    return ('<div class="widget"><div class="widget-head"><h3>Trending societies</h3>'
            '<a href="societies.html">All →</a></div><div class="soc">%s</div></div>' % ''.join(rows))

# ---------------- POST cards for feed ----------------
def post_social():
    return ('<article class="post"><span class="accent-edge" style="background:var(--coral)"></span>'
            '<div class="post-top"><div class="post-ava" style="background:linear-gradient(135deg,var(--coral),var(--amber))">CS</div>'
            '<div class="post-meta"><div class="org">Cardiff Computer Science Society%s</div>'
            '<div class="time">Posted 2h ago · reposted from @cardiffcompsci</div></div>'
            '<span class="post-cat" style="background:color-mix(in srgb,var(--coral) 16%%,transparent);color:var(--coral)">Social</span></div>'
            '<h3>Games Night + Pizza — Freshers Welcome 🎮</h3>'
            '<p>New to Cardiff? Come meet the society. Free pizza, tournaments on the big screen, no skill required. Bring a mate.</p>'
            '<div class="post-info"><div class="bit">%s Thu 2 Oct · 7:00pm</div>'
            '<div class="bit">%s Students\' Union, Y Plas</div>'
            '<div class="bit">%s 84 going</div></div>'
            '<div class="post-foot"><div class="react"><span>♥ 126</span><span>💬 18</span><span>↗ Share</span></div>'
            '<div class="post-actions"><button class="pill">Save</button>'
            '<button class="pill coral" data-rsvp="You\'re in 🎉" data-cal-title="Games Night + Pizza" '
            'data-cal-date="2026-10-02" data-cal-time="7:00pm" data-cal-place="Students\' Union, Y Plas" '
            'data-cal-color="var(--coral)">I\'m going</button></div></div></article>'
            % (VERIFY, ICONS['cal'], ICONS['pin'], ICONS['people']))

def post_deal():
    return ('<article class="post deal"><span class="accent-edge" style="background:var(--lime)"></span>'
            '<div class="deal-badge">-25%</div>'
            '<div class="post-top"><div class="post-ava" style="background:var(--lime)">☕</div>'
            '<div class="post-meta"><div class="org">Brewhouse Coffee · Cathays</div>'
            '<div class="time">Uni-Verse partner · show your student card</div></div></div>'
            '<h3>25% off everything, all term</h3>'
            '<p>Flash your Uni-Verse card at the till on Crwys Road. Coffee, cake, the lot. No minimum spend.</p>'
            '<div class="post-foot"><div class="react"><span>♥ 340</span><span>🔖 Saved by 1.2k</span></div>'
            '<div class="post-actions"><button class="pill">Directions</button>'
            '<button class="pill primary">Get code</button></div></div></article>')

def post_job():
    return ('<article class="post"><span class="accent-edge" style="background:var(--sky)"></span>'
            '<div class="post-top"><div class="post-ava" style="background:linear-gradient(135deg,var(--sky),var(--lime))">CC</div>'
            '<div class="post-meta"><div class="org">Cardiff University Careers%s</div>'
            '<div class="time">Posted today · links out to the employer</div></div>'
            '<span class="post-cat" style="background:color-mix(in srgb,var(--sky) 16%%,transparent);color:var(--sky)">Professional</span></div>'
            '<h3>Summer Internship — Admiral, Data Analyst</h3>'
            '<p>Paid 10-week placement in Cardiff. Open to 2nd &amp; penultimate-year students. Applications close 14 Nov.</p>'
            '<div class="post-info"><div class="bit">%s £24k pro-rata</div>'
            '<div class="bit">%s Cardiff / Hybrid</div><div class="bit">%s Closes 14 Nov</div></div>'
            '<div class="post-foot"><div class="react"><span>🔖 Save</span><span>↗ Share</span></div>'
            '<div class="post-actions"><button class="pill">Details</button>'
            '<button class="pill primary">Apply on site %s</button></div></div></article>'
            % (VERIFY, ICONS['money'], ICONS['pin'], ICONS['clock'], ICONS['ext']))

def post_workshop():
    return ('<article class="post"><span class="accent-edge" style="background:var(--amber)"></span>'
            '<div class="post-top"><div class="post-ava" style="background:linear-gradient(135deg,var(--amber),var(--coral))">EW</div>'
            '<div class="post-meta"><div class="org">Enactus Cardiff%s</div>'
            '<div class="time">Posted yesterday</div></div>'
            '<span class="post-cat" style="background:color-mix(in srgb,var(--amber) 16%%,transparent);color:var(--amber)">Workshop</span></div>'
            '<h3>CV Clinic + Networking with Local Startups</h3>'
            '<p>Bring your CV, leave with a better one. Founders from 6 Cardiff startups reviewing on the night — plus free drinks.</p>'
            '<div class="post-info"><div class="bit">%s Wed 8 Oct · 5:30pm</div>'
            '<div class="bit">%s sbarc | spark</div></div>'
            '<div class="post-foot"><div class="react"><span>♥ 61</span><span>💬 7</span></div>'
            '<div class="post-actions"><button class="pill">Save</button>'
            '<button class="pill primary" data-rsvp="Reserved ✓" data-cal-title="CV Clinic + Networking" '
            'data-cal-date="2026-10-08" data-cal-time="5:30pm" data-cal-place="sbarc | spark" '
            'data-cal-color="var(--amber)">Reserve spot</button></div></div></article>'
            % (VERIFY, ICONS['cal'], ICONS['pin']))

# ================= PAGE: FEED =================
def build_feed():
    body = ('<div class="content two-col"><div class="feed-col">'
            '<div class="greeting"><div class="hi display">Alright, Findlay <span class="wave">👋</span></div>'
            '<div class="sub">3 events near you this week · 2 new opportunities in your field · Freshers\' Fair is live</div></div>'
            '<div class="chips"><div class="chip on">Everything</div>'
            '<div class="chip"><span class="cd" style="background:var(--coral)"></span>Social</div>'
            '<div class="chip"><span class="cd" style="background:var(--sky)"></span>Professional</div>'
            '<div class="chip"><span class="cd" style="background:var(--lime)"></span>Discounts</div>'
            '<div class="chip"><span class="cd" style="background:var(--amber)"></span>Societies</div>'
            '<div class="chip">Affiliates</div></div>'
            '<div class="feed">%s%s%s%s</div></div>'
            '<aside class="side-col">%s%s%s%s</aside></div>'
            % (post_social(), post_deal(), post_job(), post_workshop(),
               sidebar_ai(), sidebar_journey(), sidebar_week(), sidebar_socs()))
    return page('Feed', 'feed', body)

# ================= PAGE: EVENTS =================
def event_card(emoji, bg, cat, catcol, title, org, verified, date, place, going, cta, iso_date, color,
                ticket_url='', ticket_label='', freshers=False):
    v = VERIFY if verified else ''
    cal_time = date.split(' · ')[-1]
    ticket_html = ''
    if ticket_url:
        ticket_html = ('<a class="ticket-link" href="%s" target="_blank" rel="noopener">%s %s</a>'
                        % (ticket_url, ticket_label, ICONS['ext']))
    freshers_attr = ' data-freshers="1"' if freshers else ''
    return ('<div class="card"%s><div class="card-media" style="background:%s">'
            '<span class="chip-cat">%s</span>'
            '<button class="save-heart">%s</button>'
            '<span class="emoji">%s</span></div>'
            '<div class="card-body"><h3>%s</h3>'
            '<div class="by">%s%s</div>'
            '<div class="card-info"><div class="bit">%s %s</div><div class="bit">%s %s</div></div>%s'
            '<div class="card-foot"><span class="stat">%s going</span>'
            '<button class="pill primary" data-rsvp="Going ✓" data-cal-title="%s" data-cal-date="%s" '
            'data-cal-time="%s" data-cal-place="%s" data-cal-color="%s">%s</button></div></div></div>'
            % (freshers_attr, bg, cat, ICONS['heart'], emoji, title, org, v, ICONS['cal'], date, ICONS['pin'], place,
               ticket_html, going, title, iso_date, cal_time, place, color, cta))

def build_events():
    freshers_cards = [
        event_card('🎉','linear-gradient(135deg,var(--coral),var(--amber))','Freshers Week','', 'Move-In Day &amp; Welcome BBQ','Cardiff University',True,'Mon 21 Sep · 12pm','Halls of Residence','340','I\'m going','2026-09-21','var(--coral)', freshers=True),
        event_card('🌍','linear-gradient(135deg,var(--sky),var(--amber))','Freshers Week','', 'International Students Welcome Social','International Students',True,'Tue 22 Sep · 5pm','Y Plas','210','I\'m going','2026-09-22','var(--sky)', freshers=True),
        event_card('🏃','linear-gradient(135deg,var(--lime),var(--sky))','Freshers Week','', 'Give It A Go: Try a Sport','Athletic Union',True,'Thu 24 Sep · 1pm','Sports Fields, Llanrumney','185','I\'m going','2026-09-24','var(--lime)', freshers=True),
        event_card('🎪','linear-gradient(135deg,var(--amber),var(--coral))','Freshers Week','', 'Freshers Fair','Cardiff SU',True,'Mon 28 Sep · 10am','Y Plas &amp; SU','1.2k','I\'m going','2026-09-28','var(--amber)', freshers=True),
        event_card('🪩','linear-gradient(135deg,var(--sky),var(--lime))','Freshers Week','', 'YOLO: Freshers Special','Cardiff SU',True,'Wed 30 Sep · 9pm','Y Plas','420','I\'m going','2026-09-30','var(--sky)', freshers=True,
                    ticket_url='https://www.ents24.com/cardiff-events/cardiff-university-su-the-great-hall-solus-cf10-the-taf-y-plas', ticket_label='YOLO — get tickets'),
        event_card('🍻','linear-gradient(135deg,var(--coral),var(--lime))','Freshers Week','', 'Freshers Bar Crawl: City Centre','Cardiff SU',True,'Fri 2 Oct · 8pm','City Centre','260','I\'m going','2026-10-02','var(--coral)', freshers=True),
    ]
    cards = [
        event_card('🎮','linear-gradient(135deg,var(--coral),var(--amber))','Social','', 'Games Night + Pizza','Computer Science Society',True,'Thu 2 Oct · 7pm','SU, Y Plas','84','I\'m going','2026-10-02','var(--coral)'),
        event_card('🎤','linear-gradient(135deg,var(--sky),var(--lime))','Social','', 'Open Mic Night','Music Society',True,'Fri 3 Oct · 8pm','The Taf','56','I\'m going','2026-10-03','var(--coral)'),
        event_card('💼','linear-gradient(135deg,var(--amber),var(--coral))','Workshop','', 'CV Clinic + Networking','Enactus Cardiff',True,'Wed 8 Oct · 5:30pm','sbarc | spark','40','Reserve','2026-10-08','var(--amber)'),
        event_card('🧗','linear-gradient(135deg,var(--lime),var(--sky))','Sport','', 'Give It A Go: Bouldering','Mountaineering Club',True,'Sat 11 Oct · 2pm','Boulders CDF','22','I\'m going','2026-10-11','var(--lime)'),
        event_card('🎬','linear-gradient(135deg,var(--coral),var(--sky))','Social','', 'Film Night: Cult Classics','Film Society',True,'Sun 12 Oct · 6pm','SU Cinema','70','I\'m going','2026-10-12','var(--coral)'),
        event_card('🌍','linear-gradient(135deg,var(--sky),var(--amber))','Talk','', 'Careers in Sustainability','Careers Service',True,'Tue 14 Oct · 1pm','Glamorgan Building','35','Reserve','2026-10-14','var(--sky)'),
    ]
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">What\'s on</div>'
            '<h1>Events at Cardiff</h1>'
            '<div class="sub">Every society and official event in one place — including Freshers Week (28 Sep – 2 Oct). '
            'Filter by what you\'re into — all hosted by verified organisations.</div></div>'
            '<div class="chips" data-filter-grid="eventsGrid"><div class="chip on">All</div>'
            '<div class="chip freshers-chip">🎉 Freshers Week</div>'
            '<div class="chip">Social</div>'
            '<div class="chip">Professional</div><div class="chip">Sport</div><div class="chip">Talks</div>'
            '<div class="chip">This week</div><div class="chip">Free</div></div>'
            '<div class="grid g3" id="eventsGrid">%s</div></div>' % ''.join(freshers_cards + cards))
    return page('Events', 'events', body)

# ================= PAGE: BUCS =================
def build_bucs():
    # Real fixtures — Cardiff University Men's BUCS Super Rugby, 2026-27 season (bucs.org.uk)
    fixtures = [
        event_card('🏉', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Rugby', '',
                    'Cardiff vs Hartpury', 'Round 1 · Home · BUCS Super Rugby', True,
                    'Wed 23 Sep · 2pm', 'Cardiff University Sports Fields, Llanrumney', '54', 'I\'m going',
                    '2026-09-23', 'var(--coral)',
                    'https://www.bucs.org.uk/tickets.html', 'BUCS tickets'),
        event_card('🏉', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Rugby', '',
                    'Durham vs Cardiff', 'Round 2 · Away · BUCS Super Rugby', True,
                    'Wed 30 Sep · 2pm', 'Durham', '11', 'I\'m going',
                    '2026-09-30', 'var(--coral)',
                    'https://www.bucs.org.uk/tickets.html', 'BUCS tickets'),
        event_card('🏆', 'linear-gradient(135deg,var(--amber),var(--coral))', 'Derby', '',
                    'Cardiff vs Cardiff Met', 'Round 3 · Home · The Cardiff Clash', True,
                    'Wed 7 Oct · 7:30pm', 'Cardiff Arms Park', '340', 'I\'m going',
                    '2026-10-07', 'var(--coral)',
                    'https://www.bucs.org.uk/tickets.html', 'The Cardiff Clash — get tickets'),
        event_card('🏉', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Rugby', '',
                    'Brunel vs Cardiff', 'Round 4 · Away · BUCS Super Rugby', True,
                    'Wed 14 Oct · 2pm', 'Brunel', '9', 'I\'m going',
                    '2026-10-14', 'var(--coral)',
                    'https://www.bucs.org.uk/tickets.html', 'BUCS tickets'),
        event_card('🏉', 'linear-gradient(135deg,var(--coral),var(--sky))', 'Rugby', '',
                    'Cardiff vs Nottingham', 'Round 5 · Home · BUCS Super Rugby', True,
                    'Wed 28 Oct · 2pm', 'Cardiff University Sports Fields, Llanrumney', '61', 'I\'m going',
                    '2026-10-28', 'var(--coral)',
                    'https://www.bucs.org.uk/tickets.html', 'BUCS tickets'),
        event_card('🏉', 'linear-gradient(135deg,var(--sky),var(--amber))', 'Rugby', '',
                    'Exeter vs Cardiff', 'Round 6 · Away · BUCS Super Rugby', True,
                    'Wed 4 Nov · 2pm', 'Exeter', '14', 'I\'m going',
                    '2026-11-04', 'var(--coral)',
                    'https://www.bucs.org.uk/tickets.html', 'BUCS tickets'),
    ]
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Cardiff University sport</div>'
            '<h1>BUCS fixtures</h1>'
            '<div class="sub">British Universities &amp; Colleges Sport — the competition Cardiff University\'s 100+ student '
            'teams play in. This is Cardiff University\'s own fixtures, not Cardiff Met\'s. Headline fixtures below are '
            'Men\'s BUCS Super Rugby; see the '
            '<a href="https://www.cardiffstudents.com/activities/au/bucs-fixtures/" target="_blank" rel="noopener" '
            'style="color:var(--lime);font-weight:700">Athletic Union\'s full fixture list ↗</a> for all 34 sports clubs.</div></div>'
            '<div class="chips"><div class="chip on">All</div><div class="chip">Home</div>'
            '<div class="chip">Away</div><div class="chip">Rugby</div></div>'
            '<div class="grid g3">%s</div></div>' % ''.join(fixtures))
    return page('BUCS', 'bucs', body)

# ================= PAGE: OPPORTUNITIES =================
def opp_row(logo, bg, role, kind, org, verified, tags, closes):
    v = VERIFY if verified else ''
    tagbits = ''.join('<div class="bit">%s</div>' % t for t in tags)
    return ('<article class="post"><span class="accent-edge" style="background:var(--sky)"></span>'
            '<div class="post-top"><div class="post-ava" style="background:%s">%s</div>'
            '<div class="post-meta"><div class="org">%s%s</div>'
            '<div class="time">%s · links out to employer</div></div>'
            '<span class="post-cat" style="background:color-mix(in srgb,var(--sky) 16%%,transparent);color:var(--sky)">%s</span></div>'
            '<h3>%s</h3><div class="post-info">%s</div>'
            '<div class="post-foot"><div class="react"><span>🔖 Save</span><span>↗ Share</span></div>'
            '<div class="post-actions"><button class="pill">Details</button>'
            '<button class="pill primary">Apply on site %s</button></div></div></article>'
            % (bg, logo, org, v, closes, kind, role, tagbits, ICONS['ext']))

def build_opps():
    rows = [
        opp_row('AD','linear-gradient(135deg,var(--sky),var(--lime))','Summer Internship — Data Analyst','Internship','Admiral (via Cardiff Careers)',True,
                ['%s £24k pro-rata' % ICONS['money'], '%s Cardiff / Hybrid' % ICONS['pin'], '%s Closes 14 Nov' % ICONS['clock']],'Posted today'),
        opp_row('GT','linear-gradient(135deg,var(--coral),var(--amber))','Graduate Scheme — Software Engineer','Graduate','GoCompare',True,
                ['%s £30k' % ICONS['money'], '%s Newport' % ICONS['pin'], '%s Closes 1 Dec' % ICONS['clock']],'Posted 2d ago'),
        opp_row('PT','linear-gradient(135deg,var(--amber),var(--sky))','Part-time — Student Brand Ambassador','Part-time','Uni-Verse',True,
                ['%s £12/hr' % ICONS['money'], '%s On campus' % ICONS['pin'], '%s Rolling' % ICONS['clock']],'Posted 3d ago'),
        opp_row('RS','linear-gradient(135deg,var(--lime),var(--coral))','Placement Year — Marketing Assistant','Placement','Principality',True,
                ['%s Paid' % ICONS['money'], '%s Cardiff' % ICONS['pin'], '%s Closes 20 Nov' % ICONS['clock']],'Posted 5d ago'),
    ]
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Don\'t miss out</div>'
            '<h1>Opportunities</h1>'
            '<div class="sub">Internships, placements, grad schemes and part-time work — pulled together from Cardiff Careers and partner employers. Every listing links straight back to the source to apply.</div></div>'
            '<div class="chips"><div class="chip on">All</div><div class="chip">Internships</div>'
            '<div class="chip">Placements</div><div class="chip">Graduate</div><div class="chip">Part-time</div>'
            '<div class="chip">Volunteering</div></div>'
            '<div class="feed">%s</div></div>' % ''.join(rows))
    return page('Opportunities', 'opps', body)

# ================= PAGE: DISCOUNTS =================
def deal_card(emoji, bg, cat, name, place, desc, pct, cta):
    return ('<div class="card"><div class="card-media" style="background:%s">'
            '<span class="chip-cat">%s</span>'
            '<button class="save-heart">%s</button>'
            '<span class="emoji">%s</span><span class="deal-tag">%s</span></div>'
            '<div class="card-body"><h3>%s</h3>'
            '<div class="by">%s · Uni-Verse partner</div>'
            '<p>%s</p>'
            '<div class="card-foot"><span class="stat">Show your card</span>'
            '<button class="pill primary">%s</button></div></div></div>'
            % (bg, cat, ICONS['heart'], emoji, pct, name, place, desc, cta))

def build_discounts():
    cards = [
        deal_card('☕','linear-gradient(135deg,var(--lime),var(--sky))','Food & Drink','Brewhouse Coffee','Cathays','25% off everything, all term. No minimum spend.','-25%','Get code'),
        deal_card('🍔','linear-gradient(135deg,var(--coral),var(--amber))','Food & Drink','Got Beef','City Centre','Free side with any burger, Mon–Thu.','FREE','Get code'),
        deal_card('✂️','linear-gradient(135deg,var(--sky),var(--lime))','Grooming','Sharp Cuts','Roath','£5 off student cuts, any day.','-£5','Get code'),
        deal_card('🏋️','linear-gradient(135deg,var(--amber),var(--coral))','Fitness','Pulse Gym','Cathays','No joining fee + first month half price.','-50%','Get code'),
        deal_card('📚','linear-gradient(135deg,var(--lime),var(--coral))','Study','Inkwell Books','City Centre','15% off all books and stationery.','-15%','Get code'),
        deal_card('🍕','linear-gradient(135deg,var(--coral),var(--sky))','Food & Drink','Dough Co','Cathays','2-for-1 pizzas every Tuesday.','2FOR1','Get code'),
    ]
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Your card, your savings</div>'
            '<h1>Student discounts</h1>'
            '<div class="sub">Deals from local Cardiff businesses, free with your Uni-Verse account. Show your card in-store or grab a code.</div></div>'
            '<div class="chips"><div class="chip on">All</div><div class="chip">Food &amp; Drink</div>'
            '<div class="chip">Fitness</div><div class="chip">Grooming</div><div class="chip">Study</div>'
            '<div class="chip">Nights out</div></div>'
            '<div class="grid g3">%s</div></div>' % ''.join(cards))
    return page('Discounts', 'discounts', body)

# ================= PAGE: SOCIETIES =================
def soc_card(emoji, bg, name, members, desc, slug):
    return ('<div class="card"><div class="card-media" style="background:%s">'
            '<span class="emoji">%s</span></div>'
            '<div class="card-body"><h3>%s%s</h3>'
            '<div class="by">%s members</div>'
            '<p>%s</p>'
            '<a class="ticket-link" href="%s" target="_blank" rel="noopener">How to join — Cardiff SU %s</a>'
            '<div class="card-foot"><span class="stat">Active this week</span>'
            '<div class="post-actions">'
            '<button class="soc-join" data-society="%s">Join</button>'
            '<a class="soc-view" href="society-%s.html" hidden>View society %s</a>'
            '</div></div></div></div>'
            % (bg, emoji, name, VERIFY, members, desc, SU_SOCIETIES_URL, ICONS['ext'], slug, slug, ICONS['arrow']))

def build_societies():
    cards = [
        soc_card('🎬','linear-gradient(135deg,var(--lime),var(--sky))','Film Society','1,240','Weekly screenings, cult classics and trips to the cinema. All welcome.','film'),
        soc_card('🥾','linear-gradient(135deg,var(--coral),var(--amber))','Hiking & Mountaineering','860','Weekend adventures across the Brecon Beacons and beyond. Kit provided.','hiking'),
        soc_card('💼','linear-gradient(135deg,var(--sky),var(--lime))','Entrepreneurs Society','1,510','Talks, pitch nights and startup socials. Build something at uni.','entrepreneurs'),
        soc_card('🎭','linear-gradient(135deg,var(--amber),var(--coral))','Drama Society','740','Termly productions, workshops and open auditions. No experience needed.','drama'),
        soc_card('⚽','linear-gradient(135deg,var(--lime),var(--coral))','Football Club','2,100','Teams for every level plus casual kickabouts. Give it a go.','football'),
        soc_card('🌍','linear-gradient(135deg,var(--sky),var(--amber))','International Students','1,880','Socials, trips and a friendly community away from home.','international'),
        soc_card('🏐','linear-gradient(135deg,var(--sky),var(--lime))','Netball Club','980','BUCS netball across every level, from social to competitive.','netball'),
        soc_card('🎸','linear-gradient(135deg,var(--coral),var(--sky))','Music Society','690','Open mic nights, jam sessions and a termly showcase gig.','music'),
        soc_card('🎙️','linear-gradient(135deg,var(--amber),var(--sky))','Debate Society','410','Weekly debates, national competitions and public speaking practice.','debate'),
        soc_card('🎗️','linear-gradient(135deg,var(--lime),var(--amber))','RAG Society','560','Fundraising challenges and charity events all year round.','rag'),
        soc_card('📷','linear-gradient(135deg,var(--sky),var(--coral))','Photography Society','730','Shoots around Cardiff, darkroom access and a termly exhibition.','photography'),
        soc_card('🏳️‍🌈','linear-gradient(135deg,var(--coral),var(--lime))','Pride Society','890','A safe, social space for LGBTQ+ students and allies.','pride'),
    ]
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Find your people</div>'
            '<h1>Societies</h1>'
            '<div class="sub">300+ Cardiff societies, all in one place. Join in a tap here, or head to the Students\' Union — the official place to join — for membership and the Guild of Societies. Hit "Join" and once the committee accepts you, you\'re into the society\'s own space — chat, events, timetable and kit.</div></div>'
            '<div class="chips"><div class="chip on">All</div><div class="chip">Sport</div>'
            '<div class="chip">Arts</div><div class="chip">Academic</div><div class="chip">Culture</div>'
            '<div class="chip">Volunteering</div><div class="chip">Social</div></div>'
            '<div class="grid g3">%s</div></div>' % ''.join(cards))
    return page('Societies', 'societies', body)

# ---------------- society detail page (chat, events, timetable, kit) ----------------
def society_chat_msg(initials, bg, name, text, time):
    return ('<div class="soc-msg"><div class="soc-msg-ava" style="background:%s">%s</div>'
            '<div class="soc-msg-body"><div class="soc-msg-head"><span class="soc-msg-name">%s</span>'
            '<span class="soc-msg-time">%s</span></div><div class="soc-msg-text">%s</div></div></div>'
            % (bg, initials, name, time, text))

def society_event_row(d, m, title, meta, color, iso_date, time_str, place):
    return ('<div class="up-item"><div class="up-date"><div class="d">%s</div><div class="m">%s</div></div>'
            '<div class="up-body"><div class="t">%s</div><div class="meta"><span class="k" style="background:%s"></span>%s</div>'
            '<button class="pill primary up-rsvp" data-rsvp="Going ✓" data-cal-title="%s" data-cal-date="%s" '
            'data-cal-time="%s" data-cal-place="%s" data-cal-color="%s">I\'m attending</button>'
            '</div></div>'
            % (d, m, title, color, meta, title, iso_date, time_str, place, color))

def tt_row(day_label, activity, meta):
    return ('<div class="tt-row"><div class="tt-day">%s</div>'
            '<div class="tt-info"><div class="t">%s</div><div class="m">%s</div></div></div>'
            % (day_label, activity, meta))

def build_society_page(slug, name, emoji, bg, members, tagline, chat_msgs, events, timetable, kit_label):
    kit_url = 'https://kit.uni-verse.app/' + slug
    header = ('<div class="soc-page-head"><div class="soc-page-ava" style="background:%s">%s</div>'
              '<div><h1 style="margin-bottom:4px">%s%s</h1>'
              '<div class="sub">%s members · %s</div></div></div>'
              % (bg, emoji, name, VERIFY, members, tagline))
    chat_widget = ('<div class="widget"><div class="widget-head"><h3>Society chat</h3>'
                   '<span class="mono-eyebrow">%s members</span></div>'
                   '<div class="soc-chat">%s</div>'
                   '<div class="soc-chat-input"><input type="text" class="soc-chat-field" placeholder="Message the group…">'
                   '<button class="soc-chat-send">%s</button></div></div>'
                   % (members, ''.join(chat_msgs), ICONS['send']))
    timetable_widget = ('<div class="widget"><div class="widget-head"><h3>Weekly timetable</h3></div>'
                        '<div class="timetable">%s</div></div>' % ''.join(timetable))
    events_widget = ('<div class="widget"><div class="widget-head"><h3>Upcoming events</h3>'
                     '<a href="events.html">All events →</a></div><div class="up">%s</div></div>' % ''.join(events))
    kit_widget = ('<div class="widget kit-banner"><div><h3 style="margin-bottom:4px">%s</h3>'
                  '<div style="color:var(--muted);font-size:.85rem">Official society merch — order online, collect at the next social.</div></div>'
                  '<a class="pill primary" href="%s" target="_blank" rel="noopener">Get the kit %s</a></div>'
                  % (kit_label, kit_url, ICONS['ext']))
    left = '<div class="feed-col">' + chat_widget + timetable_widget + '</div>'
    right = '<aside class="side-col">' + events_widget + kit_widget + '</aside>'
    body = '<div class="content">' + header + '<div class="two-col">' + left + right + '</div></div>'
    return page(name, 'societies', body)

SOCIETY_PAGES = {
    'society-film.html': build_society_page(
        'film', 'Film Society', '🎬', 'linear-gradient(135deg,var(--lime),var(--sky))', '1,240',
        'Weekly screenings, cult classics and trips to the cinema.',
        [society_chat_msg('EL', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Ella',
                           "Anyone free for the classics screening Thursday? We're doing Alien 👽", '2h ago'),
         society_chat_msg('DP', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Dan',
                           'In! Bringing snacks this time 🍿', '1h ago'),
         society_chat_msg('SR', 'linear-gradient(135deg,var(--amber),var(--coral))', 'Sam',
                           "Can we vote on next term's picks in here?", '32m ago')],
        [society_event_row('12', 'Oct', 'Film Night: Cult Classics', 'Sun · 6:00pm · SU Cinema', 'var(--coral)',
                            '2026-10-12', '6:00pm', 'SU Cinema'),
         society_event_row('16', 'Oct', 'Pizza & Pitch Night', 'Thu · 7:00pm · Y Plas', 'var(--amber)',
                            '2026-10-16', '7:00pm', 'Y Plas')],
        [tt_row('WEEKLY', 'Screening night', 'Thursdays · 7:00pm · SU Cinema'),
         tt_row('MONTHLY', 'Committee open meeting', 'First Sunday · Common Room, SU')],
        'Film Society hoodie & tote'),

    'society-hiking.html': build_society_page(
        'hiking', 'Hiking & Mountaineering', '🥾', 'linear-gradient(135deg,var(--coral),var(--amber))', '860',
        'Weekend adventures across the Brecon Beacons and beyond.',
        [society_chat_msg('RH', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Rhys',
                           "Weather looks decent for Sunday's Brecon walk ⛰️", '3h ago'),
         society_chat_msg('BC', 'linear-gradient(135deg,var(--coral),var(--sky))', 'Beca',
                           'Kit check — anyone need to borrow boots?', '1h ago'),
         society_chat_msg('OW', 'linear-gradient(135deg,var(--amber),var(--lime))', 'Owen',
                           'Car share sign-up sheet is in the group doc, fill it in pls', '20m ago')],
        [society_event_row('10', 'Oct', 'Weekend Hike: Brecon Beacons', 'Sat · 8:00am meet · SU forecourt', 'var(--lime)',
                            '2026-10-10', '8:00am', 'SU forecourt'),
         society_event_row('11', 'Oct', 'Give It A Go: Bouldering', 'Sun · 2:00pm · Boulders CDF', 'var(--sky)',
                            '2026-10-11', '2:00pm', 'Boulders CDF')],
        [tt_row('WEEKLY', 'Kit & trip planning', 'Tuesdays · 6:00pm · Committee Room'),
         tt_row('FORTNIGHTLY', 'Day hike (location varies)', 'Sundays · meet SU forecourt')],
        'Hiking & Mountaineering fleece & buff'),

    'society-entrepreneurs.html': build_society_page(
        'entrepreneurs', 'Entrepreneurs Society', '💼', 'linear-gradient(135deg,var(--sky),var(--lime))', '1,510',
        'Talks, pitch nights and startup socials.',
        [society_chat_msg('PR', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Priya',
                           'Pitch night applications close Friday, get yours in!', '4h ago'),
         society_chat_msg('CJ', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Callum',
                           'Guest speaker from a Cardiff startup this week, should be good', '2h ago'),
         society_chat_msg('NW', 'linear-gradient(135deg,var(--amber),var(--coral))', 'Nia',
                           'Anyone want to team up for the case study competition?', '45m ago')],
        [society_event_row('08', 'Oct', 'CV Clinic + Networking', 'Wed · 5:30pm · sbarc | spark', 'var(--amber)',
                            '2026-10-08', '5:30pm', 'sbarc | spark'),
         society_event_row('23', 'Oct', 'Pitch Night: Term 1 Final', 'Thu · 6:30pm · sbarc | spark', 'var(--sky)',
                            '2026-10-23', '6:30pm', 'sbarc | spark')],
        [tt_row('WEEKLY', 'Speaker series', 'Wednesdays · 6:00pm · sbarc | spark'),
         tt_row('MONTHLY', 'Pitch practice', 'Last Friday · Business School')],
        'Entrepreneurs Society hoodie'),

    'society-drama.html': build_society_page(
        'drama', 'Drama Society', '🎭', 'linear-gradient(135deg,var(--amber),var(--coral))', '740',
        'Termly productions, workshops and open auditions.',
        [society_chat_msg('FR', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Freya',
                           'Audition sign-ups open now for the winter show!', '5h ago'),
         society_chat_msg('JB', 'linear-gradient(135deg,var(--coral),var(--sky))', 'Josh',
                           'Rehearsal moved to Studio 2 tonight, same time', '2h ago'),
         society_chat_msg('AK', 'linear-gradient(135deg,var(--amber),var(--lime))', 'Amelia',
                           'Does anyone have a spare script copy going?', '18m ago')],
        [society_event_row('06', 'Oct', 'Open Auditions: Winter Production', 'Mon · 6:00pm · Bute Studio 2', 'var(--coral)',
                            '2026-10-06', '6:00pm', 'Bute Studio 2'),
         society_event_row('15', 'Oct', 'Improv Workshop', 'Wed · 7:00pm · Bute Studio 1', 'var(--amber)',
                            '2026-10-15', '7:00pm', 'Bute Studio 1')],
        [tt_row('WEEKLY', 'Rehearsals', 'Mondays · 6:00pm · Bute Building, Studio 2'),
         tt_row('WEEKLY', 'Improv & games night', 'Wednesdays · 7:00pm · Studio 1')],
        'Drama Society tee'),

    'society-football.html': build_society_page(
        'football', 'Football Club', '⚽', 'linear-gradient(135deg,var(--lime),var(--coral))', '2,100',
        'Teams for every level plus casual kickabouts.',
        [society_chat_msg('LM', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Liam',
                           "Match report from Saturday's win up on the group now 🔥", '6h ago'),
         society_chat_msg('FF', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Ffion',
                           'Training moved indoors this week — sports hall', '3h ago'),
         society_chat_msg('CH', 'linear-gradient(135deg,var(--amber),var(--coral))', 'Charlie',
                           "Who's in for Wednesday's fixture?", '40m ago')],
        [society_event_row('07', 'Oct', 'BUCS Football: Cardiff vs Bristol', 'Wed · 2:00pm · Sports Fields, Llanrumney', 'var(--lime)',
                            '2026-10-07', '2:00pm', 'Sports Fields, Llanrumney'),
         society_event_row('11', 'Oct', 'Casual Kickabout', 'Sun · 3:00pm · Talybont Playing Fields', 'var(--sky)',
                            '2026-10-11', '3:00pm', 'Talybont Playing Fields')],
        [tt_row('WEEKLY', 'Training', 'Tuesdays & Thursdays · 7:00pm · Sports Fields, Llanrumney'),
         tt_row('WEEKLY', 'Matchday (BUCS)', 'Saturdays · venue varies')],
        'Football Club home & away kit'),

    'society-international.html': build_society_page(
        'international', 'International Students', '🌍', 'linear-gradient(135deg,var(--sky),var(--amber))', '1,880',
        'Socials, trips and a friendly community away from home.',
        [society_chat_msg('YK', 'linear-gradient(135deg,var(--coral),var(--lime))', 'Yuki',
                           'Potluck dinner this Friday, bring a dish from home!', '4h ago'),
         society_chat_msg('MR', 'linear-gradient(135deg,var(--sky),var(--amber))', 'Marco',
                           'Anyone going on the Bath day trip next month?', '1h ago'),
         society_chat_msg('LY', 'linear-gradient(135deg,var(--amber),var(--sky))', 'Layla',
                           'Coffee morning tomorrow 10am, all welcome ☕', '25m ago')],
        [society_event_row('10', 'Oct', 'Welcome Potluck Dinner', 'Fri · 6:00pm · Y Plas', 'var(--coral)',
                            '2026-10-10', '6:00pm', 'Y Plas'),
         society_event_row('18', 'Oct', 'Day Trip: Bath', 'Sat · 9:00am meet · SU forecourt', 'var(--sky)',
                            '2026-10-18', '9:00am', 'SU forecourt')],
        [tt_row('WEEKLY', 'Coffee morning', 'Wednesdays · 10:00am · SU Café'),
         tt_row('MONTHLY', 'Potluck social', 'First Friday · Y Plas')],
        'International Students Society scarf'),

    'society-netball.html': build_society_page(
        'netball', 'Netball Club', '🏐', 'linear-gradient(135deg,var(--sky),var(--lime))', '980',
        'BUCS netball across every level, from social to competitive.',
        [society_chat_msg('MG', 'linear-gradient(135deg,var(--coral),var(--sky))', 'Meg',
                           'Great win at States on Saturday, well played everyone 🏐', '3h ago'),
         society_chat_msg('AS', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Ash',
                           'Socials training moved to 6pm this week', '1h ago'),
         society_chat_msg('RB', 'linear-gradient(135deg,var(--amber),var(--coral))', 'Ruby',
                           "Who needs a new bib, mine's falling apart 😂", '20m ago')],
        [society_event_row('07', 'Oct', 'BUCS Netball: Cardiff vs Swansea', 'Wed · 2:00pm · Sports Hall', 'var(--sky)',
                            '2026-10-07', '2:00pm', 'Sports Hall'),
         society_event_row('18', 'Oct', 'Give It A Go: Social Netball', 'Sun · 11:00am · Talybont Sports Centre', 'var(--lime)',
                            '2026-10-18', '11:00am', 'Talybont Sports Centre')],
        [tt_row('WEEKLY', 'Training', 'Tuesdays · 7:00pm · Sports Hall'),
         tt_row('WEEKLY', 'Matchday (BUCS)', 'Wednesdays · venue varies')],
        'Netball Club dress & bib set'),

    'society-music.html': build_society_page(
        'music', 'Music Society', '🎸', 'linear-gradient(135deg,var(--coral),var(--sky))', '690',
        'Open mic nights, jam sessions and a termly showcase gig.',
        [society_chat_msg('TH', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Theo',
                           'Open mic sign-up sheet is live, get your slot before it fills!', '5h ago'),
         society_chat_msg('IS', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Isla',
                           'Anyone got a spare guitar lead I can borrow Thursday?', '2h ago'),
         society_chat_msg('KY', 'linear-gradient(135deg,var(--amber),var(--sky))', 'Kai',
                           'Showcase gig lineup dropping this week 🎤', '30m ago')],
        [society_event_row('03', 'Oct', 'Open Mic Night', 'Fri · 8:00pm · The Taf', 'var(--coral)',
                            '2026-10-03', '8:00pm', 'The Taf'),
         society_event_row('24', 'Oct', 'Termly Showcase Gig', 'Fri · 7:30pm · Y Plas', 'var(--sky)',
                            '2026-10-24', '7:30pm', 'Y Plas')],
        [tt_row('WEEKLY', 'Jam session', 'Mondays · 7:00pm · Music Practice Rooms'),
         tt_row('TERMLY', 'Showcase gig', 'Last Friday of term · Y Plas')],
        'Music Society tee & tote'),

    'society-debate.html': build_society_page(
        'debate', 'Debate Society', '🎙️', 'linear-gradient(135deg,var(--amber),var(--sky))', '410',
        'Weekly debates, national competitions and public speaking practice.',
        [society_chat_msg('ZR', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Zara',
                           "This week's motion: 'This House Would Abolish Exams' 👀", '4h ago'),
         society_chat_msg('BN', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Ben',
                           'Novice training session was great, thanks for running it', '2h ago'),
         society_chat_msg('IR', 'linear-gradient(135deg,var(--amber),var(--coral))', 'Iris',
                           'Signed us up for the Cardiff Open, who\'s in?', '15m ago')],
        [society_event_row('06', 'Oct', 'Weekly Debate Night', 'Tue · 7:00pm · Committee Room, SU', 'var(--amber)',
                            '2026-10-06', '7:00pm', 'Committee Room, SU'),
         society_event_row('20', 'Oct', 'Novice Training Workshop', 'Tue · 6:00pm · Committee Room, SU', 'var(--sky)',
                            '2026-10-20', '6:00pm', 'Committee Room, SU')],
        [tt_row('WEEKLY', 'Debate night', 'Tuesdays · 7:00pm · Committee Room, SU'),
         tt_row('MONTHLY', 'Novice training', 'First Tuesday · Committee Room, SU')],
        'Debate Society pin & tote'),

    'society-rag.html': build_society_page(
        'rag', 'RAG Society', '🎗️', 'linear-gradient(135deg,var(--lime),var(--amber))', '560',
        'Fundraising challenges and charity events all year round.',
        [society_chat_msg('HL', 'linear-gradient(135deg,var(--coral),var(--lime))', 'Holly',
                           'Skydive sign-ups close Friday — last few spots!', '3h ago'),
         society_chat_msg('FN', 'linear-gradient(135deg,var(--amber),var(--sky))', 'Fin',
                           'Bake sale raised £340 today, amazing work everyone 🎉', '1h ago'),
         society_chat_msg('ZO', 'linear-gradient(135deg,var(--sky),var(--coral))', 'Zoe',
                           'Can someone cover the collection bucket Saturday morning?', '25m ago')],
        [society_event_row('14', 'Oct', 'Charity Bake Sale', 'Wed · 11:00am · SU Concourse', 'var(--lime)',
                            '2026-10-14', '11:00am', 'SU Concourse'),
         society_event_row('24', 'Oct', 'RAG Skydive Challenge', 'Sat · 9:00am · Airfield, Swansea', 'var(--amber)',
                            '2026-10-24', '9:00am', 'Airfield, Swansea')],
        [tt_row('WEEKLY', 'Committee meeting', 'Thursdays · 6:00pm · Committee Room, SU'),
         tt_row('MONTHLY', 'Big fundraiser', 'Last Saturday · venue varies')],
        'RAG Society charity tee'),

    'society-photography.html': build_society_page(
        'photography', 'Photography Society', '📷', 'linear-gradient(135deg,var(--sky),var(--coral))', '730',
        'Shoots around Cardiff, darkroom access and a termly exhibition.',
        [society_chat_msg('NH', 'linear-gradient(135deg,var(--coral),var(--sky))', 'Noah',
                           "Sunset shoot at Cardiff Bay this Friday, bring a tripod if you've got one", '4h ago'),
         society_chat_msg('MA', 'linear-gradient(135deg,var(--lime),var(--coral))', 'Mia',
                           "Darkroom's free Tuesday afternoon if anyone wants to develop film", '2h ago'),
         society_chat_msg('LO', 'linear-gradient(135deg,var(--amber),var(--sky))', 'Leo',
                           'Exhibition submissions close end of the month!', '40m ago')],
        [society_event_row('10', 'Oct', 'Sunset Shoot: Cardiff Bay', 'Fri · 6:00pm · Cardiff Bay Barrage', 'var(--sky)',
                            '2026-10-10', '6:00pm', 'Cardiff Bay Barrage'),
         society_event_row('30', 'Oct', 'Termly Exhibition Night', 'Fri · 6:30pm · Bute Building Foyer', 'var(--coral)',
                            '2026-10-30', '6:30pm', 'Bute Building Foyer')],
        [tt_row('WEEKLY', 'Darkroom access', 'Tuesdays · Bute Building'),
         tt_row('MONTHLY', 'Society shoot', 'First Friday · location varies')],
        'Photography Society tote & lens cloth'),

    'society-pride.html': build_society_page(
        'pride', 'Pride Society', '🏳️‍🌈', 'linear-gradient(135deg,var(--coral),var(--lime))', '890',
        'A safe, social space for LGBTQ+ students and allies.',
        [society_chat_msg('RO', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Robin',
                           'Coffee & chat this week is at the usual spot, 2pm', '3h ago'),
         society_chat_msg('SA', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Sasha',
                           'Pride Ball tickets go on sale Monday, mark your calendars!', '1h ago'),
         society_chat_msg('JM', 'linear-gradient(135deg,var(--lime),var(--coral))', 'Jamie',
                           'New badges just arrived, come grab one at the social', '15m ago')],
        [society_event_row('14', 'Oct', 'Coffee & Chat', 'Wed · 2:00pm · SU Café', 'var(--coral)',
                            '2026-10-14', '2:00pm', 'SU Café'),
         society_event_row('21', 'Nov', 'Pride Ball', 'Fri · 7:00pm · Great Hall', 'var(--lime)',
                            '2026-11-21', '7:00pm', 'Great Hall')],
        [tt_row('WEEKLY', 'Coffee & chat', 'Wednesdays · 2:00pm · SU Café'),
         tt_row('MONTHLY', 'Social night', 'Third Friday · Y Plas')],
        'Pride Society badge & flag'),
}

# ================= PAGE: FLATMATES =================
def flat_card(emoji, bg, area, title, poster, desc, price, available, spots, key):
    return ('<div class="card"><div class="card-media" style="background:%s">'
            '<span class="chip-cat">%s</span>'
            '<button class="save-heart">%s</button>'
            '<span class="emoji">%s</span></div>'
            '<div class="card-body"><h3>%s</h3>'
            '<div class="by">%s</div>'
            '<p>%s</p>'
            '<div class="card-info"><div class="bit">%s %s pcm</div><div class="bit">%s Available %s</div></div>'
            '<div class="card-foot"><span class="stat">%s</span>'
            '<button class="pill primary" data-rsvp="Message sent ✓" data-rsvp-key="flatmate-%s">Message</button></div></div></div>'
            % (bg, area, ICONS['heart'], emoji, title, poster, desc, ICONS['money'], price, ICONS['cal'],
               available, spots, key))

def build_flatmates():
    post_cta = ('<div class="widget" style="display:flex;align-items:center;justify-content:space-between;'
                'gap:16px;flex-wrap:wrap;margin-bottom:22px">'
                '<div><h3 style="margin-bottom:4px">Got a spare room?</h3>'
                '<div style="color:var(--muted);font-size:.85rem">Post your house — takes two minutes, free for students.</div></div>'
                '<button class="pill primary">Post your room %s</button></div>' % ICONS['arrow'])
    cards = [
        flat_card('🏠', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Cathays',
                   '4-bed house · 1 room free', 'Posted by Priya · 2nd year Biosciences',
                   'Three of us are staying on for 2nd year — chill house, 5 min walk to the Bute Building. Looking for a 4th who\'s tidy-ish and up for a Sunday roast now and then.',
                   '£450', 'July', '1 spot left', 'priya'),
        flat_card('🏡', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Roath',
                   '5-bed house · 2 rooms free', 'Posted by Jack · 3rd year Economics',
                   'Big Victorian terrace off Albany Road with a proper kitchen for house dinners. Two of our housemates are off on placement year so we\'ve got two rooms going.',
                   '£480–520', 'September', '2 spots left', 'jack'),
        flat_card('🏘️', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Heath',
                   '3-bed house · 1 room free', 'Posted by Sara · 2nd year Psychology',
                   'Quiet street near Heath Park, good if you actually want to get work done. Two of us left in the house, looking for someone chilled.',
                   '£520', 'September', '1 spot left', 'sara'),
        flat_card('🚲', 'linear-gradient(135deg,var(--amber),var(--coral))', 'Gabalfa',
                   '4-bed house · 1 room free', 'Posted by Tom · 2nd year Sport Science',
                   'Sporty house, 10 min cycle to campus, garden for BBQs. One of the lads is off on a year abroad so his room\'s free.',
                   '£420', 'September', '1 spot left', 'tom'),
        flat_card('🎨', 'linear-gradient(135deg,var(--lime),var(--coral))', 'Canton',
                   '3-bed house · 1 room free', 'Posted by Elin · 3rd year Architecture',
                   'Right by Chapter Arts Centre — good if you\'re into film or art. Laid-back house, we mostly do our own thing.',
                   '£460', 'September', '1 spot left', 'elin'),
        flat_card('🌊', 'linear-gradient(135deg,var(--sky),var(--amber))', 'Cardiff Bay',
                   '4-bed house · 1 room free', 'Posted by Liam · 3rd year Law',
                   'Quieter end of town — 20 min walk or one bus to campus. Good if you want some distance from the Cathays chaos.',
                   '£500–540', 'September', '1 spot left', 'liam'),
    ]
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Student housing</div>'
            '<h1>Find a housemate</h1>'
            '<div class="sub">Second and third years with a spare room, posted by the students who live there — not an agency, no fees. '
            'Browse what\'s going, or list your own room.</div></div>'
            '<div class="chips"><div class="chip on">All</div><div class="chip">Cathays</div>'
            '<div class="chip">Roath</div><div class="chip">Heath</div><div class="chip">Gabalfa</div>'
            '<div class="chip">Canton</div><div class="chip">Cardiff Bay</div><div class="chip">Under £450</div></div>'
            '%s'
            '<div class="grid g3">%s</div></div>' % (post_cta, ''.join(cards)))
    return page('Find a housemate', 'flatmates', body)

# ================= PAGE: MESSAGES =================
def msg_thread(slug, initials, bg, name, sub, time, unread, messages, active=False):
    # messages: list of {'them': bool, 'text': str}
    msgs_attr = json.dumps(messages).replace('"', '&quot;')
    preview = messages[-1]['text']
    cls = 'msg-thread active' if active else 'msg-thread'
    unread_dot = '<span class="msg-unread-dot"></span>' if unread else ''
    return ('<div class="%s" data-thread="%s" data-name="%s" data-sub="%s" data-initials="%s" '
            'data-bg="%s" data-messages="%s" tabindex="0" role="button" aria-label="Open conversation with %s">'
            '<div class="msg-thread-ava" style="background:%s">%s</div>'
            '<div class="msg-thread-body"><div class="msg-thread-top"><span class="n">%s</span><span class="t">%s</span></div>'
            '<div class="msg-thread-preview">%s</div></div>%s</div>'
            % (cls, slug, name, sub, initials, bg, msgs_attr, name, bg, initials, name, time, preview, unread_dot))

def build_messages():
    threads = [
        msg_thread('priya', 'PR', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Priya', 'Cathays · 4-bed house', '2h', True,
                   [{'them': True, 'text': "Hey! Saw you're interested in the room \U0001F642 It's still free if you want to come view it"},
                    {'them': False, 'text': 'Yes please! Would Thursday afternoon work?'},
                    {'them': True, 'text': "Thursday's perfect, come by around 4pm — I'll send the address"}],
                   active=True),
        msg_thread('jack', 'JK', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Jack', 'Roath · 5-bed house', '1d', False,
                   [{'them': True, 'text': "Hiya! We've got two rooms free if you fancy bringing a mate along too"},
                    {'them': False, 'text': "Oh nice, I might know someone actually — I'll ask and get back to you"}]),
        msg_thread('careers', 'CC', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Cardiff Careers', 'Admiral Data Analyst internship', '3d', False,
                   [{'them': True, 'text': "Thanks for registering interest in the Summer Internship — Data Analyst role. Applications close 14 Nov, good luck!"},
                    {'them': True, 'text': "Quick tip: tailor your cover letter to the 'why Admiral' question, it's the one most people skip \U0001F44D"}]),
        msg_thread('filmsoc', 'FS', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Film Society', 'Committee', '5d', False,
                   [{'them': True, 'text': 'Welcome to Film Society! \U0001F3AC First screening is Thursday — Alien, 7pm, SU Cinema. See you there!'}]),
    ]
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Stay in touch</div>'
            '<h1>Messages</h1>'
            '<div class="sub">Conversations from Flatmates listings, societies and opportunities — all in one inbox.</div></div>'
            '<div class="widget msg-widget"><div class="msg-layout">'
            '<div class="msg-threads">%s</div>'
            '<div class="msg-conversation">'
            '<div class="msg-conv-head"><div class="msg-thread-ava" id="msgConvAva"></div>'
            '<div><div class="n" id="msgConvName"></div><div class="sub" id="msgConvSub"></div></div></div>'
            '<div class="msg-conv-body" id="msgConvBody"></div>'
            '<div class="soc-chat-input"><input type="text" id="msgConvInput" placeholder="Type a message…">'
            '<button id="msgConvSend">%s</button></div>'
            '</div></div></div></div>' % (''.join(threads), ICONS['send']))
    return page('Messages', 'profile', body)

# ================= PAGE: SAFETY =================
def contact_row(icon, name, detail, desc):
    return ('<div class="contact-row"><div class="contact-ic">%s</div>'
            '<div class="contact-body"><div class="contact-name">%s</div>'
            '<div class="contact-detail">%s</div><div class="contact-desc">%s</div></div></div>'
            % (icon, name, detail, desc))

def build_safety():
    emergency = ('<div class="emergency-banner"><div class="eb-ic">%s</div>'
                 '<div><h3>In an emergency, call 999</h3>'
                 '<p>Not an emergency but need help on or near campus? Cardiff University Security: '
                 '<a href="tel:+442920874444">029 2087 4444</a> — staffed 24/7.</p></div></div>' % ICONS['shield'])

    talk_widget = ('<div class="widget"><div class="widget-head"><h3>Someone to talk to</h3></div>'
                   '%s%s%s</div>' % (
        contact_row(ICONS['phone'], 'Nightline Cardiff', '029 2087 0555',
                    'Student-led, confidential listening service — nothing is too big or too small. Wed &amp; Sat, 8pm–8am. Also reachable by instant message.'),
        contact_row(ICONS['phone'], 'Samaritans', '116 123',
                    'Free to call, anyone, any reason, 24/7 — you don\'t have to be suicidal to call.'),
        contact_row(ICONS['people'], 'Cardiff SU Advice', '029 2078 1410 · advice@cardiff.ac.uk',
                    'Free, confidential, independent advice on housing, money, welfare and more. 3rd floor, Students\' Union Building.'),
    ))

    outnight_widget = ('<div class="widget"><div class="widget-head"><h3>On a night out</h3></div>'
                       '%s%s%s</div>' % (
        contact_row(ICONS['shield'], 'Ask for Angela', '',
                    'Feeling unsafe or uncomfortable at a bar or club? Go to the bar and ask a member of staff for "Angela" — they\'re trained to help, discreetly. Running in venues across Cardiff.'),
        contact_row(ICONS['people'], 'Street Pastors', '',
                    'Volunteers patrol Cardiff city centre Fri &amp; Sat, 10pm–4am — water, flip-flops, and a friendly face if you need help getting home.'),
        contact_row(ICONS['heart'], 'Stick together', '',
                    'Arrive and leave with your group, keep your phone charged, and share your live location with a mate before you head out.'),
    ))

    home_widget = ('<div class="widget"><div class="widget-head"><h3>Getting home safely</h3></div>'
                   '%s%s%s</div>' % (
        contact_row(ICONS['pin'], 'Only use licensed taxis', '',
                    'Cardiff Council-licensed Hackney carriages are black with a white bonnet/roof light and a visible council plate. Never get into an unlicensed or unmarked car.'),
        contact_row(ICONS['money'], 'No cash, no problem', '',
                    'Cardiff taxis have had to accept card payment since September 2024, so you don\'t need to carry cash on you.'),
        contact_row(ICONS['send'], 'Share your trip', '',
                    'Send a mate your taxi details or live location, especially late at night — it takes ten seconds.'),
    ))

    map_cta = ('<div class="widget kit-banner"><div><h3 style="margin-bottom:4px">Where\'s all this happening?</h3>'
               '<div style="color:var(--muted);font-size:.85rem">See every club, bar and BUCS fixture on the map — plan your route home before you go out.</div></div>'
               '<a class="pill primary" href="map.html">Open the map %s</a></div>' % ICONS['arrow'])

    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Look after each other</div>'
            '<h1>Staying safe on a night out</h1>'
            '<div class="sub">Real contacts and services for Cardiff students. Worth saving this page, or adding the numbers to your phone before you go out.</div></div>'
            + emergency +
            '<div class="two-col">'
            '<div class="feed-col">%s%s</div>'
            '<aside class="side-col">%s%s</aside>'
            '</div></div>' % (talk_widget, home_widget, outnight_widget, map_cta))
    return page('Staying safe', 'map', body)

# ================= PAGE: MAP =================
def venue_card(emoji, bg, cat, name, area, desc, lat, lng, going, ticket_url='', ticket_label='', pin_color='',
                fixture_date='', fixture_time=''):
    is_fixture = bool(fixture_date)
    color = pin_color or going_color(going)
    going_label = 'going' if is_fixture else 'going tonight'
    rsvp_label = "I'm going" if is_fixture else "I'm going tonight"
    search = ('%s %s %s %s' % (name, area, cat, desc)).lower()
    ticket_html = ''
    if ticket_url:
        ticket_html = ('<a class="ticket-link" href="%s" target="_blank" rel="noopener">%s %s</a>'
                        % (ticket_url, ticket_label, ICONS['ext']))
    return ('<div class="card venue-card" data-lat="%s" data-lng="%s" data-name="%s" data-cat="%s" '
            'data-area="%s" data-going="%s" data-search="%s" data-ticket-url="%s" data-ticket-label="%s" '
            'data-pin-color="%s" data-fixture-date="%s" data-fixture-time="%s">'
            '<div class="card-media" style="background:%s">'
            '<span class="chip-cat">%s</span><span class="emoji">%s</span></div>'
            '<div class="card-body"><h3>%s</h3><div class="by">%s</div><p>%s</p>%s'
            '<div class="card-foot"><span class="stat busy-badge">'
            '<i class="busy-dot" style="background:%s"></i>'
            '<span class="going-count">%s</span> %s</span>'
            '<div class="post-actions">'
            '<button class="pill locate-btn">Show on map %s</button>'
            '<button class="pill primary venue-rsvp" data-rsvp="You\'re in 🎉">%s</button>'
            '</div></div></div></div>'
            % (lat, lng, name, cat, area, going, search, ticket_url, ticket_label, pin_color, fixture_date,
               fixture_time, bg, cat, emoji, name, area, desc, ticket_html, color, going, going_label,
               ICONS['pin'], rsvp_label))

def build_map():
    # Verified against current listings — closed venues (e.g. The Moon Club, shut Nov 2024) removed,
    # renamed ones updated (PRYZM → Circuit), and the SU's own nightclub added.
    venues = [
        ('🎓', 'linear-gradient(135deg,var(--lime),var(--coral))', 'Student Union', "Y Plas — Cardiff SU", 'Park Place',
         "The Students' Union's own nightclub — home to YOLO, Cardiff's biggest weekly student night. Links up with the Great Hall for a 4,000-capacity superclub on big nights.", 51.4874, -3.1783, 180,
         'https://www.ents24.com/cardiff-events/cardiff-university-su-the-great-hall-solus-cf10-the-taf-y-plas', 'YOLO — get tickets'),
        ('🎉', 'linear-gradient(135deg,var(--amber),var(--lime))', 'Club', 'Misfits Social Club', 'Miskin Street',
         "An independent grassroots venue a stone's throw from the SU — not part of it, just next door. Live music, street food and cheap drinks 'til 3am, in the old Koko Gorillaz building.", 51.4839, -3.1785, 64,
         'https://www.skiddle.com/whats-on/Cardiff/Misfits-Social-Club/', "What's on — get tickets"),
        ('🎶', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Club', 'Clwb Ifor Bach', 'Womanby Street',
         "Cardiff's best-loved indie &amp; alt club — three floors, gigs most nights.", 51.4816, -3.1811, 76,
         'https://clwb.net/whats-on/', "Tonight's gig — get tickets"),
        ('🪩', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Club', 'Circuit', 'Greyfriars Road',
         'Big-room commercial club — house, pop and chart anthems, on the old PRYZM site.', 51.4795, -3.1774, 95,
         'https://circuitclub.co.uk/cardiff/whats-on/', "Tonight's line-up — get tickets"),
        ('🤘', 'linear-gradient(135deg,var(--amber),var(--coral))', 'Club', 'Fuel Rock Club', 'Womanby Street',
         "Cardiff's only dedicated rock &amp; metal club — gigs out back, discos 'til late Fri &amp; Sat.", 51.4809, -3.1813, 41,
         'https://www.fuelrockclub.co.uk/', 'Rock & metal disco — get tickets'),
        ('🕺', 'linear-gradient(135deg,var(--coral),var(--sky))', 'Club', 'Metros', 'Bakers Row',
         'Backstreet basement club running alt &amp; indie nights for over 20 years.', 51.4785, -3.1770, 34,
         'https://www.fatsoma.com/p/metros---cardiff', 'Alt night — get tickets'),
        ('🎤', 'linear-gradient(135deg,var(--lime),var(--amber))', 'Club', 'Popworld Cardiff', 'St Mary Street',
         "Cheesy pop, karaoke and half-price drinks — dance floor anthems 'til 3am.", 51.4783, -3.1776, 52,
         'https://www.popworldparty.co.uk/cardiff', 'Karaoke & pop night — get tickets'),
        ('🍻', 'linear-gradient(135deg,var(--sky),var(--amber))', 'Bar', 'The Woodville', 'Cathays',
         'Classic student pub two minutes from halls — beer garden, sport, cheap pints.', 51.4913, -3.1815, 15),
        ('🍸', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Bar', 'Dead Canary', 'Charles Street',
         'Ring the bell to get in — secret cocktail bar with lab-made drinks in a Grade II building.', 51.4762, -3.1763, 28),
        ('🍺', 'linear-gradient(135deg,var(--amber),var(--sky))', 'Bar', 'BrewDog Cardiff', 'Westgate Street',
         'Craft beer bar opposite the stadium — 25 taps, big matchday crowd.', 51.4787, -3.1809, 12),
        ('🍷', 'linear-gradient(135deg,var(--coral),var(--lime))', 'Bar', 'The Owain Glyndŵr', 'St John Street',
         'Recently refurbished sports pub near the castle — 31 screens, always packed on match day.', 51.4813, -3.1800, 70),
        ('🏉', 'linear-gradient(135deg,var(--sky),var(--lime))', 'BUCS', 'Cardiff University Sports Fields', 'Llanrumney',
         'Cardiff University\'s BUCS home pitches — next up: Cardiff vs Hartpury (23 Sep) and Cardiff vs Nottingham (28 Oct).',
         51.5180, -3.1270, 54,
         'https://www.bucs.org.uk/tickets.html', 'BUCS tickets', '#1E3A8A', '2026-09-23', '2:00pm'),
        ('🏆', 'linear-gradient(135deg,var(--amber),var(--sky))', 'BUCS', 'Cardiff Arms Park', 'City Centre',
         'The Cardiff Clash — Cardiff University vs Cardiff Met, BUCS Super Rugby\'s biggest derby. Past crowds have topped 4,000.',
         51.4784, -3.1815, 340,
         'https://www.bucs.org.uk/tickets.html', 'The Cardiff Clash — get tickets', '#1E3A8A', '2026-10-07', '7:30pm'),
    ]
    cards = ''.join(venue_card(*v) for v in venues)
    legend = ('<div class="busy-legend">'
              '<span class="lg"><i style="background:#2ED573"></i>Under 20 going</span>'
              '<span class="lg"><i style="background:#FFA502"></i>20–69 going</span>'
              '<span class="lg"><i style="background:#FF4757"></i>70+ going</span>'
              '<span class="lg"><i style="background:#1E3A8A"></i>BUCS fixture</span>'
              '</div>')
    search_bar = ('<div class="map-search">%s'
                  '<input type="text" id="venueSearch" autocomplete="off" '
                  'placeholder="Search clubs, bars, the SU &amp; BUCS fixtures by name, area or vibe…">'
                  '<span class="match-count" id="venueMatchCount"></span>'
                  '<button class="clear-search" id="venueSearchClear" aria-label="Clear search">%s</button></div>'
                  % (ICONS['search'], ICONS['close']))
    safety_banner = ('<div class="widget kit-banner safety-banner"><div><h3 style="margin-bottom:4px">%s Staying safe tonight</h3>'
                     '<div style="color:var(--muted);font-size:.85rem">Emergency numbers, Ask for Angela, and how to get a safe taxi home.</div></div>'
                     '<a class="pill primary" href="safety.html">Night safety info %s</a></div>'
                     % (ICONS['shield'], ICONS['arrow']))
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Night out sorted</div>'
            '<h1>Clubs, bars, the SU &amp; BUCS near campus</h1>'
            '<div class="sub">Every club, bar, Students\' Union night and BUCS fixture students actually go to, pinned on the map — kept current, closed venues removed. Search to find one, tap a card to fly to it, or a pin to say you\'re going.</div></div>'
            '<div class="chips"><div class="chip on">All</div><div class="chip">Student Union</div><div class="chip">Clubs</div><div class="chip">Bars</div><div class="chip">BUCS</div></div>'
            '%s'
            '<div class="widget map-widget"><div id="venueMap"></div></div>'
            '%s%s'
            '<div class="grid g3" id="venueGrid">%s</div>'
            '<div class="empty-state" id="venueEmpty" hidden>No venues match “<span id="venueEmptyQuery"></span>”.</div>'
            '</div>' % (safety_banner, search_bar, legend, cards))
    return page('Map', 'map', body, extra_head=LEAFLET_CSS, extra_scripts=LEAFLET_JS)

# ================= PAGE: PROFILE / JOURNEY =================
def calendar_widget():
    add_form = ('<div class="cal-add-form" id="calAddForm" hidden>'
                '<div class="field"><label>Title</label><input type="text" id="calFTitle" placeholder="e.g. Study session with Mia"></div>'
                '<div class="cal-form-row">'
                '<div class="field"><label>Date</label><input type="date" id="calFDate"></div>'
                '<div class="field"><label>Time</label><input type="text" id="calFTime" placeholder="e.g. 3:00pm"></div>'
                '</div>'
                '<div class="field"><label>Place</label><input type="text" id="calFPlace" placeholder="e.g. Trevithick Library"></div>'
                '<div class="field"><label>Colour</label><div class="cal-color-picker" id="calColorPicker">'
                '<button type="button" class="cal-color-swatch active" data-color="var(--lime)" style="background:var(--lime)" aria-label="Lime"></button>'
                '<button type="button" class="cal-color-swatch" data-color="var(--coral)" style="background:var(--coral)" aria-label="Coral"></button>'
                '<button type="button" class="cal-color-swatch" data-color="var(--sky)" style="background:var(--sky)" aria-label="Sky"></button>'
                '<button type="button" class="cal-color-swatch" data-color="var(--amber)" style="background:var(--amber)" aria-label="Amber"></button>'
                '</div></div>'
                '<div class="cal-form-error" id="calFormError" hidden>Add at least a title and date.</div>'
                '<div class="cal-form-actions"><button class="pill" id="calCancelBtn">Cancel</button>'
                '<button class="pill primary" id="calSaveBtn">Add to calendar</button></div>'
                '</div>')
    return ('<div class="widget cal-widget"><div class="widget-head">'
            '<h3>My calendar</h3>'
            '<div class="cal-nav"><button class="cal-nav-btn" id="calPrev" aria-label="Previous month">‹</button>'
            '<span class="cal-month-label" id="calMonthLabel"></span>'
            '<button class="cal-nav-btn" id="calNext" aria-label="Next month">›</button></div></div>'
            '<div class="cal-grid" id="calGrid"></div>'
            '<div class="cal-day-detail" id="calDayDetail" hidden>'
            '<h4 id="calDayDetailTitle"></h4><div class="cal-day-events" id="calDayEvents"></div></div>'
            '<button type="button" class="pill primary cal-add-btn" id="calAddBtn">%s Add your own event</button>'
            '%s'
            '<div class="cal-foot-note mono-eyebrow">Everything you RSVP to across Uni-Verse lands here automatically</div>'
            '</div>' % (ICONS['plus'], add_form))

def messages_preview_widget():
    return ('<div class="widget"><div class="widget-head"><h3>Messages</h3>'
            '<a href="messages.html">Open inbox →</a></div>'
            '<div class="soc-msg"><div class="soc-msg-ava" style="background:linear-gradient(135deg,var(--lime),var(--sky))">PR</div>'
            '<div class="soc-msg-body"><div class="soc-msg-head"><span class="soc-msg-name">Priya</span><span class="soc-msg-time">2h ago</span></div>'
            '<div class="soc-msg-text">Thursday\'s perfect, come by around 4pm — I\'ll send the address</div></div></div></div>')

def build_profile():
    stat_strip = ('<div class="stat-strip">'
                  '<div class="stat-box"><div class="big" id="statSocieties" data-baseline="3">3</div><div class="lbl">Societies joined</div></div>'
                  '<div class="stat-box"><div class="big" id="statEvents" data-baseline="7">7</div><div class="lbl">Events attended</div></div>'
                  '<div class="stat-box"><div class="big">£46</div><div class="lbl">Saved with discounts</div></div>'
                  '<div class="stat-box"><div class="big">4</div><div class="lbl">Opportunities saved</div></div></div>')
    # big goals list
    goals = [
        (True, 'Join your first society', 'You joined Film Society'),
        (True, 'Go to a social event', 'Games Night + Pizza'),
        (True, 'Claim a discount', 'Brewhouse Coffee'),
        (False, 'Attend a careers event', 'CV Clinic is coming up'),
        (False, 'Save your first opportunity', 'Browse Opportunities'),
        (False, 'Try a new sport', 'Give It A Go events'),
    ]
    grows = []
    for done, txt, sub in goals:
        cls = 'step done' if done else 'step'
        box = ('<span class="box">%s</span>' % ICONS['check']) if done else '<span class="box"></span>'
        grows.append('<div class="%s" style="justify-content:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)">'
                     '%s<div><div class="txt" style="font-weight:700">%s</div>'
                     '<div style="color:var(--muted);font-size:.78rem">%s</div></div></div>' % (cls, box, txt, sub))
    left = ('<div class="feed-col">'
            '<div class="page-head" style="display:flex;align-items:center;gap:16px">'
            '<div class="rail-avatar" style="width:64px;height:64px;font-size:1.4rem;border-radius:18px">FW</div>'
            '<div><h1 style="margin-bottom:4px">Findlay Wyatt</h1>'
            '<div class="sub">1st year · Computer Science · Cardiff University</div></div></div>'
            + stat_strip +
            '<div class="widget"><div class="widget-head"><h3>Your uni journey</h3>'
            '<span class="mono-eyebrow">3 of 6 done</span></div>'
            '<div class="prog-ring"><div class="ring">'
            '<svg width="64" height="64" viewBox="0 0 64 64">'
            '<circle cx="32" cy="32" r="27" fill="none" stroke="rgba(128,128,128,.25)" stroke-width="7"/>'
            '<circle cx="32" cy="32" r="27" fill="none" stroke="var(--lime)" stroke-width="7" stroke-linecap="round" stroke-dasharray="169.6" stroke-dashoffset="85"/>'
            '</svg><div class="num">50%%</div></div>'
            '<div class="prog-txt"><div class="lbl">Building momentum 🚀</div>'
            '<div class="dsc">Every goal you tick is a thing you won\'t look back and wish you\'d done.</div></div></div>'
            '<div class="prog-steps">%s</div></div></div>' % ''.join(grows))
    right = ('<aside class="side-col">%s%s%s</aside>' % (messages_preview_widget(), sidebar_ai(), sidebar_week()))
    body = ('<div class="content"><div class="two-col">%s%s</div>%s</div>'
            % (left, right, calendar_widget()))
    return page('Your journey', 'profile', body)

# ================= PAGE: AI CHAT =================
def rec_card(emoji, bg, title, meta):
    return ('<div class="rec-card"><div class="rc-ic" style="background:%s">%s</div>'
            '<div><div class="rc-t">%s</div><div class="rc-m">%s</div></div></div>'
            % (bg, emoji, title, meta))

def build_ai():
    recs = (rec_card('💼','linear-gradient(135deg,var(--sky),var(--lime))','Tech Society','Meets Tuesdays · 1,510 members')
            + rec_card('🎯','linear-gradient(135deg,var(--coral),var(--amber))','Admiral Internship','Data Analyst · closes 14 Nov')
            + rec_card('🧑\u200d💻','linear-gradient(135deg,var(--amber),var(--sky))','Intro to Coding Workshop','Thu 9 Oct · free'))
    body = ('<div class="content" style="padding-top:0;padding-bottom:0">'
            '<div class="chat-wrap">'
            '<div class="chat-head"><div class="ai-orb">%s</div>'
            '<div><h1>Ask Uni-Verse</h1><div class="csub">YOUR CARDIFF GUIDE</div></div></div>'
            '<div class="chat-body">'
            '<div class="msg ai-msg"><div class="m-ava">UV</div>'
            '<div class="m-bubble">Hey Findlay 👋 I\'m your Cardiff guide. Tell me what you want to get out of uni — a career direction, new people, something to do this weekend — and I\'ll point you at the events, societies and opportunities that get you there.</div></div>'
            '<div class="msg user-msg"><div class="m-ava">FW</div>'
            '<div class="m-bubble">I want to break into tech but I\'m a shy first year and don\'t know where to start.</div></div>'
            '<div class="msg ai-msg"><div class="m-ava">UV</div>'
            '<div class="m-bubble">Totally normal — loads of people feel that in first year. The trick is small, low-pressure steps. Here\'s where I\'d start, all beginner-friendly:'
            '<div class="rec">%s</div>'
            'Want me to add the workshop to your calendar and save the internship so you don\'t lose it?</div></div>'
            '</div>'
            '<div class="chat-suggest">'
            '<div class="cs">What\'s on this weekend under a tenner?</div>'
            '<div class="cs">Find me a society for meeting people</div>'
            '<div class="cs">Part-time jobs near campus</div></div>'
            '<div class="chat-input"><input type="text" placeholder="Ask anything about Cardiff…"><button>%s</button></div>'
            '</div></div>' % (ICONS['spark'], recs, ICONS['send']))
    return page('Ask Uni-Verse AI', 'ai', body, chat=True)

# ================= PAGE: LANDING =================
def build_landing():
    val = lambda bg, ic, h, p: ('<div class="val"><div class="vic" style="background:%s">%s</div>'
                                 '<h3>%s</h3><p>%s</p></div>' % (bg, ic, h, p))
    values = (val('var(--coral)', ICONS['events'], 'Every event, one feed', 'Society socials, workshops, sports and talks — all the stuff scattered across a hundred Instagram accounts, gathered in one place.')
              + val('var(--sky)', ICONS['opps'], 'Opportunities you\'d have missed', 'Internships, placements and part-time work from Cardiff Careers and partner employers, surfaced before the deadline sneaks past.')
              + val('var(--lime)', ICONS['discounts'], 'Discounts that pay for themselves', 'Free student deals from local Cardiff cafés, gyms and shops. Show your card, save money, every week.')
              + val('var(--amber)', ICONS['ai'], 'An AI guide for uni', 'Tell it what you want out of your degree and it points you at the people, events and opportunities to actually get there.'))
    float_cards = ('<div class="hero-right">'
                   '<div class="float-card c1"><div class="fc-top">'
                   '<div class="fc-ava" style="background:linear-gradient(135deg,var(--coral),var(--amber))">CS</div>'
                   '<div><div class="fc-org">Comp Sci Society</div><div class="fc-cat">Social</div></div></div>'
                   '<h4>Games Night + Pizza 🎮</h4><div class="fc-meta">Thu 2 Oct · 84 going</div></div>'
                   '<div class="float-card c2"><div class="fc-top">'
                   '<div class="fc-ava" style="background:var(--lime)">☕</div>'
                   '<div><div class="fc-org">Brewhouse Coffee</div><div class="fc-cat">Discount</div></div></div>'
                   '<h4>25% off, all term</h4><div class="fc-meta"><span class="deal-mini">-25%</span></div></div>'
                   '<div class="float-card c3"><div class="fc-top">'
                   '<div class="fc-ava" style="background:linear-gradient(135deg,var(--sky),var(--lime))">AD</div>'
                   '<div><div class="fc-org">Admiral</div><div class="fc-cat">Internship</div></div></div>'
                   '<h4>Data Analyst — Summer</h4><div class="fc-meta">£24k · closes 14 Nov</div></div>'
                   '</div>')
    body = ('<div class="landing">'
            '<nav class="land-nav"><div class="name">Uni<span>-</span>Verse</div>'
            '<div class="land-nav-links"><a href="#what">What is it</a><a href="events.html">Events</a>'
            '<a href="discounts.html">Discounts</a>'
            '<a href="index.html" class="btn-sm" style="color:var(--lime);font-weight:800">Open app →</a></div></nav>'
            '<div class="land-hero"><div class="hero-glow"></div><div class="hero-glow two"></div>'
            '<div class="hero-left"><div class="ey mono-eyebrow">Cardiff University · student platform</div>'
            '<h1>Everything at Cardiff, <span class="hl">in one place.</span></h1>'
            '<p class="lede">Every student we spoke to said the same thing: <em>"I wish I\'d known what was on."</em> Uni-Verse pulls all the events, societies, opportunities and discounts into one feed — so you never miss the uni you could\'ve had.</p>'
            '<div class="hero-cta"><a href="index.html" class="btn-lg primary">Open the app @@ARROW@@</a>'
            '<a href="#what" class="btn-lg ghost">See how it works</a></div>'
            '<div class="hero-proof">'
            '<div class="pf"><div class="n">300+</div><div class="l">Societies</div></div>'
            '<div class="pf"><div class="n">1,200+</div><div class="l">Events a year</div></div>'
            '<div class="pf"><div class="n">50+</div><div class="l">Local discounts</div></div></div>'
            '</div>@@FLOATCARDS@@</div>'
            '<div class="land-values" id="what"><div class="vh"><div class="ey mono-eyebrow">Why Uni-Verse</div>'
            '<h2>Four things, one login.</h2></div><div class="val-grid">@@VALUES@@</div></div>'
            '<div class="auth-wrap"><div class="auth-card"><div class="ey mono-eyebrow">Students only</div>'
            '<h2>Join Uni-Verse</h2><div class="as">Sign up with your Cardiff student email</div>'
            '<div class="field"><label>Cardiff email</label><input type="email" placeholder="c1234567@cardiff.ac.uk"></div>'
            '<div class="field"><label>Password</label><input type="password" placeholder="Create a password"></div>'
            '<a href="index.html" class="btn-lg primary" style="width:100%;justify-content:center;margin-top:6px">Create account</a>'
            '<div class="divider">or</div>'
            '<a href="index.html" class="btn-lg ghost" style="width:100%;justify-content:center">I already have an account</a>'
            '<div class="auth-note">Verified with your @cardiff.ac.uk email so the community stays students-only. This is a prototype — no real account is created.</div>'
            '</div></div>'
            + footer() + '</div>')
    body = (body.replace('@@ARROW@@', ICONS['arrow'])
                .replace('@@FLOATCARDS@@', float_cards)
                .replace('@@VALUES@@', values))
    # landing has no rail/topbar — custom doc
    doc = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
           '<title>Uni-Verse Cardiff · Everything at Cardiff, in one place</title>%s'
           '<link rel="stylesheet" href="css/styles.css"></head><body>'
           '%s%s<script src="js/app.js"></script></body></html>'
           % (FONTS, body, theme_switcher()))
    return doc

# ---------------- write all ----------------
pages = {
    'index.html': build_feed(),
    'events.html': build_events(),
    'bucs.html': build_bucs(),
    'opportunities.html': build_opps(),
    'discounts.html': build_discounts(),
    'map.html': build_map(),
    'safety.html': build_safety(),
    'societies.html': build_societies(),
    'flatmates.html': build_flatmates(),
    'messages.html': build_messages(),
    'profile.html': build_profile(),
    'ai.html': build_ai(),
    'landing.html': build_landing(),
}
pages.update(SOCIETY_PAGES)
for fn, html in pages.items():
    with open(os.path.join(OUT, fn), 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', fn, len(html), 'bytes')

# search index, consumed by the topbar search dropdown (js/app.js)
search_js = 'var UV_SEARCH = ' + json.dumps(SEARCH_INDEX, ensure_ascii=False) + ';'
with open(os.path.join(OUT, 'js', 'search-data.js'), 'w', encoding='utf-8') as f:
    f.write(search_js)
print('wrote js/search-data.js', len(search_js), 'bytes')
