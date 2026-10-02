using System;
using System.Threading;

namespace ConsoleApplication1
{
    class Exercitiul8
    {
        private static int N = 10;
        private static int[] V = { 12, 5, 8, 21, 3, 17, 9, 14, 6, 11 };
        private static int minim = int.MaxValue;
        private static Mutex mutex = new Mutex();

        public static void ThreadFunction(object parameter)
        {
            int i = (int)parameter;
            mutex.WaitOne();
            if (V[i] < minim)
                minim = V[i];
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
            for (int i = 0; i < N; i++)
            {
                childThreads[i].Join();
            }

            Console.WriteLine(string.Format("MainThread: minimul = {0}", minim));
            Console.ReadLine();
        }
    }
}
