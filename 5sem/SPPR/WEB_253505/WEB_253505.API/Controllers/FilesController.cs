using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace WEB_253505.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FilesController : ControllerBase
    {
        // Путь к папке wwwroot/Images
        private readonly string _imagePath;
        public FilesController(IWebHostEnvironment webHost)
        {
            _imagePath = Path.Combine(webHost.WebRootPath, "images");
        }
        
        [HttpPost]
        [Authorize]
        public async Task<IActionResult> SaveFile(IFormFile file)
        {
            if (file is null)
            {
                return BadRequest();
            }
            // путь к сохраняемому файлу
            var filePath = Path.Combine(_imagePath, file.FileName);
            var fileInfo = new FileInfo(filePath);
            // если такой файл существует, удалить его
            if (fileInfo.Exists)
            {
                fileInfo.Delete();
            }
            // скопировать файл в поток
            using var fileStream = fileInfo.Create();
            await file.CopyToAsync(fileStream);
            // получить Url файла
            var host = HttpContext.Request.Host;
            var fileUrl = $"https://{host}/images/{file.FileName}";
            return Ok(fileUrl);
        }
        
        [HttpDelete]
        public IActionResult DeleteFile(string fileName)
        {
            if (string.IsNullOrEmpty(fileName))
            {
                return BadRequest("File name cannot be null or empty.");
            }

            // путь к файлу, который нужно удалить
            var filePath = Path.Combine(_imagePath, fileName);
            var fileInfo = new FileInfo(filePath);

            // проверить, существует ли файл
            if (!fileInfo.Exists)
            {
                return NotFound("File not found.");
            }

            // удалить файл
            fileInfo.Delete();

            return Ok("File deleted successfully.");
        }
    }
}