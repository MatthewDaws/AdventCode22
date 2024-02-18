import pytest, os

import advent.day3 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test3.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.lines) == 6
    assert p.lines[0] == ("vJrwpWtwJgWr", "hcsFMMfFFhFp")

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_commons(eg1):
    assert list(eg1.commons()) == ["p", "L", "P", "v", "t", "s"]

def test_to_priority():
    assert day.Parse.to_priority("a") == 1
    assert day.Parse.to_priority("z") == 26
    assert day.Parse.to_priority("A") == 27
    assert day.Parse.to_priority("Z") == 52
    assert day.Parse.to_priority("c") == 3
    assert day.Parse.to_priority("Y") == 51
    with pytest.raises(ValueError):
        day.Parse.to_priority("1")

def test_sum(eg1):
    assert eg1.sum() == 157

def test_triples(eg1):
    assert list(eg1.triples()) == ["r", "Z"]

def test_triple_sum(eg1):
    assert eg1.triple_sum() == 70
    