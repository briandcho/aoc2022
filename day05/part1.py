from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    # section top
    lines = (line for line in s.split("\n"))
    rows = []
    n_stacks = 0
    for line in lines:
        if not line:
            break
        row = []
        while line:
            box = line[:4].strip()
            row.append(box)
            line = line[4:]
        if not row[0].isnumeric():
            rows.append(row)
        else:
            n_stacks = len(row)
    stacks = [[] for _ in range(n_stacks)]
    for row in reversed(rows):
        for i, val in enumerate(row):
            if val:
                stacks[i].append(val)

    # section instructions
    for line in lines:
        if not line:
            break
        _, qty, _, src, _, dst = line.split()
        qty = int(qty)
        src = int(src) - 1
        dst = int(dst) - 1
        for _ in range(qty):
            box = stacks[src].pop()
            stacks[dst].append(box)
    return "".join([st[-1][1] for st in stacks])


INPUT_S = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
EXPECTED = "CMZ"


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
