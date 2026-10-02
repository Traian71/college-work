using System;
using System.Threading;

namespace ConsoleApplication1
{
    class Program
    {
        private static int N = 10;
        private static int[] V = { 12, 5, 8, 21, 3, 17, 9, 14, 6, 11 };
        private static int suma = 0;
        private static Mutex mutex = new Mutex();

        public static void ThreadFunction(object parameter)
        {
            int i = (int)parameter;
            mutex.WaitOne();
            suma = suma + V[i];
            mutex.ReleaseMutex();
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

            double media = (double)suma / N;
            Console.WriteLine(string.Format("MainThread: media = {0}", media));
            Console.ReadLine();
        }
    }
}
