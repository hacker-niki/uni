using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using WEB_253505.Domain.Entities;
using WEB_253505.UI.Services.ProductService;

namespace WEB_253505.UI.Areas.Admin.Pages
{
    public class DeleteModel : PageModel
    {
        private IProductService _productService;

        public DeleteModel(IProductService productService)
        {
            _productService = productService;
        }

        [BindProperty]
        public Product Product { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var product = await _productService.GetProductByIdAsync(id??=1);

            if (product == null)
            {
                return NotFound();
            }
            else
            {
                Product = product.Data;
            }
            return Page();
        }

        public async Task<IActionResult> OnPostAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            await _productService.DeleteProductAsync(id ??= 1);

            return RedirectToPage("./Index");
        }
    }
}
