using WEB_253505.Domain.Entities;
using WEB_253505.Domain.Models;
namespace WEB_253505.UI.Services.CategoryService;

public class MemoryCategoryService : ICategoryService
{


    List<Category> _categories;
    IServiceProvider _serviceProvider;
 
    public MemoryCategoryService(IServiceProvider serviceProvider)
    {
        _categories = new List<Category>();
        _serviceProvider = serviceProvider;
        SetupData();
    }

    void SetupData()
    {
        _categories.Add(
       new Category
       {
           Name = "Категория 1",
           NormalizedName = "category1"
       });
        _categories.Add(
            new Category
            {
                Name = "Категория 2",
                NormalizedName = "category2"
            });
        _categories.Add(
            new Category
            {
                Name = "Категория 3",
                NormalizedName = "category3"
            });
    }

    public Task<ResponseData<List<Category>>> GetCategoryListAsync()
    {

        var result = ResponseData<List<Category>>.Success(_categories);
        return Task.FromResult(result);
    }

}