def fetch_input(file='input.txt'):
    with open(file, 'r') as f:
        input = [line.replace('\n', '').split(',') for line in f]
    return input


def rangify_str(input_range: str):
    start_end = input_range.split('-')
    return range(int(start_end[0]), int(start_end[1]) + 1)


def rangify_input(input: list[list[str]]):
    return [[rangify_str(input_str) for input_str in input_line] for input_line in input]


def range_contains(container: range, containee: range) -> bool:
    return container.start <= containee.start and container.stop >= containee.stop


def ranges_overlap(range1: range, range2: range) -> bool:
    return range1.start < range2.stop and range1.stop > range2.start


def any_range_contains(range1: range, range2: range) -> bool:
    return range_contains(range1, range2) or range_contains(range2, range1)


if __name__ == '__main__':
    input = fetch_input()
    rangified = rangify_input(input)
    for pair in rangified:
        print(f"{pair}{' containing' if any_range_contains(*pair) else ' overlapping' if ranges_overlap(*pair) else ''}")
    total_containing = len([pair for pair in rangified if any_range_contains(*pair)])
    total_overlapping = len([pair for pair in rangified if ranges_overlap(*pair)])
    print(f'Total containing: {total_containing}')
    print(f'Total overlapping: {total_overlapping}')
