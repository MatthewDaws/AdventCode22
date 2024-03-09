import pytest, os
from unittest.mock import MagicMock

import advent.day11 as day

def test_parse_operation():
    cmd = day.Monkey.parse_operation("new = old * 19")
    for x,y in zip([1,2,3,4], [19, 38, 57, 76]):
        assert cmd(x) == y
    cmd = day.Monkey.parse_operation("new = old + 3")
    for x,y in zip([1,2,3,4], [4,5,6,7]):
        assert cmd(x) == y
    cmd = day.Monkey.parse_operation("new = old * old")
    for x,y in zip([1,2,3,4], [1,4,9,16]):
        assert cmd(x) == y
    cmd = day.Monkey.parse_operation("new = old + old")
    for x,y in zip([1,2,3,4], [2,4,6,8]):
        assert cmd(x) == y

def test_parse_test():
    op, arg = day.Monkey.parse_test("divisible by 23")
    assert arg == 23
    for x, r in zip([23,23*2,22,625], [True,True,False,False]):
        assert op(x) == r

def test_check_starts_with_give_rest():
    day.Monkeys.check_starts_with_give_rest("  Oper: 32s", "  Oper: ") == "32s"

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test11.txt")) as f:
        yield f

def test_parse_monkey(in1):
    parent = MagicMock()
    num, monkey = day.Monkeys.parse_monkey(parent, in1)
    assert num == 0
    monkey.take_turn()
    parent.give_to_monkey.assert_any_call(3, 500)
    parent.give_to_monkey.assert_any_call(3, 620)
    assert monkey.divisible_by == 23

def test_parse(in1):
    m = day.Monkeys(in1)
    assert len(m.monkeys) == 4

@pytest.fixture
def eg1(in1):
    return day.Monkeys(in1)

def test_turn(eg1):
    eg1.take_turn()
    assert set(eg1.monkeys[0].items) == {20, 23, 27, 26}
    assert set(eg1.monkeys[1].items) == {2080, 25, 167, 207, 401, 1046}

def test_20_turns(eg1):
    for _ in range(20):
        eg1.take_turn()
    assert eg1.monkeys[0].inspected_count == 101
    assert eg1.monkeys[1].inspected_count == 95
    assert eg1.monkeys[2].inspected_count == 7
    assert eg1.monkeys[3].inspected_count == 105
    assert eg1.monkey_business == 10605

def test_calm_20(eg1):
    eg1.calm()
    for _ in range(20):
        eg1.take_turn()
    assert eg1.monkeys[0].inspected_count == 99
    assert eg1.monkeys[1].inspected_count == 97
    assert eg1.monkeys[2].inspected_count == 8
    assert eg1.monkeys[3].inspected_count == 103
    assert eg1.monkey_business == 103*99

def test_long(eg1):
    eg1.calm()
    for _ in range(10000):
        eg1.take_turn()
    assert eg1.monkey_business == 2713310158
