using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Components.WebAssembly.Authentication;
using Microsoft.AspNetCore.Http;
using WEB_253505.Domain.Entities;
using WEB_253505.Domain.Models;

namespace WEB_253505.BlazorWasm.Services;

internal class DataService : IDataService
{
    private readonly HttpClient _httpClient;
    private readonly JsonSerializerOptions _jsonSerializerOptions;
    private readonly IAccessTokenProvider _accessTokenProvider;
    private readonly string _pageSize = "3";

    public DataService(HttpClient httpClient, IConfiguration configuration, IAccessTokenProvider accessTokenProvider)
    {
        _httpClient = httpClient;
        _pageSize = configuration.GetSection("ItemsPerPage").Value;
        _jsonSerializerOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };
        _accessTokenProvider = accessTokenProvider;
    }

    public List<Category> Categories { get; set; }
    public List<Product> Products { get; set; }
    public bool Success { get; set; }
    public string ErrorMessage { get; set; }
    public int TotalPages { get; set; }
    public int CurrentPage { get; set; }
    public Category? SelectedCategory { get; set; } = null;

    public event Action DataLoaded;

    public async Task GetCategoryListAsync()
    {
        var urlString = $"{_httpClient.BaseAddress.AbsoluteUri}Categories";
        try
        {
            var response = await _httpClient.GetAsync(new Uri(urlString));
            if (!response.IsSuccessStatusCode)
            {
                Success = false;
                ErrorMessage = $"Error occured in fetching data: {response.StatusCode.ToString()}";
            }

            var data = await response.Content.ReadFromJsonAsync<ResponseData<List<Category>>>(_jsonSerializerOptions);

            if (!data.Successfull)
            {
                Success = false;
                ErrorMessage = data.ErrorMessage;
            }

            Success = true;
            Categories = data.Data;
            DataLoaded.Invoke();
        }
        catch (Exception ex)
        {
            Success = false;
            ErrorMessage = $"Error occured in http client: {ex.Message}";
        }
    }

    public async Task GetProductListAsync(int pageNo = 1)
    {
        var tokenRequest = await _accessTokenProvider.RequestAccessToken();
        if (tokenRequest.TryGetToken(out var accessToken))
        {
            _httpClient.DefaultRequestHeaders.Authorization =
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken.Value);
        }

        try
        {
            var urlString = new StringBuilder($"{_httpClient.BaseAddress.AbsoluteUri}Products?");
            if (SelectedCategory?.Id != null)
                urlString.Append($"category={SelectedCategory?.Id}&");
            if (pageNo > 0)
                urlString.Append($"pageNo={pageNo}");
            urlString.Append($"&pageSize={_pageSize}");

            var response = await _httpClient.GetAsync(new Uri(urlString.ToString()));

            if (response.IsSuccessStatusCode)
            {
                var result =
                    await response.Content.ReadFromJsonAsync<ResponseData<ListModel<Product>>>(_jsonSerializerOptions);
                Success = true;
                Products = result.Data.Items;
                CurrentPage = result.Data.CurrentPage;
                TotalPages = result.Data.TotalPages;
                DataLoaded.Invoke();
            }
        }
        catch (Exception ex)
        {
            Success = false;
            ErrorMessage = $"Error occured in http client: {ex.Message}";
        }
    }
}