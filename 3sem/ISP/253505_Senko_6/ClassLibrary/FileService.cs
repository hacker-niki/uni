using System.Text.Json;
using _253505_Senko_6;

namespace ClassLibrary;

public class FileService : IFileService<Employee>
{
    public IEnumerable<Employee> ReadFile(string fileName)
    {
        using (FileStream fs = new FileStream(fileName, FileMode.OpenOrCreate))
        {
            var employees = JsonSerializer.Deserialize<IEnumerable<Employee>>(fs);
            foreach (var employee in employees)
            {
                yield return employee;
            }
        }
    }

    public void SaveData(IEnumerable<Employee> data, string fileName)
    {
        string jsonString = JsonSerializer.Serialize(data);
        File.WriteAllText(fileName, jsonString);

        Console.WriteLine("Data has been saved to file");
    }
}