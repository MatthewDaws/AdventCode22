import pytest, os

import advent.day20 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test20.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.numbers) == 7
    assert p.numbers[0] == 1
    assert p.numbers[-1] == 4

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def process_in(li):
    return list(enumerate(li))

def process_out(li):
    return [x[1] for x in li]

def test_mix(eg1):
    li = [1, 2, -3, 3, -2, 0, 4]
    li = eg1.mix(process_in(li), 0)
    assert process_out(li) == [2,1,-3,3,-2,0,4]
    li = eg1.mix(li, 3)
    assert process_out(li) == [2,1,-3,-2,0,4,3]
    li = [4, -2, 5, 6, 7, 8, 9]
    li = eg1.mix(process_in(li), 1)
    assert process_out(li) == [4, 5, 6, 7, 8, -2, 9]
    li = [1, 2, -3, 0, 3, 4, -2]
    li = eg1.mix(process_in(li), 5)
    assert process_out(li) == [1, 2, -3, 4, 0, 3, -2]
    li = [1, -3, 2, 3, -2, 0, 4]
    li = eg1.mix(process_in(li), 1)
    assert process_out(li) == [1, 2, 3, -2, -3, 0, 4]

def test_mix_all(eg1):
    assert eg1.mix_all() == [1, 2, -3, 4, 0, 3, -2]

def test_at_index_with_wrap(eg1):
    li = eg1.mix_all()
    assert eg1.at_index_with_wrap(li, 1004) == 4
    assert eg1.at_index_with_wrap(li, 2004) == -3
    assert eg1.at_index_with_wrap(li, 3004) == 2

def test_code_sum(eg1):
    assert eg1.code_sum() == 3
    
def test_mix_all_with_decrypt(eg1):
    assert eg1.mix_all(True, 0) == [811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612]
    assert eg1.mix_all(True) == [0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153]
    assert eg1.mix_all(True, 10) == [0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153]

def test_code_sum_with_decrypt(eg1):
    assert eg1.code_sum(True, 10) == 1623178306
