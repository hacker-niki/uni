using System.Text;
using System.Text.Json;


namespace Classes;

public class StreamService<T>
{
    private SemaphoreSlim _semaphoreSlim;

    public StreamService(SemaphoreSlim semaphore)
    {
        _semaphoreSlim = semaphore;
    }
    public async Task WriteToStreamAsync(Stream stream, IEnumerable<T> data, IProgress<string> progress)
    {
        var options = new JsonSerializerOptions
        {
            WriteIndented = true
        };
        _semaphoreSlim.Wait();
        progress?.Report($"Start writing to stream {Thread.CurrentThread.ManagedThreadId}\n");
        //Thread.Sleep(1000);       
        List<T> list = data as List<T>;
        int count = 0;
        await stream.WriteAsync(Encoding.ASCII.GetBytes("["));
        foreach (T value in list)
        {
            Thread.Sleep(10);
            int progressPercentage = (int)(((double)count / list.Count) * 100);
            await JsonSerializer.SerializeAsync(stream, value, options);
            if (count != data.Count() - 1)
                 await stream.WriteAsync(Encoding.ASCII.GetBytes(",\n"));
            
            count++;
            string s = "";
            progress?.Report($"Поток {Thread.CurrentThread.ManagedThreadId}:{count*20/list.Count()}%"); 
        }
        Thread.Sleep(1000);
        await stream.WriteAsync(Encoding.ASCII.GetBytes("]"));
        progress?.Report($"End writing to stream {Thread.CurrentThread.ManagedThreadId}\n");
        Thread.Sleep(1000);
        _semaphoreSlim.Release();
    }
    public async Task CopyFromStreamAsync(Stream stream, string fileName, IProgress<string> progress)
    {
        _semaphoreSlim.Wait();
        //Thread.Sleep(1000);
        progress?.Report($"Start coping from stream {Thread.CurrentThread.ManagedThreadId} to file {fileName}\n");
        stream.Position = 0;
        //Thread.Sleep(1000);
        using (var file = File.Open(fileName, FileMode.OpenOrCreate))
        {
            await stream.CopyToAsync(file);
        }
        progress?.Report($"End coping from stream {Thread.CurrentThread.ManagedThreadId} to file {fileName}\n");
        Thread.Sleep(1000);
        _semaphoreSlim.Release();
    }
    public async Task<int> GetStatisticsAsync(string fileName, Func<T,bool> filter)
    {
        int numberOfFilteredProducts = 0;
        List<T> list;
        using (var file = File.Open(fileName, FileMode.Open))
        {
            list = await JsonSerializer.DeserializeAsync<List<T>>(file);
        }
        return list.Where(filter).Count();
    }
}
