using System;
using System.Drawing;
using System.IO;
using System.Threading;

namespace ConsoleApplication1
{
    class Program
    {
        //atentie la calea de pe disk unde se afla imaginile!!!
        public static string sourceDirectory = @"C:\Studenti\SourceImages";
        public static string finalDirectory = @"C:\Studenti\FinalImages";
        public static int N = 4;

        static void Main(string[] args)
        {
            // folderele se pot da si la rulare: Program.exe <SourceImages> <FinalImages>
            if (args.Length == 2)
            {
                sourceDirectory = args[0];
                finalDirectory = args[1];
            }

            Console.Write("Exercitiul (1-4): ");
            switch (Console.ReadLine())
            {
                case "1": Exercitiul1.Run(); break;
                case "2": Exercitiul2.Run(); break;
                case "3": Exercitiul3.Run(); break;
                case "4": Exercitiul4.Run(); break;
            }
        }

        // Task B, C, D pentru o imagine (la fel ca in Lucrarea 2)
        public static void ProcesareImagine(string fileName)
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
                image.Save(Path.Combine(finalDirectory, Path.GetFileName(fileName))); //Task D
            }
        }

        // lansarea si asteptarea celor N threaduri
        public static void LansareThreaduri(ParameterizedThreadStart functie)
        {
            Thread[] childThreads = new Thread[N];
            for (int i = 0; i < N; i++)
            {
                childThreads[i] = new Thread(functie);
                childThreads[i].Start(i);
            }
            for (int i = 0; i < N; i++)
            {
                childThreads[i].Join();
            }
        }
    }
}
