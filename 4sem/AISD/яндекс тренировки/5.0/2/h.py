def solve_hv(g):
    maximun = -1
    maximum_i = -1
    for i in range(len(g)):
        x = max(g[i])
        if x > maximun:
            maximun = x
            maximum_i = i
    rm_i =  maximum_i
    g[rm_i] = [0] * len(g[rm_i])
    maximun = -1
    maximum_j = -1

    for i in range(len(g)):
        x = max(g[i])
        if x > maximun:
            maximun = x
            maximum_j = g[i].index(x)
    rm_j= maximum_j
    for i in range(len(g)):
        g[i][rm_j] = 0

    maximun = -1
    for i in range(len(g)):
        x = max(g[i])
        if x > maximun:
            maximun = x

    return (maximun, (rm_i, rm_j))


def solve_vh(g):
    maximum = -1
    maximum_j = -1
    for i in range(len(g)):
        x = max(g[i])
        if x > maximum:
            maximum = x
            maximum_j = g[i].index(x)
    rm_j= maximum_j
    for i in range(len(g)):
        g[i][rm_j] = 0
    maximum = -1
    maximum_i = -1
    for i in range(len(g)):
        x = max(g[i])
        if x > maximum:
            maximum = x
            maximum_i = i
    rm_i =  maximum_i
    g[rm_i] = [0] * len(g[rm_i])

    maximum = -1
    for i in range(len(g)):
        x = max(g[i])
        if x > maximum:
            maximum = x
    return (maximum, (rm_i, rm_j))



n, m = map(int, input().split())
g = [list(map(int, input().split())) for _ in range(n)]

r1 = solve_hv(list(map(list, g)))
r2 = solve_vh(list(map(list, g)))

result = min(r1, r2)

print(result[1][0] + 1, result[1][1] + 1)