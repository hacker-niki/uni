using System.Collections;
using _253505_Senko.Interfaces;

namespace _253505_Senko.Collections;

public class MyCustomCollection<T> : ICustomCollection<T>, IEnumerable<T>, IEnumerator<T>
{
    private class CollectionObject
    {
        public T? Data { get; set; }
        public CollectionObject? NextObject;
    }

    private CollectionObject? _firstObject;
    private CollectionObject? _currentObject;

    public T this[int index]
    {
        get
        {
            var currentObject = _firstObject;
            while (currentObject != null && index > 0)
            {
                index--;
                currentObject = currentObject.NextObject;
            }

            if (currentObject != null)
                return currentObject.Data;
            throw new IndexOutOfRangeException();
        }
        set
        {
            var currentObject = _firstObject;
            while (currentObject != null && index > 0)
            {
                index--;
                currentObject = currentObject.NextObject;
            }

            if (currentObject != null)
                currentObject.Data = value;
            else
                throw new IndexOutOfRangeException();
        }
    }

    public void Reset()
    {
        _currentObject = null;
    }

    object IEnumerator.Current => Current;

    public bool MoveNext()
    {
        if (_currentObject != null)
        {
            var hasNext = _currentObject.NextObject != null;
            _currentObject = _currentObject.NextObject;
            return hasNext;
        }
        if (_firstObject != null)
        {
            _currentObject = _firstObject;
            return true;
        }

        return false;
    }

    public T Current
    {
        get
        {
            if (_currentObject != null)
                return _currentObject.Data;
            throw new InvalidOperationException("No current object.");
        }
        private set => Current = value;
    }

    public int Count { get; private set; }

    public void Add(T item)
    {
        if (_firstObject == null)
        {
            _firstObject = new CollectionObject
            {
                Data = item
            };
        }
        else
        {
            var currentObject = _firstObject;
            while (currentObject.NextObject != null)
            {
                currentObject = currentObject.NextObject;
            }

            currentObject.NextObject = new CollectionObject
            {
                Data = item
            };
        }

        Count++;
    }

    public void Remove(T item)
    {
        if (_firstObject != null && _firstObject.Data.Equals(item))
        {
            _firstObject = _firstObject.NextObject;
            Count--;
            return;
        }

        var currentObject = _firstObject;
        while (currentObject != null && currentObject.NextObject != null)
        {
            if (currentObject.NextObject.Data.Equals(item))
            {
                currentObject.NextObject = currentObject.NextObject.NextObject;
                Count--;
                return;
            }
            currentObject = currentObject.NextObject;
        }
        throw new Exception("No object in collection.");
    }

    public T RemoveCurrent()
    {
        if (_currentObject == null)
            throw new Exception("No current object.");

        var currentObject = _firstObject;
        if (currentObject == _currentObject)
        {
            _firstObject = currentObject.NextObject;
            _currentObject = _firstObject;
        }
        else
        {
            while (currentObject != null && currentObject.NextObject != _currentObject)
            {
                currentObject = currentObject.NextObject;
            }

            if (currentObject != null)
            {
                currentObject.NextObject = currentObject.NextObject?.NextObject;
                _currentObject = currentObject.NextObject;
            }
            else
            {
                throw new Exception("No current object.");
            }
        }

        Count--;
        return currentObject.Data;
    }

    public IEnumerator<T> GetEnumerator()
    {
        return this;
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }

    public void Dispose()
    {
    }
}