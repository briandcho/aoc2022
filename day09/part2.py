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
    "U": lambda pos: Pos(pos.x, pos.y + 1),
}


def compute(s: str) -> int:
    lines = [line for line in s.split("\n") if line]
    rope = [Pos(0, 0) for _ in range(10)]
    grid = [[0 for _ in range(1024)] for _ in range(1024)]
    for line in lines:
        direction, dist = line.split()
        dist = int(dist)
        for _ in range(dist):
            for i, knot in enumerate(rope):
                if i == 0:
                    pos = MV_HEAD[direction](knot)
                    knot.x, knot.y = pos.x, pos.y
                else:
                    prev = rope[i - 1]
                    x_dist = prev.x - knot.x
                    y_dist = prev.y - knot.y
                    if x_dist > 1:  # Right
                        knot.x += 1
                        if y_dist != 0:
                            knot.y += 1 if y_dist > 0 else -1
                    elif x_dist < -1:  # Left
                        knot.x -= 1
                        if y_dist != 0:
                            knot.y += 1 if y_dist > 0 else -1
                    elif y_dist > 1:  # Up
                        knot.y += 1
                        if x_dist != 0:
                            knot.x += 1 if x_dist > 0 else -1
                    elif y_dist < -1:  # Down
                        knot.y -= 1
                        if x_dist != 0:
                            knot.x += 1 if x_dist > 0 else -1
                    else:
                        break
            grid[rope[-1].x][rope[-1].y] = 1
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
EXPECTED = 1

INPUT_S2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
EXPECTED2 = 36


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (INPUT_S2, EXPECTED2),
    ),
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
