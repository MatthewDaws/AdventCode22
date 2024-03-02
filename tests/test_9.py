import pytest, os

import advent.day9 as day

def test_HeadTail():
    ht = day.HeadTail()
    do_actual_HT_test(ht)

def test_HeadTailMany():
    ht = day.HeadTailMany()
    do_actual_HT_test(ht)

def do_actual_HT_test(ht):
    assert ht.head == (0,0)
    assert ht.tail == (0,0)
    ht.move_head(1,0)
    assert ht.head == (1,0)
    assert ht.tail == (0,0)
    ht.move_head(1,0)
    assert ht.head == (2,0)
    assert ht.tail == (1,0)
    ht.move_head(1,0)
    assert ht.head == (3,0)
    assert ht.tail == (2,0)
    ht.move_head(-1,0)
    assert ht.head == (2,0)
    assert ht.tail == (2,0)
    ht.move_head(0,1)
    assert ht.head == (2,1)
    assert ht.tail == (2,0)
    ht.move_head(0,1)
    assert ht.head == (2,2)
    assert ht.tail == (2,1)
    ht.move_head(1,0)
    assert ht.head == (3,2)
    assert ht.tail == (2,1)
    ht.move_head(1,0)
    assert ht.head == (4,2)
    assert ht.tail == (3,2)


@pytest.fixture
def in1():
    with open(os.path.join("tests", "test9.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.moves) == 8
    assert p.moves[2] == (0,-1,3)

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_walk(eg1):
    t = eg1.walk()
    assert len(t) == 13

def test_walk_2nd(eg1):
    t = eg1.walk(10)
    assert len(t) == 1

@pytest.fixture
def eg2():
    with open(os.path.join("tests", "test9a.txt")) as f:
        return day.Parse(f)
    
def test_walk_2nd_2(eg2):
    assert len(eg2.walk(10)) == 36
