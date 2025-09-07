n = int(input())
ships = [tuple(map(int, input().split()))for _ in range(n)]
ships.sort()
ans = n**2
for col in range(1, n+1):
    now = 0
    for i in range(n):
        now += abs(ships[i][0] - (i+1)) + abs(ships[i][1]- col)
    ans = min(now ,ans)
print(ans)
