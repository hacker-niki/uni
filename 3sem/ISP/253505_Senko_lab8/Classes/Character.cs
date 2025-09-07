namespace Classes;

public class Character
{
    private static int _objectsCount = 0;
    
    public Character(string name, Weapon weapon)
    {
        Name = name;
        Id = _objectsCount;
        _objectsCount++;
        this.weapon = weapon;
    }

    public string Name { get; set; }
    public int Id { get; set; }
    public Weapon weapon { get; set; }
}