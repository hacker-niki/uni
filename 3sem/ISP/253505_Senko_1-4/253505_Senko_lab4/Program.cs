using _253505_Senko_lab4.Comparers;
using _253505_Senko_lab4.Entities;
using _253505_Senko_lab4;


string lastName = "Senko";
var folderName = $"{lastName}_Lab4";
FileService fs = new FileService();

Directory.CreateDirectory(folderName);

var random = new Random();
string[] extensions = { ".txt", ".rtf", ".dat", ".inf" };

for (var i = 0; i < 10; i++)
{
    var fileName = Path.GetRandomFileName();
    var extension = extensions[random.Next(extensions.Length)];
    var filePath = Path.Combine(folderName, $"{fileName}{extension}");
    File.Create(filePath).Close();
}

string[] files = Directory.GetFiles(folderName);
foreach (string file in files)
{
    string fileName = Path.GetFileName(file);
    string extension = Path.GetExtension(file);
    Console.WriteLine($"Файл: {fileName} имеет расширение {extension}");
}

List<Superhero> employees = new List<Superhero>
{
    new Superhero() { Name = "John", Force = 15, IsDead = false },
    new Superhero() { Name = "Elton", Force = 999, IsDead = true },
    new Superhero() { Name = "John", Force = 15, IsDead = false },
    new Superhero() { Name = "AA", Force = 99, IsDead = true },
    new Superhero() { Name = "BB", Force = 15245, IsDead = false },
    new Superhero() { Name = "dfs", Force = 9435, IsDead = true },
    new Superhero() { Name = "egc", Force = 135, IsDead = false },
    new Superhero() { Name = "ans", Force = 42, IsDead = true }
};

string superheroFileName = "employees.txt";
fs.SaveData(employees, superheroFileName);

string newSuperheroFileName = "new_employees.txt";
File.Move(superheroFileName, newSuperheroFileName);

IEnumerable<Superhero> newSuperheroes = fs.ReadFile(newSuperheroFileName);

var superheroes = newSuperheroes.ToList();
List<Superhero> sortedSuperHeroes = superheroes.OrderBy(e => e, new MyCustomComparer<Superhero>()).ToList();

foreach (var superhero in superheroes)
{
    Console.WriteLine($"Name: {superhero.Name}, Force: {superhero.Force}, IsDead: {superhero.IsDead}");
}

Console.WriteLine();


foreach (var superhero in sortedSuperHeroes)
{
    Console.WriteLine($"Name: {superhero.Name}, Force: {superhero.Force}, IsDead: {superhero.IsDead}");
}


List<Superhero> sortedSuperHeroes2 = superheroes.OrderBy((Superhero s) => s.Force).ToList();

Console.WriteLine();


foreach (var superhero in sortedSuperHeroes2)
{
    Console.WriteLine($"Name: {superhero.Name}, Force: {superhero.Force}, IsDead: {superhero.IsDead}");
}

//
// File.Delete(superheroFileName);
// File.Delete(newSuperheroFileName);
// File.Delete(folderName);