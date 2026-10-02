using System;
using System.Threading;

namespace ConsoleApplication1
{
    class Program
    {
        public static void ThreadFunction()
        {
            Console.WriteLine(string.Format("ChildThread {0}: this is child thread", Thread.CurrentThread.ManagedThreadId));
        }

        static void Main(string[] args)
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
