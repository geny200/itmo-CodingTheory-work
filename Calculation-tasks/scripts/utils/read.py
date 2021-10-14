from exceptions.exceptions import BadInputException


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


def safe_get_from_file(file_name, entity_name='Object'):
    try:
        with open(file_name, 'r') as reader:
            matrix = read_matrix(reader)
        if not matrix:
            raise BadInputException(f'{entity_name} in file \'{file_name}\' not found')
        return matrix
    except FileNotFoundError:
        raise BadInputException(f'File with {entity_name} in path \'{file_name}\' not found')