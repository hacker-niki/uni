using Microsoft.EntityFrameworkCore;
using WEB_253505.Domain.Entities;
using WEB_253505.API.Data;
using WEB_253505.API.Services.CategoryService;
using WEB_253505.API.Services.ProductService;
using WEB_253505.Domain.Models;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.Extensions.DependencyInjection;

namespace WEB_253505.UI.Services.ProductService;

public class ProductService(
    IConfiguration config,
    IServiceProvider serviceProvider)
    : IProductService
{
    ICategoryService _categoryService = serviceProvider.GetService<ICategoryService>();
    List<Product> _products = new List<Product>();
    private readonly int _maxPageSize = 100;

    public Task<int> PagesCount(int? categoryId)
    {
        using var scope = serviceProvider.CreateScope(); // Assuming you have a way to access IServiceProvider
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        _products = context.Products.ToList();
        int pageSize = config.GetValue<int>("PageSize");
        List<Product>? products;
        if (categoryId is null)
        {
            
            products = _products.ToList();
            return Task.FromResult((products.Count()) / pageSize + ((products.Count() % pageSize) == 0 ? 0 : 1));
        }
        var category = _categoryService.GetCategoryListAsync().Result.Data.First(c => c.Id == categoryId);
        products = _products.Where(p => p.CategoryId == category.Id).ToList();
        return Task.FromResult((products.Count()) / pageSize + ((products.Count() % pageSize) == 0 ? 0 : 1));
    }

    public Task<ResponseData<ListModel<Product>>> GetProductListAsync(int? categoryId, int? pageSize,
        int pageNo = 1)
    {
        pageSize ??= _maxPageSize * 2;

        pageSize = Math.Min(pageSize ?? 1, _maxPageSize);

        using var scope = serviceProvider.CreateScope(); // Assuming you have a way to access IServiceProvider
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        _products = context.Products.ToList();

        int itemsToSkip = (pageNo - 1) * pageSize?? 1;

        if (categoryId != null)
        {
            var category = _categoryService.GetCategoryListAsync().Result.Data.First(c => c.Id == categoryId);

            // Вернуть список продуктов (пока со статическими данными)
            var products = _products.Where(p => p.CategoryId == category.Id)
                .Skip(itemsToSkip)
                .Take(pageSize?? 1)
                .ToList();
            var count = _products.Count();
            if (count == 0)
            {
                return Task.FromResult(
                    ResponseData<ListModel<Product>>.Success(new ListModel<Product> { Items = products }));
            }

            int totalPages = (int)Math.Ceiling(count / (double)pageSize);
            if (pageNo > totalPages)
                return Task.FromResult(ResponseData<ListModel<Product>>.Error("No such page"));

            return Task.FromResult(ResponseData<ListModel<Product>>
                .Success(new ListModel<Product> { Items = products }));
        }
        else
        {
            var products = _products
                .Skip(itemsToSkip)
                .Take(pageSize?? 1)
                .ToList();
            return Task.FromResult(ResponseData<ListModel<Product>>
                .Success(new ListModel<Product> { Items = products }));
        }
    }

    public Task<ResponseData<Product>> GetProductByIdAsync(int Id)
    {
        using var scope = serviceProvider.CreateScope(); // Assuming you have a way to access IServiceProvider
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        _products = context.Products.ToList();

        // Найти продукт по Id (пока со статическими данными)
        var product = _products.Find(p => p.Id == Id);
        return Task.FromResult(new ResponseData<Product> { Data = product });
    }

    public async Task UpdateProductAsync(int id, Product updatedProduct, IFormFile? formFile)
    {
        using var scope = serviceProvider.CreateScope(); // Assuming you have a way to access IServiceProvider
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var product = await context.Products.FindAsync(id);

        if (product != null)
        {
            product.Description = updatedProduct.Description;
            product.Image = updatedProduct.Image;
            product.MimeType = updatedProduct.MimeType;
            product.Price = updatedProduct.Price;
            product.Name = updatedProduct.Name;
            product.Id = id;

            await context.SaveChangesAsync();
        }
    }

    public Task DeleteProductAsync(int id)
    {
        using var scope = serviceProvider.CreateScope(); // Assuming you have a way to access IServiceProvider
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var product = context.Products.FindAsync(id);
        if (product.Result != null)
        {
            context.Products.Remove(product.Result);
            context.SaveChanges();
            return Task.CompletedTask;
        }

        return Task.CompletedTask;
    }

    public async Task<ResponseData<Product>> CreateProductAsync(Product product, IFormFile? formFile)
    {
        using var scope = serviceProvider.CreateScope(); // Assuming you have a way to access IServiceProvider
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        if (product != null)
        {
            await context.Products.AddAsync(product);
            await context.SaveChangesAsync();

            var resultProduct = await context.Products.FindAsync(product.Id);
            if (resultProduct != null)
            {
                return new ResponseData<Product> { Data = resultProduct };
            }
        }

        return new ResponseData<Product> { Data = null }; // Or handle this case as needed
    }


    public Task<ResponseData<string>> SaveImageAsync(int id, IFormFile formFile)
    {
        throw new NotImplementedException();
    }
}