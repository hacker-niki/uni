n = int(input())
numbers = list(map(int, input().split()))

dict_num = {}
for num in numbers:
    dict_num[num] = dict_num.get(num, 0) + 1

maximum = 0
for number in dict_num.keys():
    maximum = max(
        maximum,
        dict_num.get(number, 0) + dict_num.get(number + 1, 0)
    )

print(len(numbers) - maximum)