class Parse:
    def __init__(self, rows):
        self._grid = [row.strip() for row in rows]
        self._order = ["N", "S", "W", "E"]
    
    @property
    def grid(self):
        return self._grid
    
    def at(self, row, col):
        if row < 0 or row >= len(self._grid) or col < 0 or col >= len(self._grid[0]):
            return "."
        return self._grid[row][col]

    def rotate_directions(self):
        old = self._order[0]
        self._order = self._order[1:]
        self._order.append(old)

    @property
    def order(self):
        return self._order

    _checks = {"N" : [(-1,1), (-1,0), (-1,-1)], "S" : [(1,1), (1,0), (1,-1)],
               "E" : [(-1,1), (0,1), (1,1)], "W" : [(-1,-1), (0,-1), (1,-1)]}

    def no_neighbours(self, pos):
        r, c = pos
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr == 0 and dc == 0:
                    continue
                if self.at(r+dr, c+dc) == "#":
                    return False
        return True

    def proposals(self):
        props = dict()
        for r, row in enumerate(self._grid):
            for c, entry in enumerate(row):
                if entry == "#":
                    prop = None
                    if not self.no_neighbours((r,c)):
                        for direction in self._order:
                            deltas = self._checks[direction]
                            if all(self.at(r+dr, c+dc)=="." for (dr,dc) in deltas):
                                prop = deltas[1]
                                break
                    props[(r,c)] = prop
        return props
    
    @staticmethod
    def new_grid(proposals):
        new_pos = dict()
        for (r,c), prop in proposals.items():
            if prop is None:
                new_pos[(r,c)] = (r,c)
            else:
                dr, dc = prop
                rr, cc = r+dr, c+dc
                if (rr,cc) in new_pos:
                    old = new_pos[(rr,cc)]
                    del new_pos[(rr,cc)]
                    new_pos[old] = old
                    assert (r,c) not in new_pos
                    new_pos[(r,c)] = (r,c)
                else:
                    new_pos[(rr,cc)] = (r,c)

        row_range = None
        col_range = None
        for (r,c) in new_pos:
            if row_range is None:
                row_range = [r,r]
                col_range = [c,c]
            row_range[0] = min(r, row_range[0])
            row_range[1] = max(r, row_range[1])
            col_range[0] = min(c, col_range[0])
            col_range[1] = max(c, col_range[1])
        grid = [ ["." for _ in range(col_range[1]-col_range[0]+1)] for _ in range(row_range[1] - row_range[0]+1) ]
        for (r,c) in new_pos:
            grid[r - row_range[0]][c - col_range[0]] = "#"
        return ["".join(row) for row in grid]
    
    def iterate(self, count=10):
        for _ in range(count):
            props = self.proposals()
            self._grid = self.new_grid(props)
            self.rotate_directions()
    
    def empty_space(self):
        return sum( sum(entry == "." for entry in row) for row in self._grid)

    def run_to_no_move(self):
        count = 1
        while True:
            props = self.proposals()
            if all(v is None for v in props.values()):
                break
            self._grid = self.new_grid(props)
            self.rotate_directions()
            count += 1
        return count
    

def main(second_flag):
    with open("input23.txt") as f:
        grid = Parse(f)
    if not second_flag:
        grid.iterate()
        return grid.empty_space() 
    return grid.run_to_no_move()
