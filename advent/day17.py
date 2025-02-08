class Jets:
    def __init__(self, rows):
        self._instructions = next(rows).strip()
        self.reset()

    def __getitem__(self, index):
        return self._instructions[index]

    def __iter__(self):
        while True:
            yield self.next()

    def next(self):
        if len(self._instructions) == self._index:
            self._index = 0
        out = self._instructions[self._index]
        self._index += 1
        return out

    @property
    def height(self):
        return len(self._room)
    
    def reset(self):
        self._index = 0
        self._room = []

    @property
    def top_row(self):
        return self._room[-1]

    def space_used(self, row, column):
        if row >= len(self._room):
            return column < 0 or column >= 7
        if row < 0 or column < 0 or column >= 7:
            return True
        return self._room[row][column]

    _shapes = { 0:[(0,0), (0,1), (0,2), (0,3)],
                   1:[(0,1), (1,0), (1,1), (1,2), (2,1)],
                   2:[(0,0), (0,1), (0,2), (1,2), (2,2)],
                   3:[(0,0), (1,0), (2,0), (3,0)],
                   4:[(0,0), (0,1), (1,0), (1,1)]
                   }

    def overlaps(self, left, bottom, shape):
        checks = self._shapes[shape]
        return any(self.space_used(bottom+r, left+c) for (r,c) in checks)

    def place(self, left, bottom, shape):
        for r,c in self._shapes[shape]:
            rr, cc = bottom+r, left+c
            while rr >= len(self._room):
                self._room.append([False for _ in range(7)])
            self._room[rr][cc] = True

    def drop(self, shape):
        bottom = self.height + 3
        left = 2
        while True:
            wind = self.next()
            if wind == "<":
                dc = -1
            else:
                dc = 1
            if not self.overlaps(left+dc, bottom, shape):
                left += dc
            if self.overlaps(left, bottom-1, shape):
                self.place(left, bottom, shape)
                break
            bottom -= 1

    def drop_many(self, number, start_shape=0):
        shape = start_shape
        for _ in range(number):
            self.drop(shape)
            shape += 1
            if shape == 5:
                shape = 0

    def find_period(self):
        self.reset()
        shape = 0
        positions = []
        while True:
            self.drop(shape)
            shape += 1
            if shape == 5:
                shape = 0
                positions.append(self._index)
                first = positions.index(self._index)
                if first < len(positions) - 1:
                    print(positions)
                    return first, len(positions) - first - 1

    def find_period_new(self):
        self.reset()
        shape = 0
        positions = []
        while True:
            self.drop(shape)
            shape += 1
            if shape == 5:
                shape = 0
                positions.append((self._index, self.height))
                seen_last_pos = []
                for i, (p, _) in enumerate(positions):
                    if p == self._index:
                        seen_last_pos.append(i)
                if len(seen_last_pos) >= 4:
                    deltas = []
                    for i,j in zip(seen_last_pos, seen_last_pos[1:]):
                        deltas.append((j-i, positions[j][1] - positions[i][1]))
                    if deltas[-1] == deltas[-2]:
                        i = seen_last_pos[-3]
                        return (i, positions[i-1][1], *deltas[-1])

    def drop_very_many_new(self, number):
        burn_in, first_height, period, period_height = self.find_period_new()
        number -= burn_in * 5
        period *= 5
        self.reset()
        self.drop_many(burn_in*5)
        start = self.height
        self.drop_many(number % period)
        end_height = self.height - start
        return first_height + end_height + period_height * (number // period)


def main(second_flag):
    with open("input17.txt") as f:
        jets = Jets(f)
    if not second_flag:
        jets.drop_many(2022)
        return jets.height
    # 1577521613797 too high
    return jets.drop_very_many_new(1000000000000)
