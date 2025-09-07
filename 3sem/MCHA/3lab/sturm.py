from sympy import div, diff, degree

import function


def sturm_row():
    sturms_row = []
    fp = function.function
    sturms_row.append(fp)

    fn = diff(fp)
    sturms_row.append(fn)

    r = fn
    while degree(r) > 0:
        r = div(fp, fn)[1] * (-1)
        sturms_row.append(r)
        fp = fn
        fn = r

    return sturms_row


def get_root_count(interval=function.interval):
    sr = sturm_row()
    values = []
    cnt = 0
    for i in range(len(sr)):
        values.append(sr[i].subs('x', interval[0]))
    for i in range(1, len(values)):
        if values[i] * values[i - 1] < 0:
            cnt += 1

    cnt2 = 0
    values = []
    for i in range(len(sr)):
        values.append(sr[i].subs('x', interval[1]))
    for i in range(1, len(values)):
        if values[i] * values[i - 1] < 0:
            cnt2 += 1

    return abs(cnt2 - cnt)
