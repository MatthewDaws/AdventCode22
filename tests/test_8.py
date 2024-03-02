import pytest, os

import advent.day8 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test8.txt")) as f:
        yield f

def test_Parse(in1):
    grid = day.Parse(in1)
    assert grid.num_cols == 5
    assert grid.num_rows == 5
    assert grid.get(0,0) == 3
    assert grid.get(3,4) == 9

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_outside(eg1):
    assert not eg1.outside(0,0)
    assert eg1.outside(-1,0)
    assert eg1.outside(1,-2)
    assert eg1.outside(2,5)
    assert eg1.outside(5,3)

def test_is_visible(eg1):
    assert eg1.is_visible(0,0,(-1,0))
    assert eg1.is_visible(0,0,(0,-1))
    assert not eg1.is_visible(0,0,(1,0))
    assert not eg1.is_visible(0,0,(0,1))
    assert eg1.is_visible(1,1)
    assert not eg1.is_visible(2,2)

def test_count_visible(eg1):
    assert eg1.count_visible() == 21

def test_scan_count(eg1):
    assert eg1.scan_count() == 21

def test_scan_most_recent_highest(eg1):
    out = [[None for _ in range(5)] for _ in range(5)]
    eg1.scan_most_recent_highest(0,0,0,1,5,5,out)
    assert out[0] == [0, 1, 2, 3, 1]

def test_scenic_score(eg1):
    scenic = eg1.find_scenic_score()
    assert scenic[0][0] == 0
    assert scenic[1][1] == 1
    assert scenic[1][2] == 4
    assert scenic[3][2] == 8
