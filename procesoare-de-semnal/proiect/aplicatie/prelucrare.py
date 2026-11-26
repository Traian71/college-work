"""Prelucrarea semnalelor de la senzori: validare, corecție de umiditate, filtrare, medii, indice, praguri."""
import math
from statistics import median

# unitati: pm25, pm10, no2 in µg/m³, co in mg/m³, temp in °C, umid in %
PARAMETRI = {
    "pm25": {"nume": "PM2.5", "unitate": "µg/m³", "min": 0, "max": 1000},
    "pm10": {"nume": "PM10", "unitate": "µg/m³", "min": 0, "max": 1000},
    "no2": {"nume": "NO₂", "unitate": "µg/m³", "min": 0, "max": 2000},
    "co": {"nume": "CO", "unitate": "mg/m³", "min": 0, "max": 100},
    "temp": {"nume": "Temperatură", "unitate": "°C", "min": -40, "max": 60},
    "umid": {"nume": "Umiditate", "unitate": "%", "min": 0, "max": 100},
}

LIPSA = -200  # valoarea folosita pentru "lipsa" in setul UCI Air Quality

# Indicele european al calitatii aerului (EEA, benzile revizuite dupa ghidurile OMS 2021, pe valori orare):
# limitele de sus ale primelor 5 clase
NIVELURI = ["Bun", "Acceptabil", "Moderat", "Slab", "Foarte slab", "Extrem de slab"]
PRAGURI_INDICE = {
    "pm25": [5, 15, 50, 90, 140],
    "pm10": [15, 45, 120, 195, 270],
    "no2": [10, 25, 60, 100, 150],
}

# Valori limita din Legea 104/2011
LIMITE = {
    "pm10_zi": 50,    # medie zilnica, µg/m³ (max. 35 depasiri pe an)
    "no2_ora": 200,   # medie orara, µg/m³ (max. 18 depasiri pe an)
    "co_8h": 10,      # maxima zilnica a mediilor pe 8 ore, mg/m³
}

KAPPA = 0.4  # higroscopicitatea particulelor, pentru corectia de umiditate


def valid(parametru, valoare):
    if parametru not in PARAMETRI or valoare is None:
        return False
    try:
        v = float(valoare)
    except (TypeError, ValueError):
        return False
    if math.isnan(v) or v == LIPSA:
        return False
    return PARAMETRI[parametru]["min"] <= v <= PARAMETRI[parametru]["max"]


def corectie_umiditate(pm, umid):
    """Senzorii optici (SDS011) numara si apa absorbita de particule, deci supraestimeaza la umiditate mare.
    Factorul de crestere dupa teoria kappa-Köhler: C = 1 + (kappa/1.65) / (100/RH - 1)."""
    if umid is None:
        return pm
    rh = min(max(umid, 0), 95)
    if rh < 1:
        return pm
    return pm / (1 + (KAPPA / 1.65) / (100 / rh - 1))


def filtru_median(valori, fereastra=3):
    """Median cauzal: pentru fiecare esantion, mediana ultimelor `fereastra` valori. Elimina varfurile izolate."""
    return [median(valori[max(0, i - fereastra + 1): i + 1]) for i in range(len(valori))]


def medie_mobila(valori, fereastra=3):
    """Medie mobila cauzala (filtru FIR trece-jos cu coeficienti egali). Netezeste zgomotul mic."""
    return [sum(valori[max(0, i - fereastra + 1): i + 1]) / len(valori[max(0, i - fereastra + 1): i + 1])
            for i in range(len(valori))]


def este_varf(valoare, mediana):
    return abs(valoare - mediana) > max(8.0, 0.6 * mediana)


def filtreaza(valori):
    """Lantul complet: median (varfuri) apoi medie mobila (zgomot). Intoarce valorile filtrate si nr. de varfuri."""
    med = filtru_median(valori)
    varfuri = sum(1 for v, m in zip(valori, med) if este_varf(v, m))
    return medie_mobila(med), varfuri


def medii_orare(serie, pas_asteptat=600):
    """serie: lista de (timp_unix, valoare). Media pe fiecare ora, doar daca ora are cel putin 75% din esantioane."""
    pe_ora = {}
    for t, v in serie:
        pe_ora.setdefault(t - t % 3600, []).append(v)
    minim = max(1, math.ceil(0.75 * 3600 / pas_asteptat))
    return {ora: sum(v) / len(v) for ora, v in sorted(pe_ora.items()) if len(v) >= minim}


def nivel(parametru, valoare):
    if valoare is None or parametru not in PRAGURI_INDICE:
        return None
    for i, prag in enumerate(PRAGURI_INDICE[parametru]):
        if valoare <= prag:
            return i
    return 5


def indice(valori):
    """Indicele general = cel mai slab nivel dintre poluanti. Intoarce (nivel, poluantul dominant)."""
    rezultat = (None, None)
    for p, v in valori.items():
        n = nivel(p, v)
        if n is not None and (rezultat[0] is None or n > rezultat[0]):
            rezultat = (n, p)
    return rezultat


def medie_mobila_8h_max(orare):
    """orare: dict ora -> valoare. Maxima mediilor mobile pe 8 ore (pentru CO)."""
    ore = sorted(orare)
    maxim = None
    for i in range(7, len(ore)):
        bucata = ore[i - 7: i + 1]
        if bucata[-1] - bucata[0] == 7 * 3600:
            m = sum(orare[o] for o in bucata) / 8
            maxim = m if maxim is None else max(maxim, m)
    return maxim


def depasiri(orare_pm10, orare_no2, orare_co):
    """Verifica valorile limita din Legea 104/2011 pe ultimele 24 de ore."""
    alerte = []
    if len(orare_pm10) >= 18:
        zi = sum(orare_pm10.values()) / len(orare_pm10)
        if zi > LIMITE["pm10_zi"]:
            alerte.append({"parametru": "pm10", "valoare": round(zi, 1), "limita": LIMITE["pm10_zi"],
                           "text": "PM10 peste limita zilnică"})
    if orare_no2:
        maxim = max(orare_no2.values())
        if maxim > LIMITE["no2_ora"]:
            alerte.append({"parametru": "no2", "valoare": round(maxim, 1), "limita": LIMITE["no2_ora"],
                           "text": "NO₂ peste limita orară"})
    co8 = medie_mobila_8h_max(orare_co)
    if co8 is not None and co8 > LIMITE["co_8h"]:
        alerte.append({"parametru": "co", "valoare": round(co8, 2), "limita": LIMITE["co_8h"],
                       "text": "CO peste limita pe 8 ore"})
    return alerte
