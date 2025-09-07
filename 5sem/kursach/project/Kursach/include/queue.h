#pragma once

template <class T>
class Queue
{
private:
    int _front, _back, _count, _maxitems;
    T* _data;

public:
    // Конструктор
    Queue(int maxitems = 256)
        : _front(0), _back(0), _count(0), _maxitems(maxitems)
    {
        _data = new T[_maxitems];
    }

    // Деструктор
    ~Queue()
    {
        delete[] _data;
    }

    // Возвращает количество элементов в очереди
    inline int count() const
    {
        return _count;
    }

    // Возвращает индекс начала очереди
    inline int front() const
    {
        return _front;
    }

    // Возвращает индекс конца очереди
    inline int back() const
    {
        return _back;
    }

    // Добавление элемента в очередь
    void push(const T& item)
    {
        if (_count == _maxitems) // Если очередь заполнена
        {
            // Удаляем самый старый элемент (сдвигаем _front)
            _front = (_front + 1) % _maxitems;
            --_count;
        }

        _data[_back] = item; // Добавляем новый элемент в конец
        _back = (_back + 1) % _maxitems; // Сдвигаем конец очереди
        ++_count; // Увеличиваем счетчик элементов
    }

    // Возвращает элемент из начала очереди без удаления
    T peek() const
    {
        if (_count > 0)
        {
            return _data[_front];
        }
    }

    // Удаляет и возвращает элемент из начала очереди
    T pop()
    {
        if (_count > 0)
        {
            T result = _data[_front];
            _front = (_front + 1) % _maxitems;
            --_count;
            return result;
        }
    }

    // Очистка очереди
    void clear()
    {
        _front = 0;
        _back = 0;
        _count = 0;
    }

    // Итератор для очереди
    class iterator
    {
        const Queue<T>* queue;
        int current;
        int remaining; // Количество оставшихся элементов для итерации

    public:
        iterator(const Queue<T>* q, int pos, int count)
            : queue(q), current(pos), remaining(count)
        {
        }

        T operator*() const
        {
            return queue->_data[current];
        }

        iterator& operator++()
        {
            if (remaining > 0) // Если есть элементы для итерации
            {
                current = (current + 1) % queue->_maxitems;
                --remaining;
            }
            return *this;
        }

        bool operator!=(const iterator& other) const
        {
            return remaining != other.remaining;
        }
    };

    // Возвращает итератор на начало очереди
    iterator begin() const
    {
        return iterator(this, _front, _count);
    }

    // Возвращает итератор на конец очереди
    iterator end() const
    {
        return iterator(this, _back, 0); // Итерация заканчивается, когда remaining == 0
    }
};
