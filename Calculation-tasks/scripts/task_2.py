import math

import numpy as np

from exceptions.exceptions import BadInputException, TaskException, LogicException
from tools.matrixreductions import get_H_matrix_by_G, to_minimal_span_matrix
from tools.parameters import find_syndromes
from utils.common import to_line
from utils.read import safe_get_from_file


# @author Geny200
# Sorry for the code, I don't write on python.

def get_active_elements(matrix, column):
    actives = []
    for line in matrix:
        try:
            first_index_of_1 = list(line).index(1)
            last_index_of_1 = len(line) - list(line[::-1]).index(1) - 1

            if first_index_of_1 <= column and column < last_index_of_1:
                actives.append(1)
            else:
                actives.append(0)
        except ValueError:
            raise LogicException(f'Matrix is not in minimal spene form')
    return actives


def get_active_column(matrix, column):
    actives = get_active_column(matrix, column)
    active_column = list(matrix[:, column])
    return list(map(lambda x, y: x * y, list(zip(active_column, actives))))


def get_log_Vi(matrix):
    log_Vi = [0]
    for i in range(0, len(matrix[0])):
        log_Vi.append(sum(x == 1 for x in get_active_elements(matrix, i)))
    return log_Vi


def decode_word_by_H_matrix(matrix, word):
    n = len(matrix[0])
    s = word.dot(matrix.transpose())
    s %= 2

    syndrome = find_syndromes(matrix)

    code_word = list(map(lambda x, y: (x + y) % 2, list(word), list(syndrome[int(to_line(list(s)), 2)])))

    # print('logs:')
    # print(f'syndrom = {s}')
    # print(f'word = {word}')
    # print(f'T[s] = {syndrome[int(to_line(list(s)), 2)]}')
    # print(f'C    = {np.array(code_word, dtype=int)}')
    # print(f't    = {sum(x == 1 for x in syndrome[int(to_line(list(s)), 2)])}')
    return code_word


def rz_task_(g_matrix, word):
    if len(g_matrix) > len(g_matrix[0]):
        print('warning: Pls, check correctness of matrix (smth wrong);')

    rank = np.linalg.matrix_rank(g_matrix)

    if rank != len(g_matrix):
        raise BadInputException(f'If rank = ({rank}) < dim(matrix) = {len(g_matrix)} smth can be wrong')
        # print('warning: If rank < dim(matrix) smth can be wrong;')

    span_matrix = to_minimal_span_matrix(g_matrix)
    log_Vi = get_log_Vi(span_matrix)

    if word and word[0]:
        h_matrix = get_H_matrix_by_G(g_matrix)
        c = decode_word_by_H_matrix(h_matrix, np.array(word[0], dtype=int))
        return log_Vi, c
    else:
        print(f'warning: word \'Y\' not found')
        return log_Vi, []


def main():
    # Evaluate task from file
    file_name_matrix = 'data/task_2_matrix.txt'
    file_name_word = 'data/task_2_word.txt'
    sep = ' '

    try:
        g_matrix = safe_get_from_file(file_name_matrix, 'Matrix')
        g_matrix = np.array(g_matrix, dtype=int)

        word = safe_get_from_file(file_name_word, 'Word Y')

        print(f'Please make sure that this is your matrix and your word:\n'
              f'{g_matrix}\n')
        if word and word[0]:
            print(f'Y = ({to_line(np.array(word[0], dtype=int), sep)})\n')

        log_Vi, c = rz_task_(g_matrix, word)
        print('\nanswer:')
        print(f'log_2(|V_i|) = {to_line(log_Vi, sep)}\nC = ({to_line(c, sep)})')
    except TaskException as e:
        print(f'error: {e.message}')


if __name__ == '__main__':
    main()


