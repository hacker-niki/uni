using Classes;

namespace _253505_Senko_lab8;

class Program
{
    public static async Task Main(string[] args)
    {
        const int weaponsCount = 10;
        const int charactersCount = 1000;

        var characters = new List<Character>();
        var weapons = new List<Weapon>();

        var rnd = new Random();

        for (int i = 0; i < weaponsCount; i++)
        {
            var weapon = new Weapon($"Weapon {i}");
            weapons.Add(weapon);
        }

        for (int i = 0; i < charactersCount; i++)
        {
            var cWeapon = weapons[rnd.Next(weaponsCount - 1)];
            var character = new Character($"Car {i}", cWeapon);
            character.Name = $"Character {i} with {cWeapon.Name}";
            characters.Add(character);
        }

        var progress = new Progress<string>(str => Console.Write($"\r{str}"));

        StreamService<Character> streamService = new StreamService<Character>(new SemaphoreSlim(1));

        MemoryStream memoryStream = new MemoryStream();

        streamService.WriteToStreamAsync(memoryStream, characters, progress);
        streamService.CopyFromStreamAsync(memoryStream, "buffer.json", progress);

        Console.WriteLine(await streamService.GetStatisticsAsync("buffer.json",
            (Character сharacter) => сharacter.weapon.Id == 5));
    }
}