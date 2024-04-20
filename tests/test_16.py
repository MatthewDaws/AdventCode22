import pytest, os

import advent.day16 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test16.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.data) == 10
    assert p.data[0] == ("AA", 0, ["DD", "II", "BB"])
    assert p.data[9] == ("JJ", 21, ["II"])

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_full_graph(eg1):
    g = eg1.full_graph()
    assert set(g.vertices) == {x+x for x in "ABCDEFGHIJ"}
    assert set(g.neighbours_of("AA")) == {"BB", "DD", "II"}

def test_flow_rate(eg1):
    assert eg1.flow_rate("AA") == 0
    assert eg1.flow_rate("BB") == 13

def test_graph(eg1):
    rn = eg1.reduced_graph()
    assert set(rn.graph.vertices) == {"BB", "CC", "DD", "EE", "HH", "JJ"}
    assert set(rn.graph.weighted_neighbours_of("BB")) == {("BB",0), ("CC", 1), ("DD",2), ("EE",3), ("HH",6), ("JJ",3)}
    assert rn.from_start["BB"] == 1
    assert rn.from_start["HH"] == 5

@pytest.fixture
def rn1(eg1):
    return eg1.reduced_graph()

def test_total_flow(rn1):
    assert rn1.total_flow(["DD", "BB", "JJ", "HH", "EE", "CC"]) == 1651

def test_search_best_flow(rn1):
    f, r = rn1.search_best_flow()
    assert f == 1651
    assert list(r) == ["DD", "BB", "JJ", "HH", "EE", "CC"]
    
def test_backtrack(rn1):
    bt = rn1.to_backtrack()
    assert bt.solve() == 1651

def test_multi_backtrace(rn1):
    bt = rn1.to_backtrack()
    assert bt.multisolve(starttime=30, agents=1) == 1651
    assert bt.multisolve() == 1707
