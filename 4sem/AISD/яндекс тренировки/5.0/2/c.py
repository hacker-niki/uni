n = int(input())
ropes = list(map(int, input().split()))
ropes.sort()
max_rope = ropes[-1]
min_sum = sum(ropes[0:-1])
if max_rope > min_sum:
    result =  max_rope - min_sum
else:
    result =  max_rope + min_sum
print(result)