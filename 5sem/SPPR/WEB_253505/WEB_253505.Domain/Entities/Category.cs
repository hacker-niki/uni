namespace WEB_253505.Domain.Entities;

public class Category
{
    public int Id { get; set; }
    public string Name { get; set; }
    
    public string? Description { get; set; }
    public string NormalizedName { get; set; }
}