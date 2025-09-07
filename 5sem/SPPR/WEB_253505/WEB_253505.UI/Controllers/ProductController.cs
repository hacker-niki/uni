using Microsoft.AspNetCore.Mvc;
using WEB_253505.Domain.Entities;
using WEB_253505.Domain.Models;
using WEB_253505.UI.Extensions;
using WEB_253505.UI.Services.CategoryService;
using WEB_253505.UI.Services.ProductService;

namespace WEB_253505.UI.Controllers;

public class ProductController(
    ICategoryService categoryService,
    IProductService productService
    )
    : Controller
{
    IProductService _productService = productService;
    ICategoryService _categoryService = categoryService;

    // GET
    public async Task<IActionResult> Index(int? category, int? pageNo)
    {
        // int pageNumber = pageNo ?? 1;
        var productResponse = await _productService.GetProductListAsync(category, pageNo ?? 1);
        var caegoryResponse =
            await _categoryService.GetCategoryListAsync();

        if (!productResponse.Successfull)
            return NotFound(productResponse.ErrorMessage);
        if (!caegoryResponse.Successfull)
            return NotFound(caegoryResponse.ErrorMessage);

        //Console.WriteLine(productResponse.Data.Items[0].Name);

        category ??= _categoryService.GetCategoryListAsync().Result.Data[0].Id;
        ViewData["CategoryId"] = category;
        ViewData["CategoryName"] = _categoryService.GetCategoryListAsync().Result.Data.Find(c => c.Id == category).Name;
        ViewData["Categories"] = caegoryResponse.Data;
        ViewData["PagesCount"] = _productService.PagesCount(category).Result;
        ViewData["CurrentPage"] = pageNo;
        ViewData["ImagesSrc"] = "";
        Console.Error.WriteLine(ViewData["Categories"]);
        
        if (Request.IsAjaxRequest())
        {
            return PartialView("_PaginationPartial", new
            {
                CurrentCategory = category,
                Categories = productResponse.Data,
                Products = productResponse.Data!.Items,
                ReturnUrl = Request.Path + Request.QueryString.ToUriComponent(),
                CurrentPage = pageNo ?? 1,
                TotalPages = _productService.PagesCount(category).Result,
                Admin = false
            });
        }
        
        return View(new ListModel<Product>()
        {
            CurrentPage = pageNo ?? 1,
            Items = productResponse.Data.Items,
            TotalPages = _productService.PagesCount(category).Result
        });
    }
}