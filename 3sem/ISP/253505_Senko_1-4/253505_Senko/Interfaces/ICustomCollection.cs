namespace _253505_Senko.Interfaces;

public interface ICustomCollection<T>
{
    T this[int index] { get; set; }
    void Reset();
    bool MoveNext();
    T Current { get; }
    int Count { get; }
    void Add(T item);
    void Remove(T item);
    T RemoveCurrent();
}