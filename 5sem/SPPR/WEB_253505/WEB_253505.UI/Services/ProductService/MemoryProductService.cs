using WEB_253505.Domain.Entities;
using WEB_253505.Domain.Models;
using WEB_253505.UI.Services.CategoryService;

namespace WEB_253505.UI.Services.ProductService;

public class MemoryProductService    : IProductService
{
    List<Product> _products = new List<Product>();

    ICategoryService _categoryService;
    IServiceProvider _serviceProvider;
    IConfiguration _configuration;

    public MemoryProductService(IConfiguration config,
    ICategoryService categoryService,
    IServiceProvider serviceProvider)
    {   
        _categoryService = categoryService;
        _serviceProvider = serviceProvider;
        _configuration = config;
        SetupData();
    }

    private void SetupData()
    {
        _products.Add(new Product
        {
            Id = 1,
            Name = "Product 1",
            Description = "Description 1",
            CategoryId = 1,
            Price = 100,
            Image = "images/1.png",
            MimeType = "image/png"
        });
        _products.Add(new Product
        {
            Id = 2,
            Name = "Product 2",
            Description = "Description 2",
            CategoryId = 1,
            Price = 200,
            Image = "images/2.png",
            MimeType = "image/png"
        });
        _products.Add(new Product
        {
            Id = 3,
            Name = "Product 3",
            Description = "Description 3",
            CategoryId = 2,
            Price = 20,
            Image = "images/3.png",
            MimeType = "image/png"
        });
        _products.Add(new Product
        {
            Id = 4,
            Name = "Product 4",
            Description = "Description 4",
            CategoryId = 1,
            Price = 150,
            Image = "images/4.png",
            MimeType = "image/png"
        });
        _products.Add(new Product
        {
            Id = 5,
            Name = "Product 5",
            Description = "Description 5",
            CategoryId = 1,
            Price = 150,
            Image = "images/5.jpg",
            MimeType = "image/jpg"
        });
        _products.Add(new Product
        {
            Id = 6,
            Name = "Product 6",
            Description = "Description 6",
            CategoryId = 1,
            Price = 600,
            Image = "images/1.png",
            MimeType = "image/png"
        });
        _products.Add(new Product
        {
            Id = 7,
            Name = "Product 7",
            Description = "Description 7",
            CategoryId = 1,
            Price = 700,
            Image = "images/2.png",
            MimeType = "image/png"
        });
        _products.Add(new Product
        {
            Id = 8,
            Name = "Product 8",
            Description = "Description 8",
            CategoryId = 2,
            Price = 20,
            Image = "images/3.png",
            MimeType = "image/png"
        });
        _products.Add(new Product
        {
            Id = 9,
            Name = "Product 9",
            Description = "Description 9",
            CategoryId = 1,
            Price = 150,
            Image = "images/4.png",
            MimeType = "image/png"
        });
        _products.Add(new Product
        {
            Id = 10,
            Name = "Product 10",
            Description = "Description 10",
            CategoryId = 1,
            Price = 1100,
            Image = "images/5.jpg",
            MimeType = "image/jpg"
        });
    }

    public Task<int> PagesCount(int? categoryId)
    {
        return Task.FromResult(3);
    }

    public Task<ResponseData<ListModel<Product>>> GetProductListAsync(int? categoryId, int pageNo = 1)
    {
        var pageSize = _configuration.GetValue<int>("PageSize");
        //Console.WriteLine(pageSize);
        int itemsToSkip = (pageNo - 1) * pageSize;
        
        var category = _categoryService.GetCategoryListAsync().Result.Data.First(c => c.Id == categoryId);

        // Вернуть список продуктов (пока со статическими данными)
        var products = _products.Where(p => p.CategoryId == category.Id)
            .Skip(itemsToSkip)
            .Take(pageSize)
            .ToList();
        //Console.WriteLine(products[0].Name);
        return Task.FromResult(new ResponseData<ListModel<Product>>
        { Data = new ListModel<Product> { Items = products as List<Product> } });
    }

    public Task<ResponseData<Product>> GetProductByIdAsync(int Id)
    {
        throw new NotImplementedException();
    }

    public Task UpdateProductAsync(int Id, Product product, IFormFile? formFile)
    {
        throw new NotImplementedException();
    }

    public Task DeleteProductAsync(int Id)
    {
        throw new NotImplementedException();
    }

    public Task<ResponseData<Product>> CreateProductAsync(Product product, IFormFile? formFile)
    {
        throw new NotImplementedException();
    }
}