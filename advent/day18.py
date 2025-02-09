class Parse:
    def __init__(self, rows):
        self._locations = []
        for row in rows:
            coords = row.strip().split(",")
            self._locations.append( [int(x) for x in coords] )
        minc, maxc = None, None
        for loc in self._locations:
            for c in loc:
                if minc is None or c < minc:
                    minc = c
                if maxc is None or c > maxc:
                    maxc = c
        assert minc >= 0
        maxc += 1
        self._size = maxc
        self._grid = [ [ [False for _ in range(maxc)] for _ in range(maxc)
            ] for _ in range(maxc) ]
        for (x,y,z) in self._locations:
            self._grid[x][y][z] = True
        self._locations_set = { tuple(x) for x in self._locations }

    @property
    def locations(self):
        return self._locations
    
    _deltas = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]

    def free_neighbours(self, loc):
        (x,y,z) = loc
        for (dx,dy,dz) in self._deltas:
            xx = x + dx
            yy = y + dy
            zz = z + dz
            n = (xx, yy, zz)
            if n not in self._locations_set:
                yield n

    def neighbours_occupied(self, loc):
        return 6 - len(list(self.free_neighbours(loc)))
    
    def surface_area(self):
        return sum(6 - self.neighbours_occupied(loc) for loc in self._locations)
    
    @property
    def size(self):
        return self._size
    
    def in_grid(self, loc):
        return loc[0] >= 0 and loc[1] >= 0 and loc[2] >= 0 and loc[0] < self._size and loc[1] < self._size and loc[2] < self._size
    
    def walk_from(self, loc):
        assert loc not in self._locations_set
        visited = set()
        to_visit = [loc]
        while len(to_visit) > 0:
            loc = to_visit.pop()
            if loc in visited:
                continue
            visited.add(loc)
            for loc in self.free_neighbours(loc):
                if loc not in visited and self.in_grid(loc):
                    to_visit.append(loc)
        return visited

    def in_contact_with_boundary(self, set_of_locations):
        return any(
            any(c==0 or c==self._size-1 for c in loc)
                for loc in set_of_locations )

    def find_interior(self):
        interior = set()
        seen = set()
        for x in range(self._size):
            for y in range(self._size):
                for z in range(self._size):
                    l = (x,y,z)
                    if l in self._locations_set or l in seen:
                        continue
                    region = self.walk_from(l)
                    seen |= region
                    if not self.in_contact_with_boundary(region):
                        interior |= region
        return interior

    def surface_area_interior(self):
        interior = self.find_interior()
        def count_free_neighbours(loc):
            (x,y,z) = loc
            count = 0
            for (dx,dy,dz) in self._deltas:
                xx = x + dx
                yy = y + dy
                zz = z + dz
                n = (xx, yy, zz)
                if n not in interior:
                    count += 1
            return count
        return sum( count_free_neighbours(loc) for loc in interior )


def main(second_flag):
    with open("input18.txt") as f:
        cubes = Parse(f)
    if not second_flag:
        return cubes.surface_area()
    return cubes.surface_area() - cubes.surface_area_interior()
