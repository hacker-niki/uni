N = int(input())
points = [tuple(map(int, input().split())) for _ in range(N)]
sets = set(points)
x0,y0 = points[0]
min_points = [(x0+1, y0+1), (x0+1, y0), (x0, y0+1)]

for i1 in range(len(points)):
    for i2 in range(len(points)):
        if i1 != i2:
            x1,y1 = points[i1]
            x2,y2 = points[i2]
            dx = x2 -x1
            dy = y2 - y1
            x3 = x1 + dy
            y3 = y1 - dx
            x4 = x3 +dx
            y4 = y3+dy
            if (x3,y3) in sets and (x4,y4) in sets and len(min_points)>0:
                min_points = []
                break
            if (x3,y3) in sets and len(min_points)>1:
                min_points = [(x4,y4)]
            if (x4,y4) in sets and len(min_points)>1:
                min_points = [(x3,y3)]
            if len(min_points)>2:
                min_points = [(x3, y3),(x4, y4)]

print(len(min_points))
for point in min_points:
    print(f'{point[0]} {point[1]}')