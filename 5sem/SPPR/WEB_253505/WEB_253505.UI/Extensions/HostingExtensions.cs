using WEB_253505.API.HelperClasses;
using WEB_253505.UI.Services;
using WEB_253505.UI.Services.Authentication;
using WEB_253505.UI.Services.CategoryService;
using WEB_253505.UI.Services.FileService;
using WEB_253505.UI.Services.ProductService;

namespace WEB_253505.UI.Extensions;

public static class HostingExtensions
{
    public static void RegisterCustomServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddScoped<IProductService, ApiProductService>();
        builder.Services.AddScoped<ICategoryService, ApiCategoryService>();
        builder.Services.AddScoped<IFileService, ApiFileService>()
            .AddScoped<IFileService, ApiFileService>()
            .AddScoped<IAuthService, KeycloakAuthService>();
        builder.Services.Configure<KeycloakData>(builder.Configuration.GetSection("Keycloak"));
        builder.Services.AddHttpClient<ITokenAccessor, KeycloakTokenAccessor>();
        
    }
}