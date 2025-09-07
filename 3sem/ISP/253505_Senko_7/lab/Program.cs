using System.Security.Principal;
using Calculations;

Integral calc = new Integral();
calc.CompletinPercentEvent += (d) =>
{
    int id = Thread.CurrentThread.ManagedThreadId;
    int progBarCells = (int)(d + 0.01) / 5;
    lock (Console.Out)
    {
        Console.SetCursorPosition(0, id);
        string output = "$\"Stream {id}: [";
        for (int i = 0; i < progBarCells; ++i)
        {
            output += '=';
        }

        if (progBarCells < 20)
        {
            output += '>';
        }

        for (int i = 0; i < 19 - progBarCells; ++i)
        {
            output += ' ';
        }

        output += $"]{d:F1}%";
        Console.Write(output);
    }
};

calc.EndFuncionEvent += (result) =>
{
    int id = Thread.CurrentThread.ManagedThreadId;
    lock (Console.Out)
    {
        Console.SetCursorPosition(0, id);
        Console.Write($"Stream {id}: Ended with result: {result}");
    }
};

calc.ElapsedTimeEvent += (time) =>
{
    int id = Thread.CurrentThread.ManagedThreadId;
    lock (Console.Out)
    {
        Console.SetCursorPosition(60, id);
        Console.Write($"Consumed time: {time}ms");
        if (Thread.CurrentThread.Priority == ThreadPriority.Lowest)
        {
            Console.Write(" Low priority");
        }

        if (Thread.CurrentThread.Priority == ThreadPriority.Highest)
        {
            Console.Write(" High priority");
        }
    }
};

int numThreads = 10;

Thread[] threads = new Thread[numThreads+1];

for (int i = 0; i <= numThreads; ++i)
{
    threads[i] = new Thread(calc.Integrate);
}

threads[0].Priority = ThreadPriority.Highest;

threads[1].Priority = ThreadPriority.Lowest;

for (int i = 0; i <= numThreads; ++i)
{
    threads[i].Start();
}