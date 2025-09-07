using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using WEB_253505.API.Data;
using WEB_253505.API.Extensions;
using WEB_253505.API.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

var authServer = builder.Configuration
    .GetSection("AuthServer")
    .Get<AuthServerData>();
// Добавить сервис аутентификации
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(JwtBearerDefaults.AuthenticationScheme, o =>
    {
        // Адрес метаданных конфигурации OpenID
        o.MetadataAddress = $"{authServer.Host}/realms/{authServer.Realm}/.well-known/openid-configuration";
        // Authority сервера аутентификации
        o.Authority = $"{authServer.Host}/realms/{authServer.Realm}";
        // Audience для токена JWT
        o.Audience = "account";
        // Запретить HTTPS для использования локальной версии Keycloak
        // В рабочем проекте должно быть true
        o.RequireHttpsMetadata = false;
    });
builder.Services.AddAuthorization(opt => { opt.AddPolicy("admin", p => p.RequireRole("POWER-USER")); });

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("Default")));
builder.RegisterCustomServices();

builder.Services.AddCors(opts => opts.AddDefaultPolicy(bld => // <-- added this
{
    bld
        .AllowAnyOrigin()
        .AllowAnyMethod()
        .AllowAnyHeader()
        .WithExposedHeaders("*")
        ;
}));


var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseCors();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

await DbInitializer.SeedData(app);

app.Run();