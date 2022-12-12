from __future__ import annotations

import argparse
import os.path

import pytest

import support

from dataclasses import dataclass

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Pos:
    x: int
    y: int


H, W = 0, 0
GRID = []
VISITED = []


def compute(s: str) -> int:
    global GRID, H, W, VISITED
    GRID = [list(line) for line in s.split("\n") if line]
    H, W = len(GRID), len(GRID[0])
    starts = []
    for row in range(H):
        if "S" in GRID[row] or "a" in GRID[row]:
            for col in range(W):
                if GRID[row][col] in ("S", "a"):
                    starts.append(Pos(col, row))
                    GRID[row][col] = "a"
    for row in range(H):
        if "E" in GRID[row]:
            break
    end = Pos(GRID[row].index("E"), row)
    GRID[end.y][end.x] = "z"
    dists = []
    for start in starts:
        path = explore(start, end)
        if path:
            dists += [len(path) - 1]
    return min(dists)


def explore(start, end):
    VISITED = [(["."] * W) for _ in range(H)]
    breadth = [[start]]
    while breadth:
        path = breadth.pop(0)
        node = path[-1]
        if VISITED[node.y][node.x] == ".":
            neighbors = (
                ([Pos(node.x, node.y - 1)] if node.y > 0 else [])
                + ([Pos(node.x, node.y + 1)] if node.y < H - 1 else [])
                + ([Pos(node.x - 1, node.y)] if node.x > 0 else [])
                + ([Pos(node.x + 1, node.y)] if node.x < W - 1 else [])
            )
            neighbors = [
                n
                for n in neighbors
                if ord(GRID[n.y][n.x]) - ord(GRID[node.y][node.x]) <= 1
            ]
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                breadth.append(new_path)
                if neighbor == end:
                    return new_path
            VISITED[node.y][node.x] = "x"
    return []


INPUT_S = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
EXPECTED = 29


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
