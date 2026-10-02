using System;
using System.Threading;

namespace ConsoleApplication1
{
    class Program
    {
        private static int N = 8;
        private static int[] A = { 1, 2, 3, 4, 5, 6, 7, 8 };
        private static int[] B = { 10, 20, 30, 40, 50, 60, 70, 80 };
        private static int[] C = new int[N];

        // fiecare thread aduna un singur element
        public static void ThreadFunction(object parameter)
        {
            int i = (int)parameter;
            C[i] = A[i] + B[i];
        }

        static void Main(string[] args)
        {
            Thread[] childThreads = new Thread[N];
            for (int i = 0; i < N; i++)
            {
                childThreads[i] = new Thread(ThreadFunction);
                childThreads[i].Start(i);
            }
            for (int i = 0; i < N; i++)
            {
                childThreads[i].Join();
            }

            for (int i = 0; i < N; i++)
                Console.WriteLine(string.Format("C[{0}] = {1} + {2} = {3}", i, A[i], B[i], C[i]));
            Console.ReadLine();
        }
    }
}
