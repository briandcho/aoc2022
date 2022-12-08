from __future__ import annotations
from collections import namedtuple
from itertools import takewhile

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = [line for line in s.split("\n") if line]
    grid = []
    for line in lines:
        grid.append([int(c) for c in line])
    n_visible = len(grid) * 2 + (len(grid[0]) - 2) * 2
    best_view = 0
    for i in range(1, len(grid[0]) - 1):
        for j in range(1, len(grid) - 1):
            los_up = []
            for row in reversed(range(i)):
                los_up.append(grid[row][j])
                if grid[i][j] <= grid[row][j]:
                    break
            los_down = []
            for row in range(i + 1, len(grid)):
                los_down.append(grid[row][j])
                if grid[i][j] <= grid[row][j]:
                    break
            los_left = []
            for col in reversed(range(j)):
                los_left.append(grid[i][col])
                if grid[i][j] <= grid[i][col]:
                    break
            los_right = []
            for col in range(j + 1, len(grid[i])):
                los_right.append(grid[i][col])
                if grid[i][j] <= grid[i][col]:
                    break
            best_view = max(
                [
                    len(los_up) * len(los_down) * len(los_left) * len(los_right),
                    best_view,
                ]
            )
    return best_view


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 8


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
