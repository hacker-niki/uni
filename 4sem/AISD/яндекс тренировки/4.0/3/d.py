import heapq

def find_shortest_time(graph, start, finish, n):
    visited = [False] * (n + 1)
    times = [float('inf')] * (n + 1)
    times[start] = 0
    unhandled = []
    heapq.heappush(unhandled, (0, start))
    while unhandled:
        current_time, current_node = heapq.heappop(unhandled)
        if not visited[current_node]:
            visited[current_node] = True
            for bus in graph[current_node]:
                if bus['time_go'] >= times[current_node]:
                    if bus['time_finish'] < times[bus['finish']]:
                        times[bus['finish']] = bus['time_finish']
                        heapq.heappush(unhandled, (times[bus['finish']], bus['finish']))
    return times[finish] if times[finish] != float('inf') else -1


n = int(input())
d, v = map(int, input().split())
r = int(input())
graph = [[] for _ in range(n + 1)]
for _ in range(r):
    V_start, time_go, V_finish, time_finish = map(int, input().split())
    bus = {'start': V_start, 'time_go': time_go, 'finish': V_finish, 'time_finish': time_finish}
    graph[V_start].append(bus)
print(find_shortest_time(graph, d, v, n))