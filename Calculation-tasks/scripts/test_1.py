import numpy as np

from exceptions.exceptions import TaskException
from tools.matrixreductions import get_G_matrix_by_H
from tools.parameters import find_d_min_by_g_matrix, get_standard_table
from utils.common import to_line
from utils.read import safe_get_from_file


# @author Geny200
# Sorry for the code, I don't write on python.

def test_1(h_matrix):
    h_matrix_local = h_matrix.copy()

    if len(h_matrix) > len(h_matrix[0]):
        print('warning: Pls, check correctness of matrix (smth wrong);')

    rank = np.linalg.matrix_rank(h_matrix)

    if rank != len(h_matrix):
        print(f'warning: If rank < dim(matrix) smth can be wrong '
              f'(rank = {rank}; dim = {len(h_matrix)});')

    g_matrix = get_G_matrix_by_H(h_matrix_local)

    d_min = find_d_min_by_g_matrix(g_matrix)
    d_min_dual = find_d_min_by_g_matrix(h_matrix)

    standard_table = get_standard_table(h_matrix)

    return g_matrix, d_min, d_min_dual, standard_table


# Evaluate task from file
def main():
    file_name_matrix = 'data/test_1_matrix.txt'
    sep = ' '

    try:
        h_matrix = safe_get_from_file(file_name_matrix, 'Matrix')
        h_matrix = np.array(h_matrix, dtype=int)

        print(f'Please make sure that this is your H matrix:\n'
              f'H matrix = \n'
              f'{h_matrix}\n')

        g_matrix, d_min, d_min_dual, standard_table = test_1(h_matrix)

        print(f'G matrix = \n'
              f'{g_matrix}\n'
              f'\n'
              f'd_min = {d_min}\n'
              f'd_min (dual) = {d_min_dual}\n'
              f'\n'
              f'standard table (syndromes): ')

        for syndrome in standard_table:
            binary_index = format(syndrome, f'0{len(h_matrix)}b')[::-1]
            print(f'T[{binary_index}] = {to_line(standard_table[syndrome])}')

    except TaskException as e:
        print(f'error: {e.message}')


if __name__ == '__main__':
    main()
