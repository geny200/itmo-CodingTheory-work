from exceptions import BadInputException


def to_line(line, place_word=''):
    return place_word.join(str(x) for x in list(line))


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


def compare_same_weight(left, right):
    for l, r in zip(left, right):
        if l > r:
            return left
        elif r > l:
            return right
        else:
            continue


def read_matrix(reader):
    matrix = []
    for line in reader:
        line = list(filter(lambda x: x == '1' or x == '0', line))
        if not line:
            continue
        if matrix:
            if len(line) != len(matrix[0]):
                raise BadInputException(
                    f'Dimension of the line \'{line}\'({len(line)}) should be equaled '
                    f'matrix dimension ({len(matrix[0])}).'
                )
        matrix.append(list(line))
    return matrix
