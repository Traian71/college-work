using System;
using System.IO;
using System.Linq;
using System.Threading;

namespace ConsoleApplication1
{
    class Exercitiul3
    {
        public static string[] fileEntries; //lista partajata
        private static int nrThreads;

        // threadul t procesează partiția lui din listă: imaginile de la t*M/N la (t+1)*M/N - 1
        public static void ThreadFunction(object parameter)
        {
            int t = (int)parameter;
            int start = t * fileEntries.Length / nrThreads;
            int end = (t + 1) * fileEntries.Length / nrThreads;
            for (int i = start; i < end; i++)
            {
                Exercitiul2.ProcesareImagine(fileEntries[i]);
            }
        }

        public static void ProcesareParalela(int n)
        {
            fileEntries = Directory.GetFiles(Program.sourceDirectory, "*.bmp").OrderBy(x => x).ToArray(); //Task A
            nrThreads = n;

            Thread[] threads = new Thread[n];
            for (int t = 0; t < n; t++)
            {
                threads[t] = new Thread(ThreadFunction);
                threads[t].Start(t);
            }
            for (int t = 0; t < n; t++)
            {
                threads[t].Join();
            }
        }

        public static void Run()
        {
            fileEntries = Directory.GetFiles(Program.sourceDirectory, "*.bmp").OrderBy(x => x).ToArray(); //Task A

            // varianta cu două threaduri
            nrThreads = 2;
            Thread th1 = new Thread(ThreadFunction);
            Thread th2 = new Thread(ThreadFunction);
            th1.Start(0);
            th2.Start(1);
            th1.Join();
            th2.Join();
            Console.WriteLine("2 threaduri: imaginile au fost procesate");

            // varianta cu trei threaduri
            nrThreads = 3;
            th1 = new Thread(ThreadFunction);
            th2 = new Thread(ThreadFunction);
            Thread th3 = new Thread(ThreadFunction);
            th1.Start(0);
            th2.Start(1);
            th3.Start(2);
            th1.Join();
            th2.Join();
            th3.Join();
            Console.WriteLine("3 threaduri: imaginile au fost procesate");

            // varianta cu N threaduri
            Console.Write("Numarul de threaduri N: ");
            int n = int.Parse(Console.ReadLine());
            ProcesareParalela(n);
            Console.WriteLine("{0} threaduri: imaginile au fost procesate", n);
            Console.ReadLine();
        }
    }
}
