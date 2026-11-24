# Schemele SVG din conspect: rețele, grafice de activări, gradient descent, backprop, CNN, PCA.
import math

INK, MUTED, ACC, ACC2, GREEN, RED = "#2d2a26", "#7a6f64", "#b4532a", "#c98a2b", "#557a44", "#b23b3b"
FILL_IN, FILL_H, FILL_O, LINE = "#ffffff", "#fbeee0", "#f3dcc6", "#c9b8a6"

def _defs():
    return ('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
            '<marker id="arR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker></defs>')

def _lbl(x, y, t, color=INK, size=12, bold=False, anchor="middle", bg=True):
    w = 7.2 * len(t) * size / 12 + 6
    r = (f'<rect x="{x - w/2 if anchor=="middle" else x-3:.1f}" y="{y - size*0.85:.1f}" width="{w:.1f}" height="{size*1.25:.1f}" rx="3" fill="#fffaf3" opacity="0.92"/>'
         if bg else "")
    return r + (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{color}"'
                f'{" font-weight=\"700\"" if bold else ""}>{t}</text>')

def retea(straturi, muchii, W=560, H=250, r=21, titluri=None, note=None, pe_muchie=None):
    """straturi: listă de liste cu (id, eticheta, fill, sub-eticheta); muchii: (src, dst, text, t, culoare)."""
    pos = {}
    n = len(straturi)
    for li, st in enumerate(straturi):
        x = 50 + li * (W - 100) / (n - 1)
        for ni, (nid, et, fill, sub) in enumerate(st):
            y = (H - 40) * (ni + 1) / (len(st) + 1) + 20
            pos[nid] = (x, y, et, fill, sub)
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" font-family="Avenir Next, Helvetica, sans-serif">', _defs()]
    lab = []
    for (a, b, t, frac, *c) in muchii:
        x1, y1 = pos[a][:2]; x2, y2 = pos[b][:2]
        d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
        sx, sy, ex, ey = x1 + ux * r, y1 + uy * r, x2 - ux * (r + 2), y2 - uy * (r + 2)
        col = c[0] if c else LINE
        o.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{col}" stroke-width="1.6" marker-end="url(#ar)"/>')
        if t:
            lx, ly = sx + (ex - sx) * frac, sy + (ey - sy) * frac
            lab.append(_lbl(lx, ly + 4, t, ACC if not c else c[0], 11.5, True))
    for nid, (x, y, et, fill, sub) in pos.items():
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{ACC}" stroke-width="1.6"/>')
        o.append(f'<text x="{x:.1f}" y="{y+5:.1f}" font-size="14" text-anchor="middle" fill="{INK}" font-weight="600">{et}</text>')
        if sub:
            for k, line in enumerate(sub.split("|")):
                o.append(f'<text x="{x:.1f}" y="{y + r + 15 + 13*k:.1f}" font-size="11" text-anchor="middle" fill="{GREEN}">{line}</text>')
    o += lab
    if titluri:
        for li, t in enumerate(titluri):
            x = 50 + li * (W - 100) / (n - 1)
            o.append(f'<text x="{x:.1f}" y="13" font-size="11.5" text-anchor="middle" fill="{MUTED}" font-style="italic">{t}</text>')
    o.append("</svg>")
    return "".join(o)

def neuron():
    W, H = 560, 190
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" font-family="Avenir Next, Helvetica, sans-serif">', _defs()]
    ins = [("x₁ = 2", "w₁ = 0,5", 40), ("x₂ = −1", "w₂ = 1", 95), ("x₃ = 3", "w₃ = 0,2", 150)]
    for t, w, y in ins:
        o.append(f'<circle cx="55" cy="{y}" r="22" fill="#fff" stroke="{ACC}" stroke-width="1.6"/>')
        o.append(f'<text x="55" y="{y+4}" font-size="11.5" text-anchor="middle" fill="{INK}">{t}</text>')
        o.append(f'<line x1="78" y1="{y}" x2="226" y2="{95 + (y-95)*0.35}" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ar)"/>')
        o.append(_lbl(150, (y + 95 + (y-95)*0.35) / 2 + 2, w, ACC, 11.5, True))
    o.append(f'<circle cx="270" cy="95" r="42" fill="{FILL_H}" stroke="{ACC}" stroke-width="1.8"/>')
    o.append(f'<text x="270" y="92" font-size="13" text-anchor="middle" fill="{INK}" font-weight="600">Σ  + b</text>')
    o.append(f'<text x="270" y="110" font-size="9.5" text-anchor="middle" fill="{MUTED}">sumă ponderată</text>')
    o.append(f'<line x1="270" y1="22" x2="270" y2="51" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ar)"/>')
    o.append(_lbl(270, 16, "bias b = 0,1", ACC, 11.5, True))
    o.append(f'<line x1="313" y1="95" x2="368" y2="95" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ar)"/>')
    o.append(_lbl(340, 86, "a = 0,7", GREEN, 11.5, True))
    o.append(f'<rect x="370" y="73" width="70" height="44" rx="10" fill="{FILL_O}" stroke="{ACC}" stroke-width="1.6"/>')
    o.append(f'<text x="405" y="93" font-size="13" text-anchor="middle" fill="{INK}" font-weight="600">f( )</text>')
    o.append(f'<text x="405" y="109" font-size="10.5" text-anchor="middle" fill="{MUTED}">activare</text>')
    o.append(f'<line x1="440" y1="95" x2="500" y2="95" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ar)"/>')
    o.append(f'<text x="510" y="99" font-size="14" fill="{INK}" font-weight="600">y</text>')
    o.append(f'<text x="270" y="160" font-size="11" text-anchor="middle" fill="{MUTED}">pasul 1: înmulțești și aduni</text>')
    o.append(f'<text x="405" y="160" font-size="11" text-anchor="middle" fill="{MUTED}">pasul 2: treci prin f</text>')
    o.append("</svg>")
    return "".join(o)

def grafic(f, titlu, ymin, ymax, xmin=-5, xmax=5, W=170, H=120, marcaje=()):
    def X(x): return 12 + (x - xmin) / (xmax - xmin) * (W - 24)
    def Y(y): return H - 18 - (y - ymin) / (ymax - ymin) * (H - 36)
    pts = " ".join(f"{X(xmin + k*(xmax-xmin)/200):.1f},{Y(f(xmin + k*(xmax-xmin)/200)):.1f}" for k in range(201))
    o = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Avenir Next, Helvetica, sans-serif">']
    o.append(f'<line x1="{X(xmin)}" y1="{Y(0)}" x2="{X(xmax)}" y2="{Y(0)}" stroke="{LINE}"/>')
    o.append(f'<line x1="{X(0)}" y1="{Y(ymin)}" x2="{X(0)}" y2="{Y(ymax)}" stroke="{LINE}"/>')
    for yv, t in marcaje:
        o.append(f'<line x1="{X(xmin)}" y1="{Y(yv)}" x2="{X(xmax)}" y2="{Y(yv)}" stroke="{LINE}" stroke-dasharray="3 3"/>')
        o.append(f'<text x="{X(0)-4}" y="{Y(yv)-3}" font-size="9.5" text-anchor="end" fill="{MUTED}">{t}</text>')
    o.append(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="2.2"/>')
    o.append(f'<text x="{W/2}" y="{H-3}" font-size="11" text-anchor="middle" fill="{INK}" font-weight="600">{titlu}</text>')
    o.append("</svg>")
    return "".join(o)

def activari():
    s = lambda x: 1 / (1 + math.exp(-x))
    return ('<div class="grafice">'
            + grafic(s, "sigmoid: între 0 și 1", -0.1, 1.1, marcaje=[(1, "1"), (0.5, "0,5")])
            + grafic(math.tanh, "tanh: între −1 și 1", -1.2, 1.2, marcaje=[(1, "1"), (-1, "−1")])
            + grafic(lambda x: max(0, x), "ReLU = max(0, x)", -0.5, 5)
            + grafic(lambda x: x if x > 0 else 0.1 * x, "Leaky ReLU", -1, 5)
            + "</div>")

def gradient():
    W, H = 380, 190
    def X(w): return 40 + (w + 3) / 6 * (W - 80)
    def Y(e): return H - 25 - e / 9 * (H - 50)
    pts = " ".join(f"{X(-3 + k*0.03):.1f},{Y((-3 + k*0.03)**2):.1f}" for k in range(201))
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" font-family="Avenir Next, Helvetica, sans-serif">', _defs()]
    o.append(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="2.2"/>')
    ws = [2.6, 1.56, 0.94, 0.56, 0.34]
    for a, b in zip(ws, ws[1:]):
        o.append(f'<path d="M{X(a):.1f},{Y(a*a)-6:.1f} Q{(X(a)+X(b))/2:.1f},{min(Y(a*a),Y(b*b))-30:.1f} {X(b):.1f},{Y(b*b)-6:.1f}" fill="none" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#ar)"/>')
    for w in ws:
        o.append(f'<circle cx="{X(w):.1f}" cy="{Y(w*w):.1f}" r="5" fill="{ACC2}"/>')
    o.append(f'<text x="{X(2.6)+8:.1f}" y="{Y(6.76)+4:.1f}" font-size="11" fill="{INK}">start</text>')
    o.append(f'<circle cx="{X(0):.1f}" cy="{Y(0):.1f}" r="4" fill="{GREEN}"/>')
    o.append(f'<text x="{X(0):.1f}" y="{Y(0)+17:.1f}" font-size="11" text-anchor="middle" fill="{GREEN}">minim (cost mic)</text>')
    o.append(f'<text x="14" y="18" font-size="11" fill="{MUTED}">cost E</text>')
    o.append(f'<text x="{W-20}" y="{H-8}" font-size="11" text-anchor="end" fill="{MUTED}">ponderea w</text>')
    o.append("</svg>")
    return "".join(o)

def backprop():
    W, H = 580, 250
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" font-family="Avenir Next, Helvetica, sans-serif">', _defs()]
    nod = {"x": (60, 40, "x"), "y": (60, 140, "y"), "q": (250, 90, "+"), "z": (250, 200, "z"), "f": (440, 145, "×")}
    def L(a, b, fw, bw):
        x1, y1 = nod[a][:2]; x2, y2 = nod[b][:2]
        d = math.hypot(x2-x1, y2-y1); ux, uy = (x2-x1)/d, (y2-y1)/d
        o.append(f'<line x1="{x1+ux*20:.1f}" y1="{y1+uy*20:.1f}" x2="{x2-ux*22:.1f}" y2="{y2-uy*22:.1f}" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ar)"/>')
        mx, my = (x1+x2)/2, (y1+y2)/2
        o.append(_lbl(mx, my - 8, fw, GREEN, 11.5, True))
        o.append(_lbl(mx, my + 14, bw, RED, 11.5, True))
    L("x", "q", "x = −2", "∂f/∂x = −4"); L("y", "q", "y = 5", "∂f/∂y = −4")
    L("q", "f", "q = 3", "∂f/∂q = z = −4"); L("z", "f", "z = −4", "∂f/∂z = q = 3")
    for k, (x, y, t) in nod.items():
        o.append(f'<circle cx="{x}" cy="{y}" r="20" fill="{FILL_H if t in "+×" else "#fff"}" stroke="{ACC}" stroke-width="1.6"/>')
        o.append(f'<text x="{x}" y="{y+5}" font-size="15" text-anchor="middle" fill="{INK}" font-weight="600">{t}</text>')
    o.append(f'<line x1="462" y1="145" x2="505" y2="145" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ar)"/>')
    o.append(f'<text x="512" y="150" font-size="13" fill="{INK}" font-weight="600">f = −12</text>')
    o.append(f'<text x="10" y="243" font-size="10.5" fill="{GREEN}">verde = valorile (calculate de la stânga la dreapta)</text>')
    o.append(f'<text x="300" y="243" font-size="10.5" fill="{RED}">roșu = derivatele (de la dreapta la stânga)</text>')
    o.append("</svg>")
    return "".join(o)

def grila(M, x0, y0, c=26, hl=None, hlcol=ACC2, titlu="", fmt=str):
    o = []
    for i, row in enumerate(M):
        for j, v in enumerate(row):
            fill = "#fbe3c4" if hl and hl[0] <= i < hl[0]+hl[2] and hl[1] <= j < hl[1]+hl[3] else "#fff"
            o.append(f'<rect x="{x0+j*c}" y="{y0+i*c}" width="{c}" height="{c}" fill="{fill}" stroke="{LINE}"/>')
            o.append(f'<text x="{x0+j*c+c/2}" y="{y0+i*c+c/2+4}" font-size="11.5" text-anchor="middle" fill="{INK}">{fmt(v)}</text>')
    if hl:
        o.append(f'<rect x="{x0+hl[1]*c}" y="{y0+hl[0]*c}" width="{hl[3]*c}" height="{hl[2]*c}" fill="none" stroke="{hlcol}" stroke-width="2.4"/>')
    if titlu:
        o.append(f'<text x="{x0+len(M[0])*c/2}" y="{y0-8}" font-size="11.5" text-anchor="middle" fill="{MUTED}">{titlu}</text>')
    return "".join(o)

def conv():
    I = [[1, 2, 0, 1], [0, 1, 3, 1], [2, 1, 0, 0], [1, 0, 1, 2]]; K = [[1, 0, -1]] * 3; C = [[0, 2], [-1, -1]]
    f = lambda v: str(v).replace("-", "−")
    o = ['<svg viewBox="0 0 520 150" width="100%" style="max-width:520px" font-family="Avenir Next, Helvetica, sans-serif">', _defs()]
    o.append(grila(I, 10, 30, hl=(0, 1, 3, 3), titlu="imagine 4×4", fmt=f))
    o.append('<text x="132" y="86" font-size="22" fill="#7a6f64">∗</text>')
    o.append(grila(K, 155, 43, titlu="filtru 3×3", fmt=f))
    o.append('<text x="250" y="86" font-size="20" fill="#7a6f64">=</text>')
    o.append(grila(C, 280, 56, hl=(0, 1, 1, 1), titlu="ieșire 2×2", fmt=f))
    o.append(f'<text x="350" y="62" font-size="11" fill="{INK}">filtrul pus peste chenarul</text>')
    o.append(f'<text x="350" y="77" font-size="11" fill="{INK}">portocaliu dă căsuța marcată:</text>')
    o.append(f'<text x="350" y="96" font-size="11" fill="{GREEN}">(2+1+1)·1 + (0+3+0)·0</text>')
    o.append(f'<text x="350" y="111" font-size="11" fill="{GREEN}">+ (1+1+0)·(−1) = 4 − 2 = 2</text>')
    o.append("</svg>")
    return "".join(o)

def pooling():
    M = [[3, 5, 4, 6], [1, 1, 9, 4], [7, 10, 9, 5], [12, 2, 9, 4]]
    o = ['<svg viewBox="0 0 330 140" width="100%" style="max-width:330px" font-family="Avenir Next, Helvetica, sans-serif">', _defs()]
    o.append(grila(M, 10, 26, hl=(0, 0, 2, 2), titlu="intrare 4×4"))
    o.append(f'<line x1="130" y1="78" x2="185" y2="78" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ar)"/>')
    o.append(f'<text x="157" y="70" font-size="10.5" text-anchor="middle" fill="{MUTED}">max 2×2</text>')
    o.append(grila([[5, 9], [12, 9]], 195, 52, hl=(0, 0, 1, 1), titlu="ieșire 2×2"))
    o.append(f'<text x="262" y="72" font-size="11" fill="{GREEN}">max(3,5,1,1)</text>')
    o.append(f'<text x="262" y="87" font-size="11" fill="{GREEN}">= 5</text>')
    o.append("</svg>")
    return "".join(o)

def matrice_A():
    col = {"w₀": "#f6d9b8", "w₋₁": "#e9c9c0", "w₋₂": "#f1e3a6", "w₁": "#d5e2c4", "w₂": "#d9d1e8"}
    A = [["w₀", "w₋₁", "w₋₂"], ["w₁", "w₀", "w₋₁"], ["w₂", "w₁", "w₀"]]
    c = 44
    mx = 105
    o = ['<svg viewBox="0 0 560 170" width="100%" style="max-width:560px" font-family="Avenir Next, Helvetica, sans-serif">']
    o.append(f'<text x="8" y="92" font-size="16" fill="{INK}">A =</text>')
    for i in range(3):
        for j in range(3):
            t = A[i][j]
            o.append(f'<rect x="{mx+j*c}" y="{20+i*c}" width="{c}" height="{c}" fill="{col[t]}" stroke="#fff" stroke-width="2"/>')
            o.append(f'<text x="{mx+j*c+c/2}" y="{20+i*c+c/2+5}" font-size="14" text-anchor="middle" fill="{INK}">{t}</text>')
        o.append(f'<text x="{mx-6}" y="{20+i*c+c/2+4}" font-size="10" text-anchor="end" fill="{MUTED}">rând {i}</text>')
    for j in range(3):
        o.append(f'<text x="{mx+j*c+c/2}" y="{20+3*c+14}" font-size="10" text-anchor="middle" fill="{MUTED}">col. {j}</text>')
    tx = 255
    rows = [("x₀ = ", ["w₀", "w₋₁", "w₋₂"], "b₀"), ("x₁ = ", ["w₁", "w₀", "w₋₁"], "b₁"), ("x₂ = ", ["w₂", "w₁", "w₀"], "b₂")]
    for i, (lhs, ws, b) in enumerate(rows):
        y = 20 + i * c + c / 2 + 5
        o.append(f'<text x="{tx}" y="{y}" font-size="13.5" fill="{INK}">{lhs}</text>')
        x = tx + 34
        for j, w in enumerate(ws):
            o.append(f'<rect x="{x-2}" y="{y-14}" width="30" height="19" rx="4" fill="{col[w]}"/>')
            o.append(f'<text x="{x+13}" y="{y}" font-size="13.5" text-anchor="middle" fill="{INK}">{w}</text>')
            o.append(f'<text x="{x+30}" y="{y}" font-size="13.5" fill="{INK}">·y{"₀₁₂"[j]} +</text>')
            x += 70
        o.append(f'<text x="{x-4}" y="{y}" font-size="13.5" fill="{INK}">{b}</text>')
    o.append(f'<text x="{tx}" y="165" font-size="11" fill="{MUTED}">aceeași culoare = aceeași pondere (aceeași diagonală)</text>')
    o.append("</svg>")
    return "".join(o)

def overfit():
    W, H = 330, 150
    def X(t): return 30 + t / 50 * (W - 50)
    def Y(e): return H - 25 - e * (H - 45)
    tr = " ".join(f"{X(t):.1f},{Y(0.85*math.exp(-t/12)+0.05):.1f}" for t in range(51))
    va = " ".join(f"{X(t):.1f},{Y(0.85*math.exp(-t/12)+0.1+0.0002*max(0,t-15)**2):.1f}" for t in range(51))
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" font-family="Avenir Next, Helvetica, sans-serif">']
    o.append(f'<polyline points="{tr}" fill="none" stroke="{ACC}" stroke-width="2"/>')
    o.append(f'<polyline points="{va}" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    o.append(f'<line x1="{X(17)}" y1="15" x2="{X(17)}" y2="{H-25}" stroke="{ACC2}" stroke-dasharray="4 3"/>')
    o.append(f'<text x="{X(17)+4}" y="24" font-size="10.5" fill="{ACC2}">oprește aici (early stopping)</text>')
    o.append(f'<text x="{X(50)}" y="{Y(0.05)-6}" font-size="10.5" text-anchor="end" fill="{ACC}">eroare pe antrenare</text>')
    o.append(f'<text x="{X(50)}" y="{Y(0.62)}" font-size="10.5" text-anchor="end" fill="{GREEN}">eroare pe validare</text>')
    o.append(f'<text x="{W/2}" y="{H-6}" font-size="10.5" text-anchor="middle" fill="{MUTED}">epoci (timp de antrenare) →</text>')
    o.append("</svg>")
    return "".join(o)

def pca():
    import random
    random.seed(3)
    W, H = 260, 170
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" font-family="Avenir Next, Helvetica, sans-serif">', _defs()]
    cx, cy, a = 125, 88, math.radians(-28)
    for _ in range(70):
        u, v = random.gauss(0, 42), random.gauss(0, 12)
        o.append(f'<circle cx="{cx + u*math.cos(a) - v*math.sin(a):.1f}" cy="{cy + u*math.sin(a) + v*math.cos(a):.1f}" r="2.6" fill="{ACC2}" opacity="0.75"/>')
    o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+95*math.cos(a):.1f}" y2="{cy+95*math.sin(a):.1f}" stroke="{ACC}" stroke-width="2.4" marker-end="url(#ar)"/>')
    o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx-35*math.sin(a):.1f}" y2="{cy+35*math.cos(a):.1f}" stroke="{GREEN}" stroke-width="2.4" marker-end="url(#ar)"/>')
    o.append(f'<text x="{cx+95*math.cos(a)+4:.1f}" y="{cy+95*math.sin(a)-4:.1f}" font-size="11.5" fill="{ACC}" font-weight="700">u₁</text>')
    o.append(f'<text x="{cx-35*math.sin(a)+6:.1f}" y="{cy+35*math.cos(a)+10:.1f}" font-size="11.5" fill="{GREEN}" font-weight="700">u₂</text>')
    o.append(f'<text x="8" y="164" font-size="10.5" fill="{MUTED}">u₁ = direcția cu varianța cea mai mare</text>')
    o.append("</svg>")
    return "".join(o)

def iou():
    # adevărat R = [0,4]x[0,4], prezis P = [1,5]x[0,4] (unități de grilă), y crește în sus
    u, X0, Y0 = 34, 40, 200
    def X(x): return X0 + x * u
    def Y(y): return Y0 - y * u
    o = ['<svg viewBox="0 0 560 235" width="100%" style="max-width:560px" font-family="Avenir Next, Helvetica, sans-serif">', _defs()]
    for i in range(0, 7):
        o.append(f'<line x1="{X(i)}" y1="{Y(0)}" x2="{X(i)}" y2="{Y(5)}" stroke="#eee3d6" stroke-width="1"/>')
        o.append(f'<text x="{X(i)}" y="{Y(0)+15}" font-size="10" text-anchor="middle" fill="{MUTED}">{i}</text>')
    for j in range(0, 6):
        o.append(f'<line x1="{X(0)}" y1="{Y(j)}" x2="{X(6)}" y2="{Y(j)}" stroke="#eee3d6" stroke-width="1"/>')
        o.append(f'<text x="{X(0)-10}" y="{Y(j)+4}" font-size="10" text-anchor="middle" fill="{MUTED}">{j}</text>')
    o.append(f'<rect x="{X(1)}" y="{Y(4)}" width="{3*u}" height="{4*u}" fill="{FILL_O}" />')
    o.append(f'<rect x="{X(0)}" y="{Y(4)}" width="{4*u}" height="{4*u}" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-dasharray="6 4"/>')
    o.append(f'<rect x="{X(1)}" y="{Y(4)}" width="{4*u}" height="{4*u}" fill="none" stroke="{ACC}" stroke-width="2.4"/>')
    o.append(_lbl(X(2.5), Y(2), "intersecția", ACC, 11.5, True))
    o.append(_lbl(X(2.5), Y(1.45), "3 × 4 = 12", ACC, 11))
    o.append(_lbl(X(0.5), Y(4) - 8, "adevărat R", GREEN, 11, True, bg=False))
    o.append(_lbl(X(4.5), Y(4) - 8, "prezis P", ACC, 11, True, bg=False))
    tx = 300
    rows = [("R: x de la 0 la 4, y de la 0 la 4 → aria 16", GREEN),
            ("P: x de la 1 la 5, y de la 0 la 4 → aria 16", ACC),
            ("intersecția: x de la 1 la 4, y de la 0 la 4", INK),
            ("   → aria 3 · 4 = 12", INK),
            ("reuniunea = 16 + 16 − 12 = 20", INK),
            ("   (intersecția s-ar număra de 2 ori)", MUTED),
            ("IoU = 12 / 20 = 0,6 > 0,5 → corect", GREEN)]
    for k, (t, c) in enumerate(rows):
        o.append(f'<text x="{tx}" y="{48 + k*24}" font-size="11.5" fill="{c}"{" font-weight=\"700\"" if k == 6 else ""}>{t}</text>')
    o.append("</svg>")
    return "".join(o)

def nms():
    o = ['<svg viewBox="0 0 600 200" width="100%" style="max-width:600px" font-family="Avenir Next, Helvetica, sans-serif">', _defs()]
    def scena(ox, cutii, titlu):
        o.append(f'<text x="{ox+125}" y="12" font-size="11.5" text-anchor="middle" fill="{MUTED}" font-weight="700">{titlu}</text>')
        o.append(f'<rect x="{ox}" y="26" width="250" height="165" rx="6" fill="#fffaf3" stroke="{LINE}"/>')
        # două obiecte (pietoni), desenate simplu
        for cx in (ox + 72, ox + 185):
            o.append(f'<circle cx="{cx}" cy="70" r="11" fill="#d9cfc4"/>')
            o.append(f'<rect x="{cx-15}" y="84" width="30" height="62" rx="8" fill="#d9cfc4"/>')
            o.append(f'<rect x="{cx-14}" y="146" width="11" height="32" fill="#d9cfc4"/><rect x="{cx+3}" y="146" width="11" height="32" fill="#d9cfc4"/>')
        for (x, y, w, h, nume, p, col, dash) in cutii:
            o.append(f'<rect x="{ox+x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{col}" stroke-width="2"'
                     f'{" stroke-dasharray=\"5 4\"" if dash else ""}/>')
            ly = {"A": y + h - 6, "B": y - 4, "D": y + h / 2, "C": y + 12, "E": y + h - 6}[nume]
            lx = {"A": ox + x + 26, "B": ox + x + 40, "D": ox + x + 4, "C": ox + x + 22, "E": ox + x + 40}[nume]
            o.append(_lbl(lx, ly, f"{nume} {p}", col, 10.5, True))
    toate = [(40, 48, 64, 136, "A", "0,95", ACC, False), (46, 40, 68, 140, "B", "0,91", MUTED, True),
             (30, 58, 72, 124, "D", "0,75", MUTED, True), (152, 50, 66, 134, "C", "0,81", ACC2, False),
             (165, 66, 70, 118, "E", "0,62", RED, True)]
    scena(10, toate, "înainte: 5 dreptunghiuri pentru 2 obiecte")
    o.append(f'<line x1="268" y1="108" x2="328" y2="108" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ar)"/>')
    o.append(f'<text x="298" y="100" font-size="10.5" text-anchor="middle" fill="{MUTED}">NMS</text>')
    scena(340, [toate[0], toate[3]], "după: câte unul pe obiect")
    o.append("</svg>")
    return "".join(o)
