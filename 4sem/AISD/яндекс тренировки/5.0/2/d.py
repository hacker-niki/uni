N = int(input())
deleted = [list(map(int, input().split())) for _ in range(N)]
board = [[0] * 8 for _ in range(8)]
per = 0

for delet in deleted:
    row, col = delet
    board[row - 1][col - 1] = 1

for i in range(8):
    for j in range(8):
        if board[i][j] == 1:
            if i == 0 or board[i - 1][j] == 0:
                per += 1
            if i == 7 or board[i + 1][j] == 0:
                per += 1
            if j == 0 or board[i][j - 1] == 0:
                per += 1
            if j == 7 or board[i][j + 1] == 0:
                per += 1
print(per)