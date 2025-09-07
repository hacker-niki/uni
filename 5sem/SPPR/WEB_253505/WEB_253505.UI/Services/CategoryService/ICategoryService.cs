using WEB_253505.Domain.Entities;
using WEB_253505.Domain.Models;

namespace WEB_253505.UI.Services.CategoryService;

public interface ICategoryService
{
    /// <summary>
    /// Получение списка всех категорий
    /// </summary>
    /// <returns></returns>
    public Task<ResponseData<List<Category>>> GetCategoryListAsync();
}