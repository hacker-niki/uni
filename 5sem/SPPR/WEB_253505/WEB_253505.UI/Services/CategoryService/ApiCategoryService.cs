using System.Text;
using System.Text.Json;
using WEB_253505.Domain.Entities;
using WEB_253505.Domain.Models;
using WEB_253505.UI.Services.CategoryService;

namespace WEB_253505.UI.Services
{
    public class ApiCategoryService : ICategoryService
    {
        private readonly ILogger<ApiCategoryService> _logger;
        private readonly IConfiguration _configuration;
        private readonly HttpClient _httpClient;
        
        private readonly JsonSerializerOptions _serializerOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };

        public ApiCategoryService(HttpClient httpClient, IConfiguration configuration, ILogger<ApiCategoryService> logger)
        {
            _httpClient = httpClient;
            _configuration = configuration;
            _logger = logger;
        }

        public async Task<ResponseData<List<Category>>> GetCategoryListAsync()
        {
            // Prepare the request URL
            var urlString = new StringBuilder($"{_httpClient.BaseAddress.AbsoluteUri}Categories/");
            var response = await _httpClient.GetAsync(new Uri(urlString.ToString()));

            if (response.IsSuccessStatusCode)
            {
                try
                {
                    // var jsonResponse = await response.Content.ReadAsStringAsync();
                    // Console.WriteLine(jsonResponse);
                    var result =
                        await response.Content.ReadFromJsonAsync<ResponseData<List<Category>>>(_serializerOptions);
                    return ResponseData<List<Category>>.Success( result.Data  );
                }
                catch (JsonException ex)
                {
                    _logger.LogError($"-----> Error: {ex.Message}");
                    return ResponseData<List<Category>>.Error($"Error: {ex.Message}");
                }
            }

            _logger.LogError($"-----> Данные не получены от сервера. Error: {response.StatusCode.ToString()}");
            return ResponseData<List<Category>>.Error($"Данные не получены от сервера. Error: {response.StatusCode.ToString()}");
        }
    }
}