def find_marker(txt, distinct=4):
    for n in range(distinct, len(txt)):
        bits = set(txt[n - distinct : n])
        if len(bits) == distinct:
            return n
    return None

def check_back(txt, start, search_size):
    for i in range(1, min(start, search_size)):
        if txt[start-i-1] == txt[start-1]:
            return i
    return -1

def find_marker_second(txt, distinct=4):
    smallest_start = distinct
    for n in range(1, len(txt)+1):
        b = check_back(txt, n, distinct)
        if b != -1:
            smallest_start = max(smallest_start, n - b + distinct)
        else:
            if n >= smallest_start:
                return n
    return None

def main(second_flag):
    with open("input6.txt") as f:
        txt = f.read()
    if not second_flag:
        return find_marker_second(txt)
    return find_marker_second(txt, 14)

