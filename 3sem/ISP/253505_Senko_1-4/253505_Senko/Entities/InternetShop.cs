using _253505_Senko.Collections;
using _253505_Senko.Contracts;

namespace _253505_Senko.Entities
{
    public class InternetShop : IInternetShop
    {
        public delegate void MessageSystem(string message);
        
        public event MessageSystem? NotifySystem;  
        public event MessageSystem? NotifySystemOrder;  
        
        private MyCustomCollection<Product> _products = new();
        private MyCustomCollection<Client> _clients = new();
        
        public void AddProduct(Product product)
        {
            _products.Add(product);
            NotifySystem?.Invoke($"Продукт добавлен");
        }

        public void AddClient(Client client)
        {
            _clients.Add(client);
            NotifySystem?.Invoke($"Клиент добавлен");
        }

        public void AddOrder(string surname, string productName)
        {
            for (int i = 0; i < _clients.Count; i++)
            {
                if (_clients[i].Surname == surname)
                {
                    for (int j = 0; j < _products.Count; j++)
                    {
                        if (_products[j].Name == productName)
                        {
                            _clients[i].AddProduct(_products[j]);
                            NotifySystemOrder?.Invoke($"Заказ добавлен");
                            return;
                        }
                    }
                }
            }
            NotifySystemOrder?.Invoke($"Заказ не добавлен");
        }

        public MyCustomCollection<Product> GetClientProducts(string surname)
        {
            _clients.Reset();
            _clients.MoveNext();
            var client = _clients.Current;

            while (client.Surname != surname)
            {
                _clients.MoveNext();
                client = _clients.Current;
            }

            return client.GetProducts();
        }

        public int GetClientSum(string surname)
        {
            _clients.Reset();
            _clients.MoveNext();
            var client = _clients.Current;
            while (client.Surname != surname)
            {
                _clients.MoveNext();
                client = _clients.Current;
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
            for (int i = 0; i < _clients.Count; i++)
            {
                var products = _clients[i].GetProducts();

                for (int j = 0; j < products.Count; j++)
                {
                    if (products[j].Name == productName)
                    {
                        sum += products[j].Cost;
                    }
                }
            }

            return sum;
        }
    }
}