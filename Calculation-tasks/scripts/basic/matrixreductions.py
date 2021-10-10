import numpy as np

from exaptions.exceptions import AssertException, LogicException
from utils.gauss import gauss, gauss_minimize


# Makes index matching. (you can optimize up to one line)
def evaluate_num(n, swap_buff):
    line = np.array(range(n - 1, -1, -1), dtype=int)
    nums = np.zeros(n, dtype=int)
    for i, x in enumerate(line):
        nums[x] = i
    upd_buffer = []
    for l, r in swap_buff:
        upd_buffer.append((nums[l], nums[r]))

    swap_buff = upd_buffer
    return swap_buff


def get_H_matrix_by_G(g_matrix):
    local_matrix = g_matrix.copy()
    local_matrix, swap_buff = gauss(local_matrix)
    swap_buff.reverse()

    a_t = local_matrix[:len(local_matrix), len(local_matrix):].copy()

    # Create H matrix
    h_matrix = np.zeros([len(local_matrix), len(local_matrix[0])], dtype=int)
    h_matrix[:, :len(h_matrix)] = a_t.transpose()
    h_matrix[:, len(h_matrix):] = np.eye(len(h_matrix), len(h_matrix), dtype=int)

    # Swap columns
    for l, r in swap_buff:
        copy = h_matrix[:, l].copy()
        h_matrix[:, l] = h_matrix[:, r]
        h_matrix[:, r] = copy

    return h_matrix


def get_G_matrix_by_H(h__matrix):
    local_matrix = h__matrix.copy()
    n = len(local_matrix[0])

    # Some hack for minimality conditions
    for i in range(len(local_matrix[0])):
        local_matrix[:, i] = np.flip(local_matrix[:, i])
    for i in range(len(local_matrix)):
        local_matrix[i] = np.flip(local_matrix[i])

    # Evaluate I and A
    local_matrix, swap_buff = gauss(local_matrix)

    # Some hack for minimality conditions
    for i in range(len(local_matrix)):
        local_matrix[i] = np.flip(local_matrix[i])
    for i in range(len(local_matrix[0])):
        local_matrix[:, i] = np.flip(local_matrix[:, i])

    # Change index of columns (because of .flip())
    swap_buff = evaluate_num(n, swap_buff)
    swap_buff.reverse()

    a_t = local_matrix[:len(local_matrix), :len(local_matrix)].copy()

    # Create G matrix
    g_matrix = np.zeros([len(local_matrix), len(local_matrix[0])], dtype=int)
    g_matrix[:, len(g_matrix):] = a_t.transpose()
    g_matrix[:, :len(g_matrix)] = np.eye(len(g_matrix), len(g_matrix), dtype=int)

    # Swap columns
    for l, r in swap_buff:
        copy = g_matrix[:, l].copy()
        g_matrix[:, l] = g_matrix[:, r]
        g_matrix[:, r] = copy

    # Make minimal G
    g_matrix = gauss_minimize(g_matrix)

    return g_matrix


def flip_matrix(matrix):
    # Some hack for reverse traversal
    for i in range(len(matrix[0])):
        matrix[:, i] = np.flip(matrix[:, i])
    for i in range(len(matrix)):
        matrix[i] = np.flip(matrix[i])


def to_minimal_span_matrix(matrix):
    local_matrix = matrix.copy()

    back_traverse = \
        np.linalg.matrix_rank(local_matrix[:, :len(local_matrix)]) \
        != len(local_matrix)
    for i in range(0, 2):
        local_matrix = gauss_minimize(local_matrix, back_traverse)
        flip_matrix(local_matrix)

    # Third step
    local_matrix = gauss_minimize(local_matrix, False)

    head_columns = set([])
    tail_columns = set([])
    for line in local_matrix:
        try:
            first_index_of_1 = list(line).index(1)
            last_index_of_1 = list(line[::-1]).index(1)  # len(line) - line[::-1].index(1) - 1
            if first_index_of_1 in head_columns or last_index_of_1 in tail_columns:
                raise AssertException('A logical error in the code, please report it to the maintainer')

            head_columns.add(first_index_of_1)
            tail_columns.add(last_index_of_1)

        except ValueError:
            raise LogicException(f'Impossible to reduce the matrix to the spene form')

    return local_matrix
