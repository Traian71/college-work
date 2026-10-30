using System;
using System.IO;
using System.Linq;

namespace ConsoleApplication1
{
    // Exercițiul 4 - două liste de taskuri, fiecare cu lock-ul ei
    class Exercitiul4
    {
        static string[] fileEntries1;
        static string[] fileEntries2;

        static object _lock1 = new object();
        static object _lock2 = new object();

        public static void Run()
        {
            string[] fileEntries = Directory.GetFiles(Program.sourceDirectory, "*.bmp").OrderBy(x => x).ToArray(); //Task A
            fileEntries1 = fileEntries.Take(fileEntries.Length / 2).ToArray();
            fileEntries2 = fileEntries.Skip(fileEntries.Length / 2).ToArray();

            Program.LansareThreaduri(ThreadFunction);

            Console.ReadKey();
        }

        public static void ThreadFunction(object parameter)
        {
            int tid = (int)parameter; //thread ID
            string[] fileEntries = (tid % 2 == 0) ? fileEntries1 : fileEntries2;
            object _lock = (tid % 2 == 0) ? _lock1 : _lock2;

            bool exista = true;
            string fileName = string.Empty;
            while (exista)
            {
                exista = false;
                lock (_lock) //enter critical zone
                {
                    for (int i = 0; i < fileEntries.Length && !exista; i++)
                    {
                        if (!string.IsNullOrEmpty(fileEntries[i]))
                        {
                            exista = true;
                            fileName = fileEntries[i];
                            fileEntries[i] = string.Empty; //mark file as processed (by convention an empty file == file is already taken)
                            Console.WriteLine("Thread ID {0} (lista {1}) take image {2} ", tid, tid % 2 + 1, i);
                        }
                    }
                }
                if (exista)
                {
                    Program.ProcesareImagine(fileName); //Task B, C, D
                }
            }
        }
    }
}
