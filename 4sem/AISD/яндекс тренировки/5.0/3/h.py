n = int(input())
bytype = {}

for i in range(n):
    x1,y1,x2,y2 = map(int, input().split())
    if (x1,y1) > (x2,y2):
        x1, y1, x2, y2  = x2,y2,x1,y1
    dx = x2 - x1
    dy = y2- y1
    if (dx,dy) not in bytype:
        bytype[(dx,dy)] = []
    bytype[(dx, dy)].append((x1,y1))

mxmy = {}

for i in range(n):
    x1,y1,x2,y2 = map(int, input().split())
    if (x1,y1) > (x2,y2):
        x1, y1, x2, y2  = x2,y2,x1,y1
    dx = x2 - x1
    dy = y2- y1
    for xp, yp in bytype.get((dx,dy), []):
        mx = x1 - xp
        my = y1 - yp
        mxmy[(mx,my)] = mxmy.get(((mx,my)), 0) + 1

maxinplc = 0
for coords in mxmy:
    maxinplc = max(maxinplc, mxmy[coords])

print(n- maxinplc)