def binary_search(arr, target, find_first):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] > target or (find_first and arr[mid] == target):
            right = mid
        else:
            left = mid + 1
    return left


n = int(input())
arr = list(map(int, input().split()))
arr.sort()



k = int(input())
for _ in range(k):
    l, r = map(int, input().split())

    start = binary_search(arr, l, True)
    end = binary_search(arr, r, False)

    print(end - start, end=" ")