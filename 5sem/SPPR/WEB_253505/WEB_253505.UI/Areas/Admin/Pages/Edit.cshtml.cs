using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using WEB_253505.Domain.Entities;
using WEB_253505.UI.Services.CategoryService;
using WEB_253505.UI.Services.ProductService;

namespace WEB_253505.UI.Areas.Admin.Pages
{
    public class EditModel : PageModel
    {
        private IProductService _productService;
        private ICategoryService _categoryService;

        public EditModel(IProductService productService, ICategoryService categoryService)
        {
            _productService = productService;
            _categoryService = categoryService;
            Categories = new SelectList(_categoryService.GetCategoryListAsync().Result.Data, "Id", "Name");
        }

        [BindProperty] public Product Product { get; set; } = default!;

        [BindProperty] public IFormFile? Image { get; set; }
        
        public SelectList Categories { get; set; }

        public async Task<IActionResult> OnGetAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var product = await _productService.GetProductByIdAsync(id ??= 1);
            if (product == null)
            {
                return NotFound();
            }

            Product = product.Data;
            return Page();
        }

        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more information, see https://aka.ms/RazorPagesCRUD.
        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            await _productService.UpdateProductAsync(Product.Id, Product, Image);

            return RedirectToPage("./Index");
        }

        private bool ProductExists(int id)
        {
            return _productService.GetProductByIdAsync(id) != null;
        }
    }
}