n = int(input())
sum = 0
for i in range(n):
    a = int(input())
    sum += a //4 + a%4
    if a%4 == 3:
        sum-=1
print(sum)