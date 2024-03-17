import pytest, os

import advent.day13 as day

def test_split():
    assert list(day.MyList.split("1,2,3")) == ["1", "2", "3"]
    assert list(day.MyList.split("[1],[2,3,4]")) == ["[1]", "[2,3,4]"]

def test_parse():
    ml = day.MyList("[1,1,3,1,1]")
    assert str(ml) == "[1,1,3,1,1]"
    ml = day.MyList("5")
    assert str(ml) == "5"
    ml = day.MyList("[[1],[2,3,4]]")
    assert str(ml) == "[[1],[2,3,4]]"

def test_aslist():
    ml = day.MyList("5")
    ml = ml.aslist()
    assert type(ml._content) == list
    assert type(ml._content[0]) == day.MyList
    assert str(ml) == "[5]"
    with pytest.raises(TypeError):
        day.MyList("[1,2]").aslist()

def test_ordering():
    m1 = day.MyList("[1,1,3,1,1]")
    m2 = day.MyList("[1,1,5,1,1]")
    assert m1 <  m2
    m1 = day.MyList("[1,1,5,1,1]")
    assert not m1 < m2
    assert m1 == m2
    m1 = day.MyList("[1,1,7,1,1]")
    assert not m1 < m2
    assert not m1 == m2

def test_ordering2():
    m1 = day.MyList("[2,3,4]")
    m2 = day.MyList("4")
    assert m1 < m2

    m1 = day.MyList("[[1],[2,3,4]]")
    m2 = day.MyList("[[1],4]")
    assert m1 < m2

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test13.txt")) as f:
        yield f

def test_parse_input(in1):
    p = day.Parts(in1)
    assert len(p.pairs) == 8

@pytest.fixture
def eg1(in1):
    return day.Parts(in1)

def test_compares(eg1):
    for (x,y),z in zip(eg1.pairs_as_lists, [True, True, False, True, False, True, False, False]):
        assert (x<y) == z

def test_indices_of_correct(eg1):
    assert list(eg1.indices_of_correct()) == [1,2,4,6]

def test_sort(eg1):
    li = eg1.as_one_list()
    li.append(day.MyList("[[2]]"))
    li.append(day.MyList("[[6]]"))
    li.sort()
    assert str(li[0]) == "[]"
    assert str(li[-1]) == "[9]"
    assert str(li[9]) == "[[2]]"
    assert str(li[13]) == "[[6]]"

def test_places_of_dividers(eg1):
    assert eg1.places_of_dividers() == [10,14]
    