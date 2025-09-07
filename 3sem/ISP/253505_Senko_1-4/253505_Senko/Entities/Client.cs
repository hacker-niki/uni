using _253505_Senko.Collections;

namespace _253505_Senko.Entities;

public class Client
{
    private MyCustomCollection<Product> _products;

    public Client(string surname)
    {
        Surname = surname;
        _products = new MyCustomCollection<Product>();
    }

    public string Surname { get; }

    public void AddProduct(Product product)
    {
        _products.Add(product);
    }

    public MyCustomCollection<Product> GetProducts()
    {
        return _products;
    }
}