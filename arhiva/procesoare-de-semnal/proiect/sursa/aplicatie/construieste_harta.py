"""Construiește static/harta.json (contur București, sectoare, cartiere) din pachetele npm @nspot.

Surse: @nspot/geo-pack-romania-uat 1.1.1 (ANCPI, CC BY 4.0) și
@nspot/geo-pack-romania-neighbourhoods 1.6.0 (OpenStreetMap, ODbL 1.0).
Utilizare: python3 construieste_harta.py <pack-uat.json> <pack-cartiere.json> <iesire.json>
"""
import json
import sys


def simplifica(puncte, tol):
    # Douglas-Peucker pe un inel de coordonate
    if len(puncte) < 4:
        return puncte
    (x1, y1), (x2, y2) = puncte[0], puncte[-1]
    dmax, idx = 0, 0
    for i in range(1, len(puncte) - 1):
        x0, y0 = puncte[i]
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0:
            d = ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5
        else:
            t = max(0, min(1, ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)))
            d = ((x0 - x1 - t * dx) ** 2 + (y0 - y1 - t * dy) ** 2) ** 0.5
        if d > dmax:
            dmax, idx = d, i
    if dmax > tol:
        return simplifica(puncte[: idx + 1], tol)[:-1] + simplifica(puncte[idx:], tol)
    return [puncte[0], puncte[-1]]


def geometrie(g, tol):
    poligoane = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    rezultat = []
    for poli in poligoane:
        inele = []
        for inel in poli:
            s = simplifica(inel, tol)
            if len(s) >= 4:
                inele.append([[round(x, 5), round(y, 5)] for x, y in s])
        if inele:
            rezultat.append(inele)
    return {"type": "MultiPolygon", "coordinates": rezultat}


uat = json.load(open(sys.argv[1], encoding="utf-8"))["regions"]["features"]
cartiere = json.load(open(sys.argv[2], encoding="utf-8"))["regions"]["features"]

oras = next(f for f in uat if f["properties"]["slug"] == "bucuresti-b")
sectoare = [f for f in uat if f["properties"].get("parent") == "bucuresti-b"]
cart = [f for f in cartiere if f["properties"].get("parent") == "bucuresti-b"]

harta = {
    "atribuire": "Limite: ANCPI (CC BY 4.0) · Cartiere: © OpenStreetMap (ODbL)",
    "oras": geometrie(oras["geometry"], 0.0002),
    "sectoare": [{"nr": int(f["properties"]["name"].split()[-1]), "geometrie": geometrie(f["geometry"], 0.0002)}
                 for f in sorted(sectoare, key=lambda f: f["properties"]["name"])],
    "cartiere": [{"nume": f["properties"]["name"], "geometrie": geometrie(f["geometry"], 0.00012)}
                 for f in sorted(cart, key=lambda f: f["properties"]["name"])],
}
json.dump(harta, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("cartiere:", len(harta["cartiere"]), "sectoare:", len(harta["sectoare"]))
