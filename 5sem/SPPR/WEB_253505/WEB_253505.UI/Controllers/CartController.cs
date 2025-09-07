using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using WEB_253505.Domain.Cart;
using WEB_253505.UI.Extensions;
using WEB_253505.UI.Services.ProductService;

namespace WEB_253505.UI.Controllers;

public class CartController : Controller
{
    private readonly IProductService _productService;
    private readonly Cart _cart;

    public CartController(IProductService productService, Cart cart)
    {
        _productService = productService;
        _cart = cart;
    }

    [Authorize]
    [Route("[controller]/add/{id:int}")]
    public async Task<ActionResult> Add(int id, string returnUrl)
    {
        Cart cart = HttpContext.Session.Get<Cart>("cart") ?? new();
        var data = await _productService.GetProductByIdAsync(id);
        if (data.Successfull)
        {
            cart.AddToCart(data.Data);
            HttpContext.Session.Set<Cart>("cart", cart);
        }

        return Redirect(returnUrl);
    }

    [Authorize]
    public ActionResult Index()
    {
        return View(_cart);
    }

    [Authorize]
    [Route("[controller]/delete/{id:int}")]
    public ActionResult Delete(int id)
    {
        _cart.RemoveItems(id);
        return RedirectToAction("Index", "Cart");
    }
}