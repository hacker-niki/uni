namespace _253505_Senko_lab4;

public class Superhero
{
    public int Force { get; set; }
    public bool IsDead { get; set; }
    public string Name { get; set; }

    public override string ToString()
    {
        return Force.ToString() + " " + IsDead.ToString() + " " + Name;
    }
}