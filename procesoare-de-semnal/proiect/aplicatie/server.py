"""Văzduh: serverul de achiziție și aplicația web.

Primește măsurători JSON (POST /api/ingest), le prelucrează în timp real și le servește hărții.
Pornire: python3 server.py   (variabile: VAZDUH_DB, CHEIE_INGEST, ANTHROPIC_API_KEY, PORT)
"""
import json
import os
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from statistics import mean

from flask import Flask, abort, g, jsonify, request, send_from_directory

import prelucrare as pr
import prognoza

DIR = Path(__file__).resolve().parent
DB = os.environ.get("VAZDUH_DB", str(DIR / "date" / "vazduh.db"))
CHEIE_INGEST = os.environ.get("CHEIE_INGEST", "")
POLUANTI = ("pm25", "pm10", "no2")

app = Flask(__name__, static_folder=None)


def inauntru(lon, lat, geometrie):
    gasit = False
    for poligon in geometrie["coordinates"]:
        for k, inel in enumerate(poligon):
            c = False
            for i in range(len(inel)):
                (x1, y1), (x2, y2) = inel[i - 1], inel[i]
                if (y1 > lat) != (y2 > lat) and lon < (x2 - x1) * (lat - y1) / (y2 - y1) + x1:
                    c = not c
            if c:
                gasit = k == 0
        if gasit:
            return True
    return False


def incarca_statii():
    statii = json.loads((DIR / "statii.json").read_text(encoding="utf-8"))
    harta = json.loads((DIR / "static" / "harta.json").read_text(encoding="utf-8"))
    for s in statii:
        s["sector"] = next((x["nr"] for x in harta["sectoare"] if inauntru(s["lon"], s["lat"], x["geometrie"])), None)
    return {s["id"]: s for s in statii}


STATII = incarca_statii()


def db():
    if "db" not in g:
        Path(DB).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(DB)
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.executescript("""
            CREATE TABLE IF NOT EXISTS masuratori (
                statie TEXT, parametru TEXT, timp INTEGER,
                brut REAL, corectat REAL, median REAL, filtrat REAL, varf INTEGER,
                PRIMARY KEY (statie, parametru, timp));
            CREATE TABLE IF NOT EXISTS cache_ai (cheie TEXT PRIMARY KEY, creat INTEGER, continut TEXT);
        """)
    return g.db


@app.teardown_appcontext
def inchide_db(_):
    con = g.pop("db", None)
    if con is not None:
        con.close()


def timp_unix(valoare):
    if isinstance(valoare, (int, float)):
        return int(valoare)
    return int(datetime.fromisoformat(str(valoare).replace("Z", "+00:00")).timestamp())


def salveaza(con, statie, parametru, t, valoare):
    """Prelucrare cauzală la sosirea fiecărui eșantion: corecție de umiditate, median pe 3, medie mobilă pe 3."""
    corectat = valoare
    if parametru in ("pm25", "pm10"):
        rand = con.execute("SELECT corectat FROM masuratori WHERE statie=? AND parametru='umid' "
                           "AND timp BETWEEN ? AND ? ORDER BY timp DESC LIMIT 1", (statie, t - 1800, t)).fetchone()
        corectat = pr.corectie_umiditate(valoare, rand[0] if rand else None)
    anterioare = con.execute("SELECT corectat, median FROM masuratori WHERE statie=? AND parametru=? "
                             "AND timp < ? AND timp >= ? ORDER BY timp DESC LIMIT 2",
                             (statie, parametru, t, t - 3600)).fetchall()
    med = pr.filtru_median([r[0] for r in reversed(anterioare)] + [corectat])[-1]
    filtrat = mean([r[1] for r in anterioare] + [med])
    con.execute("INSERT OR REPLACE INTO masuratori VALUES (?,?,?,?,?,?,?,?)",
                (statie, parametru, t, valoare, corectat, med, filtrat, int(pr.este_varf(corectat, med))))


@app.post("/api/ingest")
def ingest():
    if CHEIE_INGEST and request.headers.get("X-Cheie") != CHEIE_INGEST:
        abort(401)
    date = request.get_json(silent=True)
    if date is None:
        return jsonify(eroare="Corpul cererii trebuie să fie JSON"), 400
    if isinstance(date, dict):
        date = [date]
    acceptate, respinse = [], 0
    for m in date:
        try:
            statie, parametru, t = m["statie"], m["parametru"], timp_unix(m["timp"])
        except (KeyError, TypeError, ValueError):
            respinse += 1
            continue
        if statie not in STATII or not pr.valid(parametru, m.get("valoare")):
            respinse += 1  # stație necunoscută, valoare lipsă (-200) sau în afara domeniului senzorului
            continue
        acceptate.append((t, parametru != "umid", statie, parametru, float(m["valoare"])))
    con = db()
    with con:
        # umiditatea intră prima, ca să fie folosită la corecția PM din același moment
        for t, _, statie, parametru, valoare in sorted(acceptate):
            salveaza(con, statie, parametru, t, valoare)
    return jsonify(primite=len(date), acceptate=len(acceptate), respinse=respinse)


def ultimul_timp(con):
    return con.execute("SELECT MAX(timp) FROM masuratori").fetchone()[0]


def serie(con, statie, parametru, de_la, pana_la, coloana="filtrat"):
    return con.execute(f"SELECT timp, {coloana} FROM masuratori WHERE statie=? AND parametru=? "
                       "AND timp > ? AND timp <= ? ORDER BY timp", (statie, parametru, de_la, pana_la)).fetchall()


def valori_curente(con, statie, acum):
    """Media ultimei ore pentru poluanți, ultima valoare filtrată pentru restul."""
    rezultat = {}
    for p in pr.PARAMETRI:
        s = serie(con, statie, p, acum - 3600, acum)
        if s:
            rezultat[p] = round(mean(v for _, v in s) if p in POLUANTI else s[-1][1], 2 if p == "co" else 1)
    return rezultat


def istoric_24h(con, statie, acum):
    ore = []
    orare = {p: pr.medii_orare(serie(con, statie, p, acum - 24 * 3600, acum)) for p in POLUANTI}
    for k in range(23, -1, -1):
        ora = acum - acum % 3600 - k * 3600
        valori = {p: orare[p].get(ora) for p in POLUANTI if orare[p].get(ora) is not None}
        n, dominant = pr.indice(valori)
        ore.append({"ora": ora, "nivel": n, "dominant": dominant,
                    "valoare": round(valori[dominant], 1) if dominant else None,
                    "pm25": round(valori["pm25"], 1) if "pm25" in valori else None})
    return ore


def alerte_statie(con, statie, acum):
    orare = {p: pr.medii_orare(serie(con, statie, p, acum - 24 * 3600, acum)) for p in ("pm10", "no2", "co")}
    alerte = pr.depasiri(orare["pm10"], orare["no2"], orare["co"])
    for a in alerte:
        a.update(statie=statie, nume=STATII[statie]["nume"])
    return alerte


def rezumat_statie(con, s, acum):
    curente = valori_curente(con, s["id"], acum)
    n, dominant = pr.indice({p: v for p, v in curente.items() if p in POLUANTI})
    return dict(s, ultim=curente, nivel=n, dominant=dominant, istoric=istoric_24h(con, s["id"], acum))


@app.get("/api/stare")
def stare():
    con = db()
    acum = ultimul_timp(con)
    if acum is None:
        return jsonify(acum=None, statii=list(STATII.values()), alerte=[], oras=None)
    statii = [rezumat_statie(con, s, acum) for s in STATII.values()]
    alerte = [a for s in STATII for a in alerte_statie(con, s, acum)]
    oras = prognoza.rezumat_oras(con, statii, alerte, acum)
    return jsonify(acum=acum, statii=statii, alerte=alerte, oras=oras)


@app.get("/api/statie/<statie>")
def detalii(statie):
    if statie not in STATII:
        abort(404)
    con = db()
    acum = ultimul_timp(con)
    if acum is None:
        abort(404)
    s = rezumat_statie(con, STATII[statie], acum)
    de_la = acum - 48 * 3600
    serii = {"timp": [t for t, _ in serie(con, statie, "pm25", de_la, acum)]}
    for p in POLUANTI:
        brut = dict(serie(con, statie, p, de_la, acum, "brut"))
        filtrat = dict(serie(con, statie, p, de_la, acum))
        serii[p] = {"brut": [brut.get(t) for t in serii["timp"]], "filtrat": [filtrat.get(t) for t in serii["timp"]]}

    zi = acum - 24 * 3600
    esantioane = con.execute("SELECT COUNT(*), COALESCE(SUM(varf),0) FROM masuratori WHERE statie=? "
                             "AND parametru IN ('pm25','pm10','no2') AND timp > ?", (statie, zi)).fetchone()
    umid = s["ultim"].get("umid")
    calitate = {
        "completitudine": round(min(100, 100 * esantioane[0] / (3 * 144)), 0),
        "varfuri": esantioane[1],
        "umiditate": umid,
        "corectie_activa": umid is not None and umid >= 70,
        "ultima_citire": acum,
    }
    istoric = {p: pr.medii_orare(serie(con, statie, p, acum - 7 * 24 * 3600, acum)) for p in POLUANTI}
    prog = prognoza.prognoza(s, istoric, acum)
    ai = prognoza.text_statie(con, s, istoric, prog, acum)
    return jsonify(dict(s, serii=serii, prognoza=prog, ai=ai, calitate=calitate,
                        alerte=alerte_statie(con, statie, acum)))


@app.get("/api/comunitate")
def comunitate():
    return jsonify(prognoza.senzori_comunitate())


@app.get("/")
def index():
    return send_from_directory(DIR / "static", "index.html")


@app.get("/<path:fisier>")
def static_files(fisier):
    return send_from_directory(DIR / "static", fisier)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
