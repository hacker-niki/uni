namespace _253505_Senko_lab4.Interfaces;

public interface IFileService<T>
{
    IEnumerable<T> ReadFile(string fileName);
    void SaveData(IEnumerable<T> data, string fileName);
}