import pytest, os

import advent.day23 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test23.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.grid) == 7
    assert p.at(1,2) == "#"

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_rotate_dirctions(eg1):
    assert eg1.order == ["N", "S", "W", "E"]
    eg1.rotate_directions()
    assert eg1.order == ["S", "W", "E", "N"]
    eg1.rotate_directions()
    assert eg1.order == ["W", "E", "N", "S"]

def test_proposals(eg1):
    p = eg1.proposals()
    assert p[(0,4)] == (-1,0)
    assert p[(1,2)] == (-1,0)
    assert p[(1,3)] is None
    assert len(p) == 22

def test_new_grid(eg1):
    g = eg1.new_grid(eg1.proposals())
    assert g[0] == ".....#..."
    assert g[1] == "...#...#."
    assert g[2] == ".#..#.#.."
    assert g[3] == ".....#..#"
# ..#.#.##.
# #..#.#...
# #.#.#.##.
# .........
# ..#..#...

def test_iterate(eg1):
    eg1.iterate(1)
    assert eg1.grid[3] == ".....#..#"
    
    eg1.iterate(1)
    assert eg1.grid[0] == "......#...."
# ......#....
# ...#.....#.
# ..#..#.#...
# ......#...#
# ..#..#.#...
# #...#.#.#..
# ...........
# .#.#.#.##..
# ...#..#....

def test_iterate_and_count(eg1):
    eg1.iterate()
    assert eg1.empty_space() == 110

def test_run_to_no_move(eg1):
    assert eg1.run_to_no_move() == 20
    