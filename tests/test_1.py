import pytest
import os

import advent.day1 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test1.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.loads) == 5
    assert p.loads[-1] == [10000]

def test_max(eg1):
    p = day.Parse(eg1)
    assert p.maximum_sum() == 24000

def test_topn(eg1):
    p = day.Parse(eg1)
    assert p.sumtop(3) == 45000
    