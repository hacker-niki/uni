using WEB_253505.UI.Services.ProductService;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using WEB_253505.Domain.Entities;

namespace WEB_253505.UI.Areas.Admin.Pages
{
    public class DetailsModel : PageModel
    {
        private IProductService _productService;

        public DetailsModel(IProductService productService)
        {
            _productService = productService;
        }

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
    }
}
