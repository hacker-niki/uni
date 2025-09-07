n = int(input())
win = list(map(int, input().split()))

minimun, maxismun, dec = map(int, input().split())
min_shift = (minimun - 1) // dec
to_visit = min(n, (maxismun - 1) // dec + 1 - min_shift)


max1 = 0
for di in [-1, 1]:
    pos = di * min_shift % n
    for i in range(to_visit):
        max1 = max(max1, win[pos])
        pos = (pos + di) % n


print(max1)
