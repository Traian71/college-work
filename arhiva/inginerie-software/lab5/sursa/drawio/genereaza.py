# Genereaza diagrama de secventa (.drawio, se deschide in app.diagrams.net) si linkul #R pentru editor.
# Exercitiul din fisa: scenariul de promovare a unui student la un curs.
import base64, urllib.parse, zlib
from xml.sax.saxutils import escape

W, H = 1000, 850

def model(cells):
    return (f'<mxfile><diagram name="Pagina-1"><mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" page="1" pageScale="1" '
            f'pageWidth="{W}" pageHeight="{H}"><root><mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>')

def esc(s):
    return escape(s, {'"': "&quot;"})

def v(id, val, style, x, y, w, h):
    return (f'<mxCell id="{id}" value="{esc(val)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def msg(id, val, x1, x2, y, style, puncte=None):
    pts = ""
    if puncte:
        pts = '<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in puncte) + "</Array>"
    y2 = puncte[-1][1] if puncte else y
    return (f'<mxCell id="{id}" value="{esc(val)}" style="{style}" edge="1" parent="1"><mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{x1}" y="{y}" as="sourcePoint"/><mxPoint x="{x2}" y="{y2}" as="targetPoint"/>{pts}'
            f'<mxPoint y="-9" as="offset"/></mxGeometry></mxCell>')

LIFE = ("shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=0;collapsible=0;"
        "recursiveResize=0;outlineConnect=0;size=40;fontSize=13;")
ACT = "html=1;points=[];perimeter=orthogonalPerimeter;outlineConnect=0;fillColor=#ffffff;"
CALL = "endArrow=block;endFill=1;html=1;fontSize=12;labelBackgroundColor=#ffffff;"
RET = "endArrow=open;endFill=0;dashed=1;html=1;fontSize=12;labelBackgroundColor=#ffffff;"
SELF = CALL + "edgeStyle=none;rounded=0;align=left;"
TXT = "text;html=1;align=left;verticalAlign=middle;fontSize=12;"

# obiectele (x = centrul liniei de viata)
X = {"s": 120, "sec": 370, "p": 620, "c": 870}
obiecte = [("s", "s : Student"), ("sec", "sec : Secretariat"), ("p", "p : Profesor"), ("c", "c : Catalog")]
celule = [v(k, nume, LIFE, X[k] - 75, 20, 150, 800) for k, nume in obiecte]

# perioadele de activare: (obiect, y inceput, y sfarsit)
for i, (k, y1, y2) in enumerate([("s", 100, 790), ("sec", 100, 210), ("sec", 590, 650), ("p", 230, 440),
                                  ("p", 680, 740), ("c", 150, 180), ("c", 330, 360), ("c", 450, 520), ("c", 740, 790)]):
    celule.append(v(f"a{i}", "", ACT, X[k] - 6, y1, 12, y2 - y1))

# mesajele, in ordinea secventei
m = [
    ("s", "sec", 110, "1 : inscrieLaCurs(student, curs)", CALL),
    ("sec", "c", 160, "2 : adaugaStudent(student)", CALL),
    ("sec", "s", 200, "3 : confirmareInscriere", RET),
    ("s", "p", 240, "*[14 săptămâni] 4 : participaLaCurs()", CALL),
    ("s", "p", 290, "*[14 săptămâni] 5 : predaLaborator(tema)", CALL),
    ("p", "c", 340, "6 : adaugaNota(student, notaLab)", CALL),
    ("s", "p", 390, "[notaLab ≥ 5] 7 : sustineExamen(lucrare)", CALL),
    ("p", "c", 460, "9 : adaugaNota(student, notaExamen)", CALL),
    ("c", "s", 510, "10 : anuntaPromovare(media)", CALL),
    ("s", "sec", 600, "11 : platesteTaxa(taxaRestanta)", CALL),
    ("sec", "s", 640, "12 : chitanta", RET),
    ("s", "p", 690, "[taxă plătită] 13 : sustineRestanta(lucrare)", CALL),
    ("p", "c", 750, "14 : adaugaNota(student, notaRestanta)", CALL),
    ("c", "s", 780, "15 : anuntaRezultat(notaRestanta)", CALL),
]
for i, (a, b, y, txt, st) in enumerate(m):
    dx = 6 if X[b] > X[a] else -6
    celule.append(msg(f"m{i}", txt, X[a] + dx, X[b] - dx, y, st))

# mesaj catre el insusi: profesorul corecteaza lucrarea
xp = X["p"] + 6
celule.append(msg("self", "", xp, xp, 410, SELF, [(xp + 45, 410), (xp + 45, 435), (xp, 435)]))
celule.append(v("selft", "8 : notaExamen := corecteaza(lucrare)", TXT, xp + 52, 410, 250, 25))

# blocul conditional alt: promovat la examen / restanta
celule.append(v("alt", "alt", "shape=umlFrame;whiteSpace=wrap;html=1;width=50;height=26;fontStyle=1;fontSize=13;fillColor=none;",
                40, 480, 900, 325))
celule.append(v("g1", "[notaExamen ≥ 5]", TXT, 140, 482, 160, 24))
celule.append(v("sep", "", "line;strokeWidth=1;dashed=1;html=1;strokeColor=#000000;", 40, 540, 900, 10))
celule.append(v("g2", "[notaExamen &lt; 5] (restanță)", TXT, 140, 552, 220, 24))

xml = model(celule)
nume_f = "secventa_promovare_student.drawio"
open(nume_f, "w", encoding="utf-8").write(xml)
c = zlib.compressobj(9, zlib.DEFLATED, -15)
raw = c.compress(xml.encode("utf-8")) + c.flush()
link = "https://app.diagrams.net/?ui=kennedy&dark=0#R" + urllib.parse.quote(base64.b64encode(raw).decode(), safe="")
open(nume_f + ".link", "w").write(link)
print(nume_f, len(link))
