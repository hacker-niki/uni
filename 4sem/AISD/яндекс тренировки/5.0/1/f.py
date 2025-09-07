def main():
    n = int(input())
    arr = [int(el) for el in input().split()]
    i1 = -1
    res = ""
    for i in range(n):
        if arr[i] % 2 == 0:
            res += '+'
        else:
            i1 = i
            break
    for i in range(i1, n):
        if arr[i] % 2 == 1:
            res += 'x'
        else:
            res = res[:-1]
            i1 = i
            break
    else:
        res = res[:-1]
        print(res)
        return

    res += '+'
    res += 'x' * (n - i1 - 1)

    print(res)


main()