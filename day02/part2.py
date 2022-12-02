from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

GAME = {
  "A": {
    "_": 1,  # rock
    "X": [3, "C"],
    "Y": [0, "A"],
    "Z": [6, "B"],
  },
  "B": {
    "_": 2,  # paper
    "X": [6, "A"],
    "Y": [3, "B"],
    "Z": [0, "C"],
  },
  "C": {
    "_": 3,  # scissor
    "X": [0, "B"],
    "Y": [6, "C"],
    "Z": [3, "A"]
  },
  "X": 0,
  "Y": 3,
  "Z": 6,
}


def compute(s: str) -> int:
    score = 0
    for game in s.split("\n"):
        if not game:
            continue
        opponent, outcome = game.split()
        you = GAME[opponent][outcome][1]
        score += GAME[you]["_"] + GAME[outcome]
    return score


INPUT_S = '''\
A Y
B X
C Z'''
EXPECTED = 12


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
