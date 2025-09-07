using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using WEB_253505.Domain.Entities;
using WEB_253505.UI.Data;
using WEB_253505.UI.Services.ProductService;

namespace WEB_253505.UI.Areas.Admin.Pages
{
    public class IndexModel : PageModel
    {
        private IProductService _productService;

        public IndexModel(IProductService productService)
        {
            _productService = productService;
        }


        public IList<Product> Product { get;set; } = default!;

        public async Task OnGetAsync()
        {
            List<Product> result = new();
            var tmp1 = _productService.PagesCount(null).Result;
            for (int i = 0; i < _productService.PagesCount(null).Result; i++)
            {
                var tmp = await _productService.GetProductListAsync(null, i + 1);
                if (tmp != null)
                {
                    result.AddRange(tmp.Data.Items);
                }
            }
            Product = result;
        }
    }
}
