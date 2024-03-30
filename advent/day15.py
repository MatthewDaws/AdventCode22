from collections import namedtuple

class Parse:
    def __init__(self, rows):
        self._data = []
        for row in rows:
            # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
            assert row[:10] == "Sensor at "
            i = row.find(": closest")
            sensor = self.parsexy(row[10:i])
            assert row[i:i+23] == ": closest beacon is at "
            beacon = self.parsexy(row[i+23:].strip())
            self._data.append( (sensor, beacon) )

    @staticmethod
    def parsexy(string):
        x, y = string.split(", ")
        assert x[:2] == "x="
        x = int(x[2:])
        assert y[:2] == "y="
        y = int(y[2:])
        return x, y
    
    @property
    def data(self):
        return self._data

    def covered(self, x, y):
        for xx, yy, distance in self._sensor_distances():
            if abs(x-xx)+abs(yy-y) <= distance:
                return True
        return False

    def _sensor_distances(self):
        for sensor, beacon in self._data:
            distance = abs(sensor[0]-beacon[0]) + abs(sensor[1]-beacon[1])
            yield sensor[0], sensor[1], distance

    def faster_find(self, maxx):
        for x,y in self.faster_find_all_candidate():
            if 0 <= x <= maxx and 0 <= y <= maxx:
                return x,y

    def faster_find_all_candidate(self):
        for s1x, s1y, d1 in self._sensor_distances():
            for s2x, s2y, d2 in self._sensor_distances():
                a = s1y+s2y
                b = s2x-s1x-2-d1-d2
                yy = a+b
                if yy%2 == 1:
                    continue
                y = yy // 2
                if s1y-d1 <= y <= s1y and s2y-d2 <= y <= s2y:
                    x = d1 - (s1y-y) + 1 + s1x
                    if not self.covered(x,y):
                        yield x,y
                y = (a-b) // 2
                if s1y <= y <= s1y+d1 and s2y <= y <= s2y+d2:
                    x = d1 - (y-s2y) + 1 + s2x
                    if not self.covered(x,y):
                        yield x,y

    def intervals_at_row(self, y):
        for sensor, beacon in self._data:
            distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
            length = distance - abs(y - sensor[1])
            if length < 0:
                continue
            yield (sensor[0] - length, sensor[0] + length)

    def cannot_be_at_row(self, y):
        return self.used_spaces_in_row(y).length()
    
    def used_spaces_in_row(self, y):
        i = Intervals()
        for start, end in self.intervals_at_row(y):
            i.add(start, end)
        return i
    
    def beacons_in_row(self, y):
        xvalues = set()
        for _, beacon in self._data:
            if beacon[1] == y:
                xvalues.add( beacon[0] )
        return len(xvalues)

    def _check_row(self, y, possible, maxcoord):
        i = self.used_spaces_in_row(y).intersect(possible)
        if i.length() == maxcoord:
            return i.segments[0][1]+1, y
        return None

    def find(self, maxcoord):
        possible = Intervals()
        possible.add(0, maxcoord)
        for y in range(0, maxcoord+1):
            ans = self._check_row(y, possible, maxcoord)
            if ans is not None: return ans


class Intervals:
    """Container for sorted integer intervals of the form `(a,b)` where this represents the
    integers a <= x <= b."""
    def __init__(self):
        self._intervals = []
    
    def add(self, start, end):
        if start > end:
            raise ValueError()
        index = 0
        new_ints = []
        a, b = start, end
        while True:
            if index == len(self._intervals):
                new_ints.append( (a,b) )
                self._intervals = new_ints
                return
            na, nb = self._intervals[index]
            if b <= na - 2:
                new_ints.append( (a,b) )
                self._intervals = new_ints + self._intervals[index:]
                return
            if a >= nb + 2:
                new_ints.append( (na, nb) )
            else:
                a = min(a, na)
                b = max(b, nb)
            index += 1

    @property
    def segments(self):
        return self._intervals
    
    def length(self):
        return sum(b-a+1 for (a,b) in self._intervals)
    
    def intersect(self, other):
        """Bit inefficient O(nm) algorithm"""
        i = Intervals()
        for a1,b1 in self.segments:
            for a2,b2 in other.segments:
                a = max(a1,a2)
                b = min(b1,b2)
                if a<=b:
                    i.add(a,b)
        return i
    

def main(second_flag):
    with open("input15.txt") as f:
        p = Parse(f)
    if not second_flag:
        y = 2000000
        return p.cannot_be_at_row(y) - p.beacons_in_row(y)
    x,y = p.faster_find(4000000)
    return x*4000000 + y
