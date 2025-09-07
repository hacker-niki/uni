n = int(input())
a = list(map(int, input().split()))
x = int(input())

low, high = 0, 0
for i in a:
    if x > i:
        low += 1
    else:
        high += 1
print(low)
print(high)
