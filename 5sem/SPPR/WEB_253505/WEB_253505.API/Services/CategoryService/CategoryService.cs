using WEB_253505.API.Data;
using WEB_253505.Domain.Entities;
using WEB_253505.Domain.Models;

namespace WEB_253505.API.Services.CategoryService;

public class CategoryService(IServiceProvider serviceProvider) : ICategoryService
{
    List<Category> _categories = new List<Category>();
    IServiceProvider _serviceProvider = serviceProvider;

    public Task<ResponseData<List<Category>>> GetCategoryListAsync()
    {
        using var scope = _serviceProvider.CreateScope();
        var context =
            scope.ServiceProvider.GetRequiredService<AppDbContext>();
        _categories = context.Categories.ToList();
        var result = ResponseData<List<Category>>.Success(_categories);
        return Task.FromResult(result);
    }
}