def pos_string(m, a):
    ans = 1
    pos = 0
    for i in range(len(a)):
        if a[i] > m:
            return 1000000000
        if a[i] + pos <= m:
            pos += a[i] + 1
        else:
            pos = a[i] + 1
            ans += 1
    return ans


w, n, k = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

l = 0
r = w
while l < r - 1:
    m = (l + r) // 2
    if pos_string(m, a) < pos_string(w - m, b):
        r = m
    else:
        l = m

result = min(max(pos_string(l, a), pos_string(w - l, b)), max(pos_string(l + 1, a), pos_string(w - l - 1, b)))
print(result)