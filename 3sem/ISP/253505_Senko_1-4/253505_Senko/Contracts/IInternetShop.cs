using _253505_Senko.Collections;
using _253505_Senko.Entities;

namespace _253505_Senko.Contracts;

public interface IInternetShop
{
    void AddProduct(Product product);

    void AddClient(Client client);
    
    void AddOrder(string surname, string product);

    public MyCustomCollection<Product> GetClientProducts(string surname);

    public int GetClientSum(string surname);

    public int GetProductSum(string product);
}