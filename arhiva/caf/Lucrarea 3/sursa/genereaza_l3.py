# Genereaza "CAF L3 rezolvare.xlsx" (ruleaza din radacina repo-ului).
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.chart.shapes import GraphicalProperties

IESIRE = 'caf/Lucrarea 3/CAF L3 rezolvare.xlsx'

t = [115, 232, 328, 368, 393, 404, 421, 457, 483, 511, 527, 540, 560, 572, 598, 605, 619, 633, 660, 681,
     736, 791, 942, 1000]
# beta Weibull: solutia ecuatiei de verosimilitate (Goal Seek pe celula C38 = 0)
BETA = 2.97377358794178
# cuantilele x(p) din tabelul aplicatiei (risc.dta, coloana pentru esantion complet)
RISCURI = [(0.01, 0.4410), (0.2, 0.6448), (0.5, 0.8276), (0.995, 1.7308)]

gri = PatternFill('solid', fgColor='D9D9D9')
sub = Side(style='thin')
chenar = Border(left=sub, right=sub, top=sub, bottom=sub)
bold = Font(bold=True)


def antet(ws, rand, col, texte):
    for k, txt in enumerate(texte):
        c = ws.cell(rand, col + k, txt)
        c.font = bold
        c.fill = gri
        c.border = chenar
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)


def celula(ws, ref, val, fmt=None):
    c = ws[ref]
    c.value = val
    c.border = chenar
    if fmt:
        c.number_format = fmt
    return c


wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Aplicatie'

ws['A1'] = 'Lucrarea 3 – Calculul indicatorilor de fiabilitate prin metode parametrice'
ws['A1'].font = Font(bold=True, size=12)
ws['A3'] = 'n ='
ws['B3'] = 24
ws['C3'] = 'fotodiode'
ws['A4'] = 'r ='
ws['B4'] = 24
ws['C4'] = 'defectări (încercare exhaustivă)'

antet(ws, 6, 1, ['i', 'ti (ore)', 'ln ti', '^F(ti) = i/(n+1)', 'i/n', '(i−1)/n',
                 'F exp.', 'F Weibull', 'F normală', 'D exp.', 'D Weibull', 'D normală'])
antet(ws, 6, 14, ['ln(1/(1−^F))', 'λ·t', 'ln ln(1/(1−^F))', 'β·ln t − ln α', 'Φ⁻¹(^F)', '(t−μ)/σ'])
ws.row_dimensions[6].height = 30

for k, ti in enumerate(t):
    r = 7 + k
    celula(ws, f'A{r}', k + 1)
    celula(ws, f'B{r}', ti)
    celula(ws, f'C{r}', f'=LN(B{r})', '0.000')
    celula(ws, f'D{r}', f'=A{r}/($B$3+1)', '0.000')
    celula(ws, f'E{r}', f'=A{r}/$B$3', '0.000')
    celula(ws, f'F{r}', f'=(A{r}-1)/$B$3', '0.000')
    celula(ws, f'G{r}', f'=1-EXP(-$C$35*B{r})', '0.000')
    celula(ws, f'H{r}', f'=1-EXP(-(B{r}^$C$36)/$C$37)', '0.000')
    celula(ws, f'I{r}', f'=NORMDIST(B{r},$C$40,$C$41,TRUE)', '0.000')
    celula(ws, f'J{r}', f'=MAX(E{r}-G{r},G{r}-F{r})', '0.000')
    celula(ws, f'K{r}', f'=MAX(E{r}-H{r},H{r}-F{r})', '0.000')
    celula(ws, f'L{r}', f'=MAX(E{r}-I{r},I{r}-F{r})', '0.000')
    celula(ws, f'N{r}', f'=LN(1/(1-D{r}))', '0.000')
    celula(ws, f'O{r}', f'=$C$35*B{r}', '0.000')
    celula(ws, f'P{r}', f'=LN(LN(1/(1-D{r})))', '0.000')
    celula(ws, f'Q{r}', f'=$C$36*C{r}-LN($C$37)', '0.000')
    celula(ws, f'R{r}', f'=NORMSINV(D{r})', '0.000')
    celula(ws, f'S{r}', f'=(B{r}-$C$40)/$C$41', '0.000')

ws['I31'] = 'Dmax ='
ws['I31'].font = bold
celula(ws, 'J31', '=MAX(J7:J30)', '0.0000')
celula(ws, 'K31', '=MAX(K7:K30)', '0.0000')
celula(ws, 'L31', '=MAX(L7:L30)', '0.0000')
ws['I32'] = '√n·Dmax ='
ws['I32'].font = bold
celula(ws, 'J32', '=SQRT($B$3)*J31', '0.0000')
celula(ws, 'K32', '=SQRT($B$3)*K31', '0.0000')
celula(ws, 'L32', '=SQRT($B$3)*L31', '0.0000')

# II. parametrii
ws['A34'] = 'II. Parametrii legilor (estimatori de maximă verosimilitate, ca în aplicație)'
ws['A34'].font = bold
rows = [
    (35, 'Exponențială', 'λ (1/h)', '=$B$3/SUM(B7:B30)', '0.000000', 'λ = r / Σti;  m = 1/λ'),
    (36, 'Weibull', 'β', BETA, '0.0000', 'soluția ecuației de verosimilitate (C38 = 0, Goal Seek)'),
    (37, 'Weibull', 'α', '=SUMPRODUCT(B7:B30^C36)/$B$3', '0.000E+00', 'α = Σti^β / r;  F(t) = 1 − exp(−t^β / α)'),
    (38, 'Weibull', 'ec. verosimilitate', '=SUMPRODUCT(B7:B30^C36,C7:C30)/SUMPRODUCT(B7:B30^C36)-1/C36-AVERAGE(C7:C30)',
     '0.0E+00', 'Σti^β·ln ti / Σti^β − 1/β − (1/r)·Σln ti = 0'),
    (39, 'Weibull', 'η (ore)', '=C37^(1/C36)', '0.0', 'η = α^(1/β)'),
    (40, 'Normală', 'μ (ore)', '=AVERAGE(B7:B30)', '0.0', 'media timpilor de defectare'),
    (41, 'Normală', 'σ (ore)', '=SQRT(SUMPRODUCT((B7:B30-C40)^2)/$B$3)', '0.0', 'împărțit la n (max. verosimilitate)'),
]
for r, lege, par, val, fmt, obs in rows:
    celula(ws, f'A{r}', lege)
    celula(ws, f'B{r}', par)
    celula(ws, f'C{r}', val, fmt)
    ws[f'D{r}'] = obs
ws['A42'] = 'm exp. ='
ws['B42'] = '=1/C35'
ws['B42'].number_format = '0.0'
ws['C42'] = 'm Weibull = η·Γ(1+1/β) ='
ws['F42'] = '=C39*EXP(GAMMALN(1+1/C36))'
ws['F42'].number_format = '0.0'
ws['G42'] = 'ore'

# I. testul K-S
ws['A44'] = 'I. Testul Kolmogorov-Smirnov: ipoteza se acceptă dacă √n·Dmax ≤ x (e0 = x/√n)'
ws['A44'].font = bold
antet(ws, 45, 1, ['Risc', 'x (tabel aplicație)', 'e0 = x/√n', 'Lege exponențială', 'Lege Weibull', 'Lege normală'])
ws.row_dimensions[45].height = 30
for k, (p, x) in enumerate(RISCURI):
    r = 46 + k
    celula(ws, f'A{r}', p)
    celula(ws, f'B{r}', x, '0.0000')
    celula(ws, f'C{r}', f'=B{r}/SQRT($B$3)', '0.0000')
    celula(ws, f'D{r}', f'=IF($J$31<=$C{r},"acceptată","respinsă")')
    celula(ws, f'E{r}', f'=IF($K$31<=$C{r},"acceptată","respinsă")')
    celula(ws, f'F{r}', f'=IF($L$31<=$C{r},"acceptată","respinsă")')
    for col in 'DEF':
        ws[f'{col}{r}'].alignment = Alignment(horizontal='center')

ws['A51'] = 'Concluzie:'
ws['A51'].font = bold
ws['A52'] = ('Legea exponențială este respinsă pentru toate riscurile, iar legile Weibull și normală sunt acceptate '
             'pentru toate riscurile.')
ws['A53'] = ('Legea normală are ecartul maxim cel mai mic, iar la Weibull β ≈ 3 dă tot o formă apropiată de normală '
             '(rată de defectare crescătoare, defectări prin uzură).')
ws['A54'] = 'Se adoptă legea normală cu μ = 549 ore și σ ≈ 198,6 ore (Weibull: β ≈ 2,97, η ≈ 613,7 ore).'

for col, w in {'A': 13, 'B': 11, 'C': 11, 'D': 11, 'E': 11, 'F': 11, 'G': 10, 'H': 10, 'I': 10, 'J': 10,
               'K': 10, 'L': 10, 'M': 3, 'N': 12, 'O': 10, 'P': 13, 'Q': 13, 'R': 10, 'S': 10}.items():
    ws.column_dimensions[col].width = w


def hartie(titlu, x_col, y_col, y_teor_col, x_titlu, y_titlu, ancora, xlim, ylim):
    ch = ScatterChart()
    ch.title = titlu
    ch.scatterStyle = 'lineMarker'
    ch.x_axis.scaling.min, ch.x_axis.scaling.max = xlim
    ch.y_axis.scaling.min, ch.y_axis.scaling.max = ylim
    ch.x_axis.crosses = 'min'
    ch.y_axis.crosses = 'min'
    ch.x_axis.number_format = '0.0' if xlim[1] < 100 else '0'
    ch.y_axis.number_format = '0.0'
    ch.x_axis.title = x_titlu
    ch.y_axis.title = y_titlu
    ch.legend.position = 'b'
    ch.legend.overlay = False
    ch.title.overlay = False
    ch.x_axis.title.overlay = False
    ch.y_axis.title.overlay = False
    xs = Reference(ws, min_col=x_col, min_row=7, max_row=30)
    puncte = Series(Reference(ws, min_col=y_col, min_row=7, max_row=30), xs, title='date experimentale')
    puncte.marker.symbol = 'circle'
    puncte.marker.size = 6
    puncte.marker.graphicalProperties = GraphicalProperties(solidFill='1F4E79')
    puncte.marker.graphicalProperties.line.solidFill = '1F4E79'
    puncte.graphicalProperties.line.noFill = True
    dreapta = Series(Reference(ws, min_col=y_teor_col, min_row=7, max_row=30), xs, title='dreapta legii')
    dreapta.marker.symbol = 'none'
    dreapta.graphicalProperties.line.solidFill = 'C00000'
    dreapta.graphicalProperties.line.width = 19050
    ch.series.append(puncte)
    ch.series.append(dreapta)
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.width = 15
    ch.height = 7.5
    ws.add_chart(ch, ancora)


hartie('Hârtie probabilistică exponențială', 2, 14, 15, 't (ore)', 'ln(1/(1−F))', 'U2', (0, 1100), (0, 3.5))
hartie('Hârtie probabilistică Weibull', 3, 16, 17, 'ln t', 'ln ln(1/(1−F))', 'U18', (4.5, 7), (-5, 1.5))
hartie('Hârtie probabilistică normală', 2, 18, 19, 't (ore)', 'Φ⁻¹(F)', 'U34', (0, 1100), (-3, 3))

ws.page_setup.orientation = 'landscape'
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True

# intrebari
wq = wb.create_sheet('Intrebari')
wq['A1'] = 'Răspunsuri la întrebări'
wq['A1'].font = Font(bold=True, size=12)
qa = [
    ('1. Care sunt metodele de evaluare a indicatorilor de fiabilitate pe baza datelor experimentale?',
     'Metoda neparametrică: indicatorii (F, R, f, z) se estimează direct din numărul de defectări, fără să presupunem '
     'o lege de distribuție. Metoda parametrică: se identifică legea de distribuție a timpului de funcționare, se '
     'estimează parametrii ei și apoi indicatorii se calculează din expresiile legii.'),
    ('2. Indicați avantajele și dezavantajele acestor metode.',
     'Neparametrică: avantaje – simplă, nu cere nicio ipoteză despre lege; dezavantaje – valorile se obțin doar în '
     'momentele de măsură și doar pe durata încercării (nu se poate extrapola), iar precizia depinde mult de volumul '
     'eșantionului. Parametrică: avantaje – indicatorii se pot calcula la orice moment, inclusiv după încheierea '
     'încercării, și au expresii analitice; dezavantaje – calcule mai complicate, trebuie identificată corect legea '
     '(test de concordanță), iar dacă legea aleasă e greșită și rezultatele sunt greșite.'),
    ('3. Pentru un set de valori pe intervale de lungime Δt (număr de defecte în interval), ce metodă permite calculul '
     'indicatorilor și câți indicatori se pot obține?',
     'Metoda neparametrică (ca în lucrarea 2), pentru că nu se cunosc momentele exacte de defectare, de care are '
     'nevoie testul Kolmogorov-Smirnov. Se pot obține 4 indicatori: funcția de repartiție F(t), funcția de fiabilitate '
     'R(t), densitatea de probabilitate f(t) și rata defectărilor z(t).'),
    ('4. De ce este necesar un test statistic de concordanță? În ce constă un astfel de test?',
     'Testul verifică dacă legea presupusă (ipoteza H0) se potrivește cu datele experimentale; fără el, parametrii și '
     'extrapolările ar putea fi calculate pe o lege greșită. Testul Kolmogorov-Smirnov: se estimează funcția de '
     'repartiție din date, se calculează funcția de repartiție a legii presupuse cu parametrii estimați, se ia ecartul '
     'maxim dintre ele (Dmax) și se compară cu valoarea critică e0, care depinde de numărul de defectări și de riscul '
     'ales. Dacă Dmax ≤ e0 ipoteza se acceptă, altfel se respinge.'),
]
r = 3
for q, a in qa:
    wq[f'A{r}'] = q
    wq[f'A{r}'].font = bold
    wq[f'A{r}'].alignment = Alignment(wrap_text=True, vertical='top')
    wq[f'A{r + 1}'] = a
    wq[f'A{r + 1}'].alignment = Alignment(wrap_text=True, vertical='top')
    r += 3
wq.column_dimensions['A'].width = 110

wb.save(IESIRE)
print('ok')
