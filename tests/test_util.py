import pytest

import advent.util as util

def test_lcm():
    assert util.lcm(1, 5) == 5
    assert util.lcm(5, 7) == 35
    assert util.lcm(4, 6) == 12

def test_bezout():
    s, t = util.bezout(1, 5)
    assert s*1 + t*5 == 1

    s, t = util.bezout(5, 10)
    assert s*5 + t*10 == 5

    s, t = util.bezout(3, 9)
    assert s*3 + t*9 == 3

    s, t = util.bezout(15, 35)
    assert s*15 + t*35 == 5

def test_brute_force_chinese_remainder():
    assert util.brute_force_chinese_remainder([(5,2)]) == 1
    assert util.brute_force_chinese_remainder([[5, 2], [7, 3]]) == 1
    assert util.brute_force_chinese_remainder([(1, 7), (3, 10), (5, 17)]) == 1093
    with pytest.raises(ValueError):
        util.brute_force_chinese_remainder([(5, 8), (102, 7), (162, 6)])

def test_chinese_remainder_single():
    assert util.chinese_remainder([(5, 2)]) == (1, 2)

def test_chinese_remainder():
    assert util.chinese_remainder([[5, 2], [7, 3]]) == (1, 6)
    td = [(1, 7), (3, 10), (5, 17)]
    assert util.chinese_remainder(td) == (util.brute_force_chinese_remainder(td), 7*10*17)
    with pytest.raises(ValueError):
        assert util.chinese_remainder([(5, 8), (102, 7), (162, 6)])

def test_Interval():
    i = util.Interval(10, 15)
    assert i.contains(10)
    assert i.contains(15)
    assert i.contains(12)
    assert not i.contains(8)
    assert repr(i) == "Interval(10,15)"

    with pytest.raises(ValueError):
        util.Interval(10, 8)

    i = util.Interval.from_start_length(10, -3)
    assert repr(i) == "Interval(7,10)"

    j = util.Interval(5, 12)
    assert j < i
    assert j <= i
    assert i > j
    assert i >= j
    assert not i==j
    assert hash(i) != hash(j)
    assert i==i
    assert i<=i
    assert i>=i

    assert i.intersect(j) == util.Interval(7,10)


@pytest.fixture
def graph1():
    g = util.Graph()
    for i in range(4):
        g.add_vertex(i)
    g.add_directed_edge(0,1)
    g.add_directed_edge(0,2)
    g.add_directed_edge(1,3)
    g.add_directed_edge(2,3)
    return g

def test_Graph(graph1):
    assert graph1.vertices == [0,1,2,3]
    assert graph1.neighbours_of(0) == [1,2]
    assert graph1.neighbours_of(1) == [3]
    assert graph1.neighbours_of(2) == [3]
    assert graph1.neighbours_of(3) == []

    with pytest.raises(ValueError):
        graph1.add_vertex(2)
    with pytest.raises(KeyError):
        graph1.neighbours_of(5)

def test_TopSort(graph1):
    ts = util.topological_sort(graph1)
    assert (ts == [0,1,2,3] or ts == [0,2,1,3])

    graph1.add_directed_edge(3,0)
    with pytest.raises(ValueError):
        util.topological_sort(graph1)

def test_Weighted_Graph():
    g = util.WeightedGraph()
    for i in range(4):
        g.add_vertex(i)
    g.add_directed_edge(0,1,5)
    g.add_directed_edge(0,2,3)

    assert g.neighbours_of(0) == [1, 2]
    assert list(g.weighted_neighbours_of(0)) == [(1,5), (2,3)]

def test_shortest_path_dag():
    g = util.WeightedGraph()
    for i in range(6):
        g.add_vertex(i)
    for s,e,l in [(0,1,5), (0,2,7), (1,3,10), (1,4,2), (2,3,4), (3,5,2), (4,5,4)]:
        g.add_directed_edge(s,e,l)
    dists, preds = util.shortest_path_dag(g, 0)
    assert dists == [0,5,7,11,7,11]
    assert preds == [None,0,0,2,1,4]

def test_integer_sqroot():
    with pytest.raises(ValueError):
        util.integer_sqrt(-1)
    for n in range(1000):
        x = util.integer_sqrt(n)
        assert x*x <= n < (x+1)*(x+1)

def test_integer_quad():
    assert util.integer_quadratic(1,2,1) == [-1]
    assert util.integer_quadratic(5,5,-30) == [-3,2]
    assert util.integer_quadratic(1,2,3) == []
    assert util.integer_quadratic(6,1,-2) == []
    assert util.integer_quadratic(0, 12288, -577536) == [47]
    assert util.integer_quadratic(-3,3,60) == [-4, 5]
    assert util.integer_quadratic(5, -62, 185) == [5]

def test_Vector():
    v = util.Vector(1,2,3)
    u = util.Vector(5,8,10)
    assert v.x == 1
    assert u.y == 8
    assert v.z == 3
    assert u*v == 51 and v*u == 51
    assert u+v == util.Vector(6,10,13)
    assert u-v == util.Vector(4,6,7)
    assert -u == util.Vector(-5,-8,-10)
    assert 3 * v == util.Vector(3,6,9)
    assert v @ u == util.Vector(-4, 5, -2)

    assert not u.is_null()
    w = util.Vector(0,0,0)
    assert w.is_null()

def test_inverse_mod_n():
    x = util.inverse_modn(5, 7)
    assert (5*x) % 7 == 1
    with pytest.raises(ValueError):
        util.inverse_modn(5, 10)

def test_DisjointUnion():
    d = util.DisjointSet("abcd")
    assert d.entries == {"a", "b", "c", "d"}

    d = util.DisjointSet()
    d.add(1)
    d.add(5)
    d.add(7)
    d.add(7)
    assert d.entries == {5,7,1}
    assert d.as_sets() == { frozenset({x}) for x in [1,5,7] }
    assert d.contains(5)
    assert not d.contains(2)

    assert d.find(1) != d.find(7)
    assert d.find(1) == d.find(1)
    with pytest.raises(KeyError):
        d.find(2)

    d.union(1,7)
    assert d.find(1) == d.find(7)
    assert d.find(1) != d.find(5)
    with pytest.raises(KeyError):
        d.union(1,2)
    assert d.as_sets() == { frozenset({1,7}), frozenset({5}) }
    d.union(5,7)
    assert d.find(1) == d.find(7)
    assert d.find(1) == d.find(5)
    d.union(1,7)
    assert d.as_sets() == { frozenset({1,5,7}) }
    assert d.find_depth() == 1

    d = util.DisjointSet(range(100))
    for x in range(1,100):
        d.union(0, x)
    ss = list(d.as_sets())
    assert len(ss) == 1
    assert len(ss[0]) == 100
    assert d.find_depth() == 1

def test_Kruskal():
    A="A"
    B="B"
    C="C"
    D="D"
    E="E"
    F="F"
    G="G"
    edges = [(A,D), (C,E), (D,F), (A,B), (B,E), (B,C), (E,F), (D,B), (G,E), (G,F), (E,D)]
    tree = util.Kruskal(edges)
    assert tree == [(A,D), (C,E), (D,F), (A,B), (B,E), (G,E)]

def test_shortest_path_unweighted():
    g = util.Graph()
    for x in range(6):
        g.add_vertex(x)
    for x in range(5):
        g.add_directed_edge(x, x+1)
    g.add_directed_edge(3,5)

    distances, prev = util.shortest_path_unweighted(g, 0)
    assert distances[5] == 4
    assert distances[4] == 4
    assert distances[3] == 3
    assert prev[5] == 3

    distances, prev = util.shortest_path_unweighted(g, 4)
    assert distances[5] == 1
    assert distances[4] == 0
    assert distances[3] == None
    