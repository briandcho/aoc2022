from __future__ import annotations

import argparse
import os.path

import pytest

import support

from dataclasses import dataclass
from itertools import zip_longest
from random import randint

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    divider_packets = [[[2]], [[6]]]
    packets = [eval(line) for line in s.split("\n") if line]
    packets = quicksort(packets + divider_packets)
    return (packets.index(divider_packets[0]) + 1) * (
        packets.index(divider_packets[1]) + 1
    )


def quicksort(array):
    if len(array) < 2:
        return array

    low, same, high = [], [], []
    pivot = array[randint(0, len(array) - 1)]
    for item in array:
        res = compare(item, pivot)
        if res < 0:
            low.append(item)
        elif res == 0:
            same.append(item)
        elif res > 0:
            high.append(item)
    return quicksort(low) + same + quicksort(high)


def compare(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        return p1 - p2
    if isinstance(p1, int):
        p1 = [p1]
    elif isinstance(p2, int):
        p2 = [p2]
    for v1, v2 in zip_longest(p1, p2):
        if v1 is None:
            return -1
        if v2 is None:
            return 1
        res = compare(v1, v2)
        if res != 0:
            return res
    return 0


INPUT_S = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
EXPECTED = 140


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
