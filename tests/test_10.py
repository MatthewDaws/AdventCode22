import pytest, os

import advent.day10 as day

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test10.txt")) as f:
        yield f

def test_parse(in1):
    p = day.RegisterMachine(in1)
    assert len(p.commands) == 3
    assert p.commands[0].cmd == day.Commands.NOOP
    assert p.commands[1].cmd == day.Commands.ADDX
    assert p.commands[1].data == 3

@pytest.fixture
def eg1(in1):
    return day.RegisterMachine(in1)

def test_step(eg1):
    assert eg1.X == 1
    eg1.step()
    assert eg1.X == 1
    eg1.step()
    assert eg1.X == 1
    eg1.step()
    assert eg1.X == 4
    eg1.step()
    assert eg1.X == 4
    eg1.step()
    assert eg1.X == -1

@pytest.fixture
def eg2():
    with open(os.path.join("tests", "test10a.txt")) as f:
        return day.RegisterMachine(f)

def test_steps(eg2):
    eg2.steps(19)
    assert eg2.X == 21
    eg2.steps(40)
    assert eg2.X == 19
    eg2.steps(40)
    assert eg2.X == 18
    eg2.steps(40)
    assert eg2.X == 21
    eg2.steps(40)
    assert eg2.X == 16
    eg2.steps(40)
    assert eg2.X == 18

def test_sum_signal_strengths(eg2):
    assert eg2.sum_signal_strengths([20,60,100,140,180,220]) == 13140

def test_pixel(eg2):
    assert eg2.determine_pixel() == "#"
    eg2.step()
    assert eg2.determine_pixel() == "#"
    eg2.step()
    assert eg2.determine_pixel() == "."

def test_screen(eg2):
    rows = eg2.compute_screen()
    with open(os.path.join("tests", "test10b.txt")) as f:
        for i in range(6):
            row = f.readline().strip()
            assert row == rows[i]
