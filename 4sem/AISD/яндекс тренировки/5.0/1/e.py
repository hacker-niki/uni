def main():
    n, k, d = [int(el) for el in input().split()]
    arr = []
    res = -1
    for num in range(10):
        if int(str(n) + str(num)) % k == 0:
            res = int(str(n) + str(num))

    if res == -1:
        print(-1)
    else:
        print(str(res) + '0' * (d - 1))


main()