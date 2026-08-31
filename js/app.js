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
        var name = card.dataset.name, cat = card.dataset.cat;
        var baseGoing = parseInt(card.dataset.going, 10) || 0;
        var ticketUrl = card.dataset.ticketUrl, ticketLabel = card.dataset.ticketLabel;
        if (isNaN(lat) || isNaN(lng)) return;

        function currentCount() { return baseGoing + (isGoing(name) ? 1 : 0); }

        function popupHtml() {
          var going = isGoing(name), count = currentCount();
          var ticketHtml = ticketUrl
            ? '<a class="popup-tickets" href="' + ticketUrl + '" target="_blank" rel="noopener">' + ticketLabel + ' ↗</a>'
            : '';
          return '<strong>' + name + '</strong><span class="popup-cat">' + cat + '</span>'
            + '<div class="popup-going"><i class="busy-dot" style="background:' + goingColor(count) + '"></i>' + count + ' going tonight</div>'
            + ticketHtml
            + '<button class="pill primary popup-rsvp"' + (going ? ' disabled' : '') + '>'
            + (going ? "You're in 🎉" : "I'm going tonight") + '</button>';
        }

        var marker = L.marker([lat, lng], { icon: pinIcon(goingColor(currentCount())) }).addTo(venueMap).bindPopup(popupHtml());

        var cardBtn = card.querySelector('.venue-rsvp');
        var dotEl = card.querySelector('.busy-dot');
        var numEl = card.querySelector('.going-count');

        function refreshUI() {
          var count = currentCount(), color = goingColor(count);
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

    // ---- chat: click suggestion or send ----
    var chatInput = document.querySelector('.chat-input input');
    var chatBody = document.querySelector('.chat-body');
    function sendChat(text) {
      if (!text || !chatBody) return;
      var u = document.createElement('div');
      u.className = 'msg user-msg';
      u.innerHTML = '<div class="m-ava">MW</div><div class="m-bubble">' + text + '</div>';
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
