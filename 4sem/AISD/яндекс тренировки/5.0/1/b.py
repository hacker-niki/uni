g1 = [int(el) for el in input().split(':')]
g2 = [int(el) for el in input().split(':')]
house = int(input())
if g1[0] + g2[0] > g1[1] + g2[1]:
    print(0)
elif g1[0] + g2[0] == g1[1] + g2[1]:
    if (house == 1 and g2[0] > g1[1]) or (house == 2 and g1[0] > g2[1]):
        print(0)
    else:
        print(1)

else:
    if house == 1:
        if g2[1] > g1[0]:
            print(g1[1] + g2[1] - g1[0] - g2[0])
        else:
            print(g1[1] + g2[1] - g1[0] - g2[0] + 1)
    else:
        if g2[1] < g1[0]:
            print(g1[1] + g2[1] - g1[0] - g2[0])
        else:
            print(g1[1] + g2[1] - g1[0] - g2[0] + 1)
