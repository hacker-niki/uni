using System.Diagnostics;

namespace Calculations;

public class Integral
{
    private SemaphoreSlim _semaphore = new SemaphoreSlim(5);
    
    public delegate void MessageNumberDelegate(double x);

    public event MessageNumberDelegate ElapsedTimeEvent;
    public event MessageNumberDelegate CompletinPercentEvent;
    public event MessageNumberDelegate EndFuncionEvent;

    private double A = 0;
    private double B = 1;
    private double Step = 0.00001;

    void setVars(double A, double B, double Step)
    {
        this.A = A;
        this.B = B;
        this.Step = Step;
    }

    private double function(double x)
    {
        return Math.Sin(x);
    }

    public void Integrate()
    {
        _semaphore.Wait();
        var time = Stopwatch.StartNew();

        double res = 0;
        double percent = 0;
        for (double i = A; i <= B; i += Step)
        {
            res += function(i) * Step;

            percent = Math.Abs(i - A) / Math.Abs(B - A) * 100;
            CompletinPercentEvent?.Invoke(percent);

            // Thread.Sleep(1);
        }

        time.Stop();
        ElapsedTimeEvent?.Invoke(time.ElapsedMilliseconds);
        EndFuncionEvent?.Invoke(res);
        _semaphore.Release();
    }
}