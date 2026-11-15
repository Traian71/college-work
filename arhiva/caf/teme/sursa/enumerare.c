/* Enumerare exhaustiva a celor 2^E stari (bun/defect) ale elementelor unui graf de fiabilitate.
 * Intrare (stdin): N E src dst, apoi E linii "u v p" (muchie neorientata u-v, fiabilitate p).
 * Iesire: P(exista drum src -> dst prin elemente bune) = R_SIST exact.
 * Compilare: cc -O2 -o enumerare enumerare.c */
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int N, E, src, dst;
    if (scanf("%d %d %d %d", &N, &E, &src, &dst) != 4 || E > 30 || N > 32) return 1;
    int u[32], v[32]; double p[32];
    for (int i = 0; i < E; i++) scanf("%d %d %lf", &u[i], &v[i], &p[i]);
    int lo = E / 2, hi = E - lo;
    double *WL = malloc(sizeof(double) << lo), *WH = malloc(sizeof(double) << hi);
    for (long s = 0; s < (1L << lo); s++) {
        double w = 1; for (int i = 0; i < lo; i++) w *= (s >> i & 1) ? p[i] : 1 - p[i]; WL[s] = w;
    }
    for (long s = 0; s < (1L << hi); s++) {
        double w = 1; for (int i = 0; i < hi; i++) w *= (s >> i & 1) ? p[lo + i] : 1 - p[lo + i]; WH[s] = w;
    }
    double R = 0;
    unsigned long total = 1UL << E;
    for (unsigned long s = 0; s < total; s++) {
        unsigned reach = 1u << src; int ch = 1;
        while (ch) {
            ch = 0;
            for (int i = 0; i < E; i++) if (s >> i & 1) {
                unsigned a = 1u << u[i], b = 1u << v[i];
                if ((reach & a) && !(reach & b)) { reach |= b; ch = 1; }
                else if ((reach & b) && !(reach & a)) { reach |= a; ch = 1; }
            }
        }
        if (reach >> dst & 1) R += WL[s & ((1UL << lo) - 1)] * WH[s >> lo];
    }
    printf("%.15f\n", R);
    return 0;
}
