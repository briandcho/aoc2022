from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

GAME = {
    "A": {"X": 3, "Y": 1, "Z": 2},
    "B": {"X": 1, "Y": 2, "Z": 3},
    "C": {"X": 2, "Y": 3, "Z": 1},
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
        score += GAME[opponent][outcome] + GAME[outcome]
    return score


INPUT_S = """\
A Y
B X
C Z"""
EXPECTED = 12


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
