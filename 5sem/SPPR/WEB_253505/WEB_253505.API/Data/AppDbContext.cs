using Microsoft.EntityFrameworkCore;
using WEB_253505.Domain.Entities;

namespace WEB_253505.API.Data
{
    public class AppDbContext(DbContextOptions<AppDbContext> options): DbContext(options)
    {
       public DbSet<Product> Products { get; set; }
       public DbSet<Category> Categories { get; set; }
    }
}
