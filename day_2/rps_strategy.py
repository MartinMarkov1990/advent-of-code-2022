from enum import Enum


class Hand(Enum):
    _ignore_ = ['hand_mapping']

    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def get_hand_from_code(cls, code):
        hand_mapping = {
            'A': cls.ROCK,
            'B': cls.PAPER,
            'C': cls.SCISSORS,
            'X': cls.ROCK,
            'Y': cls.PAPER,
            'Z': cls.SCISSORS
        }
        return hand_mapping[code]


class Outcome(Enum):
    WIN = 6
    DRAW = 3
    LOSS = 0

    @classmethod
    def get_outcome_from_code(cls, code):
        mapping = {
            'X': cls.LOSS,
            'Y': cls.DRAW,
            'Z': cls.WIN
        }
        return mapping[code]


class Game():
    hand_vs_mapping = {
        (Hand.ROCK, Hand.ROCK): Outcome.DRAW,
        (Hand.ROCK, Hand.PAPER): Outcome.WIN,
        (Hand.ROCK, Hand.SCISSORS): Outcome.LOSS,
        (Hand.PAPER, Hand.ROCK): Outcome.LOSS,
        (Hand.PAPER, Hand.PAPER): Outcome.DRAW,
        (Hand.PAPER, Hand.SCISSORS): Outcome.WIN,
        (Hand.SCISSORS, Hand.ROCK): Outcome.WIN,
        (Hand.SCISSORS, Hand.PAPER): Outcome.LOSS,
        (Hand.SCISSORS, Hand.SCISSORS): Outcome.DRAW
    }

    mapping_inverted = {(theirs, outcome): ours for (theirs, ours), outcome in hand_vs_mapping.items()}

    def __init__(self, play, part_1=True):
        self.raw = play
        self.their_move = Hand.get_hand_from_code(play[0])
        if part_1:
            self.our_move = Hand.get_hand_from_code(play[1])
            self.calculate_outcome()
        else:
            self.outcome = Outcome.get_outcome_from_code(play[1])
            self.calculate_our_move()
        self.calculate_points()

    def calculate_outcome(self):
        self.outcome = Game.hand_vs_mapping[(self.their_move, self.our_move)]

    def calculate_points(self):
        self.points = self.outcome.value + self.our_move.value

    def calculate_our_move(self):
        self.our_move = self.mapping_inverted[(self.their_move, self.outcome)]

    def __str__(self):
        return f"Their move: {self.their_move}; our move: {self.our_move}. Outcome: {self.outcome}. Points: {self.points}. Raw input: {self.raw}"


def fetch_plays(file='input.txt') -> list[list]:
    with open(file, 'r') as f:
        raw = f.readlines()
    return [row.replace('\n', '').split(' ') for row in raw]


def make_games(plays, part_1=True) -> list[Game]:
    return [Game(play, part_1=part_1) for play in plays]


if __name__ == '__main__':
    plays = fetch_plays()
    games = make_games(plays, part_1=False)
    for game in games:
        print(game)
    total_points = sum([game.points for game in games])
    print(total_points)
