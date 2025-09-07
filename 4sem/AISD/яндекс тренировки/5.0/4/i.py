def in_circle(x0,y0,r0, xp, yp):
    return (xp-x0) ** 2 +(yp-y0) ** 2 -r0 ** 2 < 0.000001


def check(xll,yll, xru, yru, time):
    if not in_circle(0,0,d, xll, yll) and not in_circle(0,0,d, xll, yru) and not in_circle(0,0,d, xru, yru) and not in_circle(0,0,d, xru, yll):
        return (False,( 0,0))
    if xru - xll < 0.000001:
        return (True, ((xll + xru) / 2, (yll + yru) / 2))

    for i in range(n):
        if in_circle(x[i], y[i], v[i]*time, xll, yll) and in_circle(x[i], y[i], v[i]*time, xll, yru) \
            and in_circle(x[i], y[i], v[i]*time, xru, yll) and in_circle(x[i], y[i], v[i]*time, xru, yru):
            return (False, (0,0))
    xs = [xll, (xll+xru)/2, xru]
    ys = [yll, (yll + yru) / 2, yru]
    for i in range(2):
        for j in range(2):
            quater = check(xs[i], ys[j], xs[i+1], ys[j+1], time)
            if quater[0]:
                return quater
    return (False, (0,0))

d,n = map(int, input().split())
x = []
y = []
v = []

for i in range(n):
    a,b,c = map(int, input().split())
    x.append(a)
    y.append(b)
    v.append(c)

l = 0
r = 4*d
while r- l > 0.000001:
    m = (l+r) /2
    if check(-d,0,d,d,m)[0]:
        l = m
    else:
        r = m

now = check(-d,0,d,d,l)
print(l)
print(*now[1])
