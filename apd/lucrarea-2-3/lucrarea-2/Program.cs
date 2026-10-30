using System;

namespace ConsoleApplication1
{
    class Program
    {
        //atentie la calea de pe disk unde se afla imaginile!!!
        public static string sourceDirectory = @"C:\Studenti\SourceImages";
        public static string finalDirectory = @"C:\Studenti\FinalImages";

        static void Main(string[] args)
        {
            // folderele se pot da si la rulare: Program.exe <SourceImages> <FinalImages>
            if (args.Length == 2)
            {
                sourceDirectory = args[0];
                finalDirectory = args[1];
            }

            Console.Write("Exercitiul (1, 2, 3, 4a, 4b, 5): ");
            switch (Console.ReadLine())
            {
                case "1": Exercitiul1.Run(); break;
                case "2": Exercitiul2.Run(); break;
                case "3": Exercitiul3.Run(); break;
                case "4a": Exercitiul4a.Run(); break;
                case "4b": Exercitiul4b.Run(); break;
                case "5": Exercitiul5.Run(); break;
            }
        }
    }
}
