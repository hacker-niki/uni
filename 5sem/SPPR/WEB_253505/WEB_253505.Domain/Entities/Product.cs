namespace WEB_253505.Domain.Entities;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public Category? Category { get; set; }
    public int? CategoryId { get; set; }
    public int Price { get; set; }
    public string? Image { get; set; }
    public string? MimeType { get; set; }
}