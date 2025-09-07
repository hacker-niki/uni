using WEB_253505.Domain.Entities;

namespace WEB_253505.Domain.Cart;

public class CartItem
{
    public Product Product { get; set; }
    public int Count { get; set; }
}