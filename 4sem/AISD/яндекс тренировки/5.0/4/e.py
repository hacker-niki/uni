n = int(input())
l = 0
r = n+1
while l<r:
    m = (l+r) //2
    if m*(m+1) // 2 >=n:
        r=m
    else:
        l=m+1

diag = l
pos = n - diag * (diag-1) // 2
if diag % 2 == 1:
    print(pos, '/',diag-pos+1, sep='')
else:
    print(diag - pos + 1, '/',pos , sep='')