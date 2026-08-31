# -*- coding: utf-8 -*-
"""Generates the Uni-Verse Cardiff site pages with a shared shell."""
import os

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
}

NAV = [
    ('index.html', 'feed', 'Feed'),
    ('events.html', 'events', 'Events'),
    ('opportunities.html', 'opps', 'Opportunities'),
    ('discounts.html', 'discounts', 'Discounts'),
    ('map.html', 'map', 'Map'),
    ('societies.html', 'societies', 'Societies'),
    ('profile.html', 'profile', 'Your journey'),
    ('ai.html', 'ai', 'Ask Uni-Verse AI'),
]

# Leaflet (OpenStreetMap) — no API key needed, used on the venue map page
LEAFLET_CSS = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">'
LEAFLET_JS = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'

def rail(active):
    btns = ['<div class="rail-logo">U</div>']
    for href, key, label in NAV:
        cls = 'rail-btn active' if key == active else 'rail-btn'
        btns.append('<a class="%s" href="%s"><span class="tip">%s</span>%s</a>' % (cls, href, label, ICONS[key]))
    btns.append('<div class="rail-spacer"></div>')
    btns.append('<a class="rail-avatar" href="profile.html">MW</a>')
    return '<nav class="rail">' + ''.join(btns) + '</nav>'

def topbar():
    return ('<header class="topbar">'
            '<div class="brand"><div class="name">Uni<span>-</span>Verse</div>'
            '<div class="loc">Cardiff University</div></div>'
            '<div class="search">%s<input type="text" placeholder="Search events, societies, jobs, discounts…"></div>'
            '<div class="top-actions">'
            '<button class="icon-btn"><span class="dot"></span>%s</button>'
            '<button class="icon-btn">%s</button>'
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
            '<button class="pill coral" data-rsvp="You\'re in 🎉">I\'m going</button></div></div></article>'
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
            '<button class="pill primary" data-rsvp="Reserved ✓">Reserve spot</button></div></div></article>'
            % (VERIFY, ICONS['cal'], ICONS['pin']))

# ================= PAGE: FEED =================
def build_feed():
    body = ('<div class="content two-col"><div class="feed-col">'
            '<div class="greeting"><div class="hi display">Alright, Murray <span class="wave">👋</span></div>'
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
def event_card(emoji, bg, cat, catcol, title, org, verified, date, place, going, cta):
    v = VERIFY if verified else ''
    return ('<div class="card"><div class="card-media" style="background:%s">'
            '<span class="chip-cat">%s</span>'
            '<button class="save-heart">%s</button>'
            '<span class="emoji">%s</span></div>'
            '<div class="card-body"><h3>%s</h3>'
            '<div class="by">%s%s</div>'
            '<div class="card-info"><div class="bit">%s %s</div><div class="bit">%s %s</div></div>'
            '<div class="card-foot"><span class="stat">%s going</span>'
            '<button class="pill primary" data-rsvp="Going ✓">%s</button></div></div></div>'
            % (bg, cat, ICONS['heart'], emoji, title, org, v, ICONS['cal'], date, ICONS['pin'], place, going, cta))

def build_events():
    cards = [
        event_card('🎮','linear-gradient(135deg,var(--coral),var(--amber))','Social','', 'Games Night + Pizza','Computer Science Society',True,'Thu 2 Oct · 7pm','SU, Y Plas','84','I\'m going'),
        event_card('🎤','linear-gradient(135deg,var(--sky),var(--lime))','Social','', 'Open Mic Night','Music Society',True,'Fri 3 Oct · 8pm','The Taf','56','I\'m going'),
        event_card('💼','linear-gradient(135deg,var(--amber),var(--coral))','Workshop','', 'CV Clinic + Networking','Enactus Cardiff',True,'Wed 8 Oct · 5:30pm','sbarc | spark','40','Reserve'),
        event_card('🧗','linear-gradient(135deg,var(--lime),var(--sky))','Sport','', 'Give It A Go: Bouldering','Mountaineering Club',True,'Sat 11 Oct · 2pm','Boulders CDF','22','I\'m going'),
        event_card('🎬','linear-gradient(135deg,var(--coral),var(--sky))','Social','', 'Film Night: Cult Classics','Film Society',True,'Sun 12 Oct · 6pm','SU Cinema','70','I\'m going'),
        event_card('🌍','linear-gradient(135deg,var(--sky),var(--amber))','Talk','', 'Careers in Sustainability','Careers Service',True,'Tue 14 Oct · 1pm','Glamorgan Building','35','Reserve'),
    ]
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">What\'s on</div>'
            '<h1>Events at Cardiff</h1>'
            '<div class="sub">Every society and official event in one place. Filter by what you\'re into — all hosted by verified organisations.</div></div>'
            '<div class="chips"><div class="chip on">All</div><div class="chip">Social</div>'
            '<div class="chip">Professional</div><div class="chip">Sport</div><div class="chip">Talks</div>'
            '<div class="chip">This week</div><div class="chip">Free</div></div>'
            '<div class="grid g3">%s</div></div>' % ''.join(cards))
    return page('Events', 'events', body)

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
def soc_card(emoji, bg, name, members, desc):
    return ('<div class="card"><div class="card-media" style="background:%s">'
            '<span class="emoji">%s</span></div>'
            '<div class="card-body"><h3>%s%s</h3>'
            '<div class="by">%s members</div>'
            '<p>%s</p>'
            '<div class="card-foot"><span class="stat">Active this week</span>'
            '<button class="soc-join">Join</button></div></div></div>'
            % (bg, emoji, name, VERIFY, members, desc))

def build_societies():
    cards = [
        soc_card('🎬','linear-gradient(135deg,var(--lime),var(--sky))','Film Society','1,240','Weekly screenings, cult classics and trips to the cinema. All welcome.'),
        soc_card('🥾','linear-gradient(135deg,var(--coral),var(--amber))','Hiking & Mountaineering','860','Weekend adventures across the Brecon Beacons and beyond. Kit provided.'),
        soc_card('💼','linear-gradient(135deg,var(--sky),var(--lime))','Entrepreneurs Society','1,510','Talks, pitch nights and startup socials. Build something at uni.'),
        soc_card('🎭','linear-gradient(135deg,var(--amber),var(--coral))','Drama Society','740','Termly productions, workshops and open auditions. No experience needed.'),
        soc_card('⚽','linear-gradient(135deg,var(--lime),var(--coral))','Football Club','2,100','Teams for every level plus casual kickabouts. Give it a go.'),
        soc_card('🌍','linear-gradient(135deg,var(--sky),var(--amber))','International Students','1,880','Socials, trips and a friendly community away from home.'),
    ]
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Find your people</div>'
            '<h1>Societies</h1>'
            '<div class="sub">300+ Cardiff societies, all in one place. Join in a tap and their events land straight in your feed.</div></div>'
            '<div class="chips"><div class="chip on">All</div><div class="chip">Sport</div>'
            '<div class="chip">Arts</div><div class="chip">Academic</div><div class="chip">Culture</div>'
            '<div class="chip">Volunteering</div><div class="chip">Social</div></div>'
            '<div class="grid g3">%s</div></div>' % ''.join(cards))
    return page('Societies', 'societies', body)

# ================= PAGE: MAP =================
def venue_card(emoji, bg, cat, name, area, desc, lat, lng):
    return ('<div class="card venue-card" data-lat="%s" data-lng="%s" data-name="%s">'
            '<div class="card-media" style="background:%s">'
            '<span class="chip-cat">%s</span><span class="emoji">%s</span></div>'
            '<div class="card-body"><h3>%s</h3><div class="by">%s</div><p>%s</p>'
            '<div class="card-foot"><span class="stat">%s</span>'
            '<button class="pill primary locate-btn">Show on map %s</button></div></div></div>'
            % (lat, lng, name, bg, cat, emoji, name, area, desc, cat, ICONS['pin']))

def build_map():
    venues = [
        ('🎶', 'linear-gradient(135deg,var(--coral),var(--amber))', 'Club', 'Clwb Ifor Bach', 'Womanby Street',
         "Cardiff's legendary indie &amp; alt club — three floors, gigs most nights.", 51.4816, -3.1811),
        ('🪩', 'linear-gradient(135deg,var(--sky),var(--lime))', 'Club', 'PRYZM Cardiff', 'Greyfriars Road',
         'Big-room clubbing — the go-to for student nights out.', 51.4795, -3.1774),
        ('🤘', 'linear-gradient(135deg,var(--amber),var(--coral))', 'Club', 'The Moon Club', 'Womanby Street',
         "Rock, metal and alt club nights on Cardiff's music street.", 51.4813, -3.1815),
        ('🎸', 'linear-gradient(135deg,var(--coral),var(--sky))', 'Club', 'Fuel Rock Club', 'Windsor Place',
         "Two floors of rock, punk and metal — Cardiff's heaviest night out.", 51.4816, -3.1751),
        ('🍻', 'linear-gradient(135deg,var(--sky),var(--amber))', 'Bar', 'The Woodville', 'Cathays',
         'Classic student pub two minutes from halls — quiz nights, sport, cheap pints.', 51.4913, -3.1815),
        ('🍸', 'linear-gradient(135deg,var(--lime),var(--sky))', 'Bar', 'Dead Canary', 'High Street Arcade',
         'Speakeasy-style cocktail bar tucked in the arcades.', 51.4816, -3.1785),
        ('🍺', 'linear-gradient(135deg,var(--amber),var(--sky))', 'Bar', 'BrewDog Cardiff', 'Westgate Street',
         'Craft beer bar opposite the stadium — big matchday crowd.', 51.4787, -3.1809),
        ('🍷', 'linear-gradient(135deg,var(--coral),var(--lime))', 'Bar', 'The Owain Glyndŵr', 'St John Street',
         'Wetherspoons in an old church — student-priced, always packed.', 51.4813, -3.1800),
    ]
    cards = ''.join(venue_card(*v) for v in venues)
    body = ('<div class="content">'
            '<div class="page-head"><div class="ey mono-eyebrow">Night out sorted</div>'
            '<h1>Clubs &amp; bars near campus</h1>'
            '<div class="sub">Every club and bar students actually go to, pinned on the map. Tap a card to fly to it, or a pin to see what it is.</div></div>'
            '<div class="chips"><div class="chip on">All</div><div class="chip">Clubs</div><div class="chip">Bars</div></div>'
            '<div class="widget map-widget"><div id="venueMap"></div></div>'
            '<div class="grid g3">%s</div></div>' % cards)
    return page('Map', 'map', body, extra_head=LEAFLET_CSS, extra_scripts=LEAFLET_JS)

# ================= PAGE: PROFILE / JOURNEY =================
def build_profile():
    stat_strip = ('<div class="stat-strip">'
                  '<div class="stat-box"><div class="big">3</div><div class="lbl">Societies joined</div></div>'
                  '<div class="stat-box"><div class="big">7</div><div class="lbl">Events attended</div></div>'
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
            '<div class="rail-avatar" style="width:64px;height:64px;font-size:1.4rem;border-radius:18px">MW</div>'
            '<div><h1 style="margin-bottom:4px">Murray Wyatt</h1>'
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
    right = ('<aside class="side-col">%s%s</aside>' % (sidebar_ai(), sidebar_week()))
    body = '<div class="content two-col">%s%s</div>' % (left, right)
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
            '<div class="m-bubble">Hey Murray 👋 I\'m your Cardiff guide. Tell me what you want to get out of uni — a career direction, new people, something to do this weekend — and I\'ll point you at the events, societies and opportunities that get you there.</div></div>'
            '<div class="msg user-msg"><div class="m-ava">MW</div>'
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
    'opportunities.html': build_opps(),
    'discounts.html': build_discounts(),
    'map.html': build_map(),
    'societies.html': build_societies(),
    'profile.html': build_profile(),
    'ai.html': build_ai(),
    'landing.html': build_landing(),
}
for fn, html in pages.items():
    with open(os.path.join(OUT, fn), 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', fn, len(html), 'bytes')
