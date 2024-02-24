import pytest

import advent.day6 as day

def test_find_marker():
    assert day.find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert day.find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert day.find_marker("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert day.find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert day.find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11
    
def test_find_start_msg():
    assert day.find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert day.find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert day.find_marker("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert day.find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert day.find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26

def test_check_back():
    assert day.check_back("mjqjpqmgbl", start=3, search_size=4) == -1
    assert day.check_back("mjqjpqmgbl", start=4, search_size=4) == 2
    assert day.check_back("mjqjpqmgbl", start=5, search_size=4) == -1
    assert day.check_back("mjqjpqmgbl", start=6, search_size=4) == 3
    assert day.check_back("abcda", start=5, search_size=4) == -1

def test_find_marker_second():
    assert day.find_marker_second("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert day.find_marker_second("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert day.find_marker_second("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert day.find_marker_second("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert day.find_marker_second("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

    assert day.find_marker_second("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert day.find_marker_second("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert day.find_marker_second("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert day.find_marker_second("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert day.find_marker_second("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26
