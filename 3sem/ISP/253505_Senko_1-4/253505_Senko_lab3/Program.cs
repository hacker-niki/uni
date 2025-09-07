using _253505_Senko.Entities;

var shop = new InternetShop();

var v = new List<int>();

Journal journal = new(shop);

shop.NotifySystemOrder += journal.Notifier;


shop.NotifySystemOrder += message =>
{
    Console.ForegroundColor = ConsoleColor.Red;
    Console.WriteLine("Program - " + message);
    Console.ResetColor();
};



v.Add(1);

foreach (var t in v)
{
    Console.WriteLine(t);
}

var client = new Client("Ahmatov");
shop.AddClient(client);

client = new Client("Ahmato");
shop.AddClient(client);

client = new Client("Ahmat");
shop.AddClient(client);

client = new Client("Ahma");
shop.AddClient(client);

client = new Client("Ahm");
shop.AddClient(client);

var product = new Product("Product", 2);
shop.AddProduct(product);

product = new Product("Produc", 1);
shop.AddProduct(product);

product = new Product("Produ", 3);
shop.AddProduct(product);

product = new Product("Prod", 5);
shop.AddProduct(product);


shop.AddOrder("Ahmatov", "Product");
shop.AddOrder("Ahmatov", "Produc");
shop.AddOrder("Ahmatov", "Produ");
shop.AddOrder("Ahmatov", "Prod");
shop.AddOrder("Ahmatov", "Prod");
shop.AddOrder("Ahmatov", "Prod");
shop.AddOrder("Ahmatov", "Prod");
shop.AddOrder("Ahmatov", "Prod");
shop.AddOrder("Ahmatov", "Prod");
shop.AddOrder("Ahm", "Prod");
shop.AddOrder("Ahm", "Produ");
shop.AddOrder("Ahm", "Produc");
shop.AddOrder("Ahm", "Produc");
shop.AddOrder("Ahm", "Produc");

Console.WriteLine(shop.GetClientSum("Ahmatov"));
Console.WriteLine(shop.GetClientSum("Ahm"));

Console.WriteLine(shop.GetProductSum("Product"));
Console.WriteLine(shop.GetProductSum("Produc"));

var products = shop.GetClientProducts("Ahmatov");
Console.WriteLine();
Console.WriteLine(products.Count);
foreach (var p in products)
{
    Console.WriteLine(p.Name);
    Console.WriteLine(p.Cost);
    Console.WriteLine();
}

Console.ReadLine();