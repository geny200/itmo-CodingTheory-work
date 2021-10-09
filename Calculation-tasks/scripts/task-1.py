import numpy as np


# @author Geny200
# @version 3.8
# Sorry for the code, I don't write on python.

def to_line(line, place_word=''):
    return place_word.join(str(x) for x in list(line))


def compare_same_weight(left, right):
    for l, r in zip(left, right):
        if l > r:
            return left
        elif r > l:
            return right
        else:
            continue


# Calculate number of '1'.
def hamming_weight(word):
    result = 0
    for i in word:
        if i > 0:
            result += 1
    return result


# Calculate number of different digit in
# the same position.
def hamming_dist(left, right):
    result = 0
    for l, r in zip(left, right):
        if l != r:
            result += 1
    return result


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


# Find first "good" column in matrix ("good" -
# means a non-zero value in the current line position;
# column index > current_row)
def find_column(matrix, current_row, current_column):
    if not matrix.any():
        return current_column

    n = len(matrix[0])
    if n <= current_column:
        return current_column

    for i in range(current_column, n):
        if np.max(matrix[current_row:, i]) > 0:
            return i
    return current_column


# Find first "good" line in matrix ("good" -
# means a non-zero value in the current column
# with the index "current_column"; row index > current_column)
def find_row(matrix, current_line, current_column):
    if not matrix.any():
        return current_line

    n = len(matrix)
    if n <= current_line:
        return current_line

    for i in range(current_line, n):
        if matrix[i, current_column] > 0:
            return i

    return current_line


# Gaussian function for constructing a I matrix in place.
def gauss(A):
    swap_buff = []
    for i in range(len(A)):
        # print(f'-------{i}--------')
        # print(A)
        cur = find_column(A, i, i)
        if cur != i:
            # print(f'swap column - {i} {cur}')
            swap_buff.append((i, cur))
            copy = A[:, i].copy()
            A[:, i] = A[:, cur]
            A[:, cur] = copy
            # print(A)
        cur = find_row(A, i, i)
        if cur != i:
            # print(f'swap line - {i} {cur}')
            copy = A[i].copy()
            A[i] = A[cur]
            A[cur] = copy
            # print(A)

        if i < len(A) - 1:
            for k in range(i + 1, len(A)):
                if A[k][i] > 0:
                    # print(f'{k} - {i}')
                    A[k] -= A[i]
                    A[k] %= 2
                    # print(f'{A}')

    for i in range(len(A), 0, -1):
        for k in range(i - 1, 0, -1):
            if A[k - 1][i - 1] > 0:
                # print(f'{k - 1} - {i - 1}')
                A[k - 1] -= A[i - 1]
                A[k - 1] %= 2
                # print(f'{A}')

    return A, swap_buff


# Gaussian function for minimize.
def gauss_minimize(A):
    columns_i_matrix = []
    column_i = 0
    for i in range(len(A)):

        cur = find_column(A, i, column_i)
        if cur != i:
            column_i = cur

        cur = find_row(A, i, column_i)
        if cur != i:
            # print(f'swap line - {i} {cur}')
            copy = A[i].copy()
            A[i] = A[cur]
            A[cur] = copy
            # print(A)

        if column_i < len(A) - 1:
            for k in range(i + 1, len(A)):
                if A[k][column_i] > 0:
                    # print(f'{k} - {i}')
                    A[k] -= A[i]
                    A[k] %= 2
        columns_i_matrix.append(column_i)
        column_i += 1
    columns_i_matrix.reverse()
    # print('end')
    # print(f'{columns_i_matrix}')
    for order, column in zip(range(len(columns_i_matrix) - 1, -1, -1), columns_i_matrix):
        for row in range(order, 0, -1):
            if A[row - 1][column] > 0:
                # print(f'{order}, {column}, {row}')
                # print(f'{row - 1} - {order}')
                A[row - 1] -= A[order]
                A[row - 1] %= 2
                # print(f'{A}')

    return A


# Makes the calculation of the generating matrix (G)
# and related parameters (n and k).
# This function takes into account the conditions of
# minimality of the column numbers of the E matrix in G.
def rz_task(file_name):
    h_matrix = []
    with open(file_name, 'r') as reader:
        for line in reader:
            line = line.rstrip()
            if h_matrix:
                if len(line) != len(h_matrix[0]):
                    print('err: This is not a matrix;')
                    return
            h_matrix.append(list(line))

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
rz_task('data/input.txt')
