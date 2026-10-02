using System;
using System.Threading;

namespace ConsoleApplication1
{
    class Exercitiul1
    {
        public static void ThreadFunction()
        {
            Console.WriteLine(string.Format("ChildThread {0}: this is child thread", Thread.CurrentThread.ManagedThreadId));
        }

        public static void Run()
        {
            Console.WriteLine("MainThread: creating child threads");
            for (int i = 0; i < 5; i++)
            {
                Thread childThread = new Thread(ThreadFunction);
                childThread.Start();
            }
            Console.WriteLine("MainThread: this is main thread");
            Console.ReadLine();
        }
    }
}
