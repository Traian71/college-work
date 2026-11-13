using System;
using System.Diagnostics;
using System.Threading;

namespace L4
{
    public class ThreadParam
    {
        public int pos; //position in array
        public int len; //partition length
    }

    internal class Program
    {
        public static int N = 128;//N items (putere a lui 2, pentru V3 si V5)
        public static int P = 16;//P threads (putere a lui 2, pentru V4)

        public static double[] a; //array of items
        public static double sTemp; //shared
        public static double[] pSum; //partial sums
        public static Mutex mutex = new Mutex();
        public static Barrier barier;

        static void Main(string[] args)
        {
            // N si P se pot da si la rulare: L4.exe <N> <P>
            if (args.Length == 2)
            {
                N = int.Parse(args[0]);
                P = int.Parse(args[1]);
            }
            Console.WriteLine("N = {0}, P = {1}", N, P);

            Init();
            Console.Write("A: ");
            Print(a);

            //sequencial reduction
            Stopwatch timerSeq = new Stopwatch();
            timerSeq.Start();
            double sSeq = ReductionSeq();
            timerSeq.Stop();
            Console.WriteLine("Sum(A)={0}; Seq time = {1} ms", sSeq, timerSeq.Elapsed.TotalMilliseconds);

            //EXERCITIUL 1 - parallel reduction V1 (fara sincronizare), rulat de 10 ori
            int gresite = 0;
            for (int k = 0; k < 10; k++)
            {
                Init();
                Stopwatch timerPar1 = new Stopwatch();
                timerPar1.Start();
                double s1 = ReductionParV1();
                timerPar1.Stop();
                if (s1 != sSeq) gresite++;
                Console.WriteLine("Sum(A)={0}; ParV1 time = {1} ms", s1, timerPar1.Elapsed.TotalMilliseconds);
            }
            Console.WriteLine("V1: {0} rezultate gresite din 10", gresite);

            //EXERCITIUL 2 - V1 cu mutex
            Init();
            Stopwatch timerPar1m = new Stopwatch();
            timerPar1m.Start();
            double s = ReductionParV1Mutex();
            timerPar1m.Stop();
            Console.WriteLine("Sum(A)={0}; ParV1 + mutex time = {1} ms", s, timerPar1m.Elapsed.TotalMilliseconds);

            //EXERCITIUL 3 - parallel reduction V2
            Init();
            Stopwatch timerPar2 = new Stopwatch();
            timerPar2.Start();
            s = ReductionParV2();
            timerPar2.Stop();
            Console.WriteLine("Sum(A)={0}; ParV2 time = {1} ms", s, timerPar2.Elapsed.TotalMilliseconds);

            //EXERCITIUL 4 - parallel reduction V3 (bariera)
            Init(); // V3 modifica vectorul a, deci il refacem inainte
            Stopwatch timerPar3 = new Stopwatch();
            timerPar3.Start();
            s = ReductionParV3();
            timerPar3.Stop();
            Console.WriteLine("Sum(A)={0}; ParV3 time = {1} ms", s, timerPar3.Elapsed.TotalMilliseconds);

            //EXERCITIUL 5 - parallel reduction V4 = V2 + V3
            Init();
            Stopwatch timerPar4 = new Stopwatch();
            timerPar4.Start();
            s = ReductionParV4();
            timerPar4.Stop();
            Console.WriteLine("Sum(A)={0}; ParV4 time = {1} ms", s, timerPar4.Elapsed.TotalMilliseconds);

            //EXERCITIUL 6 - parallel reduction V5 - recursion
            Init(); // V5 modifica vectorul a
            Stopwatch timerPar5 = new Stopwatch();
            timerPar5.Start();
            s = ReductionParV5();
            timerPar5.Stop();
            Console.WriteLine("Sum(A)={0}; ParV5 time = {1} ms", s, timerPar5.Elapsed.TotalMilliseconds);

            //EXERCITIUL 7 - minim, maxim si media, pe un vector cu valori aleatoare
            InitRandom();
            Console.Write("B: ");
            Print(a);
            Stopwatch timerMinSeq = new Stopwatch();
            timerMinSeq.Start();
            double min = MinSeq();
            double max = MaxSeq();
            double medie = ReductionSeq() / N;
            timerMinSeq.Stop();
            Console.WriteLine("Seq:  min={0}; max={1}; media={2}; time = {3} ms", min, max, medie, timerMinSeq.Elapsed.TotalMilliseconds);

            Stopwatch timerMinPar = new Stopwatch();
            timerMinPar.Start();
            MinMaxMediePar(out min, out max, out medie);
            timerMinPar.Stop();
            Console.WriteLine("Par:  min={0}; max={1}; media={2}; time = {3} ms", min, max, medie, timerMinPar.Elapsed.TotalMilliseconds);

            Console.WriteLine("Press any key for exit...");
            Console.ReadKey();
        }

        public static void Init()
        {
            a = new double[N];
            for (int i = 0; i < N; i++)
            {
                a[i] = 1;
            }
        }

        public static void InitRandom()
        {
            Random r = new Random(4);
            a = new double[N];
            for (int i = 0; i < N; i++)
            {
                a[i] = r.Next(1000);
            }
        }

        public static void Print(double[] m)
        {
            int i;
            for (i = 0; i < ((N < 8) ? N : 8); i++)
            {
                Console.Write(string.Format("{0} ", m[i]));
            }
            Console.WriteLine();
        }

        public static double ReductionSeq()
        {
            double s = a[0];
            int i;
            for (i = 1; i < N; i++)
            {
                s += a[i];
            }
            return s;
        }

        // V1: N threaduri, fiecare aduna un element la variabila partajata (fara sincronizare)
        public static double ReductionParV1()
        {
            sTemp = 0;

            Thread[] childThreads = new Thread[N];
            int i;
            for (i = 0; i < N; i++)
            {
                childThreads[i] = new Thread(ThreadFunctionV1);
                childThreads[i].Start(i);
            }
            for (i = 0; i < N; i++)
            {
                childThreads[i].Join();
            }

            return sTemp;
        }
        public static void ThreadFunctionV1(object parameter)
        {
            int idx = (int)parameter;
            sTemp += a[idx];
        }

        // V1 corectata: accesul la sTemp este protejat cu un mutex
        public static double ReductionParV1Mutex()
        {
            sTemp = 0;

            Thread[] childThreads = new Thread[N];
            int i;
            for (i = 0; i < N; i++)
            {
                childThreads[i] = new Thread(ThreadFunctionV1Mutex);
                childThreads[i].Start(i);
            }
            for (i = 0; i < N; i++)
            {
                childThreads[i].Join();
            }

            return sTemp;
        }
        public static void ThreadFunctionV1Mutex(object parameter)
        {
            int idx = (int)parameter;
            mutex.WaitOne();
            sTemp += a[idx];
            mutex.ReleaseMutex();
        }

        // V2: P partitii de N/P elemente, fiecare thread calculeaza o suma partiala
        public static double ReductionParV2()
        {
            sTemp = 0;
            pSum = new double[P];
            Thread[] childThreads = new Thread[P];
            int i;
            for (i = 0; i < P; i++)
            {
                childThreads[i] = new Thread(ThreadFunctionV2);
                childThreads[i].Start(i);
            }
            for (i = 0; i < P; i++)
            {
                childThreads[i].Join();
                sTemp += pSum[i];
            }

            return sTemp;
        }
        public static void ThreadFunctionV2(object parameter)
        {
            int idx = (int)parameter;
            pSum[idx] = 0;
            for (int i = (N / P) * idx; i < (N / P) * (idx + 1); i++)
            {
                pSum[idx] += a[i];
            }
        }

        // V3: N/2 threaduri, log(N) pasi separati prin bariera
        public static double ReductionParV3()
        {
            sTemp = 0;
            Thread[] childThreads = new Thread[N / 2];
            barier = new Barrier(N / 2);
            int i;
            for (i = 0; i < N / 2; i++)
            {
                childThreads[i] = new Thread(ThreadFunctionV3);
                childThreads[i].Start(2 * i);
            }
            for (i = 0; i < N / 2; i++)
            {
                childThreads[i].Join();
            }
            sTemp = a[0];
            return sTemp;
        }
        public static void ThreadFunctionV3(object parameter)
        {
            int idx = (int)parameter;
            for (int i = 1; i <= N / 2; i *= 2)
            {
                barier.SignalAndWait();
                if (idx % (2 * i) == 0)
                    a[idx] += a[idx + i];
            }
        }

        // V4 = V2 + V3: fiecare din cele P threaduri calculeaza suma partitiei sale (ca la V2),
        // apoi sumele partiale se reduc in log(P) pasi cu bariera (ca la V3)
        public static double ReductionParV4()
        {
            sTemp = 0;
            pSum = new double[P];
            Thread[] childThreads = new Thread[P];
            barier = new Barrier(P);
            int i;
            for (i = 0; i < P; i++)
            {
                childThreads[i] = new Thread(ThreadFunctionV4);
                childThreads[i].Start(i);
            }
            for (i = 0; i < P; i++)
            {
                childThreads[i].Join();
            }
            sTemp = pSum[0];
            return sTemp;
        }
        public static void ThreadFunctionV4(object parameter)
        {
            int idx = (int)parameter;
            pSum[idx] = 0;
            for (int i = (N / P) * idx; i < (N / P) * (idx + 1); i++)
            {
                pSum[idx] += a[i];
            }
            for (int i = 1; i <= P / 2; i *= 2)
            {
                barier.SignalAndWait();
                if (idx % (2 * i) == 0)
                    pSum[idx] += pSum[idx + i];
            }
        }

        // V5: generarea recursiva a threadurilor, fara bariera
        public static double ReductionParV5()
        {
            sTemp = 0;
            Thread[] childThreads = new Thread[2];
            int i;
            int j = 0;
            for (i = 0; i < N; i += N / 2, j++)
            {
                childThreads[j] = new Thread(ThreadFunctionV5);
                childThreads[j].Start(new ThreadParam { pos = i, len = N / 2 });
            }
            for (i = 0; i < 2; i++)
            {
                childThreads[i].Join();
            }
            sTemp = a[0] + a[N / 2];
            return sTemp;
        }
        public static void ThreadFunctionV5(object parameter)
        {
            var p = (ThreadParam)parameter;
            if (p.len > 2)
            {
                Thread[] childThreads = new Thread[2];
                int i;
                int j = 0;
                for (i = 0; i < p.len; i += p.len / 2, j++)
                {
                    childThreads[j] = new Thread(ThreadFunctionV5);
                    // pozitia copilului este relativa la partitia parintelui: p.pos + i
                    childThreads[j].Start(new ThreadParam { pos = p.pos + i, len = p.len / 2 });
                }
                for (i = 0; i < 2; i++)
                {
                    childThreads[i].Join();
                }
                a[p.pos] += a[p.pos + p.len / 2];
            }
            else
            {
                a[p.pos] += a[p.pos + 1];
            }
        }

        // EXERCITIUL 7
        public static double MinSeq()
        {
            double m = a[0];
            for (int i = 1; i < N; i++)
            {
                if (a[i] < m) m = a[i];
            }
            return m;
        }
        public static double MaxSeq()
        {
            double m = a[0];
            for (int i = 1; i < N; i++)
            {
                if (a[i] > m) m = a[i];
            }
            return m;
        }

        // varianta paralela: ca la V2, fiecare thread calculeaza minimul, maximul si suma partitiei sale,
        // iar threadul principal combina rezultatele partiale
        public static double[] pMin, pMax;
        public static void MinMaxMediePar(out double min, out double max, out double medie)
        {
            pMin = new double[P];
            pMax = new double[P];
            pSum = new double[P];
            Thread[] childThreads = new Thread[P];
            int i;
            for (i = 0; i < P; i++)
            {
                childThreads[i] = new Thread(ThreadFunctionMinMax);
                childThreads[i].Start(i);
            }
            min = double.MaxValue;
            max = double.MinValue;
            double suma = 0;
            for (i = 0; i < P; i++)
            {
                childThreads[i].Join();
                if (pMin[i] < min) min = pMin[i];
                if (pMax[i] > max) max = pMax[i];
                suma += pSum[i];
            }
            medie = suma / N;
        }
        public static void ThreadFunctionMinMax(object parameter)
        {
            int idx = (int)parameter;
            int start = (N / P) * idx;
            pMin[idx] = a[start];
            pMax[idx] = a[start];
            pSum[idx] = 0;
            for (int i = start; i < (N / P) * (idx + 1); i++)
            {
                if (a[i] < pMin[idx]) pMin[idx] = a[i];
                if (a[i] > pMax[idx]) pMax[idx] = a[i];
                pSum[idx] += a[i];
            }
        }
    }
}
