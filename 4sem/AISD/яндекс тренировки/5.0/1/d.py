mat = []
for i in range(8):
    mat.append(list(input()))

for i in range(8):
    for j in range(8):
        if i == 4 and j == 0:
            pass
        if mat[i][j] == '*':
            bit = False
            for i1 in range(i):
                if mat[i1][j] == 'R':
                    bit = True
                elif mat[i1][j] == 'B':
                    bit = False
            if not bit:
                for i1 in range(7, i, -1):
                    if mat[i1][j] == 'R':
                        bit = True
                    elif mat[i1][j] == 'B':
                        bit = False
            if not bit:
                for j1 in range(j):
                    if mat[i][j1] == 'R':
                        bit = True
                    elif mat[i][j1] == 'B':
                        bit = False
            if not bit:
                for j1 in range(7, j, -1):
                    if mat[i][j1] == 'R':
                        bit = True
                    elif mat[i][j1] == 'B':
                        bit = False

            if not bit:
                for i1 in range(i - 1, -1, -1):
                    if j - (i - i1) < 0:
                        break
                    if mat[i1][j - (i - i1)] == 'B':
                        bit = True
                        break
                    elif mat[i1][j - (i - i1)] == 'R':
                        break
            if not bit:
                for i1 in range(i - 1, -1, -1):
                    if j + i - i1 > 7:
                        break
                    if mat[i1][j + i - i1] == 'B':
                        bit = True
                        break
                    elif mat[i1][j + i - i1] == 'R':
                        break
            if not bit:
                for i1 in range(i + 1, 8):
                    if j - (i - i1) > 7:
                        break
                    if mat[i1][j - (i - i1)] == 'B':
                        bit = True
                        break
                    elif mat[i1][j - (i - i1)] == 'R':
                        break
            if not bit:
                for i1 in range(i + 1, 8):
                    if j + i - i1 < 0:
                        break
                    if mat[i1][j + i - i1] == 'B':
                        bit = True
                        break
                    elif mat[i1][j + i - i1] == 'R':
                        break
            if bit:
                mat[i][j] = '.'

print(sum([el.count('*') for el in mat]))

