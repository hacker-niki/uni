using WEB_253505.API.Services.CategoryService;
using WEB_253505.API.Services.ProductService;
using WEB_253505.UI.Services.ProductService;

namespace WEB_253505.API.Extensions;

public static class HostingExtensions
{
    public static void RegisterCustomServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddScoped<IProductService, ProductService>();
        builder.Services.AddScoped<ICategoryService, CategoryService>();
    }
}