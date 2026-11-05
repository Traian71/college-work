# Genereaza "CAF L3 rezolvare.xlsx" (ruleaza din radacina repo-ului).
# Valorile sunt cele din aplicatia de laborator (EMI.EXE): estimatori de max. verosimilitate, test Kolmogorov-Smirnov.
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

IESIRE = 'caf/Lucrarea 3/CAF L3 rezolvare.xlsx'

t = [115, 232, 328, 368, 393, 404, 421, 457, 483, 511, 527, 540, 560, 572, 598, 605, 619, 633, 660, 681,
     736, 791, 942, 1000]

gri = PatternFill('solid', fgColor='D9D9D9')
sub = Side(style='thin')
chenar = Border(left=sub, right=sub, top=sub, bottom=sub)
bold = Font(bold=True)
centru = Alignment(horizontal='center', vertical='center', wrap_text=True)


def antet(ws, rand, col, texte):
    for k, txt in enumerate(texte):
        c = ws.cell(rand, col + k, txt)
        c.font = bold
        c.fill = gri
        c.border = chenar
        c.alignment = centru


def celula(ws, rand, col, val, fmt=None):
    c = ws.cell(rand, col, val)
    c.border = chenar
    c.alignment = centru
    if fmt:
        c.number_format = fmt


wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Aplicatie'

ws['A1'] = 'Lucrarea 3 – Calculul indicatorilor de fiabilitate prin metode parametrice'
ws['A1'].font = Font(bold=True, size=12)

# datele
antet(ws, 3, 1, ['Momentul (ore)'])
for k, ti in enumerate(t):
    celula(ws, 4 + k, 1, ti)

# I. tabelul
ws['C3'] = 'I. Identificarea legii (test Kolmogorov-Smirnov)'
ws['C3'].font = bold
antet(ws, 4, 3, ['Risc', 'Lege exponențială', 'Lege Weibull', 'Lege normală'])
rezultate = [
    (0.01, 'respinsă', 'acceptată', 'acceptată'),
    (0.2, 'respinsă', 'acceptată', 'acceptată'),
    (0.5, 'respinsă', 'acceptată', 'acceptată'),
    (0.995, 'acceptată', 'acceptată', 'acceptată'),
]
for k, rand in enumerate(rezultate):
    for j, val in enumerate(rand):
        celula(ws, 5 + k, 3 + j, val)

# II. parametrii
ws['C11'] = 'II. Parametrii legilor'
ws['C11'].font = bold
antet(ws, 12, 3, ['Lege', 'Parametru', 'Valoare'])
parametri = [
    ('exponențială', 'λ (1/h)', 0.001821, '0.000000'),
    ('Weibull', 'α', 1.953e8, '0.000E+00'),
    ('Weibull', 'β', 2.974, '0.000'),
    ('normală', 'μ (ore)', 549.0, '0.0'),
    ('normală', 'σ (ore)', 198.6, '0.0'),
]
for k, (lege, par, val, fmt) in enumerate(parametri):
    celula(ws, 13 + k, 3, lege)
    celula(ws, 13 + k, 4, par)
    celula(ws, 13 + k, 5, val, fmt)

ws['C19'] = 'Weibull: F(t) = 1 − exp(−t^β / α)'

ws['C21'] = 'Concluzie:'
ws['C21'].font = bold
ws['C22'] = 'Legea exponențială este respinsă (se încadrează doar la riscul 0,995).'
ws['C23'] = 'Legile Weibull și normală sunt acceptate pentru toate riscurile.'
ws['C24'] = 'Se adoptă legea normală cu μ = 549 ore și σ ≈ 198,6 ore.'

ws.column_dimensions['A'].width = 15
ws.column_dimensions['B'].width = 3
for col in 'CDEF':
    ws.column_dimensions[col].width = 18
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
     'maxim dintre ele și se compară cu valoarea critică, care depinde de numărul de defectări și de riscul ales. '
     'Dacă ecartul nu depășește valoarea critică ipoteza se acceptă, altfel se respinge.'),
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
