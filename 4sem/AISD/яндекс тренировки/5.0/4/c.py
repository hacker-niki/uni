n, q = map(int, input().split())
orc_counts = [0] + list(map(int, input().split()))


prefix_sums = [0] * (n + 1)
for i in range(1, n + 1):
    prefix_sums[i] = prefix_sums[i - 1] + orc_counts[i]

for i in range(q):
    l, s = map(int, input().split())
    left, right = 1, n + 1 - l
    while left < right:
        mid = (left + right) // 2
        if prefix_sums[mid+l-1] - prefix_sums[mid - 1] >= s:
            right = mid
        else:
            left = mid + 1

    if prefix_sums[left+l - 1] - prefix_sums[left - 1] == s:
        print(left)
    else:
        print(-1)