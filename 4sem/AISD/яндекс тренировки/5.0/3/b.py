from collections import Counter

str1 = input().strip()
str2 = input().strip()

if Counter(str1) == Counter(str2):
    print("YES")
else:
    print("NO")
