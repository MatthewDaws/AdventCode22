import pytest, os

import advent.day12 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test12.txt")) as f:
        yield f

def test_parse(in1):
    m = day.Mountain(in1)
    assert m.start == (0,0)
    assert m.end == (2,5)
    assert m.numrows == 5
    assert m.numcols == 8

@pytest.fixture
def eg1(in1):
    return day.Mountain(in1)

def test_height(eg1):
    assert eg1.height(0,0) == 0
    assert eg1.height(2,5) == 25
    assert eg1.height(1,2) == 2

def test_canmove(eg1):
    assert eg1.can_move((0,0),(0,1))
    assert eg1.can_move((0,0),(1,0))
    assert not eg1.can_move((0,0),(-1,0))
    assert not eg1.can_move((0,0),(0,-1))
    assert not eg1.can_move((2,2),(0,1))

def test_find_path(eg1):
    assert eg1.find_path() == 31

def test_find_actual_path(eg1):
    path = eg1.find_actual_path()
    assert path[0] == (0,0)
    assert path[31] == (2,5)

def test_backwards(eg1):
    eg1.find_paths(backwards=True)
    assert eg1.minimal_path_length_to(0,0) == 31

def test_find_shortest_path_from_ground(eg1):
    eg1.find_paths(backwards=True)
    assert eg1.find_shortest_path_from_ground() == 29
