t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    res = []
    temp = []
    i = 0

    while i < n:
        if len(temp) == 0:
            minimun = 1
        elif len(temp) == 1:
            minimun = temp[-1]
        else:
            minimun = min(minimun, temp[-1])

        if minimun >= len(temp) + 1 and a[i] >= len(temp) + 1:
            temp.append(a[i])
            i += 1
        else:
            res.append(len(temp))
            temp = []

    res.append(len(temp))
    print(len(res))
    print(*res)