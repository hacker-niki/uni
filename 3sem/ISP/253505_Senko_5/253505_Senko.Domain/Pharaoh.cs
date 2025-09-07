namespace _253505_Senko.Domain;

public class Pharaoh : IEquatable<Pharaoh>
{
    public Pharaoh()
    {
    }

    public Pharaoh(int yearsOld, string name)
    {
        YearsOld = yearsOld;
        Name = name;
    }

    public int YearsOld { get; set; }
    public string Name { get; set; }

    public bool Equals(Pharaoh? other)
    {
        return other.YearsOld == YearsOld && other.Name == Name;
    }
}