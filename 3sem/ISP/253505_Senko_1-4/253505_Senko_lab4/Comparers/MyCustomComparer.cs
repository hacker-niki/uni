namespace _253505_Senko_lab4.Comparers
{
    public class MyCustomComparer<T> : IComparer<T> where T : Superhero
    {
        public int Compare(T? x, T? y)
        {
            return String.CompareOrdinal(x?.Name, y?.Name);
        }
    }
}