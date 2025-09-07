namespace _253505_Senko.Entities;

public class Client
{
    private List<Product> _products;
    private Dictionary<string, int> _orders;

    public Client(string surname)
    {
        Surname = surname;
        _products = new List<Product>();
        _orders = new Dictionary<string, int>();
    }

    public string Surname { get; }

    public void AddProduct(Product product)
    {
        if (!_products.Contains(product))
        {
            _products.Add(product);
            _orders.Add(product.Name, 0);
        }

        _orders[product.Name] += product.Cost;
    }

    public List<Product> GetProducts()
    {
        return _products;
    }

    public int GetWholeSum()
    {
        return (from p in _orders.Values select p).Sum();
    }

    public int GetProductSum(string productName)
    {
        if (_orders.ContainsKey(productName))
            return _orders[productName];
        return 0;
    }
}