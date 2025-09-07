using System;
using System.Collections.Generic;
using System.Drawing.Printing;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using WEB_253505.API.Data;
using WEB_253505.API.Services.ProductService;
using WEB_253505.Domain.Entities;

namespace WEB_253505.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProductsController : ControllerBase
    {
        private readonly AppDbContext _context;
        private IProductService _productService;

        public ProductsController(AppDbContext context, IProductService productService)
        {
            _context = context;
            _productService = productService;
        }

        // GET: api/Products
        [HttpGet]
        [Authorize]
        public async Task<ActionResult<IEnumerable<Product>>> GetProducts(int? category, int? pageSize, int pageNo = 1)
        {
            return Ok(await _productService.GetProductListAsync(category, pageSize, pageNo));
        }

        // GET: api/Products/5
        [HttpGet("{id}")]
        [Authorize]
        public async Task<ActionResult<Product>> GetProduct(int id)
        {
            try
            {
                var product = await _productService.GetProductByIdAsync(id);
                if (product == null)
                {
                    return NotFound();
                }

                return Ok(product);
            }
            catch
            {
                return NotFound();
            }
        }

        // PUT: api/Products/5
        [HttpPut("{id}")]
        [Authorize]
        public async Task<IActionResult> PutProduct(int id, Product product)
        {
            if (id != product.Id)
            {
                return BadRequest();
            }

            try
            {
                await _productService.UpdateProductAsync(id, product, null);
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!ProductExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Products
        [HttpPost]
        [Authorize]
        public async Task<ActionResult<Product>> PostProduct(Product product)
        {
            await _productService.CreateProductAsync(product, null);
            return CreatedAtAction("GetProduct", new { id = product.Id }, product);
        }

        // DELETE: api/Products/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteProduct(int id)
        {
            var product = await _productService.GetProductByIdAsync(id);
            if (product == null)
            {
                return NotFound();
            }

            await _productService.DeleteProductAsync(id);
            return NoContent();
        }

        // GET: api/Products/pages/5
        [HttpGet("pages/{id}")]
        [Authorize]
        public int GetPagesCount(int id)
        {
            var pagesCount = _productService.PagesCount(id);

            return pagesCount.Result;
        }
        
        // GET: api/Products/pages/5
        [HttpGet("pages/")]
        [Authorize]
        public int GetPagesCount()
        {
            var pagesCount = _productService.PagesCount(null);

            return pagesCount.Result;
        }

        private bool ProductExists(int id)
        {
            return _context.Products.Any(e => e.Id == id);
        }
    }
}