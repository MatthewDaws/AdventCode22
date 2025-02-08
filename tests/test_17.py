import pytest, os

import advent.day17 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test17.txt")) as f:
        yield f

def test_parse(in1):
    j = day.Jets(in1)
    assert j[0] == ">"
    assert j[3] == "<"

@pytest.fixture
def eg1(in1):
    return day.Jets(in1)

def test_Jets_iter(eg1):
    x = list(zip(eg1, range(100)))
    assert x[0] == (">", 0)
    assert x[10] == ("<", 10)
    assert x[12] == (">", 12)
    
def test_height(eg1):
    assert eg1.height == 0

def test_place(eg1):
    eg1.place(1, 2, 0)
    assert eg1.height == 3
    eg1.place(2, 3, 2)
    assert eg1.height == 6

def test_overlaps(eg1):
    assert not eg1.overlaps(2, 3, 0)
    assert not eg1.overlaps(3, 3, 0)
    assert eg1.overlaps(4, 3, 0)
    assert eg1.overlaps(5, 3, 0)
    assert eg1.overlaps(-1, 2, 0)

def test_drop(eg1):
    eg1.drop(0)
    assert eg1.height == 1
    assert not eg1.space_used(0, 0)
    assert not eg1.space_used(0, 1)
    assert eg1.space_used(0, 2)

def test_drop_many(eg1):
    eg1.drop_many(2022)
    assert eg1.height == 3068

def test_find_period(eg1):
    assert eg1.find_period() == (2,7)

def test_find_period_new(eg1):
    assert eg1.find_period_new() == (9,72, 7,53)
    eg1.reset()
    eg1.drop_many(9*5)
    assert eg1.height == 72
    for _ in range(10):
        start = eg1.height
        eg1.drop_many(7*5)
        assert eg1.height - start == 53

def test_drop_very_many_new(eg1):
    assert eg1.drop_very_many_new(2022) == 3068
    assert eg1.drop_very_many_new(1000000000000) == 1514285714288
