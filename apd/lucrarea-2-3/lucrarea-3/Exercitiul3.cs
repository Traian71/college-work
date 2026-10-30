using System;
using System.IO;
using System.Linq;

namespace ConsoleApplication1
{
    // Exercițiul 3 - câte un lock pentru fiecare task
    class Exercitiul3
    {
        static string[] fileEntries;
        //static object _lock = new object();
        static object[] _locks;

        public static void Run()
        {
            fileEntries = Directory.GetFiles(Program.sourceDirectory, "*.bmp").OrderBy(x => x).ToArray(); //Task A

            _locks = new object[fileEntries.Length];
            for (int i = 0; i < _locks.Length; i++)
                _locks[i] = new object();

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
                exista = false;

                for (int i = 0; i < fileEntries.Length && !exista; i++)
                {
                    lock (_locks[i]) //enter critical zone at task level
                    {
                        if (!string.IsNullOrEmpty(fileEntries[i]))
                        {
                            exista = true;
                            fileName = fileEntries[i];
                            fileEntries[i] = string.Empty; //mark file as processed (by convention an empty file == file is already taken)
                            Console.WriteLine("Thread ID {0} take image {1} ", tid, i);
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
