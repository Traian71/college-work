using System;
using System.Diagnostics;
using System.Threading;

namespace L5
{
    internal class Program
    {
        public static int N = 64;//N items
        public static int[] a; //array of items
        public static int MAXV = 43; //valorile sunt intre 0 si MAXV-1 (ca in fisa)

        static void Main(string[] args)
        {
            // se pot da la rulare: L5.exe <MAXV> <NMAX> (valoarea maxima si dimensiunea maxima pentru masuratori)
            int NMAX = 1000000;
            if (args.Length == 2)
            {
                MAXV = int.Parse(args[0]);
                NMAX = int.Parse(args[1]);
            }

            // ca in fisa: un vector de 64 de elemente, sortat cu toate cele 4 variante
            a = new int[N];
            int[] temp = new int[N];
            Random rand = new Random();
            for (int i = 0; i < N; i++)
            {
                a[i] = rand.Next(0, 43);
            }
            a.CopyTo(temp, 0);//copy to preserve input array
            Console.WriteLine("A: ");
            Print(a);

            QuickSort(0, a.Length - 1);
            Console.WriteLine("QuickSort(A): ");
            Print(a);

            temp.CopyTo(a, 0);
            QuickSortPar(0, a.Length - 1);
            Console.WriteLine("QuickSortPar(A): ");
            Print(a);

            temp.CopyTo(a, 0);
            MergeSort(0, a.Length - 1);
            Console.WriteLine("MergeSort(A): ");
            Print(a);

            temp.CopyTo(a, 0);
            MergeSortPar(0, a.Length - 1);
            Console.WriteLine("MergeSortPar(A): ");
            Print(a);

            //EXERCITIUL 1 si 3 - verificarea sortarii seriale pentru vectori de diverse lungimi
            Console.WriteLine();
            int[] lungimi = { 1, 2, 5, 10, 64, 1000, 10000 };
            foreach (int n in lungimi)
            {
                Genereaza(n, rand);
                QuickSort(0, a.Length - 1);
                bool okQ = EsteSortat(a);

                Genereaza(n, rand);
                MergeSort(0, a.Length - 1);
                bool okM = EsteSortat(a);

                Console.WriteLine("N = {0}: QuickSort corect = {1}, MergeSort corect = {2}", n, okQ, okM);
            }

            //EXERCITIUL 2 si 4 - timpii de executie si corectitudinea fata de varianta seriala
            Console.WriteLine();
            Console.WriteLine("Valori intre 0 si {0}", MAXV - 1);
            int[] dimensiuni = { 1000, 10000, 100000, 1000000 };

            // incalzire: prima rulare a fiecarei sortari e mai lenta (programul abia a pornit), asa ca nu o masuram
            Genereaza(10000, rand);
            int[] cald = new int[N];
            a.CopyTo(cald, 0);
            QuickSort(0, a.Length - 1);
            cald.CopyTo(a, 0); QuickSortPar(0, a.Length - 1);
            cald.CopyTo(a, 0); MergeSort(0, a.Length - 1);
            cald.CopyTo(a, 0); MergeSortPar(0, a.Length - 1);

            foreach (int n in dimensiuni)
            {
                if (n > NMAX) break;
                Genereaza(n, rand);
                int[] intrare = new int[n];
                a.CopyTo(intrare, 0);

                // fiecare timp e media a 3 rulari pe acelasi vector de intrare
                double tQ = Masoara(() => QuickSort(0, a.Length - 1), intrare);
                int[] rezQ = new int[n];
                a.CopyTo(rezQ, 0);

                double tQp = Masoara(() => QuickSortPar(0, a.Length - 1), intrare);
                bool okQp = Egale(a, rezQ);

                double tM = Masoara(() => MergeSort(0, a.Length - 1), intrare);
                int[] rezM = new int[n];
                a.CopyTo(rezM, 0);

                double tMp = Masoara(() => MergeSortPar(0, a.Length - 1), intrare);
                bool okMp = Egale(a, rezM);

                Console.WriteLine("N = {0}: QuickSort = {1:F2} ms, QuickSortPar = {2:F2} ms (egal cu serial: {3})",
                    n, tQ, tQp, okQp);
                Console.WriteLine("N = {0}: MergeSort = {1:F2} ms, MergeSortPar = {2:F2} ms (egal cu serial: {3})",
                    n, tM, tMp, okMp);

                // unde cade primul pivot: QuickSortPar da cate o parte fiecarui thread
                intrare.CopyTo(a, 0);
                int p = Partition(0, n - 1);
                Console.WriteLine("N = {0}: primul pivot imparte vectorul in {1} si {2} elemente", n, p, n - 1 - p);
            }

            Console.WriteLine("Press any key for exit...");
            Console.ReadKey();
        }

        public static void Print(int[] m)
        {
            int i;
            for (i = 0; i < ((N < 64) ? N : 64); i++)
            {
                Console.Write(string.Format("{0} ", m[i]));
            }
            Console.WriteLine();
        }

        // umple vectorul a cu n valori aleatoare
        public static void Genereaza(int n, Random rand)
        {
            N = n;
            a = new int[N];
            for (int i = 0; i < N; i++)
            {
                a[i] = rand.Next(0, MAXV);
            }
        }

        public static bool EsteSortat(int[] m)
        {
            for (int i = 0; i < m.Length - 1; i++)
            {
                if (m[i] > m[i + 1])
                    return false;
            }
            return true;
        }

        public static bool Egale(int[] x, int[] y)
        {
            for (int i = 0; i < x.Length; i++)
            {
                if (x[i] != y[i])
                    return false;
            }
            return true;
        }

        // ruleaza sortarea de 3 ori, de fiecare data pe o copie a vectorului de intrare, si intoarce timpul mediu
        public static double Masoara(Action sortare, int[] intrare)
        {
            double total = 0;
            for (int k = 0; k < 3; k++)
            {
                intrare.CopyTo(a, 0);
                Stopwatch timer = new Stopwatch();
                timer.Start();
                sortare();
                timer.Stop();
                total += timer.Elapsed.TotalMilliseconds;
            }
            return total / 3;
        }

        //EXERCITIUL 1 - QuickSort serial
        public static void QuickSort(int left, int right)
        {
            if (left < right)
            {
                int pivotIndex = Partition(left, right);
                QuickSort(left, pivotIndex - 1);
                QuickSort(pivotIndex + 1, right);
            }
        }

        private static int Partition(int left, int right)
        {
            int pivotValue = a[right];
            int i = left - 1;

            for (int j = left; j <= right - 1; j++)
            {
                if (a[j] <= pivotValue)
                {
                    i++;
                    Swap(i, j);
                }
            }

            Swap(i + 1, right);

            return i + 1;
        }

        private static void Swap(int i, int j)
        {
            int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }

        //EXERCITIUL 2 - QuickSort paralel
        public static void QuickSortPar(int left, int right)
        {
            if (left < right)
            {
                int pivotIndex = Partition(left, right);

                // Create two threads to sort the left and right subarrays
                Thread leftThread = new Thread(() => QuickSort(left, pivotIndex - 1));
                Thread rightThread = new Thread(() => QuickSort(pivotIndex + 1, right));

                // Start the threads
                leftThread.Start();
                rightThread.Start();

                // Wait for the threads to finish
                leftThread.Join();
                rightThread.Join();
            }
        }

        //EXERCITIUL 3 - MergeSort serial
        public static void MergeSort(int l, int r)
        {
            if (l < r)
            {
                int m = l + (r - l) / 2;

                MergeSort(l, m);
                MergeSort(m + 1, r);

                Merge(l, m, r);
            }
        }

        private static void Merge(int l, int m, int r)
        {
            int n1 = m - l + 1;
            int n2 = r - m;

            int[] L = new int[n1];
            int[] R = new int[n2];

            for (int i = 0; i < n1; i++)
                L[i] = a[l + i];
            for (int j = 0; j < n2; j++)
                R[j] = a[m + 1 + j];

            int k = l;
            int x = 0, y = 0;
            while (x < n1 && y < n2)
            {
                if (L[x] <= R[y])
                {
                    a[k] = L[x];
                    x++;
                }
                else
                {
                    a[k] = R[y];
                    y++;
                }
                k++;
            }

            while (x < n1)
            {
                a[k] = L[x];
                x++;
                k++;
            }

            while (y < n2)
            {
                a[k] = R[y];
                y++;
                k++;
            }
        }

        //EXERCITIUL 4 - MergeSort paralel
        public static void MergeSortPar(int l, int r)
        {
            if (l < r)
            {
                int m = l + (r - l) / 2;

                // Create two threads to sort left and right sub-arrays
                Thread leftThread = new Thread(() => MergeSort(l, m));
                Thread rightThread = new Thread(() => MergeSort(m + 1, r));

                // Start the threads
                leftThread.Start();
                rightThread.Start();

                // Wait for the threads to finish
                leftThread.Join();
                rightThread.Join();

                Merge(l, m, r);
            }
        }
    }
}
