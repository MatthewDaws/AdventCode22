import pytest, os

import advent.day18 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test18.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.locations) == 13
    assert p.locations[2] == [3,2,2]

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_neighbours_occupied(eg1):
    assert eg1.neighbours_occupied((2,2,2)) == 6

def test_surface_area(eg1):
    assert eg1.surface_area() == 64

def test_size(eg1):
    assert eg1.size == 7

def test_walk_from(eg1):
    assert eg1.walk_from((2,2,5)) == {(2,2,5)}

def test_in_contact_with_boundary(eg1):
    b = eg1.walk_from((0,0,0))
    assert eg1.in_contact_with_boundary(b)

def test_find_interior(eg1):
    assert eg1.find_interior() == {(2,2,5)}

def test_surface_area_interior(eg1):
    assert eg1.surface_area_interior() == 6
    