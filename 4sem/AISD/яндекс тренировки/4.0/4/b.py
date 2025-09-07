def is_safe(board, row, col):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True


def solve_n_queens(board, col):
    if col >= N:
        return 1
    count = 0
    for i in range(N):
        if is_safe(board, i, col):
            board[i][col] = 1
            count += solve_n_queens(board, col + 1)
            board[i][col] = 0
    return count


N = int(input())
board = [[0] * N for _ in range(N)]
count = solve_n_queens(board, 0)
print(count)