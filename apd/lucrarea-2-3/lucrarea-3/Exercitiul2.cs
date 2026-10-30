using System;
using System.IO;
using System.Linq;

namespace ConsoleApplication1
{
    // Exercițiul 2 - în zona critică doar citim și incrementăm indexul următoarei imagini
    class Exercitiul2
    {
        static string[] fileEntries;
        static object _lock = new object();
        static int next = 0;

        public static void Run()
        {
            fileEntries = Directory.GetFiles(Program.sourceDirectory, "*.bmp").OrderBy(x => x).ToArray(); //Task A
            next = 0;

            Program.LansareThreaduri(ThreadFunction);

            Console.ReadKey();
        }

        public static void ThreadFunction(object parameter)
        {
            int tid = (int)parameter; //thread ID
            bool exista = true;
            string fileName = string.Empty;
            while (exista)
            {
                int i;
                lock (_lock) //enter critical zone
                {
                    i = next;
                    next++;
                } //exit critical zone

                exista = i < fileEntries.Length;
                if (exista)
                {
                    fileName = fileEntries[i];
                    Console.WriteLine("Thread ID {0} take image {1} ", tid, i);

                    Program.ProcesareImagine(fileName); //Task B, C, D
                }
            }
        }
    }
}
