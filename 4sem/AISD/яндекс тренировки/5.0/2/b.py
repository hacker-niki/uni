N, K = map(int, input().split())
prices = list(map(int, input().split()))

max_profit = 0


for i in range(N):
    for j in range(i+1, min(i+K+1, N)):
        profit = prices[j] - prices[i]
        if profit > max_profit:
            max_profit = profit


print(max_profit)