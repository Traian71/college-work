using System;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading;

namespace ConsoleApplication1
{
    // Exercițiul 1 - codul din laborator: o singură listă de taskuri și un singur lock
    class Exercitiul1
    {
        static string[] fileEntries;
        static object _lock = new object();

        public static void Run()
        {
            fileEntries = Directory.GetFiles(Program.sourceDirectory, "*.bmp").OrderBy(x => x).ToArray(); //Task A

            Thread[] childThreads = new Thread[Program.N];
            for (int i = 0; i < Program.N; i++)
            {
                childThreads[i] = new Thread(ThreadFunction);
                childThreads[i].Start(i);
            }
            for (int i = 0; i < Program.N; i++)
            {
                childThreads[i].Join();
            }

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
                lock (_lock) //enter critical zone
                {
                    for (int i = 0; i < fileEntries.Length && !exista; i++)
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
                    using (Bitmap image = new Bitmap(fileName)) //Task B
                    {
                        for (int x = 0; x < image.Width; x++)  //Task C
                        {
                            for (int y = 0; y < image.Height; y++)
                            {
                                Color pixelColor = image.GetPixel(x, y);
                                int gray = (pixelColor.R + pixelColor.G + pixelColor.B) / 3;
                                Color newColor = Color.FromArgb(gray, gray, gray);
                                image.SetPixel(x, y, newColor);
                            }
                        }
                        image.Save(Path.Combine(Program.finalDirectory, Path.GetFileName(fileName))); //Task D
                    }
                }
            }
        }
    }
}
