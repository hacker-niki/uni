n = int(input())
dict = {}
print("Initial array:")
for i in range(10):
    dict[str(i)] = []
k = 1
mx = 0
for i in range(n):
    s = input()
    mx = len(s) # mx = max(mx, len(s))
    if i == n - 1:
        print(s)
    else:
        print(s, end=", ")
    dict[s[-1]] += [s]
print("**********")
nd = {}
for i in range(mx):
    for j in range(10):
        nd[str(j)] = []
    print("Phase", i + 1)
    for j in dict:
        for h in dict[j]:
            # print(h)
            # print(str(h[-2]))
            nd[str(h[-i-1])] += [h]
            # print('nd ', nd)
    for i in nd:
        dict[i] = nd[i]
    # print(dict)
    for j in range(10):
        j = str(j)
        print("Bucket ", j, ": ", end="", sep="")
        if len(dict[j]) == 0:
            print('empty')
        else:
            for h in range(len(dict[j])):
                if h == len(dict[j]) - 1:
                    print(dict[j][h])
                else:
                    print(dict[j][h], ', ', end="", sep="")
    print("**********")
print('Sorted array:')
res = ''
for i in dict:
    for j in dict[i]:
        res += j + ', '
print(res[:-2])