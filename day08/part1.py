from __future__ import annotations
from collections import namedtuple

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
    for i in range(1, len(grid[0]) - 1):
        for j in range(1, len(grid) - 1):
            los_up = [grid[row][j] for row in reversed(range(i))]
            los_down = [grid[row][j] for row in (range(i + 1, len(grid)))]
            los_left = [grid[i][col] for col in reversed(range(j))]
            los_right = [grid[i][col] for col in (range(j + 1, len(grid[i])))]
            if (
                grid[i][j] > max(los_up)
                or grid[i][j] > max(los_down)
                or grid[i][j] > max(los_left)
                or grid[i][j] > max(los_right)
            ):
                n_visible += 1
    return n_visible


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 21


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
