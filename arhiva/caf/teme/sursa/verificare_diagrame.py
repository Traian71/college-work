"""Verificare Tema 2 si Tema 3 (CAF): formula R_SIST vs enumerare exhaustiva 2^n stari pe graful
transcris din desen; verificarea legaturilor si taieturilor minimale (Tema 3b).
Rulare: python3 verificare_diagrame.py   (compileaza enumerare.c intr-un director temporar)"""
import os, random, subprocess, tempfile, itertools

AICI = os.path.dirname(os.path.abspath(__file__))

# ---------- grafurile transcrise (element: nod1, nod2) ----------
# Tema 2: IN -[A|B|C|D|E]- a ; a -F-G- b ; a -[(H-I)|(J-K)]- c2 -L- b ;
#         a -[M|(N-O)]- d2 -[P|R]- b ; b -[S|(T-V)|U]- OUT
T2 = {
    'A': ('IN', 'a'), 'B': ('IN', 'a'), 'C': ('IN', 'a'), 'D': ('IN', 'a'), 'E': ('IN', 'a'),
    'F': ('a', 'fg'), 'G': ('fg', 'b'),
    'H': ('a', 'hi'), 'I': ('hi', 'c2'), 'J': ('a', 'jk'), 'K': ('jk', 'c2'), 'L': ('c2', 'b'),
    'M': ('a', 'd2'), 'N': ('a', 'no'), 'O': ('no', 'd2'), 'P': ('d2', 'b'), 'R': ('d2', 'b'),
    'S': ('b', 'OUT'), 'T': ('b', 'tv'), 'V': ('tv', 'OUT'), 'U': ('b', 'OUT'),
}
# Tema 3: IN -A- n1 ; n1 -[(B-C)|D]- n2 ; n1 -E-F- n3 ; n2 -G-H- n3 (punte) ;
#         n2 -[(I-J)|(K-L)]- n4 ; n3 -[M|(N-O)]- n5 ; n4 -P- n5 (punte) ;
#         n4 -[Q|R]- n6 ; n5 -S-T- n6 ; n6 -[(U-V)|W|X|(Y-Z)]- OUT
T3 = {
    'A': ('IN', 'n1'), 'B': ('n1', 'bc'), 'C': ('bc', 'n2'), 'D': ('n1', 'n2'),
    'E': ('n1', 'ef'), 'F': ('ef', 'n3'), 'G': ('n2', 'gh'), 'H': ('gh', 'n3'),
    'I': ('n2', 'ij'), 'J': ('ij', 'n4'), 'K': ('n2', 'kl'), 'L': ('kl', 'n4'),
    'M': ('n3', 'n5'), 'N': ('n3', 'no'), 'O': ('no', 'n5'), 'P': ('n4', 'n5'),
    'Q': ('n4', 'n6'), 'R': ('n4', 'n6'), 'S': ('n5', 'st'), 'T': ('st', 'n6'),
    'U': ('n6', 'uv'), 'V': ('uv', 'OUT'), 'W': ('n6', 'OUT'), 'X': ('n6', 'OUT'),
    'Y': ('n6', 'yz'), 'Z': ('yz', 'OUT'),
}

par = lambda *r: 1 - __import__('math').prod(1 - x for x in r)   # paralel


def formula_T2(R):
    R1 = par(R['A'], R['B'], R['C'], R['D'], R['E'])
    Rhijk = R['H'] * R['I'] + R['J'] * R['K'] - R['H'] * R['I'] * R['J'] * R['K']
    Ra = Rhijk * R['L']
    Rmno = R['M'] + R['N'] * R['O'] - R['M'] * R['N'] * R['O']
    Rpr = R['P'] + R['R'] - R['P'] * R['R']
    Rb = Rmno * Rpr
    R2 = 1 - (1 - R['F'] * R['G']) * (1 - Ra) * (1 - Rb)
    R3 = 1 - (1 - R['S']) * (1 - R['T'] * R['V']) * (1 - R['U'])
    return R1 * R2 * R3


def formula_T3(R):
    R1 = R['B'] * R['C'] + R['D'] - R['B'] * R['C'] * R['D']
    R2 = R['E'] * R['F']
    R3 = R['G'] * R['H']
    R4 = R['I'] * R['J'] + R['K'] * R['L'] - R['I'] * R['J'] * R['K'] * R['L']
    R5 = R['M'] + R['N'] * R['O'] - R['M'] * R['N'] * R['O']
    R6 = R['P']
    R7 = R['Q'] + R['R'] - R['Q'] * R['R']
    R8 = R['S'] * R['T']
    R9 = 1 - (1 - R['U'] * R['V']) * (1 - R['W']) * (1 - R['X']) * (1 - R['Y'] * R['Z'])
    R12 = R1 + R2 - R1 * R2
    # P bun: n4 = n5 ; Bayes pe GH
    PS_P = (R3 * R12 * (R4 + R5 - R4 * R5) + (1 - R3) * (R1 * R4 + R2 * R5 - R1 * R2 * R4 * R5)) \
        * (R7 + R8 - R7 * R8)
    # P defect: ramurile 4-7 si 5-8 ; Bayes pe GH
    PS_nP = R3 * R12 * (R4 * R7 + R5 * R8 - R4 * R5 * R7 * R8) \
        + (1 - R3) * (R1 * R4 * R7 + R2 * R5 * R8 - R1 * R2 * R4 * R5 * R7 * R8)
    Rned = R6 * PS_P + (1 - R6) * PS_nP
    return R['A'] * Rned * R9


def conectat(G, bune):
    """Exista drum IN -> OUT folosind doar elementele din 'bune'? (graf neorientat)"""
    viz, stiva = {'IN'}, ['IN']
    while stiva:
        x = stiva.pop()
        for e in bune:
            a, b = G[e]
            for p, q in ((a, b), (b, a)):
                if p == x and q not in viz:
                    viz.add(q); stiva.append(q)
    return 'OUT' in viz


def enumerare(exe, G, R):
    noduri = sorted({n for e in G.values() for n in e})
    idx = {n: i for i, n in enumerate(noduri)}
    s = "%d %d %d %d\n" % (len(noduri), len(G), idx['IN'], idx['OUT'])
    s += "".join("%d %d %.17g\n" % (idx[G[e][0]], idx[G[e][1]], R[e]) for e in G)
    return float(subprocess.run([exe], input=s, capture_output=True, text=True, check=True).stdout)


def main():
    tmp = tempfile.mkdtemp()
    exe = os.path.join(tmp, 'enumerare')
    subprocess.run(['cc', '-O2', '-o', exe, os.path.join(AICI, 'enumerare.c')], check=True)
    random.seed(441)
    for nume, G, form in (('Tema 2', T2, formula_T2), ('Tema 3', T3, formula_T3)):
        print('==', nume, '-', len(G), 'elemente,', 2 ** len(G), 'stari')
        for k in range(4):
            R = {e: (random.uniform(0.05, 0.99) if k < 3 else 0.9) for e in G}
            f, b = form(R), enumerare(exe, G, R)
            print('  set %d: formula %.12f  enumerare %.12f  dif %.1e' % (k + 1, f, b, abs(f - b)))
            assert abs(f - b) < 1e-9

    # ---------- Tema 3b: legaturi si taieturi minimale ----------
    E = list(T3)
    legaturi = ['ABCIJQUV', 'ADKLRW', 'AEFMSTX', 'AEFNOSTYZ', 'ABCGHMSTW', 'AEFHGIJQX',
                'ADIJPSTW', 'AEFMPQUV']
    taieturi = ['A', 'BDE', 'IKMN', 'QRS', 'UWXY', 'EGIK', 'BDGMN', 'IKPS']
    print('== Tema 3b')
    for L in legaturi:
        ok = conectat(T3, set(L)) and all(not conectat(T3, set(L) - {x}) for x in L)
        print('  legatura %-10s minimala: %s' % (L, ok)); assert ok
    for T in taieturi:
        rest = set(E) - set(T)
        ok = (not conectat(T3, rest)) and all(conectat(T3, rest | {x}) for x in T)
        print('  taietura %-10s minimala: %s' % (T, ok)); assert ok
    assert len(set(legaturi)) == 8 and len(set(taieturi)) == 8

    # numarul total de legaturi minimale (drumuri simple IN-OUT) - doar informativ
    def drumuri(x, viz, ales):
        if x == 'OUT':
            yield frozenset(ales); return
        for e in E:
            a, b = T3[e]
            for p, q in ((a, b), (b, a)):
                if p == x and q not in viz:
                    yield from drumuri(q, viz | {q}, ales + [e])
    toate = set(drumuri('IN', {'IN'}, []))
    print('  total legaturi minimale in graf:', len(toate))
    print('OK - toate verificarile au trecut')


if __name__ == '__main__':
    main()
