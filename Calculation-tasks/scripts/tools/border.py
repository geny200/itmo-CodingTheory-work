import math

from exceptions.exceptions import LogicException


def gr_find_k_by_n_d(n, d, logger=None):
    if not (n >= d > 0):
        raise LogicException(f'N = {n} should be grater than or equal to d = {d},'
                             f' which should be grater than 0')
    k = 0
    sum_old = 0
    sum = 0
    pow = 1
    while n >= sum:
        sum_old = sum
        sum += math.ceil(d / pow)
        k += 1
        pow *= 2
    if logger:
        logger(f'n >= sum\n'
               f'sum by i in ceil(d / 2^i) from 0 until k - 1\n'
               f'from 0 to until = {k - 2} => sum = {sum_old}\n'
               f'from 0 until k = {k - 1} => sum {sum}\n')
    return k - 1


def gr_find_d_by_n_k(n, k, logger=None):
    if not (n >= k > 0):
        raise LogicException(f'N = {n} should be grater or equal than K = {k},'
                             f' which should be grater than 0')
    sum_old = 0
    for d in range(n):
        sum = 0
        pow = 1
        for i in range(k):
            sum += math.ceil(d / pow)
            pow *= 2
        if n < sum:
            if logger:
                logger(f'n >= sum\n'
                       f'sum by i in ceil(d / 2^i) from 0 until (k - 1) = {k - 1}\n'
                       f'search d in 0 until n = {n}\n'
                       f'for d = {d - 2} => sum = {sum_old}\n'
                       f'for d = {d - 1} => sum = {sum}\n')
            return d - 1
        sum_old = sum
    return 1


def vg_find_d_by_n_k(n, k, logger=None):
    if not (n >= k > 0):
        raise LogicException(f'N = {n} should be grater than or equal to K = {k},'
                             f' which should be grater than 0')
    r = n - k
    q = 2 ** r
    sum_old = 0
    sum = 0

    for d in range(n):
        if q <= sum:
            if logger:
                logger(f'q^(n - k) > sum\n'
                       f'q^({n} - {k}) = {q}\n'
                       f'sum by d in C_d^(n-1)*(2 - 1) ^ i\n'
                       f'from 0 until (d - 2) = {d - 2} => sum = {sum_old}\n'
                       f'from 0 until (d - 2) = {d - 1} => sum = {sum}\n')
            return d + 1
        sum_old = sum
        sum += (math.factorial(n - 1) /
                (math.factorial(d) * (math.factorial(n - 1 - d))))
    return 0


def vg_find_k_by_n_d(n, d, logger=None):
    if not (n >= d > 0):
        raise LogicException(f'N = {n} should be grater than or equal to d = {d},'
                             f' which should be grater than 0')
    if (d == 1):
        return n

    sum = 0
    for i in range(d - 2):
        sum += (math.factorial(n - 1) /
                (math.factorial(i) * (math.factorial(n - 1 - i))))

    for i in range(n):
        if (2 ** (n - i)) > sum:
            continue
        if logger:
            logger(f'q^(n - k) > sum\n'
                   f'q^({n} - k) > sum\n'
                   f'sum by i in C_i^(n-1)*(2 - 1) ^ i\n'
                   f'from 0 until (d - 2) = {d - 2} => sum = {sum}\n'
                   f'q^({n} - {i - 2}) = {2 ** (n - i + 2)}\n'
                   f'q^({n} - {i - 1}) = {2 ** (n - i + 1)}\n')
        return i - 1
    return 0
