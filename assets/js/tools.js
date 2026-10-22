/* Simple.solar — calculators. All math runs in the browser; nothing is sent anywhere. */
(function () {
  "use strict";
  var DATA = window.SS_DATA || { states: [], cpw: 3, exportFactor: 0.85 };
  var store = window.SS_STORE || { get: function () { return null; }, set: function () {} };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function money(x) { var n = Math.round(x); if (Math.abs(n) >= 1000) n = Math.round(n / 10) * 10; return (n < 0 ? "−$" : "$") + Math.abs(n).toLocaleString("en-US"); }
  function st(code) { for (var i = 0; i < DATA.states.length; i++) if (DATA.states[i].code === code) return DATA.states[i]; return null; }
  var AVG = (function () { var r = 0, s = 0, n = DATA.states.length || 1; DATA.states.forEach(function (x) { r += x.rate; s += x.sun; }); return { code: "US", name: "US average", rate: r / n, sun: s / n }; })();

  /* Core model — kept identical to the state pages */
  function estimate(o) {
    var s = st(o.state) || AVG;
    var rate = (o.rate || s.rate) / 100, sun = o.sun || s.sun;
    var shade = o.shade || 1, offset = o.offset || 0.9, cpw = o.cpw || DATA.cpw;
    var kwhYear = (o.kwhYear) || (o.bill / rate) * 12;
    var perKw = sun * 365 * 0.78 * shade;
    var size = kwhYear * offset / perKw;
    if (o.sizeOverride) size = o.sizeOverride;
    var prod = size * perKw;
    var cost = size * 1000 * cpw;
    var net = cost * (1 - (o.incentive || 0) / 100) - (o.rebate || 0);
    var exportF = o.exportFactor || DATA.exportFactor;
    var save1 = Math.min(prod, kwhYear) * rate + Math.max(0, prod - kwhYear) * rate * 0.3;
    save1 = save1 * exportF;
    var esc = (o.escalation == null ? 3 : o.escalation) / 100;
    var cum = -net, total = 0, payback = null, series = [];
    for (var y = 1; y <= 25; y++) {
      var sv = save1 * Math.pow(1 + esc, y - 1) * Math.pow(0.995, y - 1);
      total += sv; cum += sv; series.push(cum);
      if (payback === null && cum >= 0) payback = y;
    }
    return { state: s, size: size, prod: prod, kwhYear: kwhYear, cost: cost, net: net, save1: save1,
      total: total, profit: total - net, payback: payback, series: series, panels: Math.ceil(size * 1000 / 430),
      cover: Math.min(1, prod / kwhYear) };
  }
  window.SS_estimate = estimate;

  function bars(el, series) {
    if (!el) return;
    var max = Math.max.apply(null, series.map(Math.abs)) || 1;
    el.innerHTML = series.map(function (v, i) {
      return '<i class="' + (v < 0 ? "neg" : "") + '" style="height:' + Math.max(2, Math.abs(v) / max * 100) + '%" title="Year ' + (i + 1) + ": " + money(v) + '"></i>';
    }).join("");
  }

  function fillStates(sel, preferred) {
    if (!sel || sel.options.length > 2) return;
    DATA.states.slice().sort(function (a, b) { return a.name.localeCompare(b.name); }).forEach(function (s) {
      var o = document.createElement("option"); o.value = s.code; o.textContent = s.name; sel.appendChild(o);
    });
    var saved = store.get("ss-state") || preferred || "CA";
    if (saved && st(saved)) sel.value = saved;
  }

  /* ---------- Hero sun-arc ---------- */
  var hero = $("#sun-arc");
  if (hero) {
    var hs = $("#hero-state"), hb = $("#hero-bill"), hbo = $("#hero-bill-out");
    fillStates(hs, "CA");
    var arcLen = $("#arc-fill").getTotalLength();
    $("#arc-fill").style.strokeDasharray = arcLen;
    function heroUpd() {
      var bill = +hb.value; hbo.textContent = "$" + bill;
      var r = estimate({ state: hs.value, bill: bill });
      var frac = Math.max(0.08, Math.min(1, r.save1 / (bill * 12)));
      $("#arc-fill").style.strokeDashoffset = arcLen * (1 - frac);
      var pt = $("#arc-fill").getPointAtLength(arcLen * frac);
      $("#arc-sun").setAttribute("cx", pt.x); $("#arc-sun").setAttribute("cy", pt.y);
      $("#hero-total").textContent = money(r.profit);
      $("#hero-sub").textContent = "estimated 25-year net savings";
      $("#hero-size").textContent = r.size.toFixed(1) + " kW";
      $("#hero-pay").textContent = r.payback ? r.payback + " yrs" : "25+ yrs";
      $("#hero-cover").textContent = Math.round(frac * 100) + "%";
      store.set("ss-state", hs.value); store.set("ss-bill", bill);
      var go = $("#hero-go"); if (go) go.href = go.getAttribute("data-base") + "?state=" + hs.value + "&bill=" + bill;
    }
    hs.addEventListener("change", heroUpd); hb.addEventListener("input", heroUpd); heroUpd();
  }

  /* ---------- Lead form preview ---------- */
  var lf = $("#lead-form");
  if (lf) {
    var bill = $("#lf-bill"), out = $("#lf-bill-out");
    function bu() { out.textContent = "$" + bill.value; }
    bill.addEventListener("input", bu); bu();
    $$('[name="ownership"]', lf).forEach(function (r) {
      r.addEventListener("change", function () { $("#renter-note").hidden = r.value !== "Rent"; });
    });
    function preview() {
      var shadeV = (lf.querySelector('[name="sun"]:checked') || {}).value;
      var shade = shadeV === "Some shade" ? 0.85 : shadeV === "Heavy shade" ? 0.65 : 1;
      var r = estimate({ state: lf.state.value, bill: +bill.value, shade: shade });
      $('[data-p="size"]', lf).textContent = r.size.toFixed(1) + " kW";
      $('[data-p="save"]', lf).textContent = money(r.save1);
      $('[data-p="payback"]', lf).textContent = r.payback ? r.payback + " years" : "25+ years";
      var txt = r.size.toFixed(1) + " kW system, about " + r.panels + " panels; est. cost " + money(r.cost) + "; first-year savings " + money(r.save1) + "; payback " + (r.payback || "25+") + " yrs; 25-yr net " + money(r.profit);
      lf.estimate.value = txt;
      store.set("ss-estimate", txt);
    }
    $$("[data-next]", lf).forEach(function (b) { b.addEventListener("click", preview); });
    lf._extra = function () { preview(); return {}; };
  }

  /* ---------- Savings calculator ---------- */
  var sc = $("#savings-calc");
  if (sc) {
    fillStates(sc.state);
    var q = new URLSearchParams(location.search);
    if (q.get("state") && st(q.get("state"))) sc.state.value = q.get("state");
    if (q.get("bill")) sc.bill.value = q.get("bill");
    function run() {
      var r = estimate({ state: sc.state.value, bill: +sc.bill.value, shade: +sc.shade.value,
        cpw: +sc.cpw.value, incentive: +sc.incentive.value, escalation: +sc.esc.value, offset: +sc.offset.value / 100 });
      $("#sc-out-bill").textContent = "$" + sc.bill.value;
      $("#sc-out-cpw").textContent = "$" + (+sc.cpw.value).toFixed(2);
      $("#sc-out-offset").textContent = sc.offset.value + "%";
      $("#sc-out-inc").textContent = sc.incentive.value + "%";
      $("#sc-out-esc").textContent = sc.esc.value + "%";
      $("#k-size").textContent = r.size.toFixed(1) + " kW";
      $("#k-panels").textContent = r.panels;
      $("#k-cost").textContent = money(r.net);
      $("#k-save").textContent = money(r.save1);
      $("#k-pay").textContent = r.payback ? r.payback + " yrs" : "25+ yrs";
      $("#k-total").textContent = money(r.profit);
      $("#k-prod").textContent = Math.round(r.prod).toLocaleString() + " kWh";
      $("#k-rate").textContent = r.state.rate.toFixed(1) + "¢ / " + r.state.sun.toFixed(1) + " h";
      bars($("#sc-bars"), r.series);
      var v = $("#sc-verdict");
      v.textContent = !r.payback ? "On these numbers solar doesn't pay back within 25 years. Look at plug-in solar, community solar, or lowering the price per watt with more quotes."
        : r.payback <= 8 ? "Strong case. Solar pays for itself in under a decade here. Get three quotes and compare price per watt."
        : r.payback <= 12 ? "Good case. Most of the system's 25+ year life is profit. Quote shopping can shorten payback further."
        : "Thin margin. Small changes in price, shade or financing swing the result — compare several quotes before deciding.";
    }
    sc.addEventListener("input", run); run();
  }

  /* ---------- System size ---------- */
  var ss = $("#size-calc");
  if (ss) {
    fillStates(ss.state);
    function sz() {
      var s = st(ss.state.value) || AVG;
      var kwh = +ss.kwh.value || 0;
      if (ss.mode.value === "bill") kwh = (+ss.bill.value / (s.rate / 100)) * 12; else kwh = kwh * 12;
      var sun = +ss.sunh.value || s.sun;
      var eff = 1 - (+ss.loss.value / 100);
      var kw = kwh * (+ss.offset.value / 100) / (sun * 365 * eff);
      var pw = +ss.pw.value;
      $("#sz-kw").textContent = kw.toFixed(2) + " kW";
      $("#sz-panels").textContent = Math.ceil(kw * 1000 / pw);
      $("#sz-area").textContent = Math.round(Math.ceil(kw * 1000 / pw) * 21.5) + " sq ft";
      $("#sz-kwh").textContent = Math.round(kwh).toLocaleString() + " kWh/yr";
      $("#sz-sun").placeholder = s.sun.toFixed(1);
      $$(".mode-bill").forEach(function (e) { e.hidden = ss.mode.value !== "bill"; });
      $$(".mode-kwh").forEach(function (e) { e.hidden = ss.mode.value !== "kwh"; });
    }
    ss.addEventListener("input", sz); ss.addEventListener("change", sz); sz();
  }

  /* ---------- Load-list builder (battery + power station) ---------- */
  var PRESETS = [
    ["Refrigerator", 150, 24, 0.4], ["Chest freezer", 100, 24, 0.35], ["Wi-Fi router + modem", 20, 24, 1], ["LED lights (5 bulbs)", 45, 6, 1],
    ["Phone charging (2)", 20, 3, 1], ["Laptop", 60, 6, 1], ["TV (55-inch LED)", 100, 4, 1], ["Sump pump", 800, 2, 0.5],
    ["Furnace fan", 500, 8, 0.5], ["Window AC (small)", 600, 6, 0.6], ["Microwave", 1100, 0.3, 1], ["Coffee maker", 900, 0.2, 1],
    ["CPAP-type device", 40, 8, 1], ["Electric kettle", 1500, 0.15, 1], ["Portable fan", 50, 8, 1], ["Well pump", 1000, 1, 1]
  ];
  function loadBuilder(root, onChange) {
    var list = $(".loadlist", root), sel = $(".preset", root);
    PRESETS.forEach(function (p, i) { var o = document.createElement("option"); o.value = i; o.textContent = p[0] + " (" + p[1] + " W)"; sel.appendChild(o); });
    function row(name, w, h, duty) {
      var d = document.createElement("div"); d.className = "loadrow";
      d.innerHTML = '<input aria-label="Appliance" value="' + name + '"><input aria-label="Watts" type="number" min="0" value="' + w + '"><input aria-label="Hours per day" type="number" min="0" step="0.1" value="' + h + '"><button type="button" class="icon-btn" aria-label="Remove ' + name + '">×</button>';
      d.dataset.duty = duty || 1;
      $("button", d).addEventListener("click", function () { d.remove(); onChange(); });
      $$("input", d).forEach(function (x) { x.addEventListener("input", onChange); });
      list.appendChild(d); onChange();
    }
    $(".add-preset", root).addEventListener("click", function () { var p = PRESETS[+sel.value]; row(p[0], p[1], p[2], p[3]); });
    $(".add-custom", root).addEventListener("click", function () { row("My device", 100, 2, 1); });
    return {
      row: row,
      totals: function () {
        var wh = 0, peak = 0, maxW = 0;
        $$(".loadrow", list).forEach(function (d) {
          var ins = $$("input", d), w = +ins[1].value || 0, h = +ins[2].value || 0, duty = +d.dataset.duty || 1;
          wh += w * h * duty; peak += w; maxW = Math.max(maxW, w);
        });
        return { wh: wh, peak: peak, maxW: maxW };
      }
    };
  }

  var bat = $("#battery-calc");
  if (bat) {
    var bb = loadBuilder(bat, function () { bupd(); });
    function bupd() {
      if (!bb) return;
      var t = bb.totals(), days = +bat.querySelector("[name=days]").value || 1;
      var dod = 0.9, eff = 0.9;
      var need = t.wh * days / dod / eff / 1000;
      $("#bt-wh").textContent = (t.wh / 1000).toFixed(1) + " kWh/day";
      $("#bt-need").textContent = need.toFixed(1) + " kWh";
      $("#bt-kw").textContent = (t.peak / 1000).toFixed(1) + " kW";
      $("#bt-units").textContent = Math.max(1, Math.ceil(need / 13.5)) + " × 13.5 kWh";
      var B = DATA.battery || { low: 900, high: 1400 };
      $("#bt-cost").textContent = money(need * B.low) + "–" + money(need * B.high);
      $("#bt-days-out").textContent = days + (days == 1 ? " day" : " days");
    }
    bat.querySelector("[name=days]").addEventListener("input", bupd);
    [[0], [2], [3], [4], [7]].forEach(function (i) { var p = PRESETS[i[0]]; bb.row(p[0], p[1], p[2], p[3]); });
  }

  var ps = $("#station-calc");
  if (ps) {
    var pb = loadBuilder(ps, function () { pupd(); });
    function pupd() {
      if (!pb) return;
      var t = pb.totals(), cap = +ps.querySelector("[name=cap]").value, panel = +ps.querySelector("[name=panel]").value;
      var sun = +ps.querySelector("[name=sunh]").value;
      var usable = cap * 0.85;
      var hours = t.wh > 0 ? usable / (t.wh / 24) : 0;
      $("#ps-cap-out").textContent = cap.toLocaleString() + " Wh";
      $("#ps-panel-out").textContent = panel + " W";
      $("#ps-sun-out").textContent = sun + " h";
      $("#ps-day").textContent = Math.round(t.wh).toLocaleString() + " Wh/day";
      $("#ps-run").textContent = hours > 48 ? (hours / 24).toFixed(1) + " days" : hours.toFixed(1) + " hours";
      $("#ps-peak").textContent = Math.round(t.peak).toLocaleString() + " W";
      var rec = Math.ceil(t.wh / 0.85 / 256) * 256;
      $("#ps-rec").textContent = rec ? rec.toLocaleString() + "+ Wh" : "—";
      var solarWh = panel * sun * 0.75;
      $("#ps-solar").textContent = Math.round(solarWh).toLocaleString() + " Wh/day";
      $("#ps-charge").textContent = panel ? (cap / (panel * 0.75)).toFixed(1) + " sun-hours" : "—";
      var w = $("#ps-warn");
      w.hidden = !(t.maxW > 0 && t.peak > 0);
      w.textContent = "Pick a unit rated for at least " + Math.round(t.peak * 1.2).toLocaleString() + " W continuous output if everything runs at once, and check surge ratings for fridges and pumps (often 2–3× running watts).";
    }
    $$("input[type=range]", ps).forEach(function (x) { x.addEventListener("input", pupd); });
    [[0], [2], [3], [4], [5]].forEach(function (i) { var p = PRESETS[i[0]]; pb.row(p[0], p[1], p[2], p[3]); });
  }

  /* ---------- Plug-in solar ---------- */
  var pi = $("#plugin-calc");
  if (pi) {
    fillStates(pi.state);
    function piu() {
      var s = st(pi.state.value) || AVG;
      var w = +pi.watts.value, face = +pi.face.value, cost = +pi.cost.value, self = +pi.self.value / 100;
      var kwh = w / 1000 * s.sun * 365 * 0.8 * face;
      var save = kwh * self * s.rate / 100;
      $("#pi-w-out").textContent = w + " W"; $("#pi-cost-out").textContent = "$" + cost; $("#pi-self-out").textContent = Math.round(self * 100) + "%";
      $("#pi-kwh").textContent = Math.round(kwh).toLocaleString() + " kWh/yr";
      $("#pi-save").textContent = money(save) + "/yr";
      $("#pi-pay").textContent = save > 0 ? (cost / save).toFixed(1) + " yrs" : "—";
      $("#pi-co2").textContent = Math.round(kwh * 0.37) + " kg CO₂/yr";
    }
    pi.addEventListener("input", piu); pi.addEventListener("change", piu); piu();
  }

  /* ---------- Solar match quiz ---------- */
  var qz = $("#match-quiz");
  if (qz) {
    var steps = $$(".qstep", qz), idx = 0, ans = {};
    function show(n) { steps.forEach(function (s, j) { s.hidden = j !== n; }); idx = n; $("#qz-count").textContent = n < steps.length ? "Question " + (n + 1) + " of " + steps.length : ""; }
    $$("button[data-a]", qz).forEach(function (b) {
      b.addEventListener("click", function () {
        ans[b.closest(".qstep").dataset.q] = b.dataset.a;
        if (idx < steps.length - 1) show(idx + 1); else result();
      });
    });
    $$("[data-qback]", qz).forEach(function (b) { b.addEventListener("click", function () { if (idx > 0) show(idx - 1); }); });
    function result() {
      steps.forEach(function (s) { s.hidden = true; }); $("#qz-count").textContent = "";
      var key = "rooftop";
      if (ans.home === "rent" || ans.home === "apartment") key = ans.goal === "backup" ? "station" : "plugin";
      else if (ans.home === "rv") key = "rv";
      else if (ans.home === "cabin") key = "offgrid";
      else if (ans.goal === "backup" && ans.budget === "low") key = "station";
      else if (ans.goal === "backup") key = "battery";
      else if (ans.goal === "green" && ans.budget === "low") key = "community";
      else if (ans.budget === "low" || ans.bill === "small") key = "plugin";
      if ((ans.home === "rent" || ans.home === "apartment") && ans.goal === "green") key = "community";
      $$(".qresult", qz).forEach(function (r) { r.hidden = r.dataset.r !== key; });
      $("#qz-restart").hidden = false;
    }
    $("#qz-restart").addEventListener("click", function () { ans = {}; $$(".qresult", qz).forEach(function (r) { r.hidden = true; }); this.hidden = true; show(0); });
    show(0);
  }

  /* Thank-you page */
  var ty = $("#ty-estimate");
  if (ty) { var e = store.get("ss-estimate"); if (e) { ty.textContent = e; ty.parentElement.hidden = false; } }
})();
