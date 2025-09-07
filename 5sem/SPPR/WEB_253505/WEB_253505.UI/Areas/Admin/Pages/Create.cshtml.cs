using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using WEB_253505.Domain.Entities;
using WEB_253505.UI.Services.CategoryService;
using WEB_253505.UI.Services.ProductService;

namespace WEB_253505.UI.Areas.Admin.Pages
{
    public class CreateModel : PageModel
    {
        private IProductService _productService;
        private ICategoryService _categoryService;

        [BindProperty] public Product Product { get; set; } = default!;

        [BindProperty] public IFormFile? Image { get; set; }

        public SelectList Categories { get; set; }
        
        public CreateModel(IProductService productService, ICategoryService categoryService)
        {
            _productService = productService;
            _categoryService = categoryService;
            Categories = new SelectList(_categoryService.GetCategoryListAsync().Result.Data, "Id", "Name");
        }

        public IActionResult OnGet()
        {
            return Page();
        }
        


        // For more information, see https://aka.ms/RazorPagesCRUD.
        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            var response = await _productService.CreateProductAsync(Product, Image);
            if (!response.Successfull)
            {
                return Page();
            }

            return RedirectToPage("./Index");
        }
    }
}