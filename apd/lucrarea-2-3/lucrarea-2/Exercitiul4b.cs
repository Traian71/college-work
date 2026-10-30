using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading;

namespace ConsoleApplication1
{
    class Exercitiul4b
    {
        public static string[] fileEntries; //lista partajata de taskuri
        static object _lock = new object();

        // fiecare thread ia din listă următoarea imagine neprocesată, până se termină lista
        public static void ThreadFunction(object parameter)
        {
            int tid = (int)parameter;
            while (true)
            {
                string fileName = string.Empty;
                lock (_lock)
                {
                    for (int i = 0; i < fileEntries.Length && fileName == string.Empty; i++)
                    {
                        if (fileEntries[i] != string.Empty)
                        {
                            fileName = fileEntries[i];
                            fileEntries[i] = string.Empty; //imaginea a fost preluata
                        }
                    }
                }
                if (fileName == string.Empty)
                    break; //nu mai sunt imagini de procesat

                Exercitiul2.ProcesareImagine(fileName); //Task B, C, D
            }
        }

        public static void ProcesareDinamica(int n)
        {
            fileEntries = Directory.GetFiles(Program.sourceDirectory, "*.bmp").OrderBy(x => x).ToArray(); //Task A

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
            Console.Write("Numarul de threaduri N: ");
            int n = int.Parse(Console.ReadLine());
            Stopwatch timer = new Stopwatch();

            timer.Start();
            Exercitiul3.ProcesareParalela(n);
            timer.Stop();
            Console.WriteLine("Alocare statica (Exercitiul 3): {0} (ms)", timer.Elapsed.TotalMilliseconds);

            timer.Restart();
            ProcesareDinamica(n);
            timer.Stop();
            Console.WriteLine("Alocare dinamica: {0} (ms)", timer.Elapsed.TotalMilliseconds);
            Console.ReadLine();
        }
    }
}
