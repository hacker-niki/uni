using WEB_253505.Domain.Entities;
namespace WEB_253505.Domain.Cart;
public class Cart
{
    public Dictionary<int, CartItem> CartItems { get; set; } = new();
    public virtual void AddToCart(Product product)
    {
        var exists = CartItems.ContainsKey(product.Id);
        if (exists)
        {
            CartItems[product.Id].Count++;
        }
        else
        {
            CartItems.Add(product.Id, new CartItem { Count = 1, Product = product });
        }
    }
    public virtual void RemoveItems(int id)
    {
        CartItems.Remove(id);
    }
    public virtual void ClearAll()
    {
        CartItems.Clear();
    }
    public int Count { get => CartItems.Sum(item => item.Value.Count);  }
    public double TotalCost { get => CartItems.Sum(item 
        => item.Value.Product.Price * item.Value.Count); }
}