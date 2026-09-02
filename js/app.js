/* ============================================================
   UNI-VERSE CARDIFF — shared behaviour
   ============================================================ */
(function () {
  // ---- THEME: default electric, remember last choice for the session ----
  var saved = null;
  try { saved = window.sessionStorage.getItem('uv-theme'); } catch (e) {}
  document.documentElement.setAttribute('data-theme', saved || 'electric');

  function markActiveTheme() {
    var current = document.documentElement.getAttribute('data-theme');
    document.querySelectorAll('.theme-opt').forEach(function (o) {
      o.classList.toggle('active', o.dataset.set === current);
    });
  }

  // ---- MY CALENDAR: shared storage — anything RSVP'd anywhere on the site lands here ----
  function calPad(n) { return n < 10 ? '0' + n : '' + n; }
  function calIsoDate(d) { return d.getFullYear() + '-' + calPad(d.getMonth() + 1) + '-' + calPad(d.getDate()); }
  function getCalendar() {
    try { return JSON.parse(window.localStorage.getItem('uv-calendar')) || []; } catch (e) { return []; }
  }
  function saveCalendarItems(items) {
    try { window.localStorage.setItem('uv-calendar', JSON.stringify(items)); } catch (e) {}
  }
  function addToCalendar(item) {
    var items = getCalendar();
    if (!items.some(function (i) { return i.id === item.id; })) {
      items.push(item);
      saveCalendarItems(items);
    }
  }
  function removeFromCalendar(id) {
    saveCalendarItems(getCalendar().filter(function (i) { return i.id !== id; }));
  }

  // ---- RSVP persistence: remembers a clicked [data-rsvp] button across reloads ----
  // Stores a timestamp (not just a flag) so notifications can show "X ago".
  function isRsvpDone(key) {
    try { return window.localStorage.getItem('uv-rsvp-' + key) !== null; } catch (e) { return false; }
  }
  function setRsvpDone(key) {
    try { window.localStorage.setItem('uv-rsvp-' + key, String(Date.now())); } catch (e) {}
  }
  function clearRsvpDone(key) {
    try { window.localStorage.removeItem('uv-rsvp-' + key); } catch (e) {}
  }

  // ---- NOTIF READ STATE: for notification kinds that aren't tied to an existing
  // read flag (societies joined, upcoming calendar events) — lets "mark all read"
  // actually stick, instead of the same items reappearing every time you reopen the panel ----
  function isNotifRead(id) {
    try { return (JSON.parse(window.localStorage.getItem('uv-notif-read')) || []).indexOf(id) !== -1; } catch (e) { return false; }
  }
  function markNotifRead(id) {
    try {
      var arr = JSON.parse(window.localStorage.getItem('uv-notif-read')) || [];
      if (arr.indexOf(id) === -1) { arr.push(id); window.localStorage.setItem('uv-notif-read', JSON.stringify(arr)); }
    } catch (e) {}
  }

  // ---- SAVED: a personal list, built from anything saved anywhere on the site ----
  function getSaved() {
    try { return JSON.parse(window.localStorage.getItem('uv-saved')) || []; } catch (e) { return []; }
  }
  function saveSavedItems(items) {
    try { window.localStorage.setItem('uv-saved', JSON.stringify(items)); } catch (e) {}
  }
  function isSaved(id) {
    return getSaved().some(function (i) { return i.id === id; });
  }
  // Adds if not already saved, removes if it is. Returns the new saved state.
  function toggleSaved(item) {
    var items = getSaved();
    var idx = items.findIndex(function (i) { return i.id === item.id; });
    if (idx === -1) { items.unshift(item); saveSavedItems(items); return true; }
    items.splice(idx, 1); saveSavedItems(items); return false;
  }

  // ---- USER: identity set at login/signup, extended by the profile edit form ----
  function getUser() {
    try { return JSON.parse(window.localStorage.getItem('uv-user')) || null; } catch (e) { return null; }
  }
  function saveUser(user) {
    try { window.localStorage.setItem('uv-user', JSON.stringify(user)); } catch (e) {}
  }
  function initialsOf(name) {
    var words = (name || '').match(/[A-Za-z0-9]+/g) || [];
    if (!words.length) return '?';
    if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
    return (words[0][0] + words[1][0]).toUpperCase();
  }
  function downscaleImage(file, maxDim, cb) {
    var reader = new FileReader();
    reader.onload = function (e) {
      var img = new Image();
      img.onload = function () {
        var scale = Math.min(1, maxDim / Math.max(img.width, img.height));
        var w = Math.max(1, Math.round(img.width * scale));
        var h = Math.max(1, Math.round(img.height * scale));
        var canvas = document.createElement('canvas');
        canvas.width = w; canvas.height = h;
        canvas.getContext('2d').drawImage(img, 0, 0, w, h);
        cb(canvas.toDataURL('image/jpeg', 0.72));
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  document.addEventListener('DOMContentLoaded', function () {
    // ---- sidebar nav avatar: reflects whatever's set on the profile page, on every page ----
    (function () {
      var navAvatar = document.querySelector('.rail-avatar[href="profile.html"]');
      if (!navAvatar) return;
      var u = getUser();
      if (u && u.photo) {
        navAvatar.innerHTML = '<img src="' + u.photo + '" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">';
      } else if (u && u.name) {
        navAvatar.textContent = initialsOf(u.name);
      }
    })();

    // ---- theme switcher ----
    var fab = document.getElementById('themeFab');
    var panel = document.getElementById('themePanel');
    if (fab && panel) {
      fab.addEventListener('click', function (e) {
        e.stopPropagation();
        panel.classList.toggle('open');
      });
      document.addEventListener('click', function (e) {
        if (!panel.contains(e.target) && e.target !== fab) panel.classList.remove('open');
      });
      document.querySelectorAll('.theme-opt').forEach(function (opt) {
        opt.addEventListener('click', function () {
          var set = opt.dataset.set;
          document.documentElement.setAttribute('data-theme', set);
          try { window.sessionStorage.setItem('uv-theme', set); } catch (e) {}
          markActiveTheme();
        });
      });
      markActiveTheme();
    }

    // ---- sitewide search (topbar, every page) ----
    var topSearchInput = document.getElementById('topSearchInput');
    var topSearchResults = document.getElementById('topSearchResults');
    if (topSearchInput && topSearchResults && window.UV_SEARCH) {
      var lastMatches = [];
      function runTopSearch() {
        var q = topSearchInput.value.trim().toLowerCase();
        if (!q) { topSearchResults.hidden = true; topSearchResults.innerHTML = ''; lastMatches = []; return; }
        lastMatches = window.UV_SEARCH.filter(function (item) {
          return (item.t + ' ' + item.c + ' ' + (item.d || '')).toLowerCase().indexOf(q) !== -1;
        }).slice(0, 8);
        if (!lastMatches.length) {
          topSearchResults.innerHTML = '<div class="search-empty">No results</div>';
        } else {
          topSearchResults.innerHTML = lastMatches.map(function (m) {
            return '<a class="search-result" href="' + m.u + '">'
              + '<div><div class="sr-title">' + m.t + '</div>'
              + (m.d ? '<div class="sr-meta">' + m.d + '</div>' : '') + '</div>'
              + '<span class="sr-cat">' + m.c + '</span></a>';
          }).join('');
        }
        topSearchResults.hidden = false;
      }
      topSearchInput.addEventListener('input', runTopSearch);
      topSearchInput.addEventListener('focus', function () { if (topSearchInput.value.trim()) runTopSearch(); });
      topSearchInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && lastMatches.length) window.location.href = lastMatches[0].u;
        if (e.key === 'Escape') { topSearchResults.hidden = true; topSearchInput.blur(); }
      });
      document.addEventListener('click', function (e) {
        if (!topSearchResults.contains(e.target) && e.target !== topSearchInput) topSearchResults.hidden = true;
      });
    }

    // ---- notifications: messages, societies you've joined, and what's coming up ----
    var notifBtn = document.getElementById('notifBtn');
    var notifPanel = document.getElementById('notifPanel');
    var notifDot = document.getElementById('notifDot');
    var notifList = document.getElementById('notifList');
    var notifMarkAll = document.getElementById('notifMarkAll');
    if (notifBtn && notifPanel && notifList) {
      function notifTimeAgo(ts) {
        var mins = Math.floor((Date.now() - ts) / 60000);
        if (mins < 1) return 'Just now';
        if (mins < 60) return mins + 'm ago';
        var hrs = Math.floor(mins / 60);
        if (hrs < 24) return hrs + 'h ago';
        return Math.floor(hrs / 24) + 'd ago';
      }
      function notifWhen(dateStr) {
        var target = new Date(dateStr + 'T00:00:00');
        var today = new Date(); today.setHours(0, 0, 0, 0);
        var diff = Math.round((target - today) / 86400000);
        if (diff < 0) return null;
        if (diff === 0) return 'Today';
        if (diff === 1) return 'Tomorrow';
        return 'In ' + diff + ' days';
      }
      var ICON_CHAT = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>';
      var ICON_SOC = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8zM23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>';
      var ICON_CAL = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path stroke-linecap="round" d="M3 10h18M8 2v4M16 2v4"/></svg>';

      function notifItem(icon, title, meta, url) {
        return '<a class="notif-item" href="' + url + '">'
          + '<div class="notif-ic">' + icon + '</div>'
          + '<div class="notif-body"><div class="notif-title">' + title + '</div>'
          + '<div class="notif-meta">' + meta + '</div></div></a>';
      }

      // ids of everything currently unread, so "mark all read" knows what to clear
      var unreadThreadSlugs = [];
      var unreadNotifIds = [];

      function buildNotifications() {
        unreadThreadSlugs = [];
        unreadNotifIds = [];
        var messagesHtml = [];
        if (window.UV_THREADS) {
          window.UV_THREADS.forEach(function (th) {
            var read = false;
            try { read = window.localStorage.getItem('uv-msg-read-' + th.slug) !== null; } catch (e) {}
            if (th.unread && !read) {
              unreadThreadSlugs.push(th.slug);
              messagesHtml.push(notifItem('%%CHAT%%', th.name + ': ' + th.preview, 'New message', 'messages.html'));
            }
          });
        }

        var societiesHtml = [];
        try {
          Object.keys(window.localStorage).filter(function (k) { return k.indexOf('uv-joined-') === 0; })
            .map(function (k) { return { slug: k.replace('uv-joined-', ''), raw: window.localStorage.getItem(k) }; })
            .map(function (j) { var ts = parseInt(j.raw, 10); return { slug: j.slug, ts: isNaN(ts) ? 0 : ts }; })
            .sort(function (a, b) { return b.ts - a.ts; })
            .slice(0, 5)
            .forEach(function (j) {
              var id = 'soc:' + j.slug;
              if (isNotifRead(id)) return;
              unreadNotifIds.push(id);
              var match = (window.UV_SEARCH || []).find(function (i) { return i.u === 'society-' + j.slug + '.html'; });
              var name = match ? match.t : j.slug;
              societiesHtml.push(notifItem('%%SOC%%', "You're in! Welcome to " + name, j.ts ? notifTimeAgo(j.ts) : 'Joined', 'society-' + j.slug + '.html'));
            });
        } catch (e) {}

        var upcomingHtml = [];
        try {
          (JSON.parse(window.localStorage.getItem('uv-calendar')) || [])
            .map(function (ev) { return { ev: ev, when: notifWhen(ev.date) }; })
            .filter(function (x) { return x.when; })
            .sort(function (a, b) { return a.ev.date < b.ev.date ? -1 : 1; })
            .slice(0, 5)
            .forEach(function (x) {
              var id = 'cal:' + x.ev.id;
              if (isNotifRead(id)) return;
              unreadNotifIds.push(id);
              var meta = x.when + (x.ev.time ? ' · ' + x.ev.time : '');
              upcomingHtml.push(notifItem('%%CAL%%', x.ev.title, meta, 'profile.html'));
            });
        } catch (e) {}

        var total = messagesHtml.length + societiesHtml.length + upcomingHtml.length;
        notifDot.hidden = total === 0;
        if (notifMarkAll) notifMarkAll.hidden = total === 0;

        if (total === 0) {
          notifList.innerHTML = '<div class="notif-empty">You\'re all caught up — nothing new.</div>';
          return;
        }
        var html = '';
        if (messagesHtml.length) html += '<div class="notif-section-label">Messages</div>' + messagesHtml.join('');
        if (societiesHtml.length) html += '<div class="notif-section-label">Societies</div>' + societiesHtml.join('');
        if (upcomingHtml.length) html += '<div class="notif-section-label">Coming up</div>' + upcomingHtml.join('');
        notifList.innerHTML = html
          .split('%%CHAT%%').join(ICON_CHAT)
          .split('%%SOC%%').join(ICON_SOC)
          .split('%%CAL%%').join(ICON_CAL);
      }

      buildNotifications();
      notifBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        var opening = notifPanel.hidden;
        notifPanel.hidden = !notifPanel.hidden;
        if (opening) buildNotifications();
      });
      document.addEventListener('click', function (e) {
        if (!notifPanel.contains(e.target) && e.target !== notifBtn) notifPanel.hidden = true;
      });
      if (notifMarkAll) {
        notifMarkAll.addEventListener('click', function (e) {
          e.stopPropagation();
          unreadThreadSlugs.forEach(function (slug) {
            try { window.localStorage.setItem('uv-msg-read-' + slug, '1'); } catch (e2) {}
          });
          unreadNotifIds.forEach(markNotifRead);
          buildNotifications();
        });
      }
    }

    // ---- filter chips ----
    // Every chip group actually filters its grid now, not just the Freshers Week one.
    // A chip declares what it's testing for via its own data attribute, checked against the
    // matching data attribute on each card:
    //   .freshers-chip          -> card has [data-freshers]
    //   data-free="1"           -> card has [data-free] (no paid ticket link)
    //   data-venue="Home/Away"  -> card's data-venue matches exactly
    //   data-maxprice="450"     -> card's data-price (a number) is under that
    //   data-cat="X"            -> card's data-cat (space-separated — a card can carry more
    //                              than one, e.g. an event that's both "Social" and "Societies")
    //                              contains that value
    //   none of the above       -> "All" — matches everything
    // Grid is found via an explicit data-filter-grid id when set (robust), falling back to
    // "whatever follows the chips" otherwise. The map page (venueGrid) and the full society
    // directory (socDirGrid) have their own dedicated, more involved filter logic elsewhere
    // (combined with the map's markers / the directory's search box), so they're skipped here.
    function chipMatchesCard(chip, card) {
      if (chip.classList.contains('freshers-chip')) return card.hasAttribute('data-freshers');
      if (chip.dataset.free) return card.hasAttribute('data-free');
      if (chip.dataset.venue) return card.dataset.venue === chip.dataset.venue;
      if (chip.dataset.maxprice) {
        if (card.dataset.price === undefined) return false;
        return parseInt(card.dataset.price, 10) < parseInt(chip.dataset.maxprice, 10);
      }
      if (chip.dataset.cat) {
        var tokens = (card.dataset.cat || '').split(' ');
        return tokens.indexOf(chip.dataset.cat) !== -1;
      }
      return true;
    }
    document.querySelectorAll('.chips').forEach(function (group) {
      if (group.classList.contains('soc-dir-chips') || group.id === 'mapChips' || group.id === 'teamChips') return;
      var grid = group.dataset.filterGrid ? document.getElementById(group.dataset.filterGrid) : group.nextElementSibling;
      if (!grid) return;
      var cards = Array.from(grid.querySelectorAll('.card, .post'));
      group.querySelectorAll('.chip').forEach(function (c) {
        c.addEventListener('click', function () {
          group.querySelectorAll('.chip').forEach(function (x) { x.classList.remove('on'); });
          c.classList.add('on');
          cards.forEach(function (card) { card.hidden = !chipMatchesCard(c, card); });
        });
      });
    });

    // ---- AI prompt -> fill input ----
    document.querySelectorAll('.ai-prompt').forEach(function (p) {
      p.addEventListener('click', function () {
        var inp = document.querySelector('.ai-input input');
        if (inp) { inp.value = p.textContent.trim(); inp.focus(); }
      });
    });

    // ---- RSVP / action button feedback ----
    // Toggles both ways: click once to RSVP, click again to undo (a wrong tap or a
    // change of mind shouldn't be permanent). Remembers itself across reloads:
    // buttons tied to a calendar entry key off title+date (matching the calendar's
    // own id), others use an explicit data-rsvp-key. The venue map's own RSVP
    // buttons (.venue-rsvp) are handled separately below, alongside the pin/count logic.
    function wireRsvpButton(btn) {
      if (btn.classList.contains('venue-rsvp')) return;
      var key = btn.dataset.rsvpKey
        || (btn.dataset.calTitle && btn.dataset.calDate ? btn.dataset.calTitle + '|' + btn.dataset.calDate : null);
      var calId = (btn.dataset.calTitle && btn.dataset.calDate) ? btn.dataset.calTitle + '|' + btn.dataset.calDate : null;
      var beforeLabel = btn.textContent;

      function setDone() {
        btn.dataset.done = '1';
        btn.textContent = btn.dataset.rsvp;
        btn.title = 'Click to cancel';
      }
      function setUndone() {
        btn.dataset.done = '0';
        btn.textContent = beforeLabel;
        btn.removeAttribute('title');
      }

      if (key && isRsvpDone(key)) setDone();

      btn.addEventListener('click', function () {
        if (btn.dataset.done === '1') {
          setUndone();
          if (key) clearRsvpDone(key);
          if (calId) removeFromCalendar(calId);
          return;
        }
        setDone();
        if (key) setRsvpDone(key);
        if (calId) {
          addToCalendar({
            id: calId,
            title: btn.dataset.calTitle,
            date: btn.dataset.calDate,
            time: btn.dataset.calTime || '',
            place: btn.dataset.calPlace || '',
            color: btn.dataset.calColor || 'var(--lime)'
          });
        }
      });
    }
    document.querySelectorAll('[data-rsvp]').forEach(wireRsvpButton);

    // ---- save hearts ----
    function wireSaveHeart(h) {
      var item = {
        id: h.dataset.saveId, title: h.dataset.saveTitle, type: h.dataset.saveType,
        url: h.dataset.saveUrl, meta: h.dataset.saveMeta, color: h.dataset.saveColor
      };
      function applyState(on) {
        h.classList.toggle('on', on);
        h.style.color = on ? 'var(--coral)' : '#fff';
      }
      if (item.id && isSaved(item.id)) applyState(true);
      h.addEventListener('click', function () {
        if (!item.id) { applyState(!h.classList.contains('on')); return; }
        applyState(toggleSaved(item));
      });
    }
    document.querySelectorAll('.save-heart').forEach(wireSaveHeart);

    // ---- save toggles (text/emoji "Save" buttons, e.g. Feed posts, Opportunities) ----
    document.querySelectorAll('.save-toggle').forEach(function (el) {
      var item = {
        id: el.dataset.saveId, title: el.dataset.saveTitle, type: el.dataset.saveType,
        url: el.dataset.saveUrl, meta: el.dataset.saveMeta, color: el.dataset.saveColor
      };
      var defaultLabel = el.textContent.trim();
      var savedLabel = el.dataset.savedLabel || 'Saved ✓';
      function refresh() {
        var saved = isSaved(item.id);
        el.textContent = saved ? savedLabel : defaultLabel;
        el.classList.toggle('saved-active', saved);
      }
      if (item.id) refresh();
      el.addEventListener('click', function () {
        if (!item.id) return;
        toggleSaved(item);
        refresh();
      });
    });

    // ---- saved list (full page + the Account page's preview widget) ----
    var ICON_CLOSE = '<svg fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M6 6l12 12M18 6L6 18"/></svg>';
    var ICON_HEART = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.8 5.6a5.5 5.5 0 00-7.8 0L12 6.6l-1-1a5.5 5.5 0 10-7.8 7.8l1 1L12 22l7.8-7.6 1-1a5.5 5.5 0 000-7.8z"/></svg>';
    var ICON_MONEY = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path stroke-linecap="round" d="M6 9v.01M18 15v.01"/></svg>';
    function savedRowHtml(it, preview) {
      var meta = it.meta ? '<div class="saved-meta">' + it.meta + '</div>' : '';
      var remove = preview ? '' : '<button class="saved-remove" data-id="' + it.id + '" aria-label="Remove from saved">' + ICON_CLOSE + '</button>';
      return '<div class="saved-row">'
        + '<span class="saved-type" style="background:' + (it.color || 'var(--lime)') + '">' + it.type + '</span>'
        + '<a class="saved-body" href="' + it.url + '"><div class="saved-title">' + it.title + '</div>' + meta + '</a>'
        + remove + '</div>';
    }
    document.querySelectorAll('#savedList, #savedPreviewList').forEach(function (list) {
      var preview = list.dataset.preview === '1';
      function render() {
        var items = getSaved();
        if (preview) items = items.slice(0, 3);
        if (!items.length) {
          list.innerHTML = '<div class="saved-empty">' + (preview
            ? 'Nothing saved yet.'
            : 'Nothing saved yet — tap the heart or "Save" on anything across the site and it\'ll show up here.') + '</div>';
          return;
        }
        list.innerHTML = items.map(function (it) { return savedRowHtml(it, preview); }).join('');
        list.querySelectorAll('.saved-remove').forEach(function (btn) {
          btn.addEventListener('click', function () {
            toggleSaved({ id: btn.dataset.id });
            render();
          });
        });
      }
      render();
    });

    // ---- join buttons (societies) ----
    // Cards on the Societies grid carry data-society and unlock a "View society" link once
    // the (simulated) host accepts the request. The Feed's small "trending societies" widget
    // has no data-society — those just toggle Join/Joined with no approval flow.
    function isSocietyJoined(slug) {
      try { return window.localStorage.getItem('uv-joined-' + slug) !== null; } catch (e) { return false; }
    }
    function setSocietyJoined(slug) {
      try { window.localStorage.setItem('uv-joined-' + slug, String(Date.now())); } catch (e) {}
    }
    function refreshJoinButton(b) {
      var slug = b.dataset.society;
      var viewLink = b.parentElement ? b.parentElement.querySelector('.soc-view') : null;
      if (slug && isSocietyJoined(slug)) {
        b.classList.remove('pending', 'accepted');
        b.classList.add('joined');
        b.textContent = 'Joined ✓';
        if (viewLink) viewLink.hidden = false;
      } else {
        b.classList.remove('joined');
        if (viewLink) viewLink.hidden = true;
        if (b.textContent !== 'Requesting…' && b.textContent !== 'Accepted! 🎉') b.textContent = 'Join';
      }
    }
    document.querySelectorAll('.soc-join').forEach(function (b) {
      refreshJoinButton(b);
      b.addEventListener('click', function () {
        var slug = b.dataset.society;
        if (!slug) {
          // trending-societies widget: simple toggle, no approval flow
          b.classList.toggle('joined');
          b.textContent = b.classList.contains('joined') ? 'Joined' : 'Join';
          return;
        }
        if (b.classList.contains('joined') || b.classList.contains('pending')) return;
        b.classList.add('pending');
        b.textContent = 'Requesting…';
        setTimeout(function () {
          // the host accepts the request — a brief "Accepted!" beat before it settles into
          // Joined and unlocks that society's own page (chat, events, kit)
          b.classList.remove('pending');
          b.classList.add('accepted');
          b.textContent = 'Accepted! 🎉';
          setTimeout(function () {
            setSocietyJoined(slug);
            document.querySelectorAll('.soc-join[data-society="' + slug + '"]').forEach(refreshJoinButton);
            renderYourSocieties();
          }, 1100);
        }, 1400);
      });
    });

    // ---- "Your Societies" widget (societies.html) — every joined society, resolved against ----
    // the sitewide search index, which points each of the 269 real ones at its own page.
    function renderYourSocieties() {
      var list = document.getElementById('yourSocList');
      if (!list) return;
      var joined = [];
      try {
        joined = Object.keys(window.localStorage)
          .filter(function (k) { return k.indexOf('uv-joined-') === 0; })
          .map(function (k) {
            var slug = k.replace('uv-joined-', '');
            var ts = parseInt(window.localStorage.getItem(k), 10);
            var match = (window.UV_SEARCH || []).find(function (i) {
              return i.u === slug + '.html';
            });
            return match ? { name: match.t, cat: match.c, url: match.u, ts: isNaN(ts) ? 0 : ts } : null;
          })
          .filter(Boolean)
          .sort(function (a, b) { return b.ts - a.ts; });
      } catch (e) {}

      if (!joined.length) {
        list.innerHTML = '<div class="your-soc-empty">You haven\'t joined any societies yet — join one on the left and it\'ll show up here.</div>';
        return;
      }
      var shown = joined.slice(0, 8);
      list.innerHTML = shown.map(function (s) {
        return '<a class="soc-row" href="' + s.url + '">'
          + '<div class="soc-row-ava" style="background:var(--lime)">' + initialsOf(s.name) + '</div>'
          + '<div class="soc-row-body"><div class="soc-row-name">' + s.name + '</div>'
          + '<div class="soc-row-cat">' + s.cat + '</div></div></a>';
      }).join('');
      if (joined.length > shown.length) {
        list.innerHTML += '<div class="your-soc-more">+' + (joined.length - shown.length) + ' more</div>';
      }
    }
    renderYourSocieties();

    // ---- flatmates: post a room (area/price/description/photo) + a "View" modal ----
    var flatGrid = document.getElementById('flatGrid');
    if (flatGrid) {
      function getUserFlats() {
        try { return JSON.parse(window.localStorage.getItem('uv-flatmates')) || []; } catch (e) { return []; }
      }
      function saveUserFlats(items) {
        try { window.localStorage.setItem('uv-flatmates', JSON.stringify(items)); } catch (e) {}
      }
      function posterName() {
        try {
          var u = JSON.parse(window.localStorage.getItem('uv-user'));
          if (u && u.name) return u.name;
        } catch (e) {}
        return 'You';
      }
      function renderYourListings() {
        var list = document.getElementById('yourListingsList');
        if (!list) return;
        var items = getUserFlats().slice().reverse();
        if (!items.length) {
          list.innerHTML = '<div class="your-soc-empty">You haven\'t posted a room yet — post one and it\'ll show up here.</div>';
          return;
        }
        list.innerHTML = items.map(function (it) {
          var shortDesc = it.desc.length > 60 ? it.desc.slice(0, 57) + '…' : it.desc;
          return '<a class="soc-row" href="javascript:void(0)" data-flat-target="flat-' + it.id + '">'
            + '<div class="soc-row-ava" style="background:var(--lime)">🏠</div>'
            + '<div class="soc-row-body"><div class="soc-row-name">£' + it.price + ' pcm · ' + it.area + '</div>'
            + '<div class="soc-row-cat">' + shortDesc + '</div></div></a>';
        }).join('');
        list.querySelectorAll('[data-flat-target]').forEach(function (row) {
          row.addEventListener('click', function () {
            var card = document.getElementById(row.dataset.flatTarget);
            if (!card) return;
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            card.classList.add('soc-row-flash');
            setTimeout(function () { card.classList.remove('soc-row-flash'); }, 2200);
          });
        });
      }
      function flatCardEl(item) {
        var wrap = document.createElement('div');
        // .photos is the current (array) shape; .photo is kept as a fallback for older saved listings
        var photos = item.photos && item.photos.length ? item.photos : (item.photo ? [item.photo] : []);
        var mediaInner = photos.length
          ? '<div class="flat-gallery">' + photos.map(function (p) { return '<img src="' + p + '" alt="">'; }).join('') + '</div>'
            + (photos.length > 1 ? '<span class="flat-gallery-count">' + photos.length + ' photos</span>' : '')
          : '<span class="emoji">🏠</span>';
        var saveId = 'flatmate:' + item.id;
        var saveTitle = item.area + ' — Spare room';
        var saveMeta = '£' + item.price + ' pcm · ' + item.area;
        wrap.innerHTML = '<div class="card" id="flat-' + item.id + '" data-cat="' + item.area + '" data-price="' + item.price + '">'
          + '<div class="card-media" style="background:linear-gradient(135deg,var(--lime),var(--sky))">'
          + '<span class="chip-cat">' + item.area + '</span>'
          + '<button type="button" class="flat-delete-btn" aria-label="Delete this listing">' + ICON_CLOSE + '</button>'
          + '<button class="save-heart" data-save-id="' + saveId + '" data-save-title="' + saveTitle + '" data-save-type="Flatmate" '
          + 'data-save-url="flatmates.html" data-save-meta="' + saveMeta + '" data-save-color="var(--sky)">' + ICON_HEART + '</button>'
          + mediaInner + '</div>'
          + '<div class="card-body"><h3>Spare room</h3>'
          + '<div class="by">Posted by ' + item.poster + ' · just now</div>'
          + '<p>' + item.desc + '</p>'
          + '<div class="card-info"><div class="bit">' + ICON_MONEY + ' £' + item.price + ' pcm</div></div>'
          + '<div class="card-foot">'
          + '<span class="stat">New listing</span>'
          + '<div class="post-actions">'
          + '<button type="button" class="pill flat-view-btn">View</button>'
          + '<button class="pill primary" data-rsvp="Interest sent ✓" data-rsvp-key="flatmate-' + item.id + '">Show interest</button>'
          + '</div></div>'
          + '<div class="card-foot flat-delete-row" hidden>'
          + '<span class="stat">Delete this listing?</span>'
          + '<div class="post-actions">'
          + '<button type="button" class="pill flat-delete-cancel">Cancel</button>'
          + '<button type="button" class="pill coral flat-delete-confirm">Delete</button>'
          + '</div></div></div></div>';
        return wrap.firstElementChild;
      }
      function wireNewFlatCard(card, item) {
        var heart = card.querySelector('.save-heart');
        if (heart) wireSaveHeart(heart);
        var rsvpBtn = card.querySelector('[data-rsvp]');
        if (rsvpBtn) wireRsvpButton(rsvpBtn);
        var viewBtn = card.querySelector('.flat-view-btn');
        if (viewBtn) viewBtn.addEventListener('click', function () { openFlatModal(card); });

        // ---- delete this listing, with a real confirmation step first ----
        var feet = card.querySelectorAll('.card-foot');
        var defaultFoot = feet[0], confirmFoot = feet[1];
        var deleteBtn = card.querySelector('.flat-delete-btn');
        if (deleteBtn && defaultFoot && confirmFoot) {
          deleteBtn.addEventListener('click', function () {
            defaultFoot.hidden = true;
            confirmFoot.hidden = false;
          });
          var cancelBtn = confirmFoot.querySelector('.flat-delete-cancel');
          if (cancelBtn) {
            cancelBtn.addEventListener('click', function () {
              confirmFoot.hidden = true;
              defaultFoot.hidden = false;
            });
          }
          var confirmBtn = confirmFoot.querySelector('.flat-delete-confirm');
          if (confirmBtn) {
            confirmBtn.addEventListener('click', function () {
              saveUserFlats(getUserFlats().filter(function (i) { return i.id !== item.id; }));
              card.remove();
              renderYourListings();
            });
          }
        }
      }

      // restore any previously-posted rooms, most recent first
      getUserFlats().slice().reverse().forEach(function (item) {
        var card = flatCardEl(item);
        flatGrid.insertBefore(card, flatGrid.firstChild);
        wireNewFlatCard(card, item);
      });
      renderYourListings();

      // ---- post a room ----
      var postRoomBtn = document.getElementById('postRoomBtn');
      var flatAddForm = document.getElementById('flatAddForm');
      if (postRoomBtn && flatAddForm) {
        postRoomBtn.addEventListener('click', function () { flatAddForm.hidden = !flatAddForm.hidden; });

        var flatCancelBtn = document.getElementById('flatCancelBtn');
        if (flatCancelBtn) flatCancelBtn.addEventListener('click', function () { flatAddForm.hidden = true; });

        var photoInput = document.getElementById('flatFPhoto');
        var photoThumbs = document.getElementById('flatPhotoThumbs');
        var currentPhotos = [];

        function renderPhotoThumbs() {
          if (!photoThumbs) return;
          photoThumbs.innerHTML = currentPhotos.map(function (src, i) {
            return '<div class="flat-photo-thumb"><img src="' + src + '" alt="">'
              + '<button type="button" data-idx="' + i + '" aria-label="Remove photo">' + ICON_CLOSE + '</button></div>';
          }).join('');
          photoThumbs.querySelectorAll('button').forEach(function (btn) {
            btn.addEventListener('click', function () {
              currentPhotos.splice(parseInt(btn.dataset.idx, 10), 1);
              renderPhotoThumbs();
            });
          });
        }
        if (photoInput) {
          photoInput.addEventListener('change', function () {
            var files = Array.from(photoInput.files || []);
            files.forEach(function (file) {
              downscaleImage(file, 480, function (dataUrl) {
                currentPhotos.push(dataUrl);
                renderPhotoThumbs();
              });
            });
            photoInput.value = '';
          });
        }

        var flatSaveBtn = document.getElementById('flatSaveBtn');
        var flatFormError = document.getElementById('flatFormError');
        if (flatSaveBtn) {
          flatSaveBtn.addEventListener('click', function () {
            var areaInput = document.getElementById('flatFArea');
            var priceInput = document.getElementById('flatFPrice');
            var descInput = document.getElementById('flatFDesc');
            var area = areaInput.value, price = priceInput.value.trim(), desc = descInput.value.trim();
            if (!area || !price || !desc) {
              if (flatFormError) flatFormError.hidden = false;
              return;
            }
            if (flatFormError) flatFormError.hidden = true;
            var item = {
              id: 'user-' + Date.now(), area: area, price: price, desc: desc,
              photos: currentPhotos.slice(), poster: posterName()
            };
            var items = getUserFlats();
            items.push(item);
            saveUserFlats(items);

            var card = flatCardEl(item);
            flatGrid.insertBefore(card, flatGrid.firstChild);
            wireNewFlatCard(card, item);
            renderYourListings();

            areaInput.value = ''; priceInput.value = ''; descInput.value = '';
            currentPhotos = []; if (photoInput) photoInput.value = '';
            renderPhotoThumbs();
            flatAddForm.hidden = true;
          });
        }
      }

      // ---- view modal: reads whatever the card already shows, so it always matches ----
      var flatModalOverlay = document.getElementById('flatModalOverlay');
      function openFlatModal(card) {
        if (!flatModalOverlay) return;
        var media = card.querySelector('.card-media');
        var imgs = media ? Array.from(media.querySelectorAll('img')) : [];
        var emoji = media ? media.querySelector('.emoji') : null;
        var modalMedia = document.getElementById('flatModalMedia');
        if (imgs.length) {
          modalMedia.innerHTML = '<div class="flat-gallery">'
            + imgs.map(function (i) { return '<img src="' + i.src + '" alt="">'; }).join('')
            + '</div>' + (imgs.length > 1 ? '<span class="flat-gallery-count">' + imgs.length + ' photos</span>' : '');
        } else {
          modalMedia.innerHTML = '<span class="emoji">' + (emoji ? emoji.textContent : '🏠') + '</span>';
        }
        document.getElementById('flatModalArea').textContent = card.querySelector('.chip-cat').textContent;
        document.getElementById('flatModalTitle').textContent = card.querySelector('h3').textContent;
        document.getElementById('flatModalPoster').textContent = card.querySelector('.by').textContent;
        document.getElementById('flatModalDesc').textContent = card.querySelector('.card-body p').textContent;
        var bits = card.querySelectorAll('.card-info .bit');
        document.getElementById('flatModalPrice').textContent = bits[0] ? bits[0].textContent.trim() : '';
        var availWrap = document.getElementById('flatModalAvailWrap');
        if (bits[1]) {
          availWrap.hidden = false;
          document.getElementById('flatModalAvail').textContent = bits[1].textContent.trim();
        } else if (availWrap) {
          availWrap.hidden = true;
        }
        var modalMsgBtn = document.getElementById('flatModalMessage');
        var realMsgBtn = card.querySelector('[data-rsvp]');
        modalMsgBtn.textContent = realMsgBtn ? realMsgBtn.textContent : 'Show interest';
        modalMsgBtn.onclick = function () {
          if (realMsgBtn) realMsgBtn.click();
          modalMsgBtn.textContent = realMsgBtn ? realMsgBtn.textContent : 'Show interest';
        };
        flatModalOverlay.hidden = false;
      }
      function closeFlatModal() { flatModalOverlay.hidden = true; }
      var flatModalClose = document.getElementById('flatModalClose');
      if (flatModalClose) flatModalClose.addEventListener('click', closeFlatModal);
      if (flatModalOverlay) {
        flatModalOverlay.addEventListener('click', function (e) {
          if (e.target === flatModalOverlay) closeFlatModal();
        });
        document.addEventListener('keydown', function (e) {
          if (e.key === 'Escape' && !flatModalOverlay.hidden) closeFlatModal();
        });
      }
      document.querySelectorAll('.flat-view-btn').forEach(function (btn) {
        btn.addEventListener('click', function () { openFlatModal(btn.closest('.card')); });
      });
    }

    // ---- full society directory: search + category filter, combined (societies.html) ----
    var socDirGrid = document.getElementById('socDirGrid');
    if (socDirGrid) {
      var socDirRows = Array.from(socDirGrid.querySelectorAll('.soc-row'));
      var socDirSearch = document.getElementById('socDirSearch');
      var socDirClear = document.getElementById('socDirSearchClear');
      var socDirMatchCount = document.getElementById('socDirMatchCount');
      var socDirEmpty = document.getElementById('socDirEmpty');
      var socDirEmptyQuery = document.getElementById('socDirEmptyQuery');
      var socDirChips = document.querySelectorAll('.soc-dir-chips .chip');
      var activeCat = '';

      function applySocDirFilter() {
        var q = (socDirSearch.value || '').trim().toLowerCase();
        if (socDirClear) socDirClear.classList.toggle('show', q.length > 0);
        var visible = 0;
        socDirRows.forEach(function (row) {
          var matchesCat = !activeCat || row.dataset.cat === activeCat;
          var matchesQuery = !q || row.dataset.search.indexOf(q) !== -1;
          var show = matchesCat && matchesQuery;
          row.hidden = !show;
          if (show) visible++;
        });
        if (socDirMatchCount) socDirMatchCount.textContent = q ? (visible + (visible === 1 ? ' match' : ' matches')) : '';
        if (socDirEmpty) socDirEmpty.hidden = visible > 0;
        if (socDirEmptyQuery) socDirEmptyQuery.textContent = socDirSearch.value.trim();
      }
      if (socDirSearch) {
        socDirSearch.addEventListener('input', applySocDirFilter);
        if (socDirClear) {
          socDirClear.addEventListener('click', function () {
            socDirSearch.value = '';
            applySocDirFilter();
            socDirSearch.focus();
          });
        }
      }
      socDirChips.forEach(function (chip) {
        chip.addEventListener('click', function () {
          activeCat = chip.dataset.cat || '';
          applySocDirFilter();
        });
      });

    }

    // ---- society chat: post your own message into the group thread (a real society's own page) ----
    var socChatInput = document.querySelector('.soc-chat-field');
    var socChatBody = document.querySelector('.soc-chat');
    function sendSocietyChat(text) {
      if (!text || !socChatBody) return;
      var m = document.createElement('div');
      m.className = 'soc-msg self';
      m.innerHTML = '<div class="soc-msg-ava" style="background:var(--lime);color:var(--ink)">FW</div>'
        + '<div class="soc-msg-body"><div class="soc-msg-head"><span class="soc-msg-name">You</span>'
        + '<span class="soc-msg-time">Just now</span></div><div class="soc-msg-text">' + text + '</div></div>';
      socChatBody.appendChild(m);
      socChatBody.scrollTop = socChatBody.scrollHeight;
    }
    if (socChatInput) {
      var socChatSend = document.querySelector('.soc-chat-send');
      socChatInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') { sendSocietyChat(socChatInput.value.trim()); socChatInput.value = ''; }
      });
      if (socChatSend) {
        socChatSend.addEventListener('click', function () {
          sendSocietyChat(socChatInput.value.trim());
          socChatInput.value = '';
        });
      }
    }

    // ---- Men's Hockey Club: pick a team, get that team's own chat ----
    // A prototype example of sports clubs having 1st/2nd/3rd/4th teams, each with its own
    // group — kept to just this one club rather than every society. Only runs on that page,
    // since #teamChips only exists there.
    var teamChips = document.getElementById('teamChips');
    if (teamChips) {
      var teamChatWidget = document.getElementById('teamChatWidget');
      var teamChatTitle = document.getElementById('teamChatTitle');
      var teamChatBody = document.getElementById('teamChatBody');
      var teamChatField = document.getElementById('teamChatField');
      var teamChatSend = document.getElementById('teamChatSend');
      var TEAM_STORAGE_KEY = 'uv-hockey-team';

      function teamChatKey(team) { return 'uv-team-chat-' + team; }
      function getTeamChat(team) {
        try { return JSON.parse(window.localStorage.getItem(teamChatKey(team)) || '[]'); } catch (e) { return []; }
      }
      function saveTeamChat(team, msgs) {
        try { window.localStorage.setItem(teamChatKey(team), JSON.stringify(msgs)); } catch (e) {}
      }
      function renderTeamMsg(m) {
        if (m.self) {
          return '<div class="soc-msg self"><div class="soc-msg-ava" style="background:var(--lime);color:var(--ink)">FW</div>'
            + '<div class="soc-msg-body"><div class="soc-msg-head"><span class="soc-msg-name">You</span>'
            + '<span class="soc-msg-time">' + (m.time || 'Just now') + '</span></div>'
            + '<div class="soc-msg-text">' + m.text + '</div></div></div>';
        }
        return '<div class="soc-msg"><div class="soc-msg-ava" style="background:var(--sky)">' + initialsOf(m.name) + '</div>'
          + '<div class="soc-msg-body"><div class="soc-msg-head"><span class="soc-msg-name">' + m.name + '</span></div>'
          + '<div class="soc-msg-text">' + m.text + '</div></div></div>';
      }
      function openTeam(team) {
        teamChips.querySelectorAll('.chip').forEach(function (c) { c.classList.toggle('on', c.dataset.team === team); });
        teamChatTitle.textContent = team + ' chat';
        var msgs = getTeamChat(team);
        if (!msgs.length) {
          msgs = [{ name: team, text: 'Welcome to the ' + team + ' chat — say hi 👋' }];
          saveTeamChat(team, msgs);
        }
        teamChatBody.innerHTML = msgs.map(renderTeamMsg).join('');
        teamChatBody.scrollTop = teamChatBody.scrollHeight;
        teamChatWidget.hidden = false;
        try { window.localStorage.setItem(TEAM_STORAGE_KEY, team); } catch (e) {}
      }
      teamChips.querySelectorAll('.chip').forEach(function (c) {
        c.addEventListener('click', function () { openTeam(c.dataset.team); });
      });
      function sendTeamChat(text) {
        var activeChip = teamChips.querySelector('.chip.on');
        var team = activeChip ? activeChip.dataset.team : null;
        if (!team || !text) return;
        var msgs = getTeamChat(team);
        msgs.push({ text: text, self: true, time: 'Just now' });
        saveTeamChat(team, msgs);
        openTeam(team);
      }
      if (teamChatField) {
        teamChatField.addEventListener('keydown', function (e) {
          if (e.key === 'Enter') { sendTeamChat(teamChatField.value.trim()); teamChatField.value = ''; }
        });
      }
      if (teamChatSend) {
        teamChatSend.addEventListener('click', function () {
          sendTeamChat(teamChatField.value.trim());
          teamChatField.value = '';
        });
      }
      var savedTeam = null;
      try { savedTeam = window.localStorage.getItem(TEAM_STORAGE_KEY); } catch (e) {}
      if (savedTeam) openTeam(savedTeam);
    }

    // ---- venue map (clubs & bars) ----
    var mapEl = document.getElementById('venueMap');
    if (mapEl && window.L) {
      var defaultCenter = [51.4855, -3.1795], defaultZoom = 14.5;
      var venueMap = L.map('venueMap', { scrollWheelZoom: false }).setView(defaultCenter, defaultZoom);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
      }).addTo(venueMap);

      // "I'm going tonight" state per venue, remembered for the session
      function goingKey(name) { return 'uv-going-' + name; }
      function isGoing(name) {
        try { return window.sessionStorage.getItem(goingKey(name)) === '1'; } catch (e) { return false; }
      }
      function setGoing(name) {
        try { window.sessionStorage.setItem(goingKey(name), '1'); } catch (e) {}
      }
      function clearGoing(name) {
        try { window.sessionStorage.removeItem(goingKey(name)); } catch (e) {}
      }

      // pin/badge colour by exact going count — green under 20, orange 20-69, red 70+
      function goingColor(n) {
        if (n < 20) return '#2ED573';
        if (n < 70) return '#FFA502';
        return '#FF4757';
      }

      // colour-coded teardrop pin
      function pinIcon(color) {
        var svg = '<svg width="28" height="40" viewBox="0 0 28 40" xmlns="http://www.w3.org/2000/svg">'
          + '<path d="M14 0C6.3 0 0 6.3 0 14c0 10.5 14 26 14 26s14-15.5 14-26C28 6.3 21.7 0 14 0z" fill="' + color + '"/>'
          + '<circle cx="14" cy="14" r="5.5" fill="#fff"/></svg>';
        return L.divIcon({ html: svg, className: 'venue-pin', iconSize: [28, 40], iconAnchor: [14, 40], popupAnchor: [0, -36] });
      }

      var venues = [];
      document.querySelectorAll('.venue-card').forEach(function (card) {
        var lat = parseFloat(card.dataset.lat), lng = parseFloat(card.dataset.lng);
        var name = card.dataset.name, cat = card.dataset.cat, area = card.dataset.area || cat;
        var baseGoing = parseInt(card.dataset.going, 10) || 0;
        var ticketUrl = card.dataset.ticketUrl, ticketLabel = card.dataset.ticketLabel;
        var pinColor = card.dataset.pinColor || '';
        var fixtureDate = card.dataset.fixtureDate || '', fixtureTime = card.dataset.fixtureTime || '';
        var isFixture = !!fixtureDate;
        var goingWord = isFixture ? 'going' : 'going tonight';
        var rsvpWord = isFixture ? "I'm going" : "I'm going tonight";
        if (isNaN(lat) || isNaN(lng)) return;

        function currentCount() { return baseGoing + (isGoing(name) ? 1 : 0); }
        function currentColor() { return pinColor || goingColor(currentCount()); }

        function addVenueToCalendar() {
          addToCalendar({
            id: 'venue|' + name,
            title: name,
            date: isFixture ? fixtureDate : calIsoDate(new Date()),
            time: isFixture ? fixtureTime : 'Tonight',
            place: area,
            color: currentColor()
          });
        }

        function popupHtml() {
          var going = isGoing(name), count = currentCount();
          var ticketHtml = ticketUrl
            ? '<a class="popup-tickets" href="' + ticketUrl + '" target="_blank" rel="noopener">' + ticketLabel + ' ↗</a>'
            : '';
          return '<strong>' + name + '</strong><span class="popup-cat">' + cat + '</span>'
            + '<div class="popup-going"><i class="busy-dot" style="background:' + currentColor() + '"></i>' + count + ' ' + goingWord + '</div>'
            + ticketHtml
            + '<button class="pill primary popup-rsvp"' + (going ? ' title="Click to cancel"' : '') + '>'
            + (going ? "You're in 🎉" : rsvpWord) + '</button>';
        }

        var marker = L.marker([lat, lng], { icon: pinIcon(currentColor()) }).addTo(venueMap).bindPopup(popupHtml());

        var cardBtn = card.querySelector('.venue-rsvp');
        var cardBtnBeforeLabel = cardBtn ? cardBtn.textContent : '';
        var dotEl = card.querySelector('.busy-dot');
        var numEl = card.querySelector('.going-count');

        function refreshUI() {
          var count = currentCount(), color = currentColor();
          marker.setIcon(pinIcon(color));
          marker.setPopupContent(popupHtml());
          if (dotEl) dotEl.style.background = color;
          if (numEl) numEl.textContent = count;
        }

        marker.on('popupopen', function (e) {
          var popupBtn = e.popup.getElement().querySelector('.popup-rsvp');
          if (popupBtn) {
            popupBtn.addEventListener('click', function () {
              if (isGoing(name)) {
                clearGoing(name);
                removeFromCalendar('venue|' + name);
              } else {
                setGoing(name);
                addVenueToCalendar();
              }
              refreshUI();
              syncCardButton();
            });
          }
        });

        var locateBtn = card.querySelector('.locate-btn');
        if (locateBtn) {
          locateBtn.addEventListener('click', function () {
            venueMap.flyTo([lat, lng], 17);
            marker.openPopup();
          });
        }

        function syncCardButton() {
          if (!cardBtn) return;
          var going = isGoing(name);
          cardBtn.dataset.done = going ? '1' : '0';
          cardBtn.textContent = going ? cardBtn.dataset.rsvp : cardBtnBeforeLabel;
          if (going) cardBtn.title = 'Click to cancel';
          else cardBtn.removeAttribute('title');
        }
        syncCardButton();
        if (cardBtn) {
          cardBtn.addEventListener('click', function () {
            if (isGoing(name)) {
              clearGoing(name);
              removeFromCalendar('venue|' + name);
            } else {
              setGoing(name);
              addVenueToCalendar();
            }
            refreshUI();
            syncCardButton();
          });
        }

        venues.push({ card: card, marker: marker, lat: lat, lng: lng, search: card.dataset.search || '', cat: card.dataset.cat || '' });
      });

      // ---- search + category chips: filter cards & pins together, zoom the map to the matches ----
      var searchInput = document.getElementById('venueSearch');
      var clearBtn = document.getElementById('venueSearchClear');
      var matchCount = document.getElementById('venueMatchCount');
      var emptyState = document.getElementById('venueEmpty');
      var emptyQuery = document.getElementById('venueEmptyQuery');
      var mapChips = document.querySelectorAll('#mapChips .chip');
      var activeCat = '';

      function runSearch() {
        var q = (searchInput.value || '').trim().toLowerCase();
        if (clearBtn) clearBtn.classList.toggle('show', q.length > 0);
        var visible = [];
        venues.forEach(function (v) {
          var match = (!q || v.search.indexOf(q) !== -1) && (!activeCat || v.cat === activeCat);
          v.card.hidden = !match;
          if (match) {
            if (!venueMap.hasLayer(v.marker)) v.marker.addTo(venueMap);
            visible.push(v);
          } else if (venueMap.hasLayer(v.marker)) {
            venueMap.removeLayer(v.marker);
          }
        });
        if (matchCount) matchCount.textContent = q ? (visible.length + (visible.length === 1 ? ' match' : ' matches')) : '';
        if (emptyState) emptyState.hidden = visible.length > 0;
        if (emptyQuery) emptyQuery.textContent = searchInput.value.trim();
        if (q && visible.length) {
          venueMap.flyToBounds(L.latLngBounds(visible.map(function (v) { return [v.lat, v.lng]; })), { padding: [50, 50], maxZoom: 16 });
        } else if (!q) {
          venueMap.flyTo(defaultCenter, defaultZoom);
        }
      }
      if (searchInput) {
        searchInput.addEventListener('input', runSearch);
        if (clearBtn) {
          clearBtn.addEventListener('click', function () {
            searchInput.value = '';
            runSearch();
            searchInput.focus();
          });
        }
      }
      mapChips.forEach(function (chip) {
        chip.addEventListener('click', function () {
          mapChips.forEach(function (x) { x.classList.remove('on'); });
          chip.classList.add('on');
          activeCat = chip.dataset.cat || '';
          runSearch();
        });
      });
    }

    // ---- profile: editable name, photo, course, year, bio ----
    var profileEditForm = document.getElementById('profileEditForm');
    if (profileEditForm) {
      var profileAvatar = document.getElementById('profileAvatar');
      var profileName = document.getElementById('profileName');
      var profileSub = document.getElementById('profileSub');
      var profileBio = document.getElementById('profileBio');
      var defaultName = profileName.textContent;
      var defaultSubParts = profileSub.textContent.split(' · '); // "1st year · Course · Cardiff University"

      function applyProfileDisplay(u) {
        var name = (u && u.name) || defaultName;
        profileName.textContent = name;
        if (u && u.photo) {
          profileAvatar.innerHTML = '<img src="' + u.photo + '" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">';
        } else {
          profileAvatar.textContent = initialsOf(name);
        }
        var year = (u && u.year) || defaultSubParts[0] || '1st year';
        var course = (u && u.course) || defaultSubParts[1] || 'Computer Science';
        profileSub.textContent = year + ' · ' + course + ' · Cardiff University';
        if (u && u.bio) {
          profileBio.textContent = u.bio;
          profileBio.hidden = false;
        } else {
          profileBio.hidden = true;
        }
        // keep the sidebar nav avatar in sync too
        var navAvatar = document.querySelector('.rail-avatar[href="profile.html"]');
        if (navAvatar) {
          if (u && u.photo) {
            navAvatar.innerHTML = '<img src="' + u.photo + '" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">';
          } else if (u && u.name) {
            navAvatar.textContent = initialsOf(u.name);
          }
        }
      }
      applyProfileDisplay(getUser());

      var editProfileBtn = document.getElementById('editProfileBtn');
      var peName = document.getElementById('peName');
      var pePhoto = document.getElementById('pePhoto');
      var pePhotoPreview = document.getElementById('pePhotoPreview');
      var pePhotoPreviewImg = document.getElementById('pePhotoPreviewImg');
      var pePhotoRemove = document.getElementById('pePhotoRemove');
      var peCourse = document.getElementById('peCourse');
      var peYear = document.getElementById('peYear');
      var peBio = document.getElementById('peBio');
      var peFormError = document.getElementById('peFormError');
      var peCancelBtn = document.getElementById('peCancelBtn');
      var peSaveBtn = document.getElementById('peSaveBtn');
      var editingPhoto = '';

      if (editProfileBtn) {
        editProfileBtn.addEventListener('click', function () {
          var u = getUser() || {};
          peName.value = u.name || defaultName;
          peCourse.value = u.course || defaultSubParts[1] || '';
          peYear.value = u.year || defaultSubParts[0] || '1st year';
          peBio.value = u.bio || '';
          editingPhoto = u.photo || '';
          if (editingPhoto) { pePhotoPreviewImg.src = editingPhoto; pePhotoPreview.hidden = false; }
          else { pePhotoPreview.hidden = true; }
          if (peFormError) peFormError.hidden = true;
          profileEditForm.hidden = false;
        });
      }
      if (peCancelBtn) peCancelBtn.addEventListener('click', function () { profileEditForm.hidden = true; });
      if (pePhoto) {
        pePhoto.addEventListener('change', function () {
          var file = pePhoto.files && pePhoto.files[0];
          if (!file) return;
          downscaleImage(file, 300, function (dataUrl) {
            editingPhoto = dataUrl;
            pePhotoPreviewImg.src = dataUrl;
            pePhotoPreview.hidden = false;
          });
        });
      }
      if (pePhotoRemove) {
        pePhotoRemove.addEventListener('click', function () {
          editingPhoto = '';
          pePhoto.value = '';
          pePhotoPreview.hidden = true;
        });
      }
      if (peSaveBtn) {
        peSaveBtn.addEventListener('click', function () {
          var name = peName.value.trim();
          if (!name) {
            if (peFormError) peFormError.hidden = false;
            return;
          }
          if (peFormError) peFormError.hidden = true;
          var u = getUser() || {};
          u.name = name;
          u.course = peCourse.value.trim();
          u.year = peYear.value;
          u.bio = peBio.value.trim();
          u.photo = editingPhoto;
          saveUser(u);
          applyProfileDisplay(u);
          profileEditForm.hidden = true;
        });
      }
    }

    // ---- profile stat strip: numbers respond to real joins/RSVPs, on top of the starting baseline ----
    var statSocieties = document.getElementById('statSocieties');
    if (statSocieties) {
      var joinedCount = 0;
      try { joinedCount = Object.keys(window.localStorage).filter(function (k) { return k.indexOf('uv-joined-') === 0; }).length; } catch (e) {}
      statSocieties.textContent = (parseInt(statSocieties.dataset.baseline, 10) || 0) + joinedCount;
    }
    var statEvents = document.getElementById('statEvents');
    if (statEvents) {
      var calCount = 0;
      try { calCount = (JSON.parse(window.localStorage.getItem('uv-calendar')) || []).length; } catch (e) {}
      statEvents.textContent = (parseInt(statEvents.dataset.baseline, 10) || 0) + calCount;
    }

    // ---- my calendar (profile page) — month grid built from everything RSVP'd across the site ----
    var calGrid = document.getElementById('calGrid');
    if (calGrid) {
      var calMonthLabel = document.getElementById('calMonthLabel');
      var calPrevBtn = document.getElementById('calPrev');
      var calNextBtn = document.getElementById('calNext');
      var calDayDetail = document.getElementById('calDayDetail');
      var calDayDetailTitle = document.getElementById('calDayDetailTitle');
      var calDayEvents = document.getElementById('calDayEvents');

      var MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      var DOW = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
      var calToday = new Date();
      var viewYear = calToday.getFullYear(), viewMonth = calToday.getMonth();
      var selectedDate = calIsoDate(calToday);

      function entriesFor(dateStr) {
        return getCalendar().filter(function (e) { return e.date === dateStr; });
      }

      function showDayDetail(dateStr) {
        var entries = entriesFor(dateStr);
        var dateObj = new Date(dateStr + 'T00:00:00');
        calDayDetailTitle.textContent = dateObj.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
        if (!entries.length) {
          calDayEvents.innerHTML = '<div class="cal-empty-msg">Nothing here yet — RSVP to an event, workshop or a night out and it\'ll show up on this day.</div>';
        } else {
          calDayEvents.innerHTML = entries.map(function (e) {
            return '<div class="cal-entry"><span class="cal-entry-dot" style="background:' + (e.color || 'var(--lime)') + '"></span>'
              + '<div class="cal-entry-body"><div class="cal-entry-title">' + e.title + '</div>'
              + '<div class="cal-entry-meta">' + (e.time ? e.time + (e.place ? ' · ' : '') : '') + (e.place || '') + '</div></div></div>';
          }).join('');
        }
        calDayDetail.hidden = false;
      }

      function renderCalendar() {
        calMonthLabel.textContent = MONTH_NAMES[viewMonth] + ' ' + viewYear;
        var html = DOW.map(function (d) { return '<div class="cal-dow">' + d + '</div>'; }).join('');
        var firstOfMonth = new Date(viewYear, viewMonth, 1);
        var startWeekday = (firstOfMonth.getDay() + 6) % 7; // Monday = 0
        var daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate();
        var todayStr = calIsoDate(calToday);

        for (var i = 0; i < startWeekday; i++) html += '<div class="cal-cell empty"></div>';
        for (var d = 1; d <= daysInMonth; d++) {
          var dStr = viewYear + '-' + calPad(viewMonth + 1) + '-' + calPad(d);
          var dayEntries = entriesFor(dStr);
          var cls = 'cal-cell';
          if (dStr === todayStr) cls += ' today';
          if (dStr === selectedDate) cls += ' selected';
          var shown = dayEntries.slice(0, 2);
          var extra = dayEntries.length - shown.length;
          var chips = shown.map(function (e) {
            return '<span class="cal-chip" style="--chip-color:' + (e.color || 'var(--lime)') + '" title="' + e.title + (e.time ? ' · ' + e.time : '') + '">' + e.title + '</span>';
          }).join('') + (extra > 0 ? '<span class="cal-chip-more">+' + extra + ' more</span>' : '');
          html += '<button type="button" class="' + cls + '" data-date="' + dStr + '"><span class="cal-daynum">' + d + '</span>'
            + (dayEntries.length ? '<span class="cal-chips">' + chips + '</span>' : '') + '</button>';
        }
        calGrid.innerHTML = html;

        calGrid.querySelectorAll('.cal-cell:not(.empty)').forEach(function (cell) {
          cell.addEventListener('click', function () {
            selectedDate = cell.dataset.date;
            renderCalendar();
            showDayDetail(selectedDate);
          });
        });
      }

      if (calPrevBtn) {
        calPrevBtn.addEventListener('click', function () {
          viewMonth--; if (viewMonth < 0) { viewMonth = 11; viewYear--; }
          renderCalendar();
        });
      }
      if (calNextBtn) {
        calNextBtn.addEventListener('click', function () {
          viewMonth++; if (viewMonth > 11) { viewMonth = 0; viewYear++; }
          renderCalendar();
        });
      }

      renderCalendar();
      showDayDetail(selectedDate);

      // ---- add your own event ----
      var calAddBtn = document.getElementById('calAddBtn');
      var calAddForm = document.getElementById('calAddForm');
      if (calAddBtn && calAddForm) {
        calAddBtn.addEventListener('click', function () { calAddForm.hidden = !calAddForm.hidden; });

        var cancelBtn = document.getElementById('calCancelBtn');
        if (cancelBtn) cancelBtn.addEventListener('click', function () { calAddForm.hidden = true; });

        var selectedColor = 'var(--lime)';
        document.querySelectorAll('.cal-color-swatch').forEach(function (sw) {
          sw.addEventListener('click', function () {
            document.querySelectorAll('.cal-color-swatch').forEach(function (s) { s.classList.remove('active'); });
            sw.classList.add('active');
            selectedColor = sw.dataset.color;
          });
        });

        var saveBtn = document.getElementById('calSaveBtn');
        var formError = document.getElementById('calFormError');
        if (saveBtn) {
          saveBtn.addEventListener('click', function () {
            var titleInput = document.getElementById('calFTitle');
            var dateInput = document.getElementById('calFDate');
            var timeInput = document.getElementById('calFTime');
            var placeInput = document.getElementById('calFPlace');
            var title = titleInput.value.trim(), date = dateInput.value;
            if (!title || !date) {
              if (formError) formError.hidden = false;
              return;
            }
            if (formError) formError.hidden = true;
            addToCalendar({
              id: 'custom-' + Date.now(),
              title: title, date: date, time: timeInput.value.trim(),
              place: placeInput.value.trim(), color: selectedColor
            });
            titleInput.value = ''; dateInput.value = ''; timeInput.value = ''; placeInput.value = '';
            calAddForm.hidden = true;
            var parts = date.split('-');
            viewYear = parseInt(parts[0], 10);
            viewMonth = parseInt(parts[1], 10) - 1;
            selectedDate = date;
            renderCalendar();
            showDayDetail(date);
          });
        }
      }
    }

    // ---- messages inbox ----
    var msgThreadsEl = document.querySelector('.msg-threads');
    if (msgThreadsEl) {
      var convBody = document.getElementById('msgConvBody');
      var convName = document.getElementById('msgConvName');
      var convSub = document.getElementById('msgConvSub');
      var convAva = document.getElementById('msgConvAva');

      function renderThread(el) {
        msgThreadsEl.querySelectorAll('.msg-thread').forEach(function (t) { t.classList.remove('active'); });
        el.classList.add('active');
        var dot = el.querySelector('.msg-unread-dot');
        if (dot) dot.remove();
        try { window.localStorage.setItem('uv-msg-read-' + el.dataset.thread, '1'); } catch (e) {}
        convName.textContent = el.dataset.name;
        convSub.textContent = el.dataset.sub;
        convAva.style.background = el.dataset.bg;
        convAva.textContent = el.dataset.initials;
        var messages = [];
        try { messages = JSON.parse(el.dataset.messages); } catch (e) {}
        convBody.innerHTML = messages.map(function (m) {
          var ava = m.them ? el.dataset.bg : 'var(--lime)';
          var initials = m.them ? el.dataset.initials : 'FW';
          return '<div class="msg ' + (m.them ? 'ai-msg' : 'user-msg') + '">'
            + '<div class="m-ava" style="background:' + ava + '">' + initials + '</div>'
            + '<div class="m-bubble">' + m.text + '</div></div>';
        }).join('');
        convBody.scrollTop = convBody.scrollHeight;
      }

      msgThreadsEl.querySelectorAll('.msg-thread').forEach(function (t) {
        t.addEventListener('click', function () { renderThread(t); });
        t.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); renderThread(t); }
        });
      });

      var firstThread = msgThreadsEl.querySelector('.msg-thread.active') || msgThreadsEl.querySelector('.msg-thread');
      if (firstThread) renderThread(firstThread);

      var convInput = document.getElementById('msgConvInput');
      var convSend = document.getElementById('msgConvSend');
      function sendReply() {
        var text = convInput.value.trim();
        if (!text) return;
        var b = document.createElement('div');
        b.className = 'msg user-msg';
        b.innerHTML = '<div class="m-ava" style="background:var(--lime)">FW</div><div class="m-bubble">' + text + '</div>';
        convBody.appendChild(b);
        convBody.scrollTop = convBody.scrollHeight;
        convInput.value = '';
      }
      if (convInput) {
        convInput.addEventListener('keydown', function (e) { if (e.key === 'Enter') sendReply(); });
        if (convSend) convSend.addEventListener('click', sendReply);
      }
    }

    // ---- chat: click suggestion or send ----
    var chatInput = document.querySelector('.chat-input input');
    var chatBody = document.querySelector('.chat-body');
    function sendChat(text) {
      if (!text || !chatBody) return;
      var u = document.createElement('div');
      u.className = 'msg user-msg';
      u.innerHTML = '<div class="m-ava">FW</div><div class="m-bubble">' + text + '</div>';
      chatBody.appendChild(u);
      chatBody.scrollTop = chatBody.scrollHeight;
      setTimeout(function () {
        var a = document.createElement('div');
        a.className = 'msg ai-msg';
        a.innerHTML = '<div class="m-ava">UV</div><div class="m-bubble">Good question — here are a few Cardiff things that fit. (This is a prototype reply; the live version will pull real events, societies and opportunities from your feed.)</div>';
        chatBody.appendChild(a);
        chatBody.scrollTop = chatBody.scrollHeight;
      }, 500);
    }
    if (chatInput) {
      var chatSend = document.querySelector('.chat-input button');
      chatInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') { sendChat(chatInput.value.trim()); chatInput.value = ''; }
      });
      if (chatSend) chatSend.addEventListener('click', function () { sendChat(chatInput.value.trim()); chatInput.value = ''; });
      document.querySelectorAll('.chat-suggest .cs').forEach(function (s) {
        s.addEventListener('click', function () { sendChat(s.textContent.trim()); });
      });
    }

    // ---- login / sign-up page ----
    var loginForm = document.getElementById('loginForm');
    var signupForm = document.getElementById('signupForm');
    if (loginForm && signupForm) {
      var authTitle = document.getElementById('authTitle');
      var authSub = document.getElementById('authSub');
      var tabs = document.querySelectorAll('.auth-tab');
      function showTab(name) {
        var isSignup = name === 'signup';
        loginForm.hidden = isSignup;
        signupForm.hidden = !isSignup;
        tabs.forEach(function (t) { t.classList.toggle('active', t.dataset.tab === name); });
        if (authTitle) authTitle.textContent = isSignup ? 'Join Uni-Verse' : 'Welcome back';
        if (authSub) authSub.textContent = isSignup
          ? 'Sign up with your Cardiff student email'
          : 'Log in with your Cardiff student email';
      }
      tabs.forEach(function (t) {
        t.addEventListener('click', function () { showTab(t.dataset.tab); });
      });
      if (window.location.hash === '#signup') showTab('signup');

      function fieldError(box, msg) {
        if (!box) return;
        box.textContent = msg;
        box.hidden = false;
      }
      function clearErrors(form) {
        form.querySelectorAll('.field-invalid').forEach(function (f) { f.classList.remove('field-invalid'); });
        var err = form.querySelector('.field-error');
        if (err) { err.hidden = true; err.textContent = ''; }
      }
      function markInvalid(input) {
        var field = input.closest('.field');
        if (field) field.classList.add('field-invalid');
      }
      function goToApp(user) {
        try { localStorage.setItem('uv-user', JSON.stringify(user)); } catch (e) {}
        window.location.href = 'feed.html';
      }

      signupForm.addEventListener('submit', function (e) {
        e.preventDefault();
        clearErrors(signupForm);
        var errBox = document.getElementById('signupError');
        var name = signupForm.name.value.trim();
        var username = signupForm.username.value.trim();
        var email = signupForm.email.value.trim();
        var pw = signupForm.password.value;
        var pw2 = signupForm.password2.value;
        var bad = false;
        [signupForm.name, signupForm.username, signupForm.email, signupForm.password, signupForm.password2].forEach(function (input) {
          if (!input.value.trim()) { markInvalid(input); bad = true; }
        });
        if (bad) { fieldError(errBox, 'Fill in every field to create your account.'); return; }
        if (!/^[^\s@]+@[^\s@]*cardiff\.ac\.uk$/i.test(email)) {
          markInvalid(signupForm.email);
          fieldError(errBox, 'Use your Cardiff student email (ends in @cardiff.ac.uk).');
          return;
        }
        if (pw.length < 8) {
          markInvalid(signupForm.password);
          fieldError(errBox, 'Password needs to be at least 8 characters.');
          return;
        }
        if (pw !== pw2) {
          markInvalid(signupForm.password);
          markInvalid(signupForm.password2);
          fieldError(errBox, 'Passwords don\'t match — check both fields.');
          return;
        }
        goToApp({ name: name, username: username, email: email });
      });

      loginForm.addEventListener('submit', function (e) {
        e.preventDefault();
        clearErrors(loginForm);
        var errBox = document.getElementById('loginError');
        var email = loginForm.email.value.trim();
        var pw = loginForm.password.value;
        var bad = false;
        [loginForm.email, loginForm.password].forEach(function (input) {
          if (!input.value.trim()) { markInvalid(input); bad = true; }
        });
        if (bad) { fieldError(errBox, 'Enter your email and password.'); return; }
        if (!/^[^\s@]+@[^\s@]*cardiff\.ac\.uk$/i.test(email)) {
          markInvalid(loginForm.email);
          fieldError(errBox, 'Use your Cardiff student email (ends in @cardiff.ac.uk).');
          return;
        }
        var existing = null;
        try { existing = JSON.parse(localStorage.getItem('uv-user') || 'null'); } catch (e2) {}
        goToApp({ name: existing && existing.name, username: existing && existing.username, email: email });
      });
    }

    // ---- log out ----
    var logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', function () {
        try { window.localStorage.removeItem('uv-user'); } catch (e) {}
        window.location.href = 'index.html';
      });
    }
  });
})();
