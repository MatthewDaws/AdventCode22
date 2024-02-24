import pytest, os

import advent.day5 as day

def test_parse_fragment():
    assert day.Parse._parse_fragment("[5]") == ("5", None)
    assert day.Parse._parse_fragment("[5] ") == ("5", None)
    assert day.Parse._parse_fragment("as") == None
    assert day.Parse._parse_fragment("[5] [A]") == ("5", "[A]")
    assert day.Parse._parse_fragment("    [B] ") == (None, "[B] ")
    assert day.Parse._parse_fragment("   ") == (None, None)
    with pytest.raises(ValueError):
        assert day.Parse._parse_fragment(" 1   3   ")

def test_parse_line():
    assert day.Parse.parse_line("[A]     [B]") == ["A", None, "B"]
    assert day.Parse.parse_line("    [D]    ") == [None, "D", None]

@pytest.fixture
def in1():
    with open(os.path.join("tests", "test5.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    assert len(p.stacks) == 3
    assert p.stacks[0] == ["Z", "N"]
    assert p.stacks[1] == ["M", "C", "D"]
    assert p.stacks[2] == ["P"]

def test_parse_command():
    assert day.Parse.parse_command("move 5 from 7 to 3\n") == day.Parse.Command(number_to_move=5, source=7, target=3)

def test_second_parse(in1):
    p = day.Parse(in1)
    assert len(p.commands) == 4
    assert p.commands[2] == day.Parse.Command(number_to_move=2, source=2, target=1)

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_run(eg1):
    output = eg1.run()
    assert output[0] == ["C"]
    assert output[1] == ["M"]
    assert output[2] == ["P", "D", "N", "Z"]

def test_resulting_tops(eg1):
    assert eg1.resulting_tops() == "CMZ"

def test_resulting_tops_2nd(eg1):
    assert eg1.resulting_tops_2nd() == "MCD"
