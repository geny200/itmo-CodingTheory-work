import numpy as np

from utils.common import to_line, read_matrix
from utils.gauss import gauss, gauss_minimize
from utils.hamming import hamming_weight, hamming_dist, compare_same_weight


# @author Geny200
# @version 3.8
# Sorry for the code, I don't write on python.


# Makes the calculation of the generating matrix (G)
# and related parameters (n and k).
# This function takes into account the conditions of
# minimality of the column numbers of the E matrix in G.
def rz_task(file_name):
    h_matrix = []
    with open(file_name, 'r') as reader:
        h_matrix = read_matrix(reader)

    if not h_matrix or len(h_matrix) > len(h_matrix[0]):
        print('err: Smth wrong with matrix;')
        return

    h_matrix = np.array(h_matrix, dtype=int)
    h_source = h_matrix.copy()

    rank = np.linalg.matrix_rank(h_matrix)
    n = len(h_matrix[0])
    k = n - rank
    print(f'n = {n}\nk = {n - rank}')

    if rank != len(h_matrix) or len(h_matrix[0]) != rank * 2:
        print('warning: There might be mistake;')

    # Some hack for minimality conditions
    for i in range(len(h_matrix[0])):
        h_matrix[:, i] = np.flip(h_matrix[:, i])
    for i in range(len(h_matrix)):
        h_matrix[i] = np.flip(h_matrix[i])

    # Evaluate I and A
    h_matrix, swap_buff = gauss(h_matrix)

    # Some hack for minimality conditions
    for i in range(len(h_matrix)):
        h_matrix[i] = np.flip(h_matrix[i])
    for i in range(len(h_matrix[0])):
        h_matrix[:, i] = np.flip(h_matrix[:, i])

    # Change index of columns (because of .flip())
    swap_buff = evaluate_num(n, swap_buff)
    swap_buff.reverse()

    a_t = h_matrix[:len(h_matrix), :len(h_matrix)].copy()

    # Create G matrix
    g_matrix = np.zeros([len(h_matrix), len(h_matrix[0])], dtype=int)
    g_matrix[:, len(g_matrix):] = a_t.transpose()
    g_matrix[:, :len(g_matrix)] = np.eye(len(g_matrix), len(g_matrix), dtype=int)

    # Swap columns
    for l, r in swap_buff:
        copy = g_matrix[:, l].copy()
        g_matrix[:, l] = g_matrix[:, r]
        g_matrix[:, r] = copy

    # Make minimal G
    g_matrix = gauss_minimize(g_matrix)

    # Show answers
    print(f'H = \n{h_source}')
    print(f'G = \n{g_matrix}')

    copyable_show = to_line(
        list(
            to_line(y) for y in list(g_matrix)
        ), '\n'
    )
    print(f'G = \n{copyable_show}')

    g_dot_ht = g_matrix.dot(h_source.transpose())
    g_dot_ht %= 2
    print(f'Check G * H = \n{g_dot_ht}')

    # Calculate all code words (in c_all)
    c_all = []
    syndrome = {}
    for i in range(2 ** len(g_matrix)):
        word = np.array(list(format(i, f'0{len(g_matrix)}b')), dtype=int)
        word = word.dot(g_matrix)
        word %= 2
        c_all.append(word)

    # Calculate min dist (aka compare all pairs)
    d_min = rank
    for i in range(len(c_all)):
        for j in range(i, len(c_all), 1):
            if i != j:
                dist = hamming_dist(c_all[i], c_all[j])
                if dist < d_min:
                    d_min = dist
    print(f'd_min = {d_min}')

    all_code_word = []
    # Calculate syndrome for each error vector
    h_source = h_source.transpose()
    for i in range(2 ** n):
        new_word = np.array(list(format(i, f'0{n}b')), dtype=int)
        e_word = new_word.dot(h_source)
        e_word %= 2

        syndrome_word = int(to_line(list(e_word)), 2)
        if syndrome_word == 0:
            all_code_word.append(new_word)

        if syndrome_word not in syndrome:
            syndrome[syndrome_word] = new_word
        else:
            old_word = syndrome[syndrome_word]
            if hamming_weight(old_word) > hamming_weight(new_word):
                syndrome[syndrome_word] = new_word
            elif hamming_weight(old_word) == hamming_weight(new_word):
                syndrome[syndrome_word] = compare_same_weight(old_word, new_word)

    # Print standard table
    for i in range(2 ** len(h_source[0])):
        binary_index = format(i, f'0{len(h_source[0])}b')[::-1]
        index = int(binary_index, 2)
        if index not in syndrome:
            print('')
            continue
        print(f'T[{binary_index}] = {to_line(list(syndrome[index]))}')


# Evaluate task from file
# !! Input file must not contain extra lines
rz_task('data/task_1.txt')
