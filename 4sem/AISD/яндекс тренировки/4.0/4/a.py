n = int(input())
numbers = [0 for i in range(n)]

def solve(next,numbers,num=None):
    numbers[next] = 1
    if num is None:
        num = str(next+1)
    else:
        num += str(next+1)
    if 0 not in numbers:
        print(num)
        numbers[next] = 0
        return

    for i in range(len(numbers)):
        if numbers[i] == 0:
            solve(i, numbers, num)
    numbers[next] = 0

for i in range(n):
    solve(i, numbers)
