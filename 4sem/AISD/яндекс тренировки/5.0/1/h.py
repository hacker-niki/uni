L, x1, v1, x2, v2 = map(int, input().split())
ans = 10 **20

for i in range(2):
    deltax = (x2 - x1 + L) % L
    deltav = v1 - v2
    if deltav < 0:
        deltav *= -1
        deltax = (-deltax + L) % L
    if deltax == 0:
        ans = 0
    if deltav != 0:
        ans = min(ans, deltax/ deltav)
    x2 = (-x2 + L) % L
    v2 = -v2

if ans == 1e20:
    print("NO")
else:
    print(f"YES\n{ans:.10f}")