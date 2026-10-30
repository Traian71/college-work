using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using SkiaSharp;

namespace L2
{
    class Program
    {
        static string baseDir = Path.Combine(Path.GetTempPath(), "APD_Masurare");
        static StringBuilder rezultate = new StringBuilder();

        static void Main(string[] args)
        {
            Console.WriteLine("Generare imagini de test (doar la prima rulare)...");
            string mici = Genereaza("mici", Enumerable.Repeat(100, 40).ToArray());
            string medii = Genereaza("medii", Enumerable.Repeat(500, 40).ToArray());
            string mari = Genereaza("mari", Enumerable.Repeat(2000, 8).ToArray());
            string mixte = Genereaza("mixte", new int[] { 2000, 2000, 1800, 1600, 1500, 1200, 1000, 900, 700, 600, 400, 300, 250, 150, 120, 100 });

            Log("Procesoare logice: " + Environment.ProcessorCount);
            Log("Sistem: " + Environment.OSVersion);

            Static(mici, 2);

            Log("");
            Log("EX4 - imagini medii (40 x 500x500)");
            long tSerial = Serial(medii);
            Log("serial: " + tSerial + " ms");
            for (int n = 1; n <= 20; n++)
            {
                long t = Static(medii, n);
                Log("N=" + n + ": " + t + " ms, speedup = " + ((double)tSerial / t).ToString("0.00"));
            }

            Log("");
            Log("EX4 DINAMIC - imagini mixte (16 imagini, 100x100 ... 2000x2000)");
            Log("serial: " + Serial(mixte) + " ms");
            foreach (int n in new int[] { 2, 4, 8 })
                Log("N=" + n + ": static " + Static(mixte, n) + " ms, dinamic " + Dinamic(mixte, n) + " ms");

            Log("");
            Log("EX5 - N=4");
            foreach (string dir in new string[] { mici, medii, mari })
                Log(Path.GetFileName(dir) + ": serial " + Serial(dir) + " ms, static " + Static(dir, 4) + " ms, dinamic " + Dinamic(dir, 4) + " ms");

            string folder = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            if (string.IsNullOrEmpty(folder) || !Directory.Exists(folder))
                folder = AppDomain.CurrentDomain.BaseDirectory;
            string cale = Path.Combine(folder, "rezultate_APD.txt");
            try
            {
                File.WriteAllText(cale, rezultate.ToString());
            }
            catch (Exception)
            {
                cale = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "rezultate_APD.txt");
                File.WriteAllText(cale, rezultate.ToString());
            }
            Console.WriteLine();
            Console.WriteLine("Gata! Rezultatele sunt salvate in: " + cale);
        }

        static void Log(string text)
        {
            Console.WriteLine(text);
            rezultate.AppendLine(text);
        }

        static string Genereaza(string nume, int[] dimensiuni)
        {
            string dir = Path.Combine(baseDir, nume);
            string src = Path.Combine(dir, "SourceImages");
            Directory.CreateDirectory(src);
            Directory.CreateDirectory(Path.Combine(dir, "FinalImages"));
            Random rnd = new Random(1);
            for (int i = 0; i < dimensiuni.Length; i++)
            {
                string f = Path.Combine(src, "img" + i.ToString("00") + ".png");
                if (File.Exists(f))
                    continue;
                int d = dimensiuni[i];
                using (SKBitmap b = new SKBitmap(d, d))
                using (SKCanvas g = new SKCanvas(b))
                {
                    g.Clear(SKColors.White);
                    for (int k = 0; k < 50; k++)
                        using (SKPaint br = new SKPaint { Color = new SKColor((byte)rnd.Next(256), (byte)rnd.Next(256), (byte)rnd.Next(256)) })
                            g.DrawRect(rnd.Next(d), rnd.Next(d), rnd.Next(1, d), rnd.Next(1, d), br);
                    Salveaza(b, f);
                }
            }
            return dir;
        }

        static string[] Fisiere(string dir)
        {
            return Directory.GetFiles(Path.Combine(dir, "SourceImages"), "*.png").OrderBy(x => x).ToArray();
        }

        static void Salveaza(SKBitmap image, string fileName)
        {
            using (SKData data = image.Encode(SKEncodedImageFormat.Png, 100))
            using (FileStream fs = File.Create(fileName))
                data.SaveTo(fs);
        }

        static void Proceseaza(string fileName, string finalDirectory)
        {
            using (SKBitmap image = SKBitmap.Decode(fileName))
            using (SKPixmap pixmap = image.PeekPixels())
            {
                int width = image.Width, height = image.Height, rowBytes = image.RowBytes;
                Span<byte> px = pixmap.GetPixelSpan<byte>();
                for (int x = 0; x < width; x++)
                {
                    for (int y = 0; y < height; y++)
                    {
                        int i = y * rowBytes + x * 4;
                        byte gray = (byte)((px[i] + px[i + 1] + px[i + 2]) / 3);
                        px[i] = gray;
                        px[i + 1] = gray;
                        px[i + 2] = gray;
                    }
                }
                image.NotifyPixelsChanged();
                Salveaza(image, Path.Combine(finalDirectory, Path.GetFileName(fileName)));
            }
        }

        static long Serial(string dir)
        {
            string[] files = Fisiere(dir);
            string final = Path.Combine(dir, "FinalImages");
            Stopwatch timer = Stopwatch.StartNew();
            foreach (string f in files)
                Proceseaza(f, final);
            timer.Stop();
            return timer.ElapsedMilliseconds;
        }

        static long Static(string dir, int n)
        {
            string[] files = Fisiere(dir);
            string final = Path.Combine(dir, "FinalImages");
            Thread[] th = new Thread[n];
            Stopwatch timer = Stopwatch.StartNew();
            for (int t = 0; t < n; t++)
            {
                int tid = t;
                th[t] = new Thread(() =>
                {
                    int start = tid * files.Length / n;
                    int end = (tid + 1) * files.Length / n;
                    for (int i = start; i < end; i++)
                        Proceseaza(files[i], final);
                });
                th[t].Start();
            }
            foreach (Thread x in th)
                x.Join();
            timer.Stop();
            return timer.ElapsedMilliseconds;
        }

        static long Dinamic(string dir, int n)
        {
            string[] files = Fisiere(dir);
            string final = Path.Combine(dir, "FinalImages");
            object _lock = new object();
            Thread[] th = new Thread[n];
            Stopwatch timer = Stopwatch.StartNew();
            for (int t = 0; t < n; t++)
            {
                th[t] = new Thread(() =>
                {
                    while (true)
                    {
                        string? fileName = null;
                        lock (_lock)
                        {
                            for (int i = 0; i < files.Length && fileName == null; i++)
                            {
                                if (!string.IsNullOrEmpty(files[i]))
                                {
                                    fileName = files[i];
                                    files[i] = string.Empty;
                                }
                            }
                        }
                        if (fileName == null)
                            break;
                        Proceseaza(fileName, final);
                    }
                });
                th[t].Start();
            }
            foreach (Thread x in th)
                x.Join();
            timer.Stop();
            return timer.ElapsedMilliseconds;
        }
    }
}
