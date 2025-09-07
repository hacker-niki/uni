using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Text;
using System.Text.Json;
using WEB_253505.Domain.Entities;
using WEB_253505.Domain.Models;
using WEB_253505.UI.Services.CategoryService;
using WEB_253505.UI.Services.FileService;
using MimeMapping;
using WEB_253505.UI.Services.Authentication;

namespace WEB_253505.UI.Services.ProductService;

public class ApiProductService(
    HttpClient httpClient,
    IConfiguration configuration,
    ILogger<ApiProductService> logger,
    ICategoryService categoryService,
    IFileService fileService,
    ITokenAccessor tokenAccessor)
    : IProductService
{
    ICategoryService _categoryService = categoryService;
    HttpClient _httpClient = httpClient;
    IFileService _fileService = fileService;
    private ITokenAccessor _tokenAccessor = tokenAccessor;
    int _pageSize = Convert.ToInt32(configuration.GetSection("PageSize").Value);

    JsonSerializerOptions _serializerOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    ILogger<ApiProductService> _logger = logger;

    public async Task<int> PagesCount(int? categoryId)
    {
        // Prepare the URL for the request
        var urlString = new StringBuilder($"{_httpClient.BaseAddress.AbsoluteUri}Products/pages/");

        await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);
        var response = await _httpClient.GetAsync(new Uri(urlString.Append($"{categoryId}").ToString()));

        if (response.IsSuccessStatusCode)
        {
            try
            {
                // Read the content as a string
                var contentString = await response.Content.ReadAsStringAsync();

                // Assuming Swagger shows a simple integer (e.g., "3") in the response body
                if (int.TryParse(contentString, out int pages))
                {
                    return pages; // Return the integer value from the response
                }
                else
                {
                    _logger.LogError("Failed to parse the response content as an integer.");
                    return 0; // Or handle this case appropriately
                }
            }
            catch (JsonException ex)
            {
                _logger.LogError($"JSON Error: {ex.Message}");
                return 0;
            }
        }

        _logger.LogError("Failed to retrieve the data. Status code: " + response.StatusCode);
        return 0;
    }

    public async Task<ResponseData<ListModel<Product>>> GetProductListAsync(int? categoryId,
        int pageNo = 1)
    {
        // Prepare the URL for the request

        var urlString = new StringBuilder($"{_httpClient.BaseAddress.AbsoluteUri}Products?");
        if (categoryId != null)
            urlString.Append($"category={categoryId}&");
        if (pageNo > 0)
            urlString.Append($"pageNo={pageNo}");
        urlString.Append($"&pageSize={_pageSize}");

        // Send request to the API
        await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);
        var response = await _httpClient.GetAsync(new Uri(urlString.ToString()));

        if (response.IsSuccessStatusCode)
        {
            try
            {
                var result =
                    await response.Content.ReadFromJsonAsync<ResponseData<ListModel<Product>>>(_serializerOptions);
                return result;
            }
            catch (JsonException ex)
            {
                _logger.LogError($"JSON Error: {ex.Message}");
                return ResponseData<ListModel<Product>>.Error($"JSON Error: {ex.Message}");
            }
        }

        // Handle specific status codes
        string errorMessage;
        switch (response.StatusCode)
        {
            case System.Net.HttpStatusCode.NotFound:
                errorMessage = "Продукты не найдены.";
                break;
            case System.Net.HttpStatusCode.BadRequest:
                errorMessage = "Неверный запрос.";
                break;
            default:
                errorMessage = $"Ошибка: {response.StatusCode}";
                break;
        }

        _logger.LogError($"Error fetching data from server. Status: {response.StatusCode}");
        return ResponseData<ListModel<Product>>.Error(errorMessage);
    }


    public async Task<ResponseData<Product>> GetProductByIdAsync(int id)
    {
        var urlString = new StringBuilder($"{_httpClient.BaseAddress.AbsoluteUri}Products/");
        urlString.Append($"{id}");

        // Send request to the API
        await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);
        var response = await _httpClient.GetAsync(new Uri(urlString.ToString()));

        if (response.IsSuccessStatusCode)
        {
            try
            {
                var result =
                    await response.Content.ReadFromJsonAsync<ResponseData<Product>>(_serializerOptions);
                return result;
            }
            catch (JsonException ex)
            {
                _logger.LogError($"JSON Error: {ex.Message}");
                return ResponseData<Product>.Error($"JSON Error: {ex.Message}");
            }
        }

        // Handle specific status codes
        string errorMessage;
        switch (response.StatusCode)
        {
            case System.Net.HttpStatusCode.NotFound:
                errorMessage = "Продукты не найдены.";
                break;
            case System.Net.HttpStatusCode.BadRequest:
                errorMessage = "Неверный запрос.";
                break;
            default:
                errorMessage = $"Ошибка: {response.StatusCode}";
                break;
        }

        _logger.LogError($"Error fetching data from server. Status: {response.StatusCode}");
        return ResponseData<Product>.Error(errorMessage);
    }

    public async Task UpdateProductAsync(int id, Product product, IFormFile? formFile)
    {
        // Первоначально использовать картинку по умолчанию
        product.Image ??= "images/noimage.jpg";
        // Сохранить файл изображения
        if (formFile != null)
        {
            var imageUrl = await _fileService.SaveFileAsync(formFile);
            // Добавить в объект Url изображения
            if (!string.IsNullOrEmpty(imageUrl))
                product.Image = imageUrl;
        }

        product.MimeType = MimeMapping.MimeUtility.GetMimeMapping(product.Image);

        var urlString = new StringBuilder($"{_httpClient.BaseAddress.AbsoluteUri}Products/{product.Id}");
        
        // Send request to the API
        await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);
        var response = await _httpClient.PutAsJsonAsync(new Uri(urlString.ToString()), product, _serializerOptions);

        if (response.IsSuccessStatusCode)
        {
            try
            {
                var data = await response
                    .Content
                    .ReadFromJsonAsync<ResponseData<Product>>(_serializerOptions);
                return;
            }
            catch (JsonException ex)
            {
                _logger.LogError($"JSON Error: {ex.Message}");
            }
        }

        return;
    }

    public async Task DeleteProductAsync(int id)
    {
        var urlString = new StringBuilder($"{_httpClient.BaseAddress.AbsoluteUri}Products/");
        urlString.Append($"{id}");
        
        // Send request to the API
        await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);
        var response = await _httpClient.DeleteAsync(new Uri(urlString.ToString()));

        // Handle specific status codes
        string errorMessage;
        switch (response.StatusCode)
        {
            case System.Net.HttpStatusCode.NotFound:
                errorMessage = "Продукты не найдены.";
                break;
            case System.Net.HttpStatusCode.BadRequest:
                errorMessage = "Неверный запрос.";
                break;
            default:
                errorMessage = $"Ошибка: {response.StatusCode}";
                break;
        }

        _logger.LogError($"Error fetching data from server. Status: {response.StatusCode}");
    }

    public async Task<ResponseData<Product>> CreateProductAsync(Product product, IFormFile? formFile)
    {
        // Первоначально использовать картинку по умолчанию
        product.Image = "images/noimage.jpg";
        // Сохранить файл изображения
        if (formFile != null)
        {
            var imageUrl = await _fileService.SaveFileAsync(formFile);
            // Добавить в объект Url изображения
            if (!string.IsNullOrEmpty(imageUrl))
                product.Image = imageUrl;
        }

        product.MimeType = MimeMapping.MimeUtility.GetMimeMapping(product.Image);
        // product.Category = _categoryService.GetCategoryListAsync().Result.Data
        //     .FirstOrDefault(x => x.Id == product.CategoryId);
        var urlString = new StringBuilder($"{_httpClient.BaseAddress.AbsoluteUri}Products");
        
        // Send request to the API
        await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);
        var response = await _httpClient.PostAsJsonAsync(new Uri(urlString.ToString()), product, _serializerOptions);

        if (response.IsSuccessStatusCode)
        {
            try
            {
                var data = await response
                    .Content
                    .ReadFromJsonAsync<ResponseData<Product>>(_serializerOptions);
                return data;
            }
            catch (JsonException ex)
            {
                _logger.LogError($"JSON Error: {ex.Message}");
            }
        }

        return ResponseData<Product>.Error($"Error");
    }
}