from functools import reduce
import string


TYPES_PRIORITY = {v: k+1 for k, v in enumerate([*string.ascii_letters])}


class Rucksack():
    def __init__(self, input):
        self.input = input.replace('\n', '')
        self.item_types = {*self.input}
        self.compartments = [self.input[0:len(input)//2], self.input[len(input)//2:]]
        self.compute_common_type()

    def compute_common_type(self):
        self.compartment_sets = [{*compartment} for compartment in self.compartments]
        self.common_type = reduce(set.intersection, self.compartment_sets)
        self.common_type_priority = sum(TYPES_PRIORITY[type] for type in self.common_type)

    def __str__(self):
        return self.input


def fetch_rucksack_contents(file='input.txt') -> list[str]:
    with open(file, 'r') as f:
        contents = f.readlines()
    return contents


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == '__main__':
    inputs = fetch_rucksack_contents()
    rucksacks = [Rucksack(input) for input in inputs]
    rucksack_groups = chunks(rucksacks, 3)
    badges = [reduce(set.intersection, [rucksack.item_types for rucksack in rucksacks]) for rucksacks in rucksack_groups]
    badge_priorities = [(list(badge)[0], TYPES_PRIORITY[list(badge)[0]]) for badge in badges]
    total_priority = sum([priority[1] for priority in badge_priorities])
    print(f"Total priority: {total_priority}")
