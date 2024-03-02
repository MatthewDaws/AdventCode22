class HeadTail:
    def __init__(self):
        self.head = (0,0)
        self.tail = (0,0)

    @property
    def touching(self):
        drow = abs(self.head[0] - self.tail[0])
        dcol = abs(self.head[1] - self.tail[1])
        return drow <= 1 and dcol <= 1
    
    _posnegzero = {-2:-1, -1:-1, 0:0, 1:1, 2:1}

    def move_head(self, row_delta, col_delta):
        self.head = (self.head[0]+row_delta, self.head[1]+col_delta)
        if self.touching:
            return
        dr = HeadTail._posnegzero[self.head[0]-self.tail[0]]
        dc = HeadTail._posnegzero[self.head[1]-self.tail[1]]
        self.tail = (self.tail[0]+dr, self.tail[1]+dc)


class HeadTailMany:
    def __init__(self, segments=2):
        self.segs = [(0,0) for _ in range(segments)]

    _posnegzero = {-2:-1, -1:-1, 0:0, 1:1, 2:1}

    def move_head(self, row_delta, col_delta):
        self.segs[0] = (self.segs[0][0]+row_delta, self.segs[0][1]+col_delta)
        for i in range(1, len(self.segs)):
            dr = self.segs[i-1][0] - self.segs[i][0]
            dc = self.segs[i-1][1] - self.segs[i][1]
            if -1 <= dr <= 1 and -1 <= dc <= 1:
                continue
            dr = HeadTailMany._posnegzero[dr]
            dc = HeadTailMany._posnegzero[dc]
            self.segs[i] = (self.segs[i][0]+dr, self.segs[i][1]+dc)

    @property
    def head(self):
        return self.segs[0]

    @property
    def tail(self):
        return self.segs[-1]


class Parse:
    _d_delta = {"U":(-1,0), "D":(1,0), "L":(0,-1), "R":(0,1)}
    def __init__(self, rows):
        self._moves = []
        for row in rows:
            d, n = row.split()
            self._moves.append( (*Parse._d_delta[d], int (n)) )

    @property
    def moves(self):
        return self._moves
    
    def walk(self, segments=2):
        tail_positions = set()
        ht = HeadTailMany(segments)
        for dr,dc,count in self._moves:
            for _ in range(count):
                ht.move_head(dr,dc)
                tail_positions.add(ht.tail)
        return tail_positions


def main(second_flag):
    with open("input9.txt") as f:
        walker = Parse(f)
    if not second_flag:
        return len(walker.walk())
    return len(walker.walk(10))
