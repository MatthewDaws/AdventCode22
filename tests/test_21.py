import pytest, os

import advent.day21 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test21.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.variables) == 15
    assert p.variables["dbpl"].value == 5
    assert repr(p.variables["ptdq"]) == "Op('humn', '-', 'dvpt')"

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_var(eg1):
    assert eg1.var("dbpl") == 5
    assert eg1.var("ptdq") == 2
    assert eg1.var("root") == 152

# dbpl: 5
# zczc: 2
# dvpt: 3
# lfqf: 4
# humn: 5
# ljgn: 2
# sllz: 4
# hmdt: 32

# ptdq: humn - dvpt
# drzm: hmdt - zczc

# sjmn: drzm * dbpl
# lgvd: ljgn * ptdq

# cczh: sllz + lgvd

# pppw: cczh / lfqf

# root: pppw + sjmn

def test_Solver(eg1):
    s = day.Solver(eg1)
    assert len(s.levels) == 6
    assert len(s.levels[0]) == 8
    assert [len(l) for l in s.levels] == [8,2,2,1,1,1]
    assert list(s.levels[-1]) == ["root"]

@pytest.fixture
def solver1(eg1):
    return day.Solver(eg1)

def test_Solver_call(solver1):
    a,b = solver1(5)
    assert a+b == 152
    a,b = solver1(301)
    assert a == 150
    assert b == 150

def test_Solver_simplify(solver1):
    solver1.simplify()
    assert "drzm" in solver1.levels[0]
    assert "drzm" not in solver1.levels[1]
    assert "sjmn" in solver1.levels[0]
    a,b = solver1(5)
    assert a+b == 152
    a,b = solver1(301)
    assert a == 150
    assert b == 150

def test_Solver_check_div(solver1):
    solver1.check_divs()

def test_Solver_binary_search(solver1):
    assert solver1.binary_search(True) == 301
