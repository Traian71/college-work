using System;
using System.Diagnostics;

namespace ConsoleApplication1
{
    class Exercitiul4a
    {
        public static void Run()
        {
            Stopwatch timer = new Stopwatch();

            timer.Start();
            Exercitiul2.ProcesareSeriala();
            timer.Stop();
            double tSerial = timer.Elapsed.TotalMilliseconds;
            Console.WriteLine("Tserial = {0} (ms)", tSerial);

            // implementarea paralelă de la Exercițiul 3, pentru N = 1..20
            for (int n = 1; n <= 20; n++)
            {
                timer.Restart();
                Exercitiul3.ProcesareParalela(n);
                timer.Stop();
                double tParalel = timer.Elapsed.TotalMilliseconds;
                Console.WriteLine("N = {0}: Tparalel = {1} (ms), S = {2:F2}", n, tParalel, tSerial / tParalel);
            }
            Console.ReadLine();
        }
    }
}
