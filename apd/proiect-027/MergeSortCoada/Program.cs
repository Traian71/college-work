using System;
using System.Collections.Concurrent;
using System.Diagnostics;
using System.Threading;

namespace ConsoleApplication1
{
    // descrierea unei perechi de interclasat: [st, mij) si [mij, dr)
    struct Pereche
    {
        public int st, mij, dr;
        public Pereche(int st, int mij, int dr) { this.st = st; this.mij = mij; this.dr = dr; }
    }

    class Program
    {
        static int B = 512;           // dimensiunea unui bloc initial (constanta)
        static int K = 4;             // numarul de threaduri consumatoare (constant)
        static int P = K + 1;         // p = 1 producator + K consumatori

        static int[] sursa, dest;     // vectorii de pe nivelul curent
        static BlockingCollection<Pereche> coada;

        // ---------- Merge Sort secvential pe un interval [st, dr) ----------
        static void MergeSort(int[] a, int[] aux, int st, int dr)
        {
            if (dr - st < 2) return;
            int mij = (st + dr) / 2;
            MergeSort(a, aux, st, mij);
            MergeSort(a, aux, mij, dr);
            Interclaseaza(a, aux, st, mij, dr);
            Array.Copy(aux, st, a, st, dr - st);
        }

        // interclaseaza a[st..mij) cu a[mij..dr) in d[st..dr)
        static void Interclaseaza(int[] a, int[] d, int st, int mij, int dr)
        {
            int i = st, j = mij, k = st;
            while (i < mij && j < dr)
            {
                if (a[i] <= a[j]) d[k++] = a[i++];
                else d[k++] = a[j++];
            }
            while (i < mij) d[k++] = a[i++];
            while (j < dr) d[k++] = a[j++];
        }

        // sorteaza fiecare bloc de B elemente cu Merge Sort secvential
        static void SorteazaBlocuri(int[] a, int[] aux)
        {
            for (int st = 0; st < a.Length; st += B)
                MergeSort(a, aux, st, Math.Min(st + B, a.Length));
        }

        // ---------- Referinta: Merge Sort secvential cu interclasare pe perechi ----------
        static int[] SortareSecventiala(int[] v)
        {
            int n = v.Length;
            int[] a = v, d = new int[n];
            SorteazaBlocuri(a, d);
            for (int w = B; w < n; w *= 2)
            {
                int st = 0;
                for (; st + w < n; st += 2 * w)
                    Interclaseaza(a, d, st, st + w, Math.Min(st + 2 * w, n));
                if (st < n) Array.Copy(a, st, d, st, n - st);   // intervalul fara pereche
                int[] t = a; a = d; d = t;                        // schimbam rolurile
            }
            return a;
        }

        // ---------- Varianta paralela: producator + K consumatori pe fiecare nivel ----------
        static int nCurent, wCurent;

        static void Producator()
        {
            for (int st = 0; st + wCurent < nCurent; st += 2 * wCurent)
                coada.Add(new Pereche(st, st + wCurent, Math.Min(st + 2 * wCurent, nCurent)));
            coada.CompleteAdding();       // semnalam finalul listei
        }

        static void Consumator()
        {
            // se blocheaza cand coada e goala si se termina cand coada e inchisa si golita
            foreach (Pereche p in coada.GetConsumingEnumerable())
                Interclaseaza(sursa, dest, p.st, p.mij, p.dr);
        }

        static int[] SortareParalela(int[] v, int capacitate)
        {
            int n = v.Length;
            sursa = v;
            dest = new int[n];
            SorteazaBlocuri(sursa, dest);
            nCurent = n;

            for (int w = B; w < n; w *= 2)
            {
                wCurent = w;
                coada = new BlockingCollection<Pereche>(capacitate);

                Thread prod = new Thread(Producator);
                Thread[] cons = new Thread[K];
                prod.Start();
                for (int t = 0; t < K; t++)
                {
                    cons[t] = new Thread(Consumator);
                    cons[t].Start();
                }
                prod.Join();
                for (int t = 0; t < K; t++)
                    cons[t].Join();       // asteptam consumatorii inainte de nivelul urmator

                // intervalul fara pereche se copiaza inainte de a schimba rolurile vectorilor
                int fara = (n / (2 * w)) * (2 * w);
                if (fara + w >= n && fara < n) Array.Copy(sursa, fara, dest, fara, n - fara);

                int[] tmp = sursa; sursa = dest; dest = tmp;
                coada.Dispose();
            }
            return sursa;
        }

        // ---------- masurare ----------
        static bool Egale(int[] x, int[] y)
        {
            if (x.Length != y.Length) return false;
            for (int i = 0; i < x.Length; i++) if (x[i] != y[i]) return false;
            return true;
        }

        static int[] Genereaza(int n, int maxVal, int seed)
        {
            Random r = new Random(seed);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = r.Next(maxVal);
            return v;
        }

        // media a 5 masurari, dupa o rulare de incalzire; copiile se fac inainte de cronometrare
        static double Masoara(int[] original, int capacitate)
        {
            int rulari = 5;
            int[][] copii = new int[rulari + 1][];
            for (int i = 0; i <= rulari; i++) copii[i] = (int[])original.Clone();

            Stopwatch sw = new Stopwatch();
            double total = 0;
            for (int i = 0; i <= rulari; i++)
            {
                sw.Restart();
                if (capacitate == 0) SortareSecventiala(copii[i]);
                else SortareParalela(copii[i], capacitate);
                sw.Stop();
                if (i > 0) total += sw.Elapsed.TotalMilliseconds;   // i = 0 este incalzirea
            }
            return total / rulari;
        }

        static void Main(string[] args)
        {
            int[] lungimi = { 1000000, 4000000 };
            int[] capacitati = { 1, 8, 64 };

            Console.WriteLine("Merge Sort cu BlockingCollection: bloc B = {0}, consumatori K = {1}, p = {2}", B, K, P);
            Console.WriteLine("Procesoare logice: {0}", Environment.ProcessorCount);

            // verificare fata de referinta secventiala, inclusiv cu valori duplicate
            foreach (int n in lungimi)
                foreach (int maxVal in new int[] { int.MaxValue, 100 })
                {
                    int[] v = Genereaza(n, maxVal, 7);
                    int[] refr = SortareSecventiala((int[])v.Clone());
                    int[] copieSortata = (int[])v.Clone();
                    Array.Sort(copieSortata);
                    bool ok = Egale(refr, copieSortata);
                    foreach (int c in capacitati)
                        ok = ok && Egale(SortareParalela((int[])v.Clone(), c), refr);
                    Console.WriteLine("Verificare n = {0}, valori in [0, {1}): {2}", n,
                        maxVal == int.MaxValue ? "2^31-1" : maxVal.ToString(), ok ? "corect" : "GRESIT");
                }

            Console.WriteLine();
            Console.WriteLine("n;capacitate;Ts(ms);Tp(ms);S;E;C(ms)");
            foreach (int n in lungimi)
            {
                int[] v = Genereaza(n, int.MaxValue, 11);
                double ts = Masoara(v, 0);
                foreach (int c in capacitati)
                {
                    double tp = Masoara(v, c);
                    double s = ts / tp;
                    Console.WriteLine("{0};{1};{2:F1};{3:F1};{4:F2};{5:F2};{6:F1}", n, c, ts, tp, s, s / P, P * tp);
                }
            }
        }
    }
}
