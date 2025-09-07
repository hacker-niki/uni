using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using System.Diagnostics;
using WEB_253505.UI.Models;

namespace WEB_253505.UI.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            var labViewModel = new LabViewModel(1);
            ViewData["Laboratory"] = "Лабораторная работа 2";

            SelectList selectList = new SelectList(new List<ListDemo>()
        {
            new ListDemo() { Id = 1, Name = "11111" },
            new ListDemo() { Id = 2, Name = "22222" },
            new ListDemo() { Id = 3, Name = "33333" },
        }, "Id", "Name", labViewModel.SelectedId);

            ViewBag.selectList = selectList;
            return View(labViewModel);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
