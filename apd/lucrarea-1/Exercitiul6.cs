using System;
using System.Threading;

namespace ConsoleApplication1
{
    class Exercitiul6
    {
        private static int N = 10;
        private static int[] V = { 12, 5, 8, 21, 3, 17, 9, 14, 6, 11 };
        private static int suma = 0;
        private static int terminate = 0;
        private static Mutex mutex = new Mutex();

        public static void ThreadFunction(object parameter)
        {
            int i = (int)parameter;
            mutex.WaitOne();
            suma = suma + V[i];
            terminate++;
            // ultimul thread care aduna afiseaza suma
            if (terminate == N)
                Console.WriteLine(string.Format("Thread {0}: suma = {1}", Thread.CurrentThread.ManagedThreadId, suma));
            mutex.ReleaseMutex();
        }

        public static void Run()
        {
            Thread[] childThreads = new Thread[N];
            for (int i = 0; i < N; i++)
            {
                childThreads[i] = new Thread(ThreadFunction);
                childThreads[i].Start(i);
            }
            Console.ReadLine();
        }
    }
}
