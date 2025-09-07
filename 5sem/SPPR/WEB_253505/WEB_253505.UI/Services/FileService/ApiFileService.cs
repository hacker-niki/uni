using Microsoft.AspNetCore.Http;
using System.Net.Http;
using System.Text;
using WEB_253505.UI.Services.Authentication;

namespace WEB_253505.UI.Services.FileService
{
    public class ApiFileService : IFileService
    {
        private readonly HttpClient _httpClient;
        private ITokenAccessor _tokenAccessor;

        public ApiFileService(HttpClient httpClient, ITokenAccessor tokenAccessor)
        {
            _httpClient = httpClient;
            _tokenAccessor = tokenAccessor;
        }

        public async Task DeleteFileAsync(string fileUri)
        {
            // Создать объект запроса
            var request = new HttpRequestMessage
            {
                Method = HttpMethod.Delete,
                RequestUri = new Uri(fileUri)
            };

            // Отправить запрос к API
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);
            var response = await _httpClient.SendAsync(request);

            // Файл успешно удален
            Console.WriteLine(response.IsSuccessStatusCode
                ? "File deleted successfully."
                // Обработка ошибки, если файл не был удален
                : $"Error deleting file: {response.StatusCode}");
        }

        public async Task<string> SaveFileAsync(IFormFile formFile)
        {
            var urlString = new StringBuilder($"{_httpClient.BaseAddress.AbsoluteUri}Files");
            // Создать объект запроса
            var request = new HttpRequestMessage
            {
                Method = HttpMethod.Post,
                RequestUri = new Uri(urlString.ToString())
            };
            // Сформировать случайное имя файла, сохранив расширение
            var extension = Path.GetExtension(formFile.FileName);
            var newName = Path.ChangeExtension(Path.GetRandomFileName(), extension);
            // Создать контент, содержащий поток загруженного файла
            var content = new MultipartFormDataContent();
            var streamContent = new StreamContent(formFile.OpenReadStream());
            content.Add(streamContent, "file", newName);
            // Поместить контент в запрос
            request.Content = content;
            
            // Отправить запрос к API
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);
            var response = await _httpClient.SendAsync(request);
            if (response.IsSuccessStatusCode)
            {
                // Вернуть полученный Url сохраненного файла
                return await response.Content.ReadAsStringAsync();
            }

            return String.Empty;
        }
    }
}