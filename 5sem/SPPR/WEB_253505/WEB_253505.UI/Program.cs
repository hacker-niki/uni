using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Protocols.OpenIdConnect;
using WEB_253505.API.HelperClasses;
using WEB_253505.Domain.Cart;
using WEB_253505.UI.Controllers;
using Serilog;
using WEB_253505.UI.Data;
using WEB_253505.UI.Extensions;
using WEB_253505.UI.Middleware;
using WEB_253505.UI.Services.ProductService;
using WEB_253505.UI.Services;
using WEB_253505.UI.Services.CartService;
using WEB_253505.UI.Services.CategoryService;
using WEB_253505.UI.Services.FileService;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();
builder.RegisterCustomServices(); // Custom service registration

var uriData = builder.Configuration.GetSection("UriData").Get<UriData>();

builder.Services
    .AddHttpClient<IProductService, ApiProductService>(opt => opt.BaseAddress = new Uri(uriData.ApiUri));
builder.Services
    .AddHttpClient<ICategoryService, ApiCategoryService>(opt => opt.BaseAddress = new Uri(uriData.ApiUri));
builder.Services.AddRazorPages();
builder.Services
    .AddHttpClient<IFileService, ApiFileService>(opt => opt.BaseAddress = new Uri(uriData.ApiUri));
builder.Services.AddRazorPages();

var keycloakData =
    builder.Configuration.GetSection("Keycloak").Get<KeycloakData>();
builder.Services
    .AddAuthentication(options =>
    {
        options.DefaultScheme =
            CookieAuthenticationDefaults.AuthenticationScheme;
        options.DefaultChallengeScheme =
            OpenIdConnectDefaults.AuthenticationScheme;
    })
    .AddCookie()
    .AddJwtBearer()
    .AddOpenIdConnect(options =>
    {
        options.Authority =
            $"{keycloakData.Host}/auth/realms/{keycloakData.Realm}";
        options.ClientId = keycloakData.ClientId;
        options.ClientSecret = keycloakData.ClientSecret;
        options.ResponseType = OpenIdConnectResponseType.Code;
        options.Scope.Add("openid"); // Customize scopes as needed
        options.SaveTokens = true;
        options.RequireHttpsMetadata = false; // позволяет обращаться к локальному Keycloak по http
        options.MetadataAddress = $"{keycloakData.Host}/realms/{keycloakData.Realm}/.well-known/openid-configuration";
    });
builder.Services.AddHttpContextAccessor();

builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession();
builder.Services.AddScoped<Cart>(sp => SessionCart.GetCart(sp));

builder.Host.UseSerilog((context, configuration) =>
{
    configuration.ReadFrom.Configuration(context.Configuration);
});


var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseSession();

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();


app.UseAuthentication();
app.UseAuthorization();

app.UseMiddleware<LoggingMiddleware>();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");
app.MapRazorPages();

app.Run();
