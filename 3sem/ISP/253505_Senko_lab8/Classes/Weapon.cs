namespace Classes;

public class Weapon
{
    private static int _objectsCount = 0;
    public string Name { get; set; }
    public int Id { get; set; }

    public Weapon(string name)
    {
        Name = name;
        Id = _objectsCount;
        _objectsCount++;
    }
}