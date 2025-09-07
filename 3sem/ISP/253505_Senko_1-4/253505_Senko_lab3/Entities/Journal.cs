namespace _253505_Senko.Entities;

public class Journal
{
    public void Notifier(string message)
    {
        Console.WriteLine("Journal - "+message);
    }
    
    public Journal(InternetShop shop)
    {
        shop.NotifySystemProductClient += Notifier;
    }
}