def find_best_unvisited(visited, dist, n):
    min_dist = 10 ** 6
    index = None
    for i in range(1, n + 1):
        if not visited[i] and dist[i] < min_dist:
            min_dist = dist[i]
            index = i
    return index


def best_way(n, s, f, graph):
    visited = [False] * (n + 1)
    dist = [10 ** 6] * (n + 1)
    parent = [-1] * (n + 1)
    dist[s] = 0
    while now := find_best_unvisited(visited, dist, n):
        visited[now] = True
        now_dst = dist[now]
        for neib_i in range(1, n + 1):
            if graph[now][neib_i] <= 0:
                continue
            if dist[neib_i] > now_dst + graph[now][neib_i]:
                dist[neib_i] = now_dst + graph[now][neib_i]
                parent[neib_i] = now
    if not visited[f]:
        return [-1]
    way = []
    now = f
    while now != s:
        way.append(now)
        now = parent[now]
    way.append(s)
    return reversed(way)

n, s, f = [int(x) for x in input().split()]
graph = [[-1] for _ in range(n + 1)]
for i in range(1, n + 1):
    graph[i].extend([int(x) for x in input().split()])

print(*best_way(n,s,f,graph))
