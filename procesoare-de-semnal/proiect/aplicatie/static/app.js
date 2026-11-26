(() => {
  "use strict";

  const NIVELURI = ["Bun", "Acceptabil", "Moderat", "Slab", "Foarte slab", "Extrem de slab"];
  const PRAGURI = { pm25: [5, 15, 50, 90, 140], pm10: [15, 45, 120, 195, 270], no2: [10, 25, 60, 100, 150] };
  const LIMITE = { pm25: { v: 25, t: "limită anuală 25" }, pm10: { v: 50, t: "limită zilnică 50" }, no2: { v: 200, t: "limită orară 200" } };
  const PARAM = {
    pm25: { n: "PM2.5", u: "µg/m³", max: 90 }, pm10: { n: "PM10", u: "µg/m³", max: 195 },
    no2: { n: "NO₂", u: "µg/m³", max: 150 }, co: { n: "CO", u: "mg/m³", max: 10 },
    temp: { n: "Temperatură", u: "°C", max: 40 }, umid: { n: "Umiditate", u: "%", max: 100 },
  };
  const TIPURI = {
    trafic: {
      nume: "Trafic", filtru: "Trafic",
      forma: '<rect class="forma" x="4.5" y="4.5" width="25" height="25" rx="7.5"/>',
      glif: '<g class="glif"><path d="M10.5 19.6v-3.1l1.8-3.8h9.4l1.8 3.8v3.1z"/><circle class="plin" cx="13.4" cy="20.6" r="1.6"/><circle class="plin" cx="20.6" cy="20.6" r="1.6"/></g>',
    },
    parc: {
      nume: "Parc", filtru: "Parcuri",
      forma: '<circle class="forma" cx="17" cy="17" r="13"/>',
      glif: '<g class="glif"><path d="M11.2 22.8c-.4-6.2 3.4-10.6 11.6-11.4.6 8-3.6 11.8-11.6 11.4zM11.2 22.8l6.2-6.2"/></g>',
    },
    scoala: {
      nume: "Școală", filtru: "Școli",
      forma: '<path class="forma" d="M17 3.6 29.6 13.1v14.4a2.6 2.6 0 0 1-2.6 2.6H7a2.6 2.6 0 0 1-2.6-2.6V13.1z"/>',
      glif: '<g class="glif"><path d="M10.6 15.2c2.2-.8 4.4-.7 6.4.7 2-1.4 4.2-1.5 6.4-.7v8.2c-2.2-.8-4.4-.7-6.4.7-2-1.4-4.2-1.5-6.4-.7zM17 15.9v8.2"/></g>',
    },
    industrial: {
      nume: "Industrial", filtru: "Industrie",
      forma: '<path class="forma" d="M17 2.6 31.4 17 17 31.4 2.6 17z"/>',
      glif: '<g class="glif"><path class="plin" d="M11.6 21.4v-4.8l2.9 1.7v-1.7l2.9 1.7v-1.7l2.9 1.7v-5.2h2.1v8.3z"/></g>',
    },
  };
  const ICON = {
    play: '<svg viewBox="0 0 12 12"><path d="M3 1.8v8.4L10 6z" fill="currentColor"/></svg>',
    pauza: '<svg viewBox="0 0 12 12"><path d="M3 2h2v8H3zM7 2h2v8H7z" fill="currentColor"/></svg>',
    ai: '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 1.5c.4 2.9 1.6 4.1 4.5 4.5-2.9.4-4.1 1.6-4.5 4.5-.4-2.9-1.6-4.1-4.5-4.5 2.9-.4 4.1-1.6 4.5-4.5zM12.5 10c.2 1.3.7 1.8 2 2-1.3.2-1.8.7-2 2-.2-1.3-.7-1.8-2-2 1.3-.2 1.8-.7 2-2z"/></svg>',
    inapoi: '<svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10 3.5 5.5 8l4.5 4.5"/></svg>',
    tema: '<svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="5.6"/><path d="M8 2.4a5.6 5.6 0 0 1 0 11.2z" fill="currentColor"/></svg>',
    marca: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M3 9.5h11.5a3 3 0 1 0-3-3"/><path d="M3 14h16a3 3 0 1 1-3 3"/><path d="M3 18.5h7"/></svg>',
  };

  const S = { stare: null, demo: null, filtru: "toate", ordine: "poluat", ora: 23, selectat: null, detalii: null,
              param: "pm25", brut: false, estimare: true, redare: null };
  const $ = (sel) => document.querySelector(sel);
  const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const ZONA = "Europe/Bucharest";
  const hh = (t) => new Date(t * 1000).toLocaleTimeString("ro-RO", { hour: "2-digit", minute: "2-digit", timeZone: ZONA });
  const zi = (t) => new Date(t * 1000).toLocaleDateString("ro-RO", { weekday: "short", timeZone: ZONA }).replace(".", "");
  const data = (t) => new Date(t * 1000).toLocaleDateString("ro-RO", { day: "numeric", month: "short", timeZone: ZONA });
  const culoare = (n) => (n === null || n === undefined ? "var(--text-3)" : `var(--n${n})`);
  const nivel = (p, v) => {
    if (v === null || v === undefined || !PRAGURI[p]) return null;
    const i = PRAGURI[p].findIndex((x) => v <= x);
    return i === -1 ? 5 : i;
  };
  const fmt = (v, p) => (v === null || v === undefined ? "–" : p === "co" ? v.toLocaleString("ro-RO", { maximumFractionDigits: 2 }) : Math.round(v).toLocaleString("ro-RO"));
  const svgTip = (tip, n, extra = "") => `<svg viewBox="0 0 34 34" style="--c:${culoare(n)}" ${extra}>${TIPURI[tip].forma}${TIPURI[tip].glif}</svg>`;
  const tipMic = (tip) => `<svg viewBox="0 0 34 34">${TIPURI[tip].forma}</svg>`;

  // ---------- date: API-ul serverului sau, fără server, setul demonstrativ ----------
  async function incarcaStare() {
    if (!window.VAZDUH_DEMO && S.demo !== true) {
      try {
        const r = await fetch("api/stare", { cache: "no-store" });
        const d = r.ok ? await r.json() : null;
        if (d && d.acum) { S.stare = d; S.demo = false; return; }
      } catch (e) { /* fără server: trecem pe datele demonstrative */ }
    }
    const r = await fetch("demo.json");
    S.demoDate = await r.json();
    S.stare = S.demoDate.stare;
    S.demo = true;
  }
  async function incarcaStatie(id) {
    if (S.demo) return S.demoDate.statii[id];
    const r = await fetch(`api/statie/${encodeURIComponent(id)}`, { cache: "no-store" });
    return r.json();
  }

  // ---------- harta ----------
  const ingust = () => window.matchMedia("(max-width: 760px)").matches;
  const harta = L.map("harta", { zoomControl: false, attributionControl: false, minZoom: 10.5, maxZoom: 17,
                                 zoomSnap: 0.25, zoomDelta: 0.5, renderer: L.svg({ padding: 0.6 }) });
  const LIMITE_ORAS = L.latLngBounds([44.334, 25.966], [44.541, 26.226]);
  function incadreaza() {
    const h = window.innerHeight;
    harta.fitBounds(LIMITE_ORAS, ingust()
      ? { paddingTopLeft: [0, 40], paddingBottomRight: [0, h * 0.48 + 56] }
      : { paddingTopLeft: [424, 24], paddingBottomRight: [24, 80] });
  }
  incadreaza();

  const cartiere = [];
  const marcaje = {};
  let stratComunitate = null, stratStrazi = null;

  async function incarcaHarta() {
    const g = await (await fetch("harta.json")).json();
    for (const c of g.cartiere) {
      const strat = L.geoJSON(c.geometrie, { style: { className: "cartier" } }).addTo(harta);
      strat.bindTooltip(c.nume, { sticky: true, className: "eticheta-cartier", direction: "top", offset: [0, -10] });
      const inel = c.geometrie.coordinates.reduce((a, p) => (p[0].length > a.length ? p[0] : a), []);
      const centru = inel.reduce((a, [x, y]) => [a[0] + y / inel.length, a[1] + x / inel.length], [0, 0]);
      cartiere.push({ strat, centru });
    }
    for (const s of g.sectoare) L.geoJSON(s.geometrie, { style: { className: "sector" }, interactive: false }).addTo(harta);
    L.geoJSON(g.oras, { style: { className: "contur-oras" }, interactive: false }).addTo(harta);
    S.atribuire = g.atribuire;
  }

  function distKm(a, b) {
    const dx = (a[1] - b[1]) * 111.32 * Math.cos((a[0] * Math.PI) / 180), dy = (a[0] - b[0]) * 110.57;
    return Math.hypot(dx, dy);
  }

  // estimarea PM2.5 pe cartiere: interpolare cu inversul pătratului distanței (IDW) față de stații
  function coloreazaCartiere() {
    const puncte = S.stare.statii.map((s) => [[s.lat, s.lon], valoareLa(s, S.ora, "pm25")]).filter((p) => p[1] !== null);
    for (const c of cartiere) {
      let sw = 0, sv = 0;
      for (const [poz, v] of puncte) {
        const d = Math.max(distKm(c.centru, poz), 0.4);
        if (d > 5) continue;
        sw += 1 / (d * d); sv += v / (d * d);
      }
      const n = sw ? nivel("pm25", sv / sw) : null;
      c.strat.eachLayer((l) => {
        const el = l.getElement && l.getElement();
        if (!el) return;
        el.classList.remove("n0", "n1", "n2", "n3", "n4", "n5");
        if (n !== null) el.classList.add(`n${n}`);
      });
    }
    document.getElementById("harta").classList.toggle("estimare", S.estimare);
  }

  function valoareLa(s, i, p) {
    if (i === 23) return s.ultim ? s.ultim[p] ?? null : null;
    const h = s.istoric[i];
    if (!h) return null;
    return p === "pm25" ? h.pm25 ?? null : h.dominant === p ? h.valoare : null;
  }
  const nivelLa = (s, i) => (i === 23 ? s.nivel : s.istoric[i]?.nivel ?? null);

  function deseneazaMarcaje() {
    for (const s of S.stare.statii) {
      if (!marcaje[s.id]) {
        const icon = L.divIcon({ className: "marcaj", html: svgTip(s.tip, null), iconSize: [34, 34], iconAnchor: [17, 17] });
        marcaje[s.id] = L.marker([s.lat, s.lon], { icon, title: s.nume, riseOnHover: true, keyboard: true })
          .addTo(harta).on("click", () => deschide(s.id));
      }
      const el = marcaje[s.id].getElement();
      if (!el) continue;
      el.querySelector("svg").style.setProperty("--c", culoare(nivelLa(s, S.ora)));
      el.classList.toggle("ales", S.selectat === s.id);
      el.classList.toggle("stins", S.filtru !== "toate" && s.tip !== S.filtru);
      marcaje[s.id].setZIndexOffset(S.selectat === s.id ? 1000 : 0);
    }
  }

  // ---------- panoul: lista stațiilor ----------
  function nivelOras(i) {
    const n = S.stare.statii.map((s) => nivelLa(s, i)).filter((x) => x !== null).sort((a, b) => a - b);
    return n.length ? n[Math.floor((n.length - 1) / 2)] : null;
  }

  function randeazaAcasa() {
    const st = S.stare, i = S.ora, live = i === 23;
    const statii = st.statii
      .filter((s) => S.filtru === "toate" || s.tip === S.filtru)
      .map((s) => {
        const p = (live ? s.dominant : s.istoric[i]?.dominant) || "pm25";
        return { s, n: nivelLa(s, i), p, v: valoareLa(s, i, p) };
      })
      .sort((a, b) => (S.ordine === "poluat" ? 1 : -1) * (((b.n ?? -1) - (a.n ?? -1)) || ((b.v ?? 0) - (a.v ?? 0))));
    const n = live && st.oras ? st.oras.nivel : nivelOras(i);
    const ora = live ? st.acum : st.statii[0].istoric[i].ora;
    const sursa = st.oras?.sursa === "claude" ? "Rezumat scris de Claude" : S.demo ? "Rezumat automat · pe server îl scrie Claude" : "Rezumat automat";

    $("#continut").innerHTML = `
      <header class="cap">
        <div class="marca">${ICON.marca}văzduh</div>
        <span class="oras">București</span>
        <span class="live ${S.demo ? "demo" : ""}"><i></i>${S.demo ? `Demo · ${data(st.acum)}, ${hh(st.acum)}` : `Live · ${hh(st.acum)}`}</span>
        <button class="buton-tema" id="tema" aria-label="Schimbă tema">${ICON.tema}</button>
      </header>
      <section class="rezumat-oras" aria-live="polite">
        <div class="eticheta">${live ? "Aerul acum" : `Aerul la ${hh(ora)}`}</div>
        <div class="nivel-mare"><span class="punct" style="--c:${culoare(n)}"></span>${n === null ? "Fără date" : NIVELURI[n]}</div>
        ${live && st.oras ? `<p>${esc(st.oras.text)}</p><div class="sursa-ai">${ICON.ai}${sursa}</div>`
                          : `<p>Starea rețelei la ${hh(ora)}, ${zi(ora)}. Trage cursorul până la capăt pentru valorile de acum.</p>`}
      </section>
      ${live && st.alerte.length ? `<section class="alerte" aria-label="Depășiri ale limitelor legale">${st.alerte.map((a) => `
        <button class="alerta" data-id="${esc(a.statie)}"><span class="punct"></span>
          <span><b>${esc(a.text)}</b><span>${esc(a.nume)} · ${fmt(a.valoare, a.parametru)} față de limita de ${a.limita} ${PARAM[a.parametru].u}</span></span>
        </button>`).join("")}</section>` : ""}
      <nav class="filtre" aria-label="Tipul stației">
        <button class="filtru" data-filtru="toate" aria-pressed="${S.filtru === "toate"}">Toate</button>
        ${Object.entries(TIPURI).map(([k, t]) => `<button class="filtru" data-filtru="${k}" aria-pressed="${S.filtru === k}">${tipMic(k)}${t.filtru}</button>`).join("")}
      </nav>
      <div>
        <div class="lista-cap"><span>${statii.length} ${statii.length === 1 ? "stație" : "stații"}</span>
          <button id="ordine">${S.ordine === "poluat" ? "Cele mai poluate întâi" : "Cele mai curate întâi"} ⇅</button></div>
        <ul class="lista">${statii.map(({ s, n, p, v }) => `
          <li><button class="rand ${S.selectat === s.id ? "ales" : ""}" data-id="${esc(s.id)}">
            ${svgTip(s.tip, n)}
            <span><b>${esc(s.nume)}</b><small>${TIPURI[s.tip].nume}${s.sector ? ` · Sector ${s.sector}` : ""}</small></span>
            <span class="val num"><b>${fmt(v, p)}</b><small>${PARAM[p].n}</small></span>
            <span class="pastila" style="--c:${culoare(n)}">${n === null ? "–" : NIVELURI[n]}</span>
          </button></li>`).join("")}
        </ul>
      </div>
      <p class="subsol">${S.stare.statii.length} stații proprii · un set de măsurători la 10 minute · indicele european al calității aerului (EEA)</p>`;
  }

  // ---------- panoul: o stație ----------
  function randeazaStatie() {
    const d = S.detalii, n = d.nivel, dom = d.dominant || "pm25";
    const metrici = ["pm25", "pm10", "no2", "co", "temp", "umid"].map((p) => {
      const v = d.ultim[p];
      const nv = p === "co" ? (v < 5 ? 0 : v < 10 ? 2 : 4) : nivel(p, v);
      const fr = p === "temp" ? (v + 10) / 50 : (v ?? 0) / PARAM[p].max;
      return `<div class="metrica"><span>${PARAM[p].n}</span><b class="num">${fmt(v, p)}<small>${PARAM[p].u}</small></b>
        <div class="bara"><i style="width:${Math.max(4, Math.min(100, fr * 100)).toFixed(0)}%;--c:${nv === null ? "var(--text-3)" : culoare(nv)}"></i></div></div>`;
    }).join("");
    const ai = d.ai || {};
    const sursaAi = ai.sursa === "claude" ? `Claude · ${hh(d.calitate.ultima_citire)}` : S.demo ? "Exemplu · pe server îl scrie Claude" : "Calculat automat";
    const f = d.prognoza?.fereastra;
    const c = d.calitate;
    $("#continut").innerHTML = `
      <div class="cap-statie"><button class="inapoi" id="inapoi">${ICON.inapoi}Stații</button>
        <span class="live ${S.demo ? "demo" : ""}"><i></i>${S.demo ? "Demonstrativ" : `Live · ${hh(c.ultima_citire)}`}</span></div>
      <div class="titlu-statie"><h2>${esc(d.nume)}</h2>
        <p>${TIPURI[d.tip].nume}${d.sector ? ` · Sector ${d.sector}` : ""} · nod ESP32 cu SDS011 și BME280</p></div>
      <div class="erou" style="--c:${culoare(n)}">
        <div class="valoare-mare num">${fmt(d.ultim[dom], dom)}<small>${PARAM[dom].u}</small></div>
        <div><b>${n === null ? "Fără date" : NIVELURI[n]}</b><span>${PARAM[dom].n}, media ultimei ore${dom === "pm25" ? "" : " · poluantul dominant"}</span></div>
      </div>
      <div class="grila">${metrici}</div>
      <section class="card">
        <div class="grafic-cap">
          <div class="segment" role="group" aria-label="Poluant">${["pm25", "pm10", "no2"].map((p) => `<button data-param="${p}" aria-pressed="${S.param === p}">${PARAM[p].n}</button>`).join("")}</div>
          <label class="comutator"><input type="checkbox" id="brut" ${S.brut ? "checked" : ""}>Semnal brut</label>
        </div>
        <div class="grafic" id="grafic"></div>
        <div class="legenda-grafic"><span><i></i>măsurat, filtrat</span><span><i class="p"></i>prognoză 24 h</span>${S.brut ? '<span><i class="b"></i>brut, de la senzor</span>' : ""}<span><i class="l"></i>limită legală</span></div>
      </section>
      <section class="card ai">
        <div class="ai-cap">${ICON.ai}Prognoză AI<span>${sursaAi}</span></div>
        <p>${esc(ai.rezumat)}</p>
        ${ai.recomandare ? `<p class="rec">${esc(ai.recomandare)}</p>` : ""}
        ${f ? `<div class="fereastra">Cel mai curat aer · ${hh(f.start)}–${hh(f.sfarsit)}</div>` : ""}
      </section>
      <section class="card calitate">
        <h3>Calitatea semnalului, ultimele 24 h</h3>
        <dl class="num">
          <dt>Completitudine</dt><dd>${c.completitudine}%</dd>
          <dt>Vârfuri eliminate (filtru median)</dt><dd>${c.varfuri}</dd>
          <dt>Corecție de umiditate pentru PM</dt><dd>${c.corectie_activa ? "puternică" : "mică"} · ${fmt(c.umiditate, "umid")}%</dd>
          <dt>Filtrare</dt><dd>median 3 + medie mobilă 3</dd>
          <dt>Model de prognoză</dt><dd>${esc(d.prognoza?.model || "–")}</dd>
          <dt>Ultima citire</dt><dd>${hh(c.ultima_citire)}</dd>
        </dl>
      </section>`;
    grafic();
  }

  // ---------- graficul: 48 h măsurate + 24 h prognoză ----------
  function grafic() {
    const box = $("#grafic");
    if (!box) return;
    const d = S.detalii, p = S.param, ser = d.serii, prog = d.prognoza?.[p];
    const W = Math.max(280, box.clientWidth), H = 176, st = 30, dr = 8, sus = 10, jos = 22;
    const T = ser.timp, F = ser[p].filtrat, B = ser[p].brut;
    const PO = prog ? d.prognoza.ore : [], PV = prog ? prog.valoare : [];
    const t0 = T[0], t1 = PO.length ? PO[PO.length - 1] : T[T.length - 1];
    // scala se face după semnalul filtrat și prognoză; vârfurile brute care o depășesc sunt tăiate sus
    const vals = [...F, ...(prog ? prog.sus : [])].filter((v) => v !== null);
    let vmax = Math.max(...vals, 1);
    const lim = LIMITE[p];
    const arataLimita = lim && lim.v < vmax * 1.6;
    if (arataLimita) vmax = Math.max(vmax, lim.v);
    const pas = [5, 10, 20, 25, 50, 100, 200].find((x) => vmax / x <= 4) || 500;
    vmax = Math.ceil((vmax * 1.05) / pas) * pas;
    const x = (t) => st + ((t - t0) / (t1 - t0)) * (W - st - dr);
    const y = (v) => sus + (1 - v / vmax) * (H - sus - jos);
    const linie = (ts, vs) => {
      let s = "", sus2 = false;
      ts.forEach((t, i) => {
        if (vs[i] === null || vs[i] === undefined) { sus2 = false; return; }
        s += `${sus2 ? "L" : "M"}${x(t).toFixed(1)},${y(vs[i]).toFixed(1)}`; sus2 = true;
      });
      return s;
    };
    let grid = "";
    for (let v = 0; v <= vmax; v += pas) grid += `<line class="grid" x1="${st}" x2="${W - dr}" y1="${y(v)}" y2="${y(v)}"/><text class="axa" x="${st - 6}" y="${y(v) + 3}" text-anchor="end">${v}</text>`;
    let axaX = "";
    for (let t = t0 - (t0 % 3600) + 3600; t <= t1; t += 3600) {
      const ora = Number(new Date(t * 1000).toLocaleString("en-GB", { hour: "2-digit", hour12: false, timeZone: ZONA }));
      if (ora === 0) axaX += `<line class="grid" x1="${x(t)}" x2="${x(t)}" y1="${sus}" y2="${H - jos}"/><text class="axa" x="${x(t)}" y="${H - 6}" text-anchor="middle">${zi(t)}</text>`;
      else if (ora === 12 && x(t) > st + 14 && x(t) < W - 20) axaX += `<text class="axa" x="${x(t)}" y="${H - 6}" text-anchor="middle">12:00</text>`;
    }
    const acum = T[T.length - 1];
    const filt = linie(T, F);
    const zona = filt ? `${filt}L${x(acum).toFixed(1)},${y(0)}L${x(T.find((t, i) => F[i] !== null)).toFixed(1)},${y(0)}Z` : "";
    const banda = prog ? `M${PO.map((t, i) => `${x(t).toFixed(1)},${y(prog.sus[i]).toFixed(1)}`).join("L")}L${PO.map((t, i) => `${x(t).toFixed(1)},${y(prog.jos[i]).toFixed(1)}`).reverse().join("L")}Z` : "";
    box.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${PARAM[p].n}: ultimele 48 de ore și prognoza pe 24 de ore">
      ${grid}${axaX}
      ${arataLimita ? `<line class="limita" x1="${st}" x2="${W - dr}" y1="${y(lim.v)}" y2="${y(lim.v)}"/><text class="limita-txt" x="${W - dr}" y="${y(lim.v) - 4}" text-anchor="end">${lim.t}</text>` : ""}
      ${banda ? `<path class="banda" d="${banda}"/>` : ""}
      <path class="zona" d="${zona}"/>
      ${S.brut ? `<clipPath id="decupaj"><rect x="${st}" y="${sus}" width="${W - st - dr}" height="${H - sus - jos}"/></clipPath><path class="brut" clip-path="url(#decupaj)" d="${linie(T, B)}"/>` : ""}
      <path class="filtrat" d="${filt}"/>
      ${prog ? `<path class="prog" d="M${x(acum).toFixed(1)},${y(F[F.length - 1] ?? PV[0]).toFixed(1)}L${linie(PO, PV).slice(1)}"/>` : ""}
      <line class="acum" x1="${x(acum)}" x2="${x(acum)}" y1="${sus}" y2="${H - jos}"/>
      <text class="axa" x="${x(acum) + 4}" y="${sus + 8}">acum</text>
      <g id="ghid" style="display:none"><line class="ghid" y1="${sus}" y2="${H - jos}"/><circle class="punct-ghid" r="3.5"/></g>
    </svg><div class="indicatie num" id="indicatie" hidden></div>`;

    const svg = box.querySelector("svg"), ghid = box.querySelector("#ghid"), ind = box.querySelector("#indicatie");
    const toate = [...T.map((t, i) => ({ t, v: F[i], b: B[i] })), ...PO.map((t, i) => ({ t, v: PV[i], prog: true }))].filter((q) => q.v !== null);
    const muta = (ev) => {
      const r = svg.getBoundingClientRect();
      const tx = t0 + (((ev.clientX - r.left) * (W / r.width) - st) / (W - st - dr)) * (t1 - t0);
      const q = toate.reduce((a, b) => (Math.abs(b.t - tx) < Math.abs(a.t - tx) ? b : a));
      ghid.style.display = "";
      ghid.querySelector("line").setAttribute("x1", x(q.t)); ghid.querySelector("line").setAttribute("x2", x(q.t));
      ghid.querySelector("circle").setAttribute("cx", x(q.t)); ghid.querySelector("circle").setAttribute("cy", y(q.v));
      ind.hidden = false;
      ind.style.left = `${Math.min(Math.max((x(q.t) / W) * 100, 16), 84)}%`;
      ind.textContent = `${zi(q.t)} ${hh(q.t)} · ${fmt(q.v, p)} ${PARAM[p].u}${q.prog ? " (prognoză)" : S.brut && q.b !== null ? ` · brut ${fmt(q.b, p)}` : ""}`;
    };
    svg.addEventListener("pointermove", muta);
    svg.addEventListener("pointerdown", muta);
    svg.addEventListener("pointerleave", () => { ghid.style.display = "none"; ind.hidden = true; });
  }

  // ---------- navigare ----------
  async function deschide(id) {
    S.selectat = id;
    deseneazaMarcaje();
    const s = S.stare.statii.find((q) => q.id === id);
    if (s) {
      const z = Math.max(harta.getZoom(), 13);
      const pt = harta.project([s.lat, s.lon], z).add(ingust() ? [0, window.innerHeight * 0.2] : [-200, 0]);
      harta.flyTo(harta.unproject(pt, z), z, { duration: 0.6 });
    }
    S.detalii = await incarcaStatie(id);
    if (S.selectat !== id) return;
    randeazaStatie();
    $("#continut").scrollTop = 0;
  }
  function inchide() {
    S.selectat = null; S.detalii = null;
    deseneazaMarcaje();
    randeazaAcasa();
  }
  const randeaza = () => (S.detalii ? randeazaStatie() : randeazaAcasa());

  $("#continut").addEventListener("click", (ev) => {
    const t = ev.target.closest("button");
    if (!t) return;
    if (t.dataset.id) deschide(t.dataset.id);
    else if (t.dataset.filtru) { S.filtru = t.dataset.filtru; randeazaAcasa(); deseneazaMarcaje(); }
    else if (t.id === "ordine") { S.ordine = S.ordine === "poluat" ? "curat" : "poluat"; randeazaAcasa(); }
    else if (t.id === "inapoi") inchide();
    else if (t.dataset.param) { S.param = t.dataset.param; randeazaStatie(); }
    else if (t.id === "tema") schimbaTema();
  });
  $("#continut").addEventListener("change", (ev) => {
    if (ev.target.id === "brut") { S.brut = ev.target.checked; randeazaStatie(); }
  });

  // ---------- cronologia: ultimele 24 de ore pe hartă ----------
  const reda = $("#reda"), cursor = $("#ora"), oraTxt = $("#ora-txt");
  reda.innerHTML = ICON.play;
  function seteazaOra(i) {
    S.ora = i;
    cursor.value = i;
    oraTxt.textContent = i === 23 ? "Acum" : `${zi(S.stare.statii[0].istoric[i].ora)} ${hh(S.stare.statii[0].istoric[i].ora)}`;
    deseneazaMarcaje();
    coloreazaCartiere();
    if (!S.detalii) randeazaAcasa();
  }
  cursor.addEventListener("input", () => { opresteRedarea(); seteazaOra(Number(cursor.value)); });
  function opresteRedarea() { clearInterval(S.redare); S.redare = null; reda.innerHTML = ICON.play; reda.setAttribute("aria-label", "Redă ultimele 24 de ore"); }
  reda.addEventListener("click", () => {
    if (S.redare) return opresteRedarea();
    if (S.ora === 23) seteazaOra(0);
    reda.innerHTML = ICON.pauza; reda.setAttribute("aria-label", "Oprește redarea");
    S.redare = setInterval(() => { if (S.ora >= 23) opresteRedarea(); else seteazaOra(S.ora + 1); }, 650);
  });

  // ---------- legenda și straturile opționale ----------
  function randeazaLegenda() {
    $("#legenda").innerHTML = `
      <h4>Tipul stației</h4>
      <div class="tipuri">${Object.entries(TIPURI).map(([k, t]) => `<span>${tipMic(k)}${t.nume}</span>`).join("")}</div>
      <h4>Indicele european al calității aerului</h4>
      <div class="scala">${NIVELURI.map((_, i) => `<i style="--c:var(--n${i})" title="${NIVELURI[i]}"></i>`).join("")}</div>
      <div class="scala-txt"><span>Bun</span><span>Moderat</span><span>Extrem de slab</span></div>
      <label class="comutator"><span>Estimare PM2.5 pe cartiere</span><input type="checkbox" id="estimare" ${S.estimare ? "checked" : ""}></label>
      ${S.demo ? "" : `<label class="comutator"><span>Senzori cetățeni</span><input type="checkbox" id="comunitate"></label>
      <label class="comutator"><span>Străzi</span><input type="checkbox" id="strazi"></label>`}
      <div class="atribuire">${esc(S.atribuire || "")}${S.demo ? "" : " · Sensor.Community · © CARTO"}</div>`;
  }
  $("#legenda").addEventListener("change", async (ev) => {
    if (ev.target.id === "estimare") { S.estimare = ev.target.checked; coloreazaCartiere(); }
    if (ev.target.id === "comunitate") {
      if (!ev.target.checked) { stratComunitate?.remove(); return; }
      const senzori = await (await fetch("api/comunitate")).json();
      stratComunitate = L.layerGroup(senzori.map((q) => L.circleMarker([q.lat, q.lon], { radius: 4, className: "comunitate" })
        .bindTooltip(`Senzor cetățean #${q.id} · PM2.5 ${fmt(q.pm25)} µg/m³`, { className: "eticheta-cartier" })
        .on("add", (e) => e.target.getElement()?.style.setProperty("--c", culoare(nivel("pm25", q.pm25))))));
      stratComunitate.addTo(harta);
    }
    if (ev.target.id === "strazi") {
      if (!ev.target.checked) { stratStrazi?.remove(); return; }
      const intunecat = getComputedStyle(document.documentElement).colorScheme === "dark";
      stratStrazi = L.tileLayer(`https://{s}.basemaps.cartocdn.com/${intunecat ? "dark_all" : "light_all"}/{z}/{x}/{y}{r}.png`,
        { subdomains: "abcd", className: "strazi", maxZoom: 19 }).addTo(harta);
    }
  });
  $("#buton-legenda").addEventListener("click", () => {
    const deschisa = $("#legenda").classList.toggle("deschisa");
    $("#buton-legenda").setAttribute("aria-expanded", deschisa);
  });
  $("#zoom-plus").addEventListener("click", () => harta.zoomIn());
  $("#zoom-minus").addEventListener("click", () => harta.zoomOut());

  // foaia de jos pe telefon: atinge sau trage mânerul
  const panou = $("#panou");
  let yStart = null;
  $("#maner").addEventListener("pointerdown", (e) => { yStart = e.clientY; });
  window.addEventListener("pointerup", (e) => {
    if (yStart === null) return;
    const dy = e.clientY - yStart;
    yStart = null;
    if (Math.abs(dy) < 8) panou.classList.toggle("extins");
    else panou.classList.toggle("extins", dy < 0);
  });

  function schimbaTema() {
    const r = document.documentElement;
    const acum = r.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    r.dataset.theme = acum === "dark" ? "light" : "dark";
    try { localStorage.setItem("vazduh-tema", r.dataset.theme); } catch (e) { /* fără stocare */ }
  }
  try { const t = localStorage.getItem("vazduh-tema"); if (t) document.documentElement.dataset.theme = t; } catch (e) { /* fără stocare */ }

  window.addEventListener("resize", () => { if (S.detalii) grafic(); });

  // ---------- pornire ----------
  (async () => {
    await Promise.all([incarcaHarta(), incarcaStare()]);
    randeazaLegenda();
    deseneazaMarcaje();
    coloreazaCartiere();
    seteazaOra(23);
    if (!S.demo) {
      setInterval(async () => {
        await incarcaStare();
        if (S.ora === 23) { deseneazaMarcaje(); coloreazaCartiere(); if (!S.detalii) randeazaAcasa(); }
      }, 60000);
    }
  })();
})();
