n,k = map(int, input().split())

min_dist = {}
numbers = list(map(int, input().split()))
for i in range(n):
    if numbers[i] not in min_dist.keys():
        min_dist[numbers[i]] = (1e9, i)
    else:
        min_dist[numbers[i]] = (min(min_dist[numbers[i]][0], i-min_dist[numbers[i]][1]), i)

for el in min_dist.values():
    if el[0] <= k:
        print("YES")
        exit(0)

print("NO")