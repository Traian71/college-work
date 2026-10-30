using System;
using System.Drawing;
using System.IO;
using System.Linq;

namespace ConsoleApplication1
{
    // Exercițiul 2 - dependențele de date pentru un set de imagini
    //
    // Task A produce lista fileEntries. Pentru fiecare imagine i din listă se execută
    // lanțul Bi -> Ci -> Di, la fel ca la Exercițiul 1.
    //
    // Dependențe:
    //   A -> Bi         : Bi citește fileEntries[i], scris de A
    //   Bi -> Ci -> Di  : ca la Exercițiul 1, pentru imaginea i
    //   Între lanțurile a două imagini diferite i și j nu există dependențe: citesc fișiere
    //   diferite, lucrează pe obiecte Bitmap diferite și salvează fișiere diferite, deci
    //   condițiile lui Bernstein sunt îndeplinite (I_i ∩ O_j = Ø, I_j ∩ O_i = Ø, O_i ∩ O_j = Ø).
    //
    // Graful dependențelor:
    //
    //                  A
    //         /        |        \
    //        v         v         v
    //        B1        B2  ...   Bn
    //        |         |         |
    //        v         v         v
    //        C1        C2  ...   Cn
    //        |         |         |
    //        v         v         v
    //        D1        D2  ...   Dn
    //
    // Da, problema se poate paraleliza: după Task A, imaginile se împart între threaduri și
    // fiecare thread execută B, C, D pentru imaginile lui. În codul serial variabilele
    // fileName și image sunt refolosite la fiecare iterație, dar dacă fiecare thread are
    // propriile variabile locale, această dependență dispare.
    class Exercitiul2
    {
        // Task B, C, D pentru o imagine
        public static void ProcesareImagine(string fileName)
        {
            using (Bitmap image = new Bitmap(fileName)) //Task B
            {
                for (int x = 0; x < image.Width; x++) //Task C
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

        public static void ProcesareSeriala()
        {
            string[] fileEntries = Directory.GetFiles(Program.sourceDirectory, "*.bmp").OrderBy(x => x).ToArray(); //Task A
            foreach (string fileName in fileEntries)
            {
                ProcesareImagine(fileName);
            }
        }

        public static void Run()
        {
            ProcesareSeriala();
            Console.WriteLine("Imaginile au fost procesate");
            Console.ReadLine();
        }
    }
}
