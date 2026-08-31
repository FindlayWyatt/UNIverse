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

  // ---- RSVP persistence: remembers a clicked [data-rsvp] button across reloads ----
  function isRsvpDone(key) {
    try { return window.localStorage.getItem('uv-rsvp-' + key) === '1'; } catch (e) { return false; }
  }
  function setRsvpDone(key) {
    try { window.localStorage.setItem('uv-rsvp-' + key, '1'); } catch (e) {}
  }

  document.addEventListener('DOMContentLoaded', function () {
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

    // ---- filter chips ----
    // Mostly decorative (visual toggle only). The one exception: a "Freshers Week"
    // chip actually filters its grid down to freshers-tagged cards, when present.
    // Grid is found via an explicit data-filter-grid id when set (robust), falling
    // back to "whatever follows the chips" for the purely-decorative rows elsewhere.
    document.querySelectorAll('.chips').forEach(function (group) {
      var grid = group.dataset.filterGrid ? document.getElementById(group.dataset.filterGrid) : group.nextElementSibling;
      var hasFreshersCards = grid && grid.querySelector && grid.querySelector('[data-freshers]');
      group.querySelectorAll('.chip').forEach(function (c) {
        c.addEventListener('click', function () {
          group.querySelectorAll('.chip').forEach(function (x) { x.classList.remove('on'); });
          c.classList.add('on');
          if (hasFreshersCards) {
            var wantFreshers = c.classList.contains('freshers-chip');
            grid.querySelectorAll('.card').forEach(function (card) {
              card.hidden = wantFreshers && !card.hasAttribute('data-freshers');
            });
          }
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
    // Remembers itself across reloads: buttons tied to a calendar entry key off
    // title+date (matching the calendar's own id), others use an explicit
    // data-rsvp-key. Buttons with neither (e.g. venue/society ones, which have
    // their own dedicated persistence already) just keep today's session-only feel.
    document.querySelectorAll('[data-rsvp]').forEach(function (btn) {
      var key = btn.dataset.rsvpKey
        || (btn.dataset.calTitle && btn.dataset.calDate ? btn.dataset.calTitle + '|' + btn.dataset.calDate : null);

      if (key && isRsvpDone(key)) {
        btn.dataset.done = '1';
        btn.textContent = btn.dataset.rsvp;
      }

      btn.addEventListener('click', function () {
        if (btn.dataset.done === '1') return;
        btn.dataset.done = '1';
        btn.textContent = btn.dataset.rsvp;
        if (key) setRsvpDone(key);
        if (btn.dataset.calTitle && btn.dataset.calDate) {
          addToCalendar({
            id: btn.dataset.calTitle + '|' + btn.dataset.calDate,
            title: btn.dataset.calTitle,
            date: btn.dataset.calDate,
            time: btn.dataset.calTime || '',
            place: btn.dataset.calPlace || '',
            color: btn.dataset.calColor || 'var(--lime)'
          });
        }
      });
    });

    // ---- save hearts ----
    document.querySelectorAll('.save-heart').forEach(function (h) {
      h.addEventListener('click', function () {
        h.classList.toggle('on');
        h.style.color = h.classList.contains('on') ? 'var(--coral)' : '#fff';
      });
    });

    // ---- join buttons (societies) ----
    // Cards on the Societies grid carry data-society and unlock a "View society" link
    // once the (simulated) host accepts the request. The Feed's small "trending
    // societies" widget has no data-society — those just toggle Join/Joined.
    function isSocietyJoined(slug) {
      try { return window.localStorage.getItem('uv-joined-' + slug) === '1'; } catch (e) { return false; }
    }
    function setSocietyJoined(slug) {
      try { window.localStorage.setItem('uv-joined-' + slug, '1'); } catch (e) {}
    }
    document.querySelectorAll('.soc-join').forEach(function (b) {
      var slug = b.dataset.society;
      var viewLink = b.parentElement ? b.parentElement.querySelector('.soc-view') : null;

      if (slug && isSocietyJoined(slug)) {
        b.classList.add('joined');
        b.textContent = 'Joined ✓';
        if (viewLink) viewLink.hidden = false;
      }

      b.addEventListener('click', function () {
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
          b.classList.remove('pending');
          b.classList.add('joined');
          b.textContent = 'Joined ✓';
          setSocietyJoined(slug);
          if (viewLink) viewLink.hidden = false;
        }, 1400);
      });
    });

    // ---- society chat: post your own message into the group thread ----
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
            + '<button class="pill primary popup-rsvp"' + (going ? ' disabled' : '') + '>'
            + (going ? "You're in 🎉" : rsvpWord) + '</button>';
        }

        var marker = L.marker([lat, lng], { icon: pinIcon(currentColor()) }).addTo(venueMap).bindPopup(popupHtml());

        var cardBtn = card.querySelector('.venue-rsvp');
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
          if (popupBtn && !popupBtn.disabled) {
            popupBtn.addEventListener('click', function () {
              setGoing(name);
              refreshUI();
              syncCardButton();
              addVenueToCalendar();
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
          if (cardBtn && isGoing(name)) {
            cardBtn.dataset.done = '1';
            cardBtn.textContent = cardBtn.dataset.rsvp;
          }
        }
        syncCardButton();
        if (cardBtn) {
          cardBtn.addEventListener('click', function () {
            setGoing(name);
            refreshUI();
            addVenueToCalendar();
          });
        }

        venues.push({ card: card, marker: marker, lat: lat, lng: lng, search: card.dataset.search || '' });
      });

      // ---- search: filters cards + pins together, zooms the map to the matches ----
      var searchInput = document.getElementById('venueSearch');
      var clearBtn = document.getElementById('venueSearchClear');
      var matchCount = document.getElementById('venueMatchCount');
      var emptyState = document.getElementById('venueEmpty');
      var emptyQuery = document.getElementById('venueEmptyQuery');

      function runSearch() {
        var q = (searchInput.value || '').trim().toLowerCase();
        if (clearBtn) clearBtn.classList.toggle('show', q.length > 0);
        var visible = [];
        venues.forEach(function (v) {
          var match = !q || v.search.indexOf(q) !== -1;
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
  });
})();
