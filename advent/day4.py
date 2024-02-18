class Range:
    def __init__(self, a, b):
        if a > b:
            a, b = b, a
        self._range = (a, b)

    @property
    def start(self):
        return self._range[0]

    @property
    def end(self):
        return self._range[1]

    def __contains__(self, x):
        return self._range[0] <= x <= self._range[1]
    
    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def __eq__(self, other):
        return self._range == other._range

    def intersect(self, other):
        s = max(self.start, other.start)
        e = min(self.end, other.end)
        if s <= e:
            return Range(s, e)
        return None


class Parse:
    def __init__(self, rows):
        def bit(x):
            return [int(t) for t in x.split("-")]
        self._pairs = []
        for row in rows:
            a, b = row.strip().split(",")
            self._pairs.append( (bit(a), bit(b)) )

    @property
    def pairs(self):
        return self._pairs

    def as_ranges(self):
        for a, b in self._pairs:
            yield Range(*a), Range(*b)

    def count_fully_contained(self):
        count = 0
        for a, b in self.as_ranges():
            if a.contains(b) or b.contains(a):
                count += 1
        return count

    def count_any_overlap(self):
        count = 0
        for a, b in self.as_ranges():
            if a.intersect(b) is not None:
                count += 1
        return count



def main(second_flag):
    with open("input4.txt") as f:
        p = Parse(f)
    if not second_flag:
        return p.count_fully_contained()
    return p.count_any_overlap()
