import pytest, os

import advent.day4 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test4.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.pairs) == 6

def test_Range():
    r = day.Range(4, 8)
    assert r.start == 4
    assert r.end == 8
    assert 5 in r
    assert 2 not in r
    r = day.Range(3, 1)
    assert r.start == 1
    assert r.end == 3

def test_Range_contains():
    r = day.Range(4, 8)
    rr = day.Range(4,6)
    assert r.contains(rr)
    assert not rr.contains(r)

def test_Range_equals():
    assert day.Range(4, 8) == day.Range(4, 8)
    assert day.Range(3, 7) != day.Range(2, 5)

def test_Range_intersect():
    r1 = day.Range(4, 8)
    r2 = day.Range(5, 10)
    assert r1.intersect(r2) == day.Range(5, 8)#
    r3 = day.Range(2, 3)
    assert r1.intersect(r3) is None

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_count_fully_contained(eg1):
    assert eg1.count_fully_contained() == 2

def test_count_any_overlap(eg1):
    assert eg1.count_any_overlap() == 4
    