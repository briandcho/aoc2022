from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

GAME = {
    "X": {"_": 1, "A": 3, "B": 0, "C": 6},  # rock
    "Y": {"_": 2, "A": 6, "B": 3, "C": 0},  # paper
    "Z": {"_": 3, "A": 0, "B": 6, "C": 3},  # scissor
}


def compute(s: str) -> int:
    score = 0
    for game in s.split("\n"):
        if not game:
            continue
        opponent, you = game.split()
        score += GAME[you]["_"] + GAME[you][opponent]
    return score


INPUT_S = """\
A Y
B X
C Z"""
EXPECTED = 15


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
