class Parse:
    def __init__(self, rows):
        self._grid = [[int(x) for x in row.strip()] for row in rows]

    def get(self, row, col):
        return self._grid[row][col]
    
    @property
    def num_rows(self):
        return len(self._grid)
    
    @property
    def num_cols(self):
        return len(self._grid[0])
    
    def outside(self, row, col):
        return row < 0 or col < 0 or row >= self.num_rows or col >= self.num_cols
    
    def is_visible(self, row, col, dir=None):
        if dir is None:
            return any(self.is_visible(row,col,d) for d in [(-1,0), (1,0), (0,-1), (0,1)])
        dr, dc = dir
        r, c = row, col
        tallest = -1
        while True:
            r += dr
            c += dc
            if self.outside(r,c):
                break
            tallest = max(tallest, self.get(r,c))
        return self.get(row, col) > tallest
    
    def count_visible(self):
        count = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.is_visible(row, col):
                    count += 1
        return count

    def scan_count(self):
        mask = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        nr, nc = self.num_rows, self.num_cols
        for row in range(nr):
            self._scan(row,0,0,1,nr,nc,mask)
            self._scan(row,nc-1,0,-1,nr,-1,mask)
        for col in range(nc):
            self._scan(0,col,1,0,nr,nc,mask)
            self._scan(nr-1,col,-1,0,-1,nc,mask)
        return sum(sum(r) for r in mask)

    def _scan(self, row, col, dr, dc, lr, lc, mask):
        height = -1
        while row != lr and col != lc:
            h = self.get(row,col)
            if h > height:
                height = h
                mask[row][col] = 1
            row += dr
            col += dc

    def scan_most_recent_highest(self, row, col, dr, dc, lr, lc, output):
        last_seen = [0 for _ in range(10)]
        while row != lr and col != lc:
            h = self.get(row,col)
            output[row][col] = last_seen[h]
            for i in range(h+1):
                last_seen[i] = 1
            for i in range(h+1,10):
                last_seen[i] = last_seen[i] + 1
            row += dr
            col += dc

    def find_scenic_score(self):
        mask = [[[None for _ in range(self.num_cols)] for _ in range(self.num_rows)] for _ in range(4)]
        nr, nc = self.num_rows, self.num_cols
        for row in range(nr):
            self.scan_most_recent_highest(row,0,0,1,nr,nc,mask[0])
        for row in range(nr):
            self.scan_most_recent_highest(row,nc-1,0,-1,nr,-1,mask[1])
        for col in range(nc):
            self.scan_most_recent_highest(0,col,1,0,nr,nc,mask[2])
        for col in range(nc):
            self.scan_most_recent_highest(nr-1,col,-1,0,-1,nc,mask[3])
        scenic = [
            [mask[0][r][c]*mask[1][r][c]*mask[2][r][c]*mask[3][r][c] for c in range(nc)]
            for r in range(nr) ]
        return scenic


def main(second_flag):
    with open("input8.txt") as f:
        grid = Parse(f)
    if not second_flag:
        return grid.scan_count()
    return max(max(row) for row in grid.find_scenic_score())
