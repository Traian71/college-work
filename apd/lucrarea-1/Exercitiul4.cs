using System;
using System.Threading;

namespace ConsoleApplication1
{
    class Exercitiul4
    {
        private static int N = 8;
        private static int[] A = { 1, 2, 3, 4, 5, 6, 7, 8 };
        private static int[] B = { 10, 20, 30, 40, 50, 60, 70, 80 };
        private static int[] C = new int[N];

        // threadul 0 aduna prima jumatate, threadul 1 a doua jumatate
        public static void ThreadFunction(object parameter)
        {
            int t = (int)parameter;
            int start = t * (N / 2);
            int end = start + N / 2;
            for (int i = start; i < end; i++)
                C[i] = A[i] + B[i];
        }

        public static void Run()
        {
            Thread thread0 = new Thread(ThreadFunction);
            Thread thread1 = new Thread(ThreadFunction);
            thread0.Start(0);
            thread1.Start(1);
            thread0.Join();
            thread1.Join();

            for (int i = 0; i < N; i++)
                Console.WriteLine(string.Format("C[{0}] = {1} + {2} = {3}", i, A[i], B[i], C[i]));
            Console.ReadLine();
        }
    }
}
