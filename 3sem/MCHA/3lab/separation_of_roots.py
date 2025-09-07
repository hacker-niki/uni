import function
from sturm import get_root_count


def split_interval(interval=function.interval, max_roots=get_root_count(function.interval)):
    l = interval[0]
    r = interval[1]

# print(zeidel_method(addons.read_matrix_from_file('a.mcha'), addons.read_matrix_from_file('b.mcha').T))

    mid = (r + l) // 2
    rk = get_root_count([l, r])
    if rk == 1:
        return [(l, r)]
    elif rk > 1:
        result = split_interval([l, mid]) + split_interval([mid, r])
        return result

    return []
