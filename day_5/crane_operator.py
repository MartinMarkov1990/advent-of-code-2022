from copy import deepcopy
from collections import deque
import re


def fetch_input(file='input.txt') -> list[str]:
    with open(file, 'r') as f:
        input = [line.replace('\n', '') for line in f]
    return input


def parse_input(input: list[str]) -> tuple[list[str], list[str]]:
    sep = input.index('')
    return input[:sep], input[sep+1:]


def parse_stack_input(line: str) -> list[str]:
    ranges = range(0, len(line), 4)
    return [re.sub('[\\[\\]\\s]', '', line[start:start+4]) for start in ranges]


def parse_move(line: str) -> list:
    matches = re.search('move ([0-9]+) from ([0-9]+) to ([0-9]+)', line)
    return [int(matches.group(1)), matches.group(2), matches.group(3)]


class Stacks():
    def __init__(self, stack_input: list[str], move_input: list):
        self.stack_input = deepcopy(stack_input)
        self.move_input = deepcopy(move_input)
        parsed_stacks = [parse_stack_input(line) for line in stack_input]
        transposed_stacks = [list(sublist) for sublist in zip(*parsed_stacks[0:-1])]
        self.start_stacks = dict(zip(parsed_stacks[-1], [[item for item in stack[::-1] if item != ''] for stack in transposed_stacks]))
        self.stacks = deepcopy(self.start_stacks)
        self.all_moves = [parse_move(line) for line in move_input]
        self.remaining_moves = deque(self.all_moves)
        self.print_stacks()
        # self.make_all_moves()

    def print_stacks(self):
        stacks = [[f' {v[i] if i < len(v) else " "} ' for v in self.stacks.values()] for i in range(max([len(v) for v in self.stacks.values()])-1, -1, -1)]
        keys = [f" {k} " for k in self.stacks.keys()]
        for stack in stacks:
            print(''.join(stack))
        print(''.join(keys))

    def make_move(self, move: list, keep_order=False):
        count, start_stack, end_stack = move
        print(f"Moving {count} from {start_stack} to {end_stack}")
        if keep_order:
            self.stacks[end_stack].extend(self.stacks[start_stack][-count:])
            self.stacks[start_stack] = self.stacks[start_stack][0:-count]
        else:
            for i in range(count):
                try:
                    self.stacks[end_stack].append(self.stacks[start_stack].pop())
                except IndexError:
                    break
        # self.print_stacks()

    def make_all_moves(self, keep_order=False):
        while self.remaining_moves:
            self.make_move(self.remaining_moves.popleft(), keep_order=keep_order)

    @property
    def top_crates(self):
        return ''.join([stack[-1] if stack else ' ' for stack in self.stacks.values()])


if __name__ == '__main__':
    raw_input = fetch_input()
    stacks = Stacks(*parse_input(raw_input))
    # stacks.make_move(stacks.remaining_moves.popleft(), keep_order=True)
    stacks.make_all_moves(keep_order=True)
    stacks.print_stacks()
    print(stacks.top_crates)
