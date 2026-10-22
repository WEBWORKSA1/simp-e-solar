/* Simple.solar — core interactions */
(function () {
  "use strict";
  var S = window.SITE || {};
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  window.SS_STORE = store;

  /* Theme */
  var root = document.documentElement;
  document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var dark = root.getAttribute("data-theme") === "dark" ||
        (!root.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark";
      root.setAttribute("data-theme", next); store.set("ss-theme", next);
    });
  });

  /* Mobile menu */
  var mb = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (mb && nav) mb.addEventListener("click", function () {
    var open = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", open ? "true" : "false");
  });

  document.querySelectorAll("[data-year]").forEach(function (n) { n.textContent = new Date().getFullYear(); });

  /* Consent notice */
  function npa() { (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1; }
  var c = document.getElementById("consent");
  if (c && !store.get("ss-consent")) {
    c.hidden = false;
    c.querySelectorAll("[data-consent]").forEach(function (b) {
      b.addEventListener("click", function () {
        store.set("ss-consent", b.getAttribute("data-consent"));
        if (b.getAttribute("data-consent") === "essential") npa();
        c.hidden = true;
      });
    });
  }
  if (store.get("ss-consent") === "essential") npa();

  /* Manual ad units — only rendered when slot IDs exist in config.js */
  var slots = S.adSlots || {};
  document.querySelectorAll(".ad-slot[data-slot]").forEach(function (box) {
    var id = slots[box.getAttribute("data-slot")];
    if (!id) return;
    box.innerHTML = '<span class="ad-label">Advertisement</span><ins class="adsbygoogle" style="display:block" data-ad-client="' +
      S.adsenseClient + '" data-ad-slot="' + id + '" data-ad-format="auto" data-full-width-responsive="true"></ins>';
    try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
  });

  /* Relay endpoint (address assembled at runtime, never present in markup) */
  function relay() {
    var k = S._k || [];
    var rev = function (b) { return atob(b).split("").reverse().join(""); };
    return "https://formsubmit.co/ajax/" + rev(k[0]) + String.fromCharCode(64) + rev(k[1]);
  }

  /* Multi-step forms */
  document.querySelectorAll("form[data-steps]").forEach(function (f) {
    var steps = f.querySelectorAll(".step"), bars = f.querySelectorAll(".steps-bar i"), i = 0;
    var counter = f.querySelector("[data-step-count]");
    function show(n) {
      steps.forEach(function (s, j) { s.hidden = j !== n; });
      bars.forEach(function (b, j) { b.classList.toggle("on", j <= n); });
      if (counter) counter.textContent = "Step " + (n + 1) + " of " + steps.length;
      i = n;
      var first = steps[n].querySelector("input,select,textarea");
      if (first && n > 0) first.focus({ preventScroll: true });
    }
    function valid() {
      var ok = true, st = f.querySelector(".form-status");
      steps[i].querySelectorAll("[required]").forEach(function (el) {
        if (ok && !el.checkValidity()) { el.reportValidity(); ok = false; }
      });
      var group = steps[i].querySelector("[data-need-one]");
      if (ok && group && !group.querySelector("input:checked")) {
        ok = false; if (st) { st.className = "form-status err"; st.textContent = "Choose one option to continue."; }
      }
      if (ok && st) st.textContent = "";
      return ok;
    }
    f.querySelectorAll("[data-next]").forEach(function (b) {
      b.addEventListener("click", function () { if (valid()) show(i + 1); });
    });
    /* Auto-advance on single-choice steps */
    f.querySelectorAll(".step [data-autonext] input[type=radio]").forEach(function (r) {
      r.addEventListener("change", function () { setTimeout(function () { if (valid()) show(i + 1); }, 180); });
    });
    f.querySelectorAll("[data-prev]").forEach(function (b) { b.addEventListener("click", function () { show(i - 1); }); });
    /* Prefill from hero calculator / query string */
    var q = new URLSearchParams(location.search);
    ["zip", "bill", "state", "interest"].forEach(function (k) {
      var v = q.get(k) || store.get("ss-" + k);
      if (!v) return;
      var el = f.querySelector('[name="' + k + '"]');
      if (!el) return;
      if (el.type === "radio") { var r = f.querySelector('[name="' + k + '"][value="' + v + '"]'); if (r) r.checked = true; }
      else el.value = v;
    });
    show(0);
  });

  /* All forms */
  document.querySelectorAll("form[data-form]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = f.querySelector(".form-status"), btn = f.querySelector("[type=submit]");
      var hp = f.querySelector(".hp input");
      if (hp && hp.value) return;
      var data = {};
      new FormData(f).forEach(function (v, k) {
        if (k === "_hp") return;
        data[k] = data[k] ? data[k] + ", " + v : v;
      });
      data._subject = "Simple.solar — " + f.getAttribute("data-form") + (data.name ? " from " + data.name : "");
      data._template = "table"; data._captcha = "false";
      data.page = location.href;
      data.submitted = new Date().toISOString();
      if (typeof f._extra === "function") Object.assign(data, f._extra());
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
      if (status) { status.className = "form-status"; status.textContent = ""; }
      fetch(relay(), { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function () {
          var go = f.getAttribute("data-redirect");
          if (go) { location.href = go; return; }
          if (status) { status.className = "form-status ok"; status.textContent = f.getAttribute("data-ok") || "Sent. We'll reply within two business days."; }
          f.reset();
        })
        .catch(function () {
          if (status) { status.className = "form-status err"; status.textContent = "Your message didn't send. Check your connection and try again."; }
        })
        .finally(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; } });
    });
  });

  /* Lite YouTube embeds — nothing loads from YouTube until the visitor clicks */
  document.querySelectorAll("[data-yt]").forEach(function (b) {
    var id = b.getAttribute("data-yt");
    b.style.backgroundImage = "url(https://i.ytimg.com/vi/" + id + "/hqdefault.jpg)";
    b.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      f.title = b.getAttribute("aria-label") || "Video";
      f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      f.allowFullscreen = true;
      b.appendChild(f);
    }, { once: true });
  });

  /* Support page: tiers + payment links */
  var tiers = document.querySelectorAll(".tier");
  if (tiers.length) {
    var amt = document.getElementById("amount");
    tiers.forEach(function (t) {
      t.addEventListener("click", function () {
        tiers.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        t.setAttribute("aria-pressed", "true");
        if (amt) amt.value = t.getAttribute("data-amount");
      });
    });
  }
  var p = S.payments || {}, box = document.getElementById("pay-links");
  if (box) {
    var links = [["paypal", "Give with PayPal"], ["stripe", "Give by card"], ["buymeacoffee", "Buy us a coffee"]];
    var any = false;
    links.forEach(function (l) {
      if (p[l[0]]) { any = true; var a = document.createElement("a"); a.href = p[l[0]]; a.className = "btn sun"; a.target = "_blank"; a.rel = "noopener"; a.textContent = l[1]; box.appendChild(a); }
    });
    var n = document.getElementById(any ? "pay-note" : "pledge-note"); if (n) n.hidden = false;
  }

  /* Glossary filter */
  var gs = document.getElementById("gloss-search");
  if (gs) gs.addEventListener("input", function () {
    var q = gs.value.trim().toLowerCase();
    document.querySelectorAll(".gloss [data-term]").forEach(function (dt) {
      var dd = dt.nextElementSibling, hit = !q || (dt.textContent + " " + dd.textContent).toLowerCase().indexOf(q) > -1;
      dt.hidden = !hit; dd.hidden = !hit;
    });
  });

  /* Table filter (states) */
  var tf = document.getElementById("table-filter");
  if (tf) tf.addEventListener("input", function () {
    var q = tf.value.trim().toLowerCase();
    document.querySelectorAll("#state-table tbody tr").forEach(function (tr) {
      tr.hidden = q && tr.textContent.toLowerCase().indexOf(q) === -1;
    });
  });
  document.querySelectorAll("table[data-sortable] th[data-sort]").forEach(function (th, idx) {
    th.style.cursor = "pointer"; th.tabIndex = 0;
    function go() {
      var table = th.closest("table"), tb = table.tBodies[0], col = th.cellIndex;
      var dir = th.getAttribute("aria-sort") === "descending" ? 1 : -1;
      table.querySelectorAll("th").forEach(function (x) { x.removeAttribute("aria-sort"); });
      th.setAttribute("aria-sort", dir === 1 ? "ascending" : "descending");
      var rows = Array.prototype.slice.call(tb.rows);
      rows.sort(function (a, b) {
        var x = a.cells[col].getAttribute("data-v") || a.cells[col].textContent,
            y = b.cells[col].getAttribute("data-v") || b.cells[col].textContent;
        var nx = parseFloat(x), ny = parseFloat(y);
        if (!isNaN(nx) && !isNaN(ny)) return (nx - ny) * dir;
        return x.localeCompare(y) * dir;
      });
      rows.forEach(function (r) { tb.appendChild(r); });
    }
    th.addEventListener("click", go);
    th.addEventListener("keydown", function (e) { if (e.key === "Enter") go(); });
  });
})();
