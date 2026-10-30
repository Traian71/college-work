using System;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

namespace ConsoleApplication1
{
    class Exercitiul5
    {
        private static int[] dimensiuni = { 100, 500, 2000 };
        private static int[] nrImagini = { 40, 40, 8 }; // câte imagini din fiecare dimensiune

        // creează nr imagini BMP 24bpp de dimensiune x dimensiune
        public static void CreareImagini(string directory, int dimensiune, int nr)
        {
            Directory.CreateDirectory(directory);
            Random rnd = new Random();
            for (int k = 0; k < nr; k++)
            {
                using (Bitmap image = new Bitmap(dimensiune, dimensiune, PixelFormat.Format24bppRgb))
                {
                    using (Graphics g = Graphics.FromImage(image))
                    {
                        g.Clear(Color.FromArgb(rnd.Next(256), rnd.Next(256), rnd.Next(256)));
                        g.FillEllipse(Brushes.Orange, 0, 0, dimensiune / 2, dimensiune / 2);
                    }
                    image.Save(Path.Combine(directory, "img" + k + ".bmp"), ImageFormat.Bmp);
                }
            }
        }

        public static void Run()
        {
            Console.Write("Numarul de threaduri N: ");
            int n = int.Parse(Console.ReadLine());
            string sourceRoot = Program.sourceDirectory;
            string finalRoot = Program.finalDirectory;
            Stopwatch timer = new Stopwatch();

            for (int j = 0; j < dimensiuni.Length; j++)
            {
                int d = dimensiuni[j];
                // fiecare set de imagini în subfolderul lui, ex. SourceImages\100x100
                string folder = d + "x" + d;
                Program.sourceDirectory = Path.Combine(sourceRoot, folder);
                Program.finalDirectory = Path.Combine(finalRoot, folder);
                if (!Directory.Exists(Program.sourceDirectory))
                    CreareImagini(Program.sourceDirectory, d, nrImagini[j]);
                Directory.CreateDirectory(Program.finalDirectory);

                timer.Restart();
                Exercitiul2.ProcesareSeriala();
                timer.Stop();
                double tSerial = timer.Elapsed.TotalMilliseconds;

                timer.Restart();
                Exercitiul3.ProcesareParalela(n);
                timer.Stop();
                double tStatic = timer.Elapsed.TotalMilliseconds;

                timer.Restart();
                Exercitiul4b.ProcesareDinamica(n);
                timer.Stop();
                double tDinamic = timer.Elapsed.TotalMilliseconds;

                Console.WriteLine("Imagini {0}:", folder);
                Console.WriteLine("   serial = {0} (ms)", tSerial);
                Console.WriteLine("   static (Ex. 3) = {0} (ms), S = {1:F2}", tStatic, tSerial / tStatic);
                Console.WriteLine("   dinamic (Ex. 4) = {0} (ms), S = {1:F2}", tDinamic, tSerial / tDinamic);
            }
            Console.ReadLine();
        }
    }
}
