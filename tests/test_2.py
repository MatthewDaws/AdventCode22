import pytest

import advent.day2 as day

def test_score():
    assert day.Parse.score("A", "A") == 3
    assert day.Parse.score("B", "A") == 6
    assert day.Parse.score("B", "C") == 0

@pytest.fixture
def eg1():
    return "A Y\nB X\nC Z\n".split("\n")

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.plays) == 3

@pytest.fixture
def p1(eg1):
    return day.Parse(eg1)

def test_sum_scores(p1):
    assert p1.sum_scores() == 15

def test_solve():
    assert day.Parse.solve_game("A", "B") == "A"
    assert day.Parse.solve_game("B", "B") == "B"
    assert day.Parse.solve_game("C", "B") == "C"
    assert day.Parse.solve_game("A", "A") == "C"
    assert day.Parse.solve_game("B", "A") == "A"
    assert day.Parse.solve_game("C", "A") == "B"
    assert day.Parse.solve_game("A", "C") == "B"
    assert day.Parse.solve_game("B", "C") == "C"
    assert day.Parse.solve_game("C", "C") == "A"

def test_scores_with_solve(p1):
    row = p1.plays[0]
    assert p1.scores_with_solve(row) == 4
    row = p1.plays[1]
    assert p1.scores_with_solve(row) == 1
    row = p1.plays[2]
    assert p1.scores_with_solve(row) == 7

    assert p1.all_scores_with_solve() == 12
