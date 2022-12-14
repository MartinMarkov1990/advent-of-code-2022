def fetch_input(file='input.txt'):
    return [[int(x) for x in [*line.replace('\n', '')]] for line in open(file, 'r')]


def is_hidden_left(matrix: list[list[int]], i: int, j: int):
    if j == 0:
        return False
    return matrix[i][j] <= max(matrix[i][0:j])


def is_hidden_right(matrix: list[list[int]], i: int, j: int):
    if j >= len(matrix[i]) - 1:
        return False
    return matrix[i][j] <= max(matrix[i][j+1:])


def is_hidden_top(matrix: list[list[int]], i: int, j: int):
    if i == 0:
        return False
    return matrix[i][j] <= max([matrix[k][j] for k in range(i)])


def is_hidden_bottom(matrix: list[list[int]], i: int, j: int):
    if i >= len(matrix) - 1:
        return False
    return matrix[i][j] <= max([matrix[k][j] for k in range(i+1, len(matrix))])


def is_hidden(matrix: list[list[int]], i: int, j: int):
    return is_hidden_left(matrix, i, j) and is_hidden_right(matrix, i, j) and \
           is_hidden_top(matrix, i, j) and is_hidden_bottom(matrix, i, j)


def compute_hidden_flags(matrix: list[list[int]]):
    num_rows = len(matrix)
    num_columns = len(matrix[0])
    hidden_flags = []
    for i in range(num_rows):
        hidden_flags.append([is_hidden(input, i, j) for j in range(num_columns)])
    return hidden_flags


def trees_seen_in_line(tree_height: int, line_heights: list[int]):
    seen = 0
    for seen_tree in line_heights:
        seen += 1
        if tree_height <= seen_tree:
            break
    return seen


def scenic_score(matrix: list[list[int]], i: int, j: int):
    tree_height = matrix[i][j]
    trees_left = matrix[i][0:j]
    trees_left.reverse()
    trees_right = matrix[i][j + 1:]
    trees_top = [matrix[k][j] for k in range(i - 1, -1, -1)]
    trees_bottom = [matrix[k][j] for k in range(i + 1, len(matrix))]
    seen_trees_left = trees_seen_in_line(tree_height, trees_left)
    seen_trees_right = trees_seen_in_line(tree_height, trees_right)
    seen_trees_top = trees_seen_in_line(tree_height, trees_top)
    seen_trees_bottom = trees_seen_in_line(tree_height, trees_bottom)
    return seen_trees_left * seen_trees_right * seen_trees_top * seen_trees_bottom


def calculate_scenic_scores(matrix: list[list[int]]):
    num_rows = len(matrix)
    num_columns = len(matrix[0])
    scenic_scores = []
    for i in range(num_rows):
        scenic_scores.append([scenic_score(matrix, i, j) for j in range(num_columns)])
    return scenic_scores


if __name__ == '__main__':
    input = fetch_input()
    test_input = [[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]]

    # part 1
    # hidden_flags = compute_hidden_flags(input)
    # total_visible = sum([sum(not flag for flag in row) for row in hidden_flags])
    # print('Total visible trees: ', total_visible)

    # part 2
    scenic_scores = calculate_scenic_scores(input)

    print('Scenic Scores:')
    for row in scenic_scores:
        print(','.join([str(i) for i in row]))

    max_scenic_score = max([max(row) for row in scenic_scores])
    print("Max scenic score: ", max_scenic_score)
