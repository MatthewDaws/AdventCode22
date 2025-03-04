import pytest, os

import advent.day24 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test24.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.grid) == 4
    assert len(p.grid[0]) == 6

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_repeat_time(eg1):
    assert eg1.repeat_time == 12

def test_hurricane_positions(eg1):
    assert len(eg1.hurriances) == 19
    assert eg1.hurriances[0] == (0,0,0,1)
    assert eg1.hurriances[2] == (0,3,0,-1)

def test_move_hurricanes(eg1):
    eg1.move_hurricanes()
    assert eg1.hurriances[0] == (0,1,0,1)
    assert eg1.hurriances[2] == (0,2,0,-1)

def test_make_graph(eg1):
    g = eg1.graph()
    assert set(g.neighbours_of((0,-1,0))) == {(1,-1,0), (1,0,0)}
    assert set(g.neighbours_of((1,0,0))) == {(2,0,0), (2,-1,0), (2,1,0)}
    assert set(g.neighbours_of((2,1,0))) == {(3,1,0)}

def test_shortest_path(eg1):
    assert eg1.path() == 18

def test_path_there_and_back(eg1):
    assert eg1.path_there_and_back() == 54


def test_Integer_Priority_Queue():
    q = day.Integer_Priority_Queue()
    assert q.is_empty
    q.add("a", 5)
    assert q.pop() == ("a", 5)
    assert q.is_empty
    q.add("a", 5)
    q.add("b", 10)
    q.add("c", 5)
    e,w = q.pop()
    assert e in "ac"
    assert w == 5
    e,w = q.pop()
    assert e in "ac"
    assert w == 5
    e,w = q.pop()
    assert e == "b"
    assert w == 10
    assert q.is_empty
    q.add("a", 5)
    q.add("b", 10)
    q.add("c", 7)
    q.add("b", 3)
    q.add("c", 4)
    assert q.pop() == ("b",3)
    assert q.pop() == ("c", 4)
    assert q.pop() == ("a", 5)
    assert q.is_empty
