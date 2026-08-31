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
      var venueMap = L.map('venueMap', { scrollWheelZoom: false }).setView([51.4855, -3.1795], 14.5);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
      }).addTo(venueMap);
      document.querySelectorAll('.venue-card').forEach(function (card) {
        var lat = parseFloat(card.dataset.lat), lng = parseFloat(card.dataset.lng), name = card.dataset.name;
        if (isNaN(lat) || isNaN(lng)) return;
        var marker = L.marker([lat, lng]).addTo(venueMap).bindPopup('<strong>' + name + '</strong>');
        var btn = card.querySelector('.locate-btn');
        if (btn) {
          btn.addEventListener('click', function () {
            venueMap.flyTo([lat, lng], 17);
            marker.openPopup();
          });
        }
      });
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
