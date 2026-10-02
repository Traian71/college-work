using System;
using System.Threading;

namespace ConsoleApplication1
{
    class Program
    {
        public static void ThreadFunction1()
        {
            Console.WriteLine("ChildThread 1: this is the first child thread");
        }

        public static void ThreadFunction2()
        {
            Console.WriteLine("ChildThread 2: this is the second child thread");
        }

        public static void ThreadFunction3()
        {
            Console.WriteLine("ChildThread 3: this is the third child thread");
        }

        static void Main(string[] args)
        {
            Console.WriteLine("MainThread: creating child threads");
            Thread thread1 = new Thread(ThreadFunction1);
            Thread thread2 = new Thread(ThreadFunction2);
            Thread thread3 = new Thread(ThreadFunction3);
            thread1.Start();
            thread2.Start();
            thread3.Start();
            Console.WriteLine("MainThread: this is main thread");
            Console.ReadLine();
        }
    }
}
