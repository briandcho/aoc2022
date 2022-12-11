from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    monkeys = [[] for _ in range(8)]
    activity = [0] * 8
    for round in range(20):
        lines = iter(line for line in s.split("\n") if line)
        while lines:
            try:
                monkey = int(next(lines).split()[1].strip(":"))
            except:
                break
            items = [int(i) for i in next(lines).split(":")[1].split(",")]
            operand1, op, operand2 = next(lines).split("=")[1].strip().split()
            denom = int(next(lines).split()[-1])
            true_monkey = int(next(lines).split()[-1])
            false_monkey = int(next(lines).split()[-1])
            if round == 0:
                items += monkeys[monkey]
            else:
                items = monkeys[monkey]
            activity[monkey] += len(items)
            monkeys[monkey] = []
            for item in items:
                o1 = item if operand1 == "old" else int(operand1)
                o2 = item if operand2 == "old" else int(operand2)
                if op == "*":
                    worry_lvl = o1 * o2 // 3
                elif op == "+":
                    worry_lvl = (o1 + o2) // 3
                else:
                    raise AssertionError(f"unknown op '{op}'")
                if worry_lvl % denom == 0:
                    monkeys[true_monkey].append(worry_lvl)
                else:
                    monkeys[false_monkey].append(worry_lvl)
    activity.sort(reverse=True)
    return activity[0] * activity[1]


INPUT_S = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
EXPECTED = 10605


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
