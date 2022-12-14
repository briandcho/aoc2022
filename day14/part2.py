from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

from dataclasses import dataclass
from itertools import zip_longest
from pprint import pprint as pp

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
UP, DOWN, LEFT, RIGHT = 1, -1, -2, 2


@dataclass
class Pos:
    x: int
    y: int


NEXT_POS = {
    UP: lambda p: Pos(p.x, p.y - 1),
    DOWN: lambda p: Pos(p.x, p.y + 1),
    LEFT: lambda p: Pos(p.x - 1, p.y),
    RIGHT: lambda p: Pos(p.x + 1, p.y),
}
HEIGHT, WIDTH, OFFSET = 0, 0, 0


def compute(s: str) -> int:
    global HEIGHT, WIDTH, OFFSET
    structs = [line for line in s.split("\n") if line]
    rock_paths = []
    for struct in structs:
        rock_path = []
        for s in re.split(r"\s->\s", struct):
            rock_path.append(Pos(*[int(n) for n in s.split(",")]))
        rock_paths.append(rock_path)
    HEIGHT = max(p.y for rock_path in rock_paths for p in rock_path) + 1 + 2
    OFFSET = min(p.x for rock_path in rock_paths for p in rock_path) - HEIGHT
    WIDTH = (
        max(p.x for rock_path in rock_paths for p in rock_path) - OFFSET + 1 + HEIGHT
    )
    rock_paths.append([Pos(OFFSET, HEIGHT - 1), Pos(OFFSET + WIDTH - 1, HEIGHT - 1)])
    cave = [["."] * WIDTH for _ in range(HEIGHT)]
    for rock_path in rock_paths:
        start = rock_path.pop(0)
        while rock_path:
            end = rock_path.pop(0)
            direction = (
                UP
                if start.y - end.y > 0
                else DOWN
                if start.y - end.y < 0
                else LEFT
                if start.x - end.x > 0
                else RIGHT
            )
            p = start
            while True:
                cave[p.y][p.x - OFFSET] = "#"
                p = NEXT_POS[direction](p)
                if p == end:
                    cave[p.y][p.x - OFFSET] = "#"
                    break
            start = end
    n = 0
    while pour_one(cave, Pos(500 - OFFSET, 0)):
        n += 1
    return n


def pour_one(cave, entry):
    p = entry
    while p.y < HEIGHT - 1 and 0 < p.x < WIDTH - 1 and cave[p.y][p.x] == ".":
        next_p = NEXT_POS[DOWN](p)
        if cave[next_p.y][next_p.x] != ".":
            left_p, right_p = NEXT_POS[LEFT](next_p), NEXT_POS[RIGHT](next_p)
            if cave[left_p.y][left_p.x] == ".":
                return pour_one(cave, left_p)
            if cave[right_p.y][right_p.x] == ".":
                return pour_one(cave, right_p)
            cave[p.y][p.x] = "o"
            return True
        p = next_p
    return False


INPUT_S = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
EXPECTED = 93


@pytest.mark.parametrize(("input_s", "expected"), ((INPUT_S, EXPECTED),))
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
