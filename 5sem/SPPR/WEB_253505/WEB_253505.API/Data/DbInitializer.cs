using Microsoft.EntityFrameworkCore;
using WEB_253505.Domain.Entities;

namespace WEB_253505.API.Data
{
    public class DbInitializer
    {
        public static async Task SeedData(WebApplication app)
        {
            using var scope = app.Services.CreateScope();
            var context =
                scope.ServiceProvider.GetRequiredService<AppDbContext>();

            await context.Database.EnsureCreatedAsync();
            
            // Выполнение миграций
            await context.Database.MigrateAsync();
            
            string imegeUrl = app.Configuration.GetSection("ImageUrl").Get<string>();

            await context.SaveChangesAsync();

           
            if (!context.Categories.Any())
            {
                context.Categories.Add(
                    new Category
                    {
                        Name = "Категория 1",
                        NormalizedName = "category1"
                    });
                context.Categories.Add(
                    new Category
                    {
                        Name = "Категория 2",
                        NormalizedName = "category2"
                    });
                context.Categories.Add(
                    new Category
                    {
                        Name = "Категория 3",
                        NormalizedName = "category3"
                    });

                await context.SaveChangesAsync();
            }

            if (!context.Products.Any())
            {
                context.Products.Add(new Product
                {
                    Name = "Product 1",
                    Description = "Description 1",
                    CategoryId = 1,
                    Price = 100,
                    Image = imegeUrl + "/1.png",
                    MimeType = "image/png"
                });
                context.Products.Add(new Product
                {
                    Name = "Product 2",
                    Description = "Description 2",
                    CategoryId = 1,
                    Price = 200,
                    Image = imegeUrl+"/2.png",
                    MimeType = "image/png"
                });
                context.Products.Add(new Product
                {
                    Name = "Product 3",
                    Description = "Description 3",
                    CategoryId = 2,
                    Price = 20,
                    Image = imegeUrl+"/3.png",
                    MimeType = "image/png"
                });
                context.Products.Add(new Product
                {
                    Name = "Product 4",
                    Description = "Description 4",
                    CategoryId = 1,
                    Price = 150,
                    Image = imegeUrl+"/4.png",
                    MimeType = "image/png"
                });
                context.Products.Add(new Product
                {
                    Name = "Product 5",
                    Description = "Description 5",
                    CategoryId = 1,
                    Price = 150,
                    Image = imegeUrl+"/5.jpg",
                    MimeType = "image/jpg"
                });
                context.Products.Add(new Product
                {
                    Name = "Product 6",
                    Description = "Description 6",
                    CategoryId = 1,
                    Price = 600,
                    Image = imegeUrl+"/1.png",
                    MimeType = "image/png"
                });
                context.Products.Add(new Product
                {
                    Name = "Product 7",
                    Description = "Description 7",
                    CategoryId = 1,
                    Price = 700,
                    Image = imegeUrl+"/2.png",
                    MimeType = "image/png"
                });
                context.Products.Add(new Product
                {
                    Name = "Product 8",
                    Description = "Description 8",
                    CategoryId = 2,
                    Price = 20,
                    Image = imegeUrl+"/3.png",
                    MimeType = "image/png"
                });
                context.Products.Add(new Product
                {
                    Name = "Product 9",
                    Description = "Description 9",
                    CategoryId = 1,
                    Price = 150,
                    Image = imegeUrl+"/4.png",
                    MimeType = "image/png"
                });
                context.Products.Add(new Product
                {
                    Name = "Product 10",
                    Description = "Description 10",
                    CategoryId = 1,
                    Price = 1100,
                    Image = "images/5.jpg",
                    MimeType = "image/jpg"
                });

                await context.SaveChangesAsync();
            }
        }
    }
}
