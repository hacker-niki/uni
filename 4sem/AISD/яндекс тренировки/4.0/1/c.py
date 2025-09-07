def merge(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result



n = int(input())
a = list(map(int, input().split()))
m = int(input())
b = list(map(int, input().split()))
print(*merge(a, b))

