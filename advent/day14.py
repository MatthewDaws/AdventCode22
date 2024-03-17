class Parse:
    def __init__(self, rows):
        self._rows = []
        for row in rows:
            pairs = []
            for part in row.strip().split(" -> "):
                x,y = part.split(",")
                pairs.append( (int(x), int(y)) )
            self._rows.append(pairs)

    def _all_coords(self):
        for row in self._rows:
                yield from row

    def xrange(self):
        xmin = self._rows[0][0][0]
        xmax = xmin
        for x, _ in self._all_coords():
            xmin = min(x, xmin)
            xmax = max(x, xmax)
        return xmin, xmax
    
    def yrange(self):
        ymin = self._rows[0][0][1]
        ymax = ymin
        for _, y in self._all_coords():
            ymin = min(y, ymin)
            ymax = max(y, ymax)
        return ymin, ymax
    
    @staticmethod
    def _delta(a, b):
        if a < b:
            return 1
        elif a > b:
            return -1
        return 0

    def as_map(self):
        xmin, xmax = self.xrange()
        _, ymax = self.yrange()
        map = [[False for _ in range(xmin, xmax+1)] for y in range(ymax+1)]
        for row in self._rows:
            x, y = row[0]
            for tx, ty in row[1:]:
                dx, dy = self._delta(x, tx), self._delta(y, ty)
                while True:
                    map[y][x-xmin] = True
                    if x==tx and y==ty:
                        break
                    x += dx
                    y += dy
        return Map(map, xmin)


class Map:
    def __init__(self, map, xstart):
        self._map = map
        self._xstart = xstart
        self._sand = [[False for _ in map[0]] for _ in map]

    def __getitem__(self, row):
        return self._map[row]
    
    @property
    def xstart(self):
        return self._xstart

    def __str__(self):
        out = [["." for _ in self._map[0]] for _ in self._map]
        out[0][500-self._xstart] = "+"
        def place(map, ch):
            for y, row in enumerate(map):
                for x, cell in enumerate(row):
                    if cell:
                        out[y][x] = ch
        place(self._map, "#")
        place(self._sand, "o")
        return "\n".join("".join(row) for row in out)

    def occupied(self, x, y):
        return self._map[y][x-self._xstart] or self._sand[y][x-self._xstart]

    def dropone(self):
        x, y = 500, 0
        while True:
            if y >= len(self._sand)-1:
                raise StopIteration()
            if not self.occupied(x,y+1):
                y +=1
                continue
            if not self.occupied(x-1,y+1):
                y += 1
                x -= 1
                continue
            if not self.occupied(x+1,y+1):
                y += 1
                x += 1
                continue
            self._sand[y][x-self._xstart] = True
            return x, y
        
    def dropall(self):
        count = 0
        while True:
            try:
                self.dropone()
            except StopIteration:
                return count
            count += 1

class ExpandingMap(Map):
    def __init__(self, map):
        self._xstart = map._xstart
        def copy(input):
            return [list(x) for x in input]
        self._map = copy(map._map)
        self._sand = copy(map._sand)
        self._sand.append([False for _ in self._sand[0]])
        self._sand.append([False for _ in self._sand[0]])
        self._maxy = len(self._map)
        needed = self._maxy + 4
        leftadd = needed - (500 - self._xstart)
        if leftadd > 0:
            self._map = [[False]*leftadd + row for row in self._map]
            self._sand = [[False]*leftadd + row for row in self._sand]
            self._xstart -= leftadd
        rightadd = needed+needed - len(self._map[0])
        if rightadd > 0:
            self._map = [row + [False]*rightadd for row in self._map]
            self._sand = [row + [False]*rightadd for row in self._sand]

    def occupied(self, x, y):
        xx = x-self._xstart
        if y == self._maxy:
            return self._sand[y][xx]
        if y > self._maxy:
            return True
        return self._map[y][xx] or self._sand[y][xx]

    def dropall(self):
        count = 0
        while True:
            x,y = self.dropone()
            count += 1
            if (x,y) == (500,0):
                return count


def main(secondflag):
    with open("input14.txt") as f:
        p = Parse(f)
    map = p.as_map()
    if not secondflag:
        return map.dropall()
    map = ExpandingMap(map)
    return map.dropall()
