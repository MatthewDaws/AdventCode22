import pytest, os

import advent.day25 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test25.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.data) == 13
    assert p.data[2] == "2=0="

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_Snafu_to_int():
    s = day.Snafu("11")
    assert int(s) == 6
    assert int(day.Snafu("1=11-2")) == 2022

def test_Snafu_from_int():
    s = day.Snafu(8)
    assert str(s) == "2="
    assert str(day.Snafu(9)) == "2-"

def test_Snafu_from_to_int():
    for n in range(1,1000):
        s = day.Snafu(n)
        assert int(s) == n

def test_sum(eg1):
    assert eg1.sum() == "2=-1=0"
