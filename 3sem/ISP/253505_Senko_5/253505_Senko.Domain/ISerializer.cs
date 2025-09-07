namespace _253505_Senko.Domain;

public interface ISerializer
{
    IEnumerable<Pyramid> DeSerializeByLINQ(string fileName);
    IEnumerable<Pyramid> DeSerializeXML(string fileName);
    IEnumerable<Pyramid> DeSerializeJSON(string fileName);
    void SerializeByLINQ(IEnumerable<Pyramid> pyramids, string fileName);
    void SerializeXML(IEnumerable<Pyramid> pyramids, string fileName);
    void SerializeJSON(IEnumerable<Pyramid> pyramids, string fileName);
}