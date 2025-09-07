using System.ComponentModel.DataAnnotations;

namespace WEB_253505_SENKO.Blazor.SSR.Components.Models;

public class Counter
{
    [Required]
    [Range(0, 10, ErrorMessage = "Value must be between 1 and 10.")]
    public int count { get; set; }
}