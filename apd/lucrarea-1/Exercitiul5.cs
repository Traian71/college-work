using System;
using System.Threading;

namespace ConsoleApplication1
{
    class Program
    {
        private static int N = 8;
        private static int K = 4;   // 1 <= K <= N/2
        private static int[] A = { 1, 2, 3, 4, 5, 6, 7, 8 };
        private static int[] B = { 10, 20, 30, 40, 50, 60, 70, 80 };
        private static int[] C = new int[N];

        // fiecare thread aduna o partitie de N/K elemente
        public static void ThreadFunction(object parameter)
        {
            int t = (int)parameter;
            int start = t * (N / K);
            int end = start + N / K;
            for (int i = start; i < end; i++)
                C[i] = A[i] + B[i];
        }

        static void Main(string[] args)
        {
            Thread[] childThreads = new Thread[K];
            for (int t = 0; t < K; t++)
            {
                childThreads[t] = new Thread(ThreadFunction);
                childThreads[t].Start(t);
            }
            for (int t = 0; t < K; t++)
            {
                childThreads[t].Join();
            }

            for (int i = 0; i < N; i++)
                Console.WriteLine(string.Format("C[{0}] = {1} + {2} = {3}", i, A[i], B[i], C[i]));
            Console.ReadLine();
        }
    }
}
