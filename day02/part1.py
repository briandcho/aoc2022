from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

GAME = {
  "A": {
    "_": 1,
    "X": 3,
    "Y": 0,
    "Z": 6,
  },
  "B": {
    "_": 2,  # paper
    "X": 6,
    "Y": 3,
    "Z": 0,
  },
  "C": {
    "_": 3,  # scissor
    "X": 0,
    "Y": 6,
    "Z": 3,
  },
  "X": {
    "_": 1,
    "A": 3,
    "B": 0,
    "C": 6,
  },
  "Y": {
    "_": 2,  # paper
    "A": 6,
    "B": 3,
    "C": 0,
  },
  "Z": {
    "_": 3,  # scissor
    "A": 0,
    "B": 6,
    "C": 3,
  }
}


def compute(s: str) -> int:
    p1_score, p2_score = 0, 0
    for game in s.split("\n"):
        if not game:
            continue
        p1, p2 = game.split()
        p1_score += GAME[p1]["_"] + GAME[p1][p2]
        p2_score += GAME[p2]["_"] + GAME[p2][p1]
    return p2_score


INPUT_S = '''\
A Y
B X
C Z'''
EXPECTED = 15


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
