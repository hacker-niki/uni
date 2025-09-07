using Microsoft.AspNetCore.Mvc;
using WEB_253505.Domain.Cart;
using WEB_253505.UI.Extensions;

namespace WEB_253505.UI.Components;

public class CartViewComponent : ViewComponent
{
    // GET
    public Task<IViewComponentResult> InvokeAsync()
    {
        Cart cart = HttpContext.Session.Get<Cart>("cart") ?? new Cart();
        return Task.FromResult<IViewComponentResult>(View(cart));
    }
}