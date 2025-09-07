def find_prev(s):
    a1,a2 = 0,0
    for i in range(len(s)-1, -1, -1):

        if s[i] == ')':
            a1 += 1
        elif s[i] == ']':
            a2 += 1
        elif s[i] == '(':
            a1 -= 1
        elif s[i] == '[':
            a2 -= 1
        if a1<0:
            return '('
        if a2 <0:
            return '['


def generate_brackets(n, open_brackets1=0, close_brackets1=0, open_brackets2=0, close_brackets2=0,sequence=''):


    if open_brackets1 == close_brackets1 and  open_brackets2 == close_brackets2 and  open_brackets1+close_brackets1+close_brackets2+open_brackets2 ==2*n:
        print(sequence)
        return
    elif open_brackets1+close_brackets1+close_brackets2+open_brackets2 ==2*n:
        return
    if open_brackets1+open_brackets2 < n:

        generate_brackets(n, open_brackets1+1, close_brackets1, open_brackets2, close_brackets2, sequence + '(')

        generate_brackets(n, open_brackets1, close_brackets1, open_brackets2 + 1, close_brackets2, sequence + '[')


    if close_brackets1 < open_brackets1 and find_prev(sequence) == '(':

        generate_brackets(n, open_brackets1, close_brackets1 + 1, open_brackets2, close_brackets2, sequence + ')')

    if close_brackets2 < open_brackets2 and find_prev(sequence) == '[':
        generate_brackets(n, open_brackets1, close_brackets1, open_brackets2, close_brackets2 + 1, sequence + ']')


n = int(input())
if n % 2==1 or n == 0:
    exit(0)

pairs = generate_brackets(n // 2)