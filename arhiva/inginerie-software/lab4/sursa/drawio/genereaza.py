# Genereaza cele doua diagrame .drawio (se deschid in app.diagrams.net) si linkurile #R pentru editor
import base64, urllib.parse, zlib
from xml.sax.saxutils import escape

def model(cells):
    body = "".join(cells)
    return f'<mxfile><diagram name="Pagina-1"><mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" page="1" pageScale="1" pageWidth="1100" pageHeight="850"><root><mxCell id="0"/><mxCell id="1" parent="0"/>{body}</root></mxGraphModel></diagram></mxfile>'

def v(id, val, style, x, y, w, h):
    return f'<mxCell id="{id}" value="{escape(val, {chr(34): "&quot;"})}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'

def e(id, s, t, style, val=""):
    return f'<mxCell id="{id}" value="{escape(val)}" style="{style}" edge="1" parent="1" source="{s}" target="{t}"><mxGeometry relative="1" as="geometry"/></mxCell>'

# ---------- 1. Use case: Tema 20 (Lab 3) ----------
ACT = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fontSize=13;"
UC = "ellipse;whiteSpace=wrap;html=1;fontSize=13;"
LN = "endArrow=none;html=1;"
uc = [v("sys", "Sistem administrare fabrică", "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fillColor=none;fontSize=14;", 250, 40, 300, 470),
      v("M", "Manager", ACT, 90, 130, 30, 60), v("O", "Operator", ACT, 690, 350, 30, 60)]
nume = ["Adaugă secție", "Adaugă linie de producție", "Mută mașină pe altă linie", "Supraveghează mașină", "Înregistrează intervenție"]
for i, n in enumerate(nume):
    uc.append(v(f"u{i}", n, UC, 300, 80 + i * 85, 200, 60))
for i in range(3):
    uc.append(e(f"m{i}", "M", f"u{i}", LN))
for i in (3, 4):
    uc.append(e(f"o{i}", f"u{i}", "O", LN))

# ---------- 2. Activitate: APD Lucrarea 4, Exercitiul 3 (V2) ----------
ACTN = "rounded=1;whiteSpace=wrap;html=1;arcSize=40;fontSize=13;"
BAR = "rounded=0;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=none;"
ARR = "endArrow=block;endFill=1;html=1;edgeStyle=orthogonalEdgeStyle;rounded=0;"
cx = 420
ac = [v("st", "", "ellipse;html=1;fillColor=#000000;strokeColor=none;", cx - 12, 20, 24, 24),
      v("a1", "Inițializează vectorul a cu N elemente", ACTN, cx - 150, 70, 300, 46),
      v("a2", "Creează P threaduri și vectorul pSum[P]", ACTN, cx - 150, 145, 300, 46),
      v("f1", "", BAR, cx - 330, 220, 660, 8)]
thr = [("t0", "Thread 0:<br>pSum[0] = suma elementelor<br>0 … N/P − 1"),
       ("t1", "Thread 1:<br>pSum[1] = suma elementelor<br>N/P … 2N/P − 1"),
       ("tp", "Thread P−1:<br>pSum[P−1] = suma elementelor<br>(P−1)N/P … N − 1")]
for k, (id, txt) in enumerate(thr):
    ac.append(v(id, txt, ACTN, cx - 335 + k * 245, 255, 200, 70))
ac += [v("dots", "…", "text;html=1;align=center;fontSize=20;fontStyle=1;", cx + 112, 272, 30, 30),
       v("j1", "", BAR, cx - 330, 355, 660, 8),
       v("a3", "Thread principal: Join pe fiecare thread<br>și sTemp = sTemp + pSum[i]", ACTN, cx - 170, 390, 340, 56),
       v("a4", "Afișează Sum(A) și timpul ParV2", ACTN, cx - 150, 475, 300, 46),
       v("d1", "Sum(A) = suma serială?", "rhombus;whiteSpace=wrap;html=1;fontSize=13;", cx - 110, 550, 220, 80),
       v("ok", "Rezultat corect", ACTN, cx - 330, 660, 180, 46),
       v("ko", "Rezultat greșit", ACTN, cx + 150, 660, 180, 46),
       v("mg", "", "rhombus;whiteSpace=wrap;html=1;", cx - 20, 740, 40, 40),
       v("fin", "", "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;", cx - 15, 810, 30, 30)]
ac += [e("e1", "st", "a1", ARR), e("e2", "a1", "a2", ARR), e("e3", "a2", "f1", ARR)]
for k, (id, _) in enumerate(thr):
    ac += [e(f"ef{k}", "f1", id, ARR), e(f"ej{k}", id, "j1", ARR)]
ac += [e("e4", "j1", "a3", ARR), e("e5", "a3", "a4", ARR), e("e6", "a4", "d1", ARR),
       e("e7", "d1", "ok", ARR, "[da]"), e("e8", "d1", "ko", ARR, "[nu]"),
       e("e9", "ok", "mg", ARR + "exitX=0.5;exitY=1;entryX=0;entryY=0.5;"), e("e10", "ko", "mg", ARR + "exitX=0.5;exitY=1;entryX=1;entryY=0.5;"), e("e11", "mg", "fin", ARR)]

for nume_f, cells in (("use_case_tema20.drawio", uc), ("activitate_APD_L4_ex3.drawio", ac)):
    xml = model(cells)
    open(nume_f, "w", encoding="utf-8").write(xml)
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    raw = c.compress(xml.encode("utf-8")) + c.flush()
    link = "https://app.diagrams.net/?ui=kennedy&dark=0#R" + urllib.parse.quote(base64.b64encode(raw).decode(), safe="")
    open(nume_f + ".link", "w").write(link)
    print(nume_f, len(link))
