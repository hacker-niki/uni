namespace _253505_Senko.Entities;

public class Product
{
    public Product(string name, int cost)
    {
        Name = name;
        Cost = cost;
    }

    public string Name { get; }
    public int Cost { get; set; }
}