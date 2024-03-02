import pytest, os

import advent.day7 as day

# def test_add_dir():
#     assert day.Parse.add_dir("ahda/ahda/ad", "/") == "/"
#     assert day.Parse.add_dir("ahda/ahda/ad", "xyz") == "ahda/ahda/ad/xyz"

# def test_move_to_parent():
#     assert day.Parse.move_to_parent("ahda/ahda/ad") == "ahda/ahda"
#     assert day.Parse.move_to_parent("ahda") == "/"

def test_Dir():
    d = day.Dir()
    d.directories.append("a")
    d.files.append(day.File("a.txt", 123))
    assert len(d.directories) == 1
    assert d.files[0].name == "a.txt"
    assert d.parent is None


@pytest.fixture
def in1():
    with open(os.path.join("tests", "test7.txt")) as f:
        yield f

def test_parse(in1):
    p = day.Parse(in1)
    fs = p.file_system
    assert len(fs.directories) == 2
    assert len(fs.files) == 2
    assert fs.files[0].name == "b.txt"
    assert fs.files[0].size == 14848514

    d = fs.find_dir("d")
    assert len(d.files) == 4
    assert len(d.directories) == 0

@pytest.fixture
def eg1(in1):
    return day.Parse(in1)

def test_total_size(eg1):
    assert eg1.file_system.find_dir("a").total_size() == 94853
    assert eg1.file_system.find_dir("d").total_size() == 24933642
    assert eg1.file_system.total_size() == 48381165

def test_find_all_dirs(eg1):
    assert set(d.name for d in eg1.file_system.find_all_dirs()) == {"a", "d", "e"}

def test_find_small_dirs(eg1):
    assert set(d.name for d in eg1.find_small_dirs(100000)) == {"a", "e"}
    assert eg1.sum_small_dirs() == 95437

def test_find_root(eg1):
    fs = eg1.file_system
    assert fs.find_dir("/") == fs
    assert fs.find_dir("a").find_dir("/") == fs
    assert fs.find_dir("a").find_dir("e").find_dir("/") == fs

def test_dir_to_delete(eg1):
    n, d = eg1.dir_to_delete()
    assert n == "d"
    assert d.total_size() == 24933642
    