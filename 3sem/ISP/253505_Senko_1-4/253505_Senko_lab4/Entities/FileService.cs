using _253505_Senko_lab4.Interfaces;

namespace _253505_Senko_lab4.Entities;

public class FileService : IFileService<Superhero>
{
    public IEnumerable<Superhero> ReadFile(string fileName)
    {
        if (!File.Exists(fileName))
            throw new Exception("No such file");
        using var stream = new FileStream(fileName, FileMode.Open);
        using var binReader = new BinaryReader(stream);
        while (stream.Position < stream.Length)
        {
            var superhero = new Superhero();
            try
            {
                superhero.Force = binReader.ReadInt32();
                superhero.IsDead = binReader.ReadBoolean();
                superhero.Name = binReader.ReadString();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                yield break;
            }

            yield return superhero;
        }
    }

    public void SaveData(IEnumerable<Superhero> data, string fileName)
    {
        using var stream = new FileStream(fileName, FileMode.OpenOrCreate);
        var binWriter = new BinaryWriter(stream);
        foreach (var superhero in data)
        {
            try
            {
                binWriter.Write(superhero.Force);
                binWriter.Write(superhero.IsDead);
                binWriter.Write(superhero.Name);
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                return;
            }
        }
    }
}