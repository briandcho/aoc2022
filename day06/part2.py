from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    marker = ""
    for c in s:
        if c in marker:
            marker = marker[marker.index(c) + 1 :]
        marker += c
        if len(marker) == 4:
            break
    for c in s:
        if c in marker:
            marker = marker[marker.index(c) + 1 :]
        marker += c
        if len(marker) == 14:
            break
    return s.index(marker) + 14


INPUT_S = """\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""
EXPECTED = 19


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S, EXPECTED),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
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
