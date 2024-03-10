class Mountain:
    def __init__(self, rows):
        self._grid = []
        for n, row in enumerate(rows):
            self._grid.append(row.strip())
            i = row.find("S")
            if i != -1:
                self._start = (n, i)
                self._grid[-1] = self._grid[-1][:i] + "a" + self._grid[-1][i+1:]
            i = row.find("E")
            if i != -1:
                self._end = (n, i)
                self._grid[-1] = self._grid[-1][:i] + "z" + self._grid[-1][i+1:]

    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    @property
    def numrows(self):
        return len(self._grid)
    
    @property
    def numcols(self):
        return len(self._grid[0])

    def height(self, row, col):
        return ord(self._grid[row][col]) - ord("a")

    def can_move(self, pos, delta, backwards=False):
        row, col = pos
        nrow, ncol = row + delta[0], col + delta[1]
        if nrow < 0 or ncol < 0  or nrow >= self.numrows or ncol >= self.numcols:
            return False
        if backwards:
            return self.height(nrow, ncol) >= self.height(row, col) - 1
        else:
            return self.height(nrow, ncol) <= 1 + self.height(row, col)

    def find_paths(self, backwards=False):
        visited = [[False for _ in range(self.numcols)] for _ in range(self.numrows)]
        self._minlength = [[-1 for _ in range(self.numcols)] for _ in range(self.numrows)]
        if backwards:
            self._minlength[self._end[0]][self._end[1]] = 0
            current = [self._end]
        else:
            self._minlength[self._start[0]][self._start[1]] = 0
            current = [self._start]
        next_set = set()
        while True:
            row, col = current.pop()
            visited[row][col] = True
            length = self._minlength[row][col]
            for d in [(1,0), (-1,0), (0,1), (0,-1)]:
                if self.can_move((row,col), d, backwards):
                    nr, nc = row + d[0], col + d[1]
                    nl = self._minlength[nr][nc]
                    if nl==-1 or nl > length + 1:
                        self._minlength[nr][nc] = length + 1
                    if not visited[nr][nc]:
                        next_set.add((nr,nc))
            if len(current) == 0:
                current = list(next_set)
                if len(current) == 0:
                    break
                next_set = set()

    def find_path(self):
        self.find_paths()
        return self._minlength[self._end[0]][self._end[1]]

    def minimal_path_length_to(self, row, col):
        return self._minlength[row][col]
    
    def find_shortest_path_from_ground(self):
        minimal = None
        for row in range(self.numrows):
            for col in range(self.numcols):
                if self.height(row, col) == 0:
                    l = self.minimal_path_length_to(row, col)
                    if l>-1 and (minimal is None or minimal > l):
                        minimal = l
        return minimal

    def find_actual_path(self):
        # Just used to testing
        self.find_paths()
        p = self._end
        path = []
        while p != self._start:
            path.append(p)
            found = False
            for d in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = p[0]+d[0], p[1]+d[1]
                if nr<0 or nc<0 or nr>=self.numrows or nc>=self.numcols:
                    continue
                if self._minlength[nr][nc] == self._minlength[p[0]][p[1]] - 1:
                    p = (nr,nc)
                    found = True
                    break
            assert found
        path.append(self._start)
        path.reverse()
        return path
            

def main(second_flag):
    with open("input12.txt") as f:
        m = Mountain(f)
    if not second_flag:
        #m.find_actual_path()
        return m.find_path()
    m.find_paths(backwards=True)
    return m.find_shortest_path_from_ground()
