using System.Reflection;
using _253505_Senko_6;

List<Employee> le = new List<Employee>()
{
    new() { age = 42, fired = false, Name = "Jon" },
    new() { age = 24, fired = false, Name = "Dave" },
    new() { age = 18, fired = true, Name = "Ivan" },
    new() { age = 111, fired = true, Name = "Mike" },
    new() { age = 13, fired = false, Name = "indian child" },
    new() { age = 90, fired = true, Name = "Kevin" }
};

string fileName = "file.json";

Assembly asm = Assembly.LoadFrom("ClassLibrary.dll");

Type? type = asm.GetType("ClassLibrary.FileService");

var fileService = Activator.CreateInstance(type!) as IFileService<Employee>;

fileService?.SaveData(le, fileName);
var list = fileService?.ReadFile(fileName);

foreach (var employee in list)
{
    Console.WriteLine($"{employee.age} {employee.Name} {employee.fired}");
}