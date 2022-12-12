from __future__ import annotations

import argparse
import math
import os.path

import pytest

import support

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Monkey:
    id: int
    items: List[int]
    fn: Callable[[int, int], int]
    denom: int
    target: Tuple[int, int]
    activity: int = 0


def get_adder(c: int) -> Callable[[int], int]:
    return lambda n: n + c


def get_multiplier(c: int) -> Callable[[int], int]:
    return lambda n: n * c


def parse(s: str) -> List[Monkey]:
    monkeys = []
    lines = iter(line for line in s.split("\n") if line)
    while lines:
        try:
            monkey = int(next(lines).split()[1].strip(":"))
        except:
            break
        items = [int(i) for i in next(lines).split(":")[1].split(",")]
        operand1, op, operand2 = next(lines).split("=")[1].strip().split()
        if operand2 == "old":
            fn = lambda n: n * n
        elif op == "+":
            fn = get_adder(int(operand2))
        else:
            fn = get_multiplier(int(operand2))
        denom = int(next(lines).split()[-1])
        true_monkey = int(next(lines).split()[-1])
        false_monkey = int(next(lines).split()[-1])
        monkeys.append(Monkey(monkey, items, fn, denom, (false_monkey, true_monkey)))
    return monkeys


def do_round(monkeys, fac) -> List[Monkey]:
    for monkey in monkeys:
        for item in monkey.items:
            worry_lvl = monkey.fn(item) % fac
            is_true = worry_lvl % monkey.denom == 0
            target_monkey = monkeys[monkey.target[is_true]]
            target_monkey.items.append(worry_lvl)
            monkey.activity += 1
        monkey.items = []
    return monkeys


def compute(s: str) -> int:
    monkeys = parse(s)
    fac = math.prod([m.denom for m in monkeys])
    for _ in range(10000):
        do_round(monkeys, fac)
    activity = [m.activity for m in monkeys]
    print(monkeys)
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
EXPECTED = 2_713_310_158


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
