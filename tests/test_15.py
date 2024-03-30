import pytest, os

import advent.day15 as day

def test_parsexy():
    assert day.Parse.parsexy("x=5, y=7") == (5,7)
    assert day.Parse.parsexy("x=-10, y=-2") == (-10,-2)

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test15.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.data) == 14
    assert p.data[0] == ((2,18), (-2,15))
    
@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_intervals_at_row(eg1):
    list(eg1.intervals_at_row(10))

def test_beacons_in_row(eg1):
    assert eg1.beacons_in_row(10) == 1

def test_row_Length(eg1):
    assert eg1.cannot_be_at_row(10) == 27

def test_find_manual(eg1):
    possible = day.Intervals()
    possible.add(0, 20)
    for y in range(0, 21):
        i = eg1.used_spaces_in_row(y).intersect(possible)
        if y != 11:
            assert i.length() == 21
        else:
            assert i.length() == 20
            assert i.segments == [(0,13), (15,20)]

def test_find(eg1):
    assert eg1.find(20) == (14, 11)

def test_covered(eg1):
    assert eg1.covered(14, 10)
    assert eg1.covered(13, 11)
    assert not eg1.covered(14, 11)

def test_find_faster(eg1):
    assert eg1.faster_find(20) == (14,11)

def test_Intervals():
    i = day.Intervals()
    assert i.segments == []
    i.add(5, 10)
    assert i.segments == [(5,10)]
    assert i.length() == 6
    i.add(12,13)
    assert i.segments == [(5,10), (12,13)]
    assert i.length() == 8
    with pytest.raises(ValueError):
        i.add(2,1)
    i.add(15,20)
    i.add(7,8)
    assert i.segments == [(5,10), (12,13), (15,20)]
    i.add(2,4)
    assert i.segments == [(2,10), (12,13), (15,20)]
    i.add (20,22)
    assert i.segments == [(2,10), (12,13), (15,22)]
    i.add(23,23)
    assert i.segments == [(2,10), (12,13), (15,23)]
    i.add(10,13)
    assert i.segments == [(2,13), (15,23)]
    i.add(10,30)
    assert i.segments == [(2,30)]
    i.add(0,32)
    assert i.segments == [(0,32)]
    assert i.length() == 33
