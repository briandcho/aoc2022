from __future__ import annotations
from collections import namedtuple

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = [line for line in s.split("\n") if line]
    lines.reverse()
    fs = {"/": {}}
    cwd = []
    while lines:
        line = lines.pop()
        if line.startswith("$"):
            cmd, _, arg = line[2:].partition(" ")
            if cmd == "cd":
                if arg == "..":
                    cwd.pop()
                else:
                    cwd.append(arg)
            elif cmd == "ls":
                while lines:
                    ls = lines.pop()
                    if ls.startswith("$"):
                        lines.append(ls)
                        break
                    d = fs
                    for _d in cwd:
                        d = d[_d]
                    c1, _, c2 = ls.partition(" ")
                    if c1 == "dir":
                        if c1 not in d:
                            d[c2] = {}
                    else:
                        d[c2] = int(c1)
    size, dir_sizes = compute_size(fs)
    return sum(dir_sizes)


def compute_size(fs):
    size = 0
    dirs = []
    for k, v in fs.items():
        if isinstance(fs[k], dict):
            d_size, dir_list = compute_size(fs[k])
            size += d_size
            dirs += dir_list
            if d_size < 100_000:
                dirs += [d_size]
        else:
            size += v
    return size, dirs


INPUT_S = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
EXPECTED = 95437


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
