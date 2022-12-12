from functools import reduce
import string


TYPES_PRIORITY = {v: k+1 for k, v in enumerate([*string.ascii_letters])}


class Rucksack():
    def __init__(self, input):
        self.input = input
        self.compartments = [input[0:len(input)//2], input[len(input)//2:]]
        self.common_type()

    def common_type(self):
        self.compartment_sets = [{*compartment} for compartment in self.compartments]
        self.common_type = reduce(set.intersection, self.compartment_sets)
        self.common_type_priority = sum(TYPES_PRIORITY[type] for type in self.common_type)

    def __str__(self):
        return f"Common type {', '.join(list(self.common_type))} with priority {self.common_type_priority}"


def fetch_rucksack_contents(file='input.txt') -> list[str]:
    with open(file, 'r') as f:
        contents = f.readlines()
    return contents


if __name__ == '__main__':
    inputs = fetch_rucksack_contents()
    rucksacks = [Rucksack(input) for input in inputs]
    total_priority = 0
    for rucksack in rucksacks:
        print(rucksack)
        total_priority += rucksack.common_type_priority
    print(f"Total priority: {total_priority}")
