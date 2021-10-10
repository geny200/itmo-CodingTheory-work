from exaptions.exceptions import BadInputException


def to_line(line, place_word=''):
    return place_word.join(str(x) for x in list(line))


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
