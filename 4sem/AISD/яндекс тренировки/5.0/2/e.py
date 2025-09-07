n = int(input())
berries = []

maxgoodi = -1
maxbadi = -1
used = [False]* (n+1)
for i in range(n):
    ta,tb = map(int, input().split())
    berries.append((ta,tb))
    if ta >=tb and (maxgoodi == -1 or tb  > berries[maxgoodi][1]):
        maxgoodi = i
    if ta <tb and (maxbadi == -1 or ta  > berries[maxbadi][0]):
        maxbadi = i
ans = []
maxh = 0
for i in range(n):
    if berries[i][0] > berries[i][1] and i != maxgoodi:
        ans.append(i+1)
        used[i + 1]= True
        maxh += berries[i][0] - berries[i][1]
if maxgoodi != -1 and (maxbadi != -1 and berries[maxgoodi][1] >berries[maxbadi][0] or maxbadi == -1):
    maxh += berries[maxgoodi][0]
    ans.append(maxgoodi+1)
    used[maxgoodi + 1] = True
else:
    if maxbadi != -1:
        if maxgoodi != -1:
            maxh += berries[maxgoodi][0]-berries[maxgoodi][1]
            ans.append(maxgoodi + 1)
            used[maxgoodi + 1] = True
        maxh += berries[maxbadi][0]
        ans.append(maxbadi + 1)
        used[maxbadi + 1] = True

print(maxh)
for i in range(1,n+1):
    if not used[i]:
        ans.append(i)
print(*ans)