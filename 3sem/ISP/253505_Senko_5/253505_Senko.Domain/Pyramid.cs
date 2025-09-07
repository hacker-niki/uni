namespace _253505_Senko.Domain;

public class Pyramid : IEquatable<Pyramid>
{
    public Pyramid()
    {
    }

    public Pyramid(string name)
    {
        Name = name;
        Pharaohs = new List<Pharaoh>();
    }

    public Pyramid(string name, List<Pharaoh> list)
    {
        Name = name;
        Pharaohs = list;
    }

    public string Name { get; set; }
    public List<Pharaoh> Pharaohs { get; set; }

    public void AddRunaway(Pharaoh pharaoh)
    {
        Pharaohs.Add(pharaoh);
    }

    public bool Equals(Pyramid? other)
    {
        bool ans = other.Name == Name;
        for (int i = 0; i < Pharaohs.Count; i++)
        {
            ans = ans && Pharaohs[i].Equals(other.Pharaohs[i]);
        }

        return ans;
    }

    public override string ToString()
    {
        string ans = "Name: " + Name + "\nPharaohs:\n";
        foreach (var pharaoh in Pharaohs)
        {
            ans += '\t' + pharaoh.Name + ' ' + pharaoh.YearsOld.ToString() + "yo\n";
        }

        return ans;
    }
}