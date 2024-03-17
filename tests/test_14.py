import pytest, os

import advent.day14 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test14.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert p.xrange() == (494, 503)
    assert p.yrange() == (4, 9)

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_map(eg1):
    map = eg1.as_map()
    assert map.xstart == 494
    assert map[0] == [False]*10
    assert map[4] == [False,False,False,False,True,False,False,False,True,True]

@pytest.fixture
def map1(eg1):
    return eg1.as_map()

def test_map_to_string(map1):
    x = str(map1).split("\n")
    assert x[0] == "......+..."
    assert x[1] == ".........."
    assert x[4] == "....#...##"
    assert x[6] == "..###...#."
    assert x[9] == "#########."

def test_drop_one(map1):
    assert map1.dropone() == (500,8)
    assert map1.dropone() == (499,8)
    assert map1.dropone() == (501,8)
    assert map1.dropone() == (500,7)
    assert map1.dropone() == (498,8)
    assert map1.dropone() == (499,7)
    assert map1.dropone() == (501,7)

def test_drop_stops(map1):
    for _ in range(24):
        map1.dropone()
    with pytest.raises(StopIteration):
        map1.dropone()

def test_dropall(map1):
    assert map1.dropall() == 24

def test_expanding_map(map1):
    map = day.ExpandingMap(map1)
    assert map.dropone() == (500,8)
    assert map.dropone() == (499,8)
    assert map.dropone() == (501,8)
    assert map.dropone() == (500,7)
    assert map.dropone() == (498,8)
    assert map.dropone() == (499,7)
    assert map.dropone() == (501,7)
    for _ in range(24-7):
        map.dropone()
    assert map.dropone() == (493, 10)
    assert map.dropone() == (492, 10)

def test_expanding_dropall(map1):
    map = day.ExpandingMap(map1)
    assert map.dropall() == 93

def test_faster_2nd(map1):
    map = day.ExpandingMap(map1)
    assert map.fastall() == 93
