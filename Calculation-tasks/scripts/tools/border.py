import math


def gr_find_k_by_n_d(n, d):
    k = 0
    sum = 0
    pow = 1
    while n >= sum:
        sum += math.ceil(d / pow)
        k += 1
        pow *= 2
    return k - 1


def gr_find_d_by_n_k(n, k):
    for d in range(n):
        sum = 0
        pow = 1
        for i in range(k):
            sum += math.ceil(d / pow)
            pow *= 2
        if n < sum:
            return d - 1


def vg_find_d_by_n_k(n, k):
    r = n - k
    q = 2 ** r
    sum = 0
    d = 0
    # print(f'q^{r} = {q}')
    while q > sum:
        sum += (math.factorial(n - 1) /
                (math.factorial(d) * (math.factorial(n - 1 - d))))
        d += 1
    # print(f'sum = {sum}')
    return d + 1


def vg_find_k_by_n_d(n, d):
    sum = 0
    for i in range(d - 2):
        sum += (math.factorial(n - 1) /
                (math.factorial(i) * (math.factorial(n - 1 - i))))

    # print(f'sum = {sum}')
    for i in range(n):
        if (2 ** (n - i)) > sum:
            continue
        # print(f'q^{n}-{i - 1} = {2 ** (n - i + 1)}')
        return i - 1
