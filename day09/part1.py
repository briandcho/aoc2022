from __future__ import annotations
from dataclasses import dataclass

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Pos:
    x: int
    y: int


MV_HEAD = {
  "D": lambda pos: Pos(pos.x, pos.y - 1),
  "L": lambda pos: Pos(pos.x - 1, pos.y),
  "R": lambda pos: Pos(pos.x + 1, pos.y),
  "U": lambda pos: Pos(pos.x, pos.y + 1)
}

MV_TAIL = {
  "D": lambda head, tail: Pos(head.x, head.y + 1) if tail.y - head.y > 1 else tail,
  "L": lambda head, tail: Pos(head.x + 1, head.y) if tail.x - head.x > 1 else tail,
  "R": lambda head, tail: Pos(head.x - 1, head.y) if head.x - tail.x > 1 else tail,
  "U": lambda head, tail: Pos(head.x, head.y - 1) if head.y - tail.y > 1 else tail
}

def compute(s: str) -> int:
    lines = [line for line in s.split("\n") if line]
    head = Pos(0, 0)
    tail = Pos(0, 0)
    grid = [[0 for _ in range(1024)] for _ in range(1024)]
    for line in lines:
        direction, dist = line.split()
        dist = int(dist)
        for _ in range(dist):
            head = MV_HEAD[direction](head)
            tail = MV_TAIL[direction](head, tail)
            grid[tail.x][tail.y] = 1
    n_visited = sum([sum(grid[i]) for i in range(len(grid))])
    return n_visited


INPUT_S = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
EXPECTED = 13


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
