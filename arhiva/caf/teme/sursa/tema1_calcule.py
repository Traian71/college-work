# CAF Tema 1, problema 2: estimarea neparametrica (formulele din curs 3 / lab 2)
n = 100
t = [100, 200, 300, 400, 500, 600]
r = [2, 5, 9, 11, 13, 20]
rc = dict(zip(t, r)); rc[0] = 0

R = lambda x: (n - rc[x]) / n          # R^(t) = (n - r)/n
F = lambda x: rc[x] / n                # F^(t) = r/n
nt = lambda x: n - rc[x]               # n(t)

print("R^(200) =", R(200))
print("R^(800): test oprit la 600 h, nu se poate estima; R^(600) =", R(600))
print("F^(400) =", F(400))
dr = rc[300] - rc[200]
print("f^(200,300) = %d/(%d*100) = %.3e 1/h" % (dr, n, dr / (n * 100)))
dr = rc[400] - rc[300]
print("z^(300,400) = %d/(%d*100) = %.4e 1/h" % (dr, nt(300), dr / (nt(300) * 100)))
print("   verificare f/R: %.4e" % ((dr / (n * 100)) / R(300)))

# media: doar pentru cele r = 20 CI defectate, cu mijlocul intervalului (ca in lab 2)
prev, s_mij, s_cap = 0, 0, 0
for ti in t:
    d = rc[ti] - rc[ti - 100]
    s_mij += d * (ti - 50)
    s_cap += d * ti
print("m^ (mijloace) = %d/%d = %.1f h" % (s_mij, rc[600], s_mij / rc[600]))
print("   (cu capetele intervalelor ar fi %d/%d = %.1f h)" % (s_cap, rc[600], s_cap / rc[600]))
print("   limita inferioara pt tot lotul (cele 80 >= 600 h): (%d + 80*600)/100 = %.1f h"
      % (s_mij, (s_mij + 80 * 600) / 100))
print("   TTT/r (lege exponentiala, NU neparametric): %.1f h" % ((s_mij + 80 * 600) / 20))
# cuantila t0,2: momentul in care r = n*alfa = 20
print("t^0,2: n*alfa =", n * 0.2, "-> r = 20 la t =", [ti for ti in t if rc[ti] >= 20][0], "h")

# problema 1: verificare numerica R, F, z, m pentru a1 + a2 = 1
import math
a1, l1, l2 = 0.3, 2e-3, 5e-4; a2 = 1 - a1
f = lambda x: a1*l1*math.exp(-l1*x) + a2*l2*math.exp(-l2*x)
Rf = lambda x: a1*math.exp(-l1*x) + a2*math.exp(-l2*x)
h = 1.0
F300 = sum(f(i*h + h/2) for i in range(300)) * h          # integrala 0..300 din f
m_num = sum(Rf(i*h + h/2) for i in range(60000)) * h       # integrala 0..inf din R
print("pb1: F(300) numeric %.6f vs 1-R(300) %.6f" % (F300, 1 - Rf(300)))
print("pb1: m numeric %.2f vs a1/l1 + a2/l2 = %.2f" % (m_num, a1/l1 + a2/l2))
