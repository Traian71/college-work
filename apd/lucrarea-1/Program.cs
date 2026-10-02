using System;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Exercitiul (1-8): ");
            switch (Console.ReadLine())
            {
                case "1": Exercitiul1.Run(); break;
                case "2": Exercitiul2.Run(); break;
                case "3": Exercitiul3.Run(); break;
                case "4": Exercitiul4.Run(); break;
                case "5": Exercitiul5.Run(); break;
                case "6": Exercitiul6.Run(); break;
                case "7": Exercitiul7.Run(); break;
                case "8": Exercitiul8.Run(); break;
            }
        }
    }
}
