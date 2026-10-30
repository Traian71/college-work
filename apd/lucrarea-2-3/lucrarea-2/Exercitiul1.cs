using System;
using System.Drawing;
using System.IO;

namespace ConsoleApplication1
{
    // Exercițiul 1 - dependențele de date pentru o singură imagine
    //
    //   Task A: fileName = calea imaginii         I = {}           O = {fileName}
    //   Task B: image = new Bitmap(fileName)      I = {fileName}   O = {image}
    //   Task C: conversia pixelilor în gri        I = {image}      O = {image}
    //   Task D: image.Save(...)                   I = {image}      O = {fișierul salvat}
    //
    // Dependențe (toate prin succesiune):
    //   A -> B : B citește fileName, scris de A
    //   B -> C : C citește image, creat de B
    //   C -> D : D salvează image, modificat de C
    //
    // Graful dependențelor:
    //
    //   A ---> B ---> C ---> D
    //
    // Taskurile formează un lanț, fiecare are nevoie de rezultatul celui dinainte, deci
    // condițiile lui Bernstein nu sunt îndeplinite (ex. I_B ∩ O_A = {fileName} ≠ Ø).
    // Taskurile A-D nu se pot executa în paralel. Se poate paraleliza doar în interiorul
    // taskului C: fiecare pixel se calculează independent de ceilalți, deci imaginea ar
    // putea fi împărțită în zone procesate de threaduri diferite.
    class Exercitiul1
    {
        public static void Run()
        {
            string fileName = Path.Combine(Program.sourceDirectory, "a.bmp"); //Task A

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
                image.Save(Path.Combine(Program.finalDirectory, "a.bmp")); //Task D
            }

            Console.WriteLine("Imaginea a fost salvata");
            Console.ReadLine();
        }
    }
}
