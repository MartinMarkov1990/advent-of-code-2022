import logging
from dataclasses import dataclass
from enum import Enum

from anytree import NodeMixin


class Direction(Enum):
    D = 'D'
    U = 'U'
    L = 'L'
    R = 'R'


@dataclass
class Point:
    x: int
    y: int

    def copy(self):
        return Point(self.x, self.y)


class Knot(Point, NodeMixin):
    def __init__(self, name, x, y, parent=None, children=None):
        self.name = name
        self.x = x
        self.y = y
        self.parent = parent
        if children:
            self.children = children

    def update_position(self):
        if self.parent:
            diff = Point(self.parent.x - self.x, self.parent.y - self.y)
            if abs(diff.x) >= 2 or (abs(diff.x) == 1 and abs(diff.y) >= 2):
                self.x += sign(diff.x)
            if abs(diff.y) >= 2 or (abs(diff.y) == 1 and abs(diff.x) >= 2):
                self.y += sign(diff.y)
        for child in self.children:
            child.update_position()


@dataclass
class Move:
    direction: Direction
    steps: int


def sign(n: float):
    return 1 if n >= 0 else -1


class Rope:
    starting_position = Point(0, 0)
    no_knots = 2

    def __init__(self, moves: list[Move], no_knots=2):
        self.moves = moves
        self.head = Knot('H', self.starting_position.x, self.starting_position.y)
        self.knots = [self.head]
        for i in range(1, no_knots):
            self.knots.append(Knot(str(i), self.starting_position.x, self.starting_position.y, parent=self.knots[i-1]))
        self.visited_tails = {(self.knots[-1].x, self.knots[-1].y)}

    def make_step(self, direction: Direction):
        # This needs to be on the rope level in order to record visited_tails
        # Otherwise it makes slightly more sense on the Knot level
        match direction:
            case Direction.D:
                self.head.y += 1
            case Direction.U:
                self.head.y -= 1
            case Direction.L:
                self.head.x -= 1
            case Direction.R:
                self.head.x += 1
        self.update_tail()

    def make_move(self, move: Move):
        for i in range(move.steps):
            self.make_step(move.direction)
        logging.info("; ".join([f"{knot.name}: {knot.x}, {knot.y}" for knot in self.knots]))

    def update_tail(self):
        self.knots[1].update_position()
        self.visited_tails.add((self.knots[-1].x, self.knots[-1].y))

    def make_all_moves(self):
        for move in self.moves:
            self.make_move(move)


def fetch_input(file='input.txt'):
    return [line.replace('\n', '') for line in open(file, 'r')]


def parse_to_moves(input: list[str]) -> list[Move]:
    return [Move(Direction(line.split(' ')[0]), int(line.split(' ')[1])) for line in input]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    input = fetch_input()
    moves = parse_to_moves(input)
    # part 1
    rope = Rope(moves)
    rope.make_all_moves()
    print('Total points visited by tail: ', len(rope.visited_tails))
    # part 2
    rope = Rope(moves, 10)
    rope.make_all_moves()
    print('Total points visited by tail: ', len(rope.visited_tails))
