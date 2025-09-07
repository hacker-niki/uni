using _253505_Senko.Contracts;

namespace _253505_Senko.Entities
{
    public class InternetShop : IInternetShop
    {
        public delegate void MessageSystem(string message);

        public event MessageSystem? NotifySystemProductClient;
        public event MessageSystem? NotifySystemOrder;

        private Dictionary<string, Product> _products = new();
        private List<Client> _clients = new();

        public void AddProduct(Product product)
        {
            _products.Add(product.Name, product);
            NotifySystemProductClient?.Invoke($"Продукт добавлен");
        }

        public void AddClient(Client client)
        {
            _clients.Add(client);
            NotifySystemProductClient?.Invoke($"Клиент добавлен");
        }

        public void AddOrder(string surname, string productName)
        {
            for (int i = 0; i < _clients.Count; i++)
            {
                if (_clients[i].Surname == surname)
                {
                    if (!_products.ContainsKey(productName))
                    {
                        break;
                    }

                    _clients[i].AddProduct(_products[productName]);
                    NotifySystemOrder?.Invoke($"Заказ добавлен");
                    return;
                }
            }

            NotifySystemOrder?.Invoke($"Заказ не добавлен");
        }

        public List<Product> GetClientProducts(string surname)
        {
            foreach (var client in _clients)
            {
                if (client.Surname == surname)
                    return client.GetProducts();
            }

            throw new Exception("Нет такой фамилии");
        }

        public int GetClientSum(string surname)
        {
            Client client = null;
            foreach (var cl in _clients)
            {
                if (cl.Surname == surname)
                {
                    client = cl;
                    break;
                }
            }

            int sum = 0;
            var products = client.GetProducts();
            for (int i = 0; i < products.Count; i++)
            {
                sum += products[i].Cost;
            }

            return sum;
        }

        public int GetProductSum(string productName)
        {
            int sum = 0;
            foreach (var client in _clients)
            {
                sum += client.GetProductSum(productName);
            }

            return sum;
        }

        public List<string> GetAllSortedProducts()
        {
            var ans = from product in new List<Product>(_products.Values) orderby product.Cost select product.Name;

            return (List<string>)ans;
        }

        public int GetOrdersSum()
        {
            var ans = from client in new List<Client>(_clients) select client.GetWholeSum();
            return ((List<int>)ans).Sum();
        }

        public int GetClientOrdersSum(string surname)
        {
            foreach (var client in _clients)
            {
                if (client.Surname == surname)
                {
                    return client.GetWholeSum();
                }
            }

            throw new Exception("Нет такой фамилии");
        }

        public string GetBestClientName()
        {
            var ans = from client in _clients orderby client.GetWholeSum() select client.Surname;
            return ((List<string>)ans)[0];
        }

        public int ClientsCountPaidMoreThan(int cost)
        {
            return _clients.Aggregate(0, (total, client) => client.GetWholeSum() > cost ? total + 1 : total);
        }
    }
}