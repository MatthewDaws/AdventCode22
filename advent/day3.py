class Parse:
    def __init__(self, rows):
        self._lines = []
        for row in rows:
            row = row.strip()
            l = len(row) // 2
            self._lines.append( (row[:l], row[l:]) )

    @property
    def lines(self):
        return self._lines
    
    def commons(self):
        for a, b in self._lines:
            intersection = set(a).intersection(set(b))
            assert len(intersection) == 1
            yield list(intersection)[0]

    @staticmethod
    def to_priority(c):
        t = ord(c) - ord("a")
        if 0 <= t <= 25:
            return t+1
        t = ord(c) - ord("A")
        if 0 <= t <= 25:
            return t+27
        raise ValueError()
    
    def sum(self):
        return sum(self.to_priority(c) for c in self.commons())
    
    def triples(self):
        it = iter(self._lines)
        def nxt():
            x, y = next(it)
            return set(x+y)
        while True:
            try:
                intersection = nxt().intersection(nxt()).intersection(nxt())
            except StopIteration:
                return
            assert len(intersection) == 1
            yield list(intersection)[0]

    def triple_sum(self):
        return sum(self.to_priority(c) for c in self.triples())


def main(second_flag):
    with open("input3.txt") as f:
        p = Parse(f)
    if not second_flag:
        return p.sum()
    return p.triple_sum()
