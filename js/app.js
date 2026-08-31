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

    // ---- filter chips ----
    document.querySelectorAll('.chips').forEach(function (group) {
      group.querySelectorAll('.chip').forEach(function (c) {
        c.addEventListener('click', function () {
          group.querySelectorAll('.chip').forEach(function (x) { x.classList.remove('on'); });
          c.classList.add('on');
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
    document.querySelectorAll('[data-rsvp]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (btn.dataset.done === '1') return;
        btn.dataset.done = '1';
        btn.textContent = btn.dataset.rsvp;
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
    document.querySelectorAll('.soc-join').forEach(function (b) {
      b.addEventListener('click', function () {
        b.classList.toggle('joined');
        b.textContent = b.classList.contains('joined') ? 'Joined' : 'Join';
      });
    });

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
