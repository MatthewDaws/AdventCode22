import math
from .util import Graph#, shortest_path_unweighted

class Integer_Priority_Queue:
    def __init__(self, infinity = 10000000):
        self.entries_to_weight = dict()
        self.weight_to_entry = dict()
        self.infinity = infinity
        self.current_min_weight = self.infinity

    @property
    def is_empty(self):
        return len(self.entries_to_weight) == 0

    def weight_is_infinity(self, weight):
        return weight == self.infinity

    def pop(self):
        """Remove lowest weight object"""
        key = self.weight_to_entry[self.current_min_weight].pop()
        weight = self.current_min_weight
        del self.entries_to_weight[key]
        if len(self.weight_to_entry[self.current_min_weight]) == 0:
            del self.weight_to_entry[self.current_min_weight]
            if self.is_empty:
                self.current_min_weight = self.infinity
            else:
                self.current_min_weight += 1
                while self.current_min_weight not in self.weight_to_entry:
                    self.current_min_weight += 1
        return key, weight

    def add(self, key, weight):
        if weight is None:
            weight = self.infinity
        if key in self.entries_to_weight:
            old_weight = self.entries_to_weight[key]
            self.weight_to_entry[old_weight].remove(key)
            #self.entries_to_weight[key] = weight
            #self.add(key, weight)
        self.entries_to_weight[key] = weight
        if weight not in self.weight_to_entry:
            self.weight_to_entry[weight] = set()
            if weight < self.current_min_weight:
                self.current_min_weight = weight
        self.weight_to_entry[weight].add(key)


def shortest_path_unweighted(graph, source):
    """Uses Dijkstra's algorithm to find all the shortest paths from `source`, in an unweighted
     graph `graph`.  Doesn't use a priority queue, so perhaps slow.
     
    Returns: `distances, previous` both dictionaries from vertices to distances, respectively,
       previous vertex in shortest path to `source`.
    """
    distances = {v:None for v in graph.vertices}
    previous = {v:None for v in graph.vertices}
    queue = Integer_Priority_Queue()
    distances[source] = 0
    queue.add(source, 0)
    visited = {source}
    while not queue.is_empty:
        vertex, mindist = queue.pop()
        if queue.weight_is_infinity(mindist):
            break
        visited.add(vertex)
        newdist = distances[vertex] + 1
        for v in graph.neighbours_of(vertex):
            if distances[v] is None or newdist < distances[v]:
                distances[v] = newdist
                previous[v] = vertex
                if v not in visited:
                    queue.add(v, newdist)
    return distances, previous


class Parse:
    def __init__(self, rows):
        self._grid = [row.strip() for row in rows]
        assert self._grid[0][1] == "."
        assert self._grid[-1][-2] == "."
        self._grid = [ row[1:-1] for row in self._grid[1:-1]]
        assert all(row[0] in ".<>" for row in self._grid)
        assert all(row[-1] in ".<>" for row in self._grid)
        self._positions = []
        for r, row in enumerate(self._grid):
            for c, entry in enumerate(row):
                if entry == "^":
                    self._positions.append((r,c,-1,0))
                elif entry == "v":
                    self._positions.append((r,c,1,0))
                elif entry == ">":
                    self._positions.append((r,c,0,1))
                elif entry == "<":
                    self._positions.append((r,c,0,-1))

    @property
    def grid(self):
        return self._grid
    
    @property
    def hurriances(self):
        return self._positions
    
    @property
    def width(self):
        return len(self._grid[0])

    @property
    def height(self):
        return len(self._grid)

    @property
    def repeat_time(self):
        width = len(self._grid[0])
        height = len(self._grid)
        return width * height // math.gcd(width, height)
    
    def move_hurricanes(self):
        width = len(self._grid[0])
        height = len(self._grid)
        new_positions = []
        for (r,c,dr,dc) in self._positions:
            rr, cc = r + dr, c + dc
            if rr < 0:
                rr += height
            if rr >= height:
                rr -= height
            if cc < 0:
                cc += width
            if cc >= width:
                cc -= width
            new_positions.append((rr,cc,dr,dc))
        self._positions = new_positions

    def locations_at_all_times(self):
        vertices_by_time = dict()
        for i in range(self.repeat_time):
            vertices_by_time[i] = {(r,c) for (r,c,dr,dc) in self._positions}
            self.move_hurricanes()
        return vertices_by_time

    def graph(self, start_time = 0):
        all_positions = { (r,c) for r in range(self.height) for c in range(self.width) }
        end_pos = (self.height, self.width-1)
        g = Graph()
        vertices_by_time = self.locations_at_all_times()
        for i in range(self.repeat_time):
            g.add_vertex((i,-1,0))
            g.add_vertex((i,*end_pos))
            for (r,c) in all_positions - vertices_by_time[(start_time + i) % self.repeat_time]:
                g.add_vertex((i,r,c))
            self.move_hurricanes()

        vertices = dict()
        for time,r,c in g.vertices:
            if time not in vertices:
                vertices[time] = set()
            vertices[time].add((r,c))
        for i in range(self.repeat_time):
            nexti = i + 1
            if nexti == self.repeat_time:
                nexti = 0
            for (r,c) in vertices[i]:
                for delta in [(0,0), (1,0), (-1,0), (0,1), (0,-1)]:
                    rr, cc = r+delta[0], c+delta[1]
                    if (rr,cc) in vertices[nexti]:
                        g.add_directed_edge((i,r,c), (nexti,rr,cc))
        return g

    def path(self):
        return self._path_from(self.graph(), (0,-1,0), (self.height, self.width-1))
    
    def _path_from(self, graph, initial_vertex, target_place):
        distances, previous = shortest_path_unweighted(graph, initial_vertex)
        min_distance = None
        for time in range(self.repeat_time):
            d = distances[(time,*target_place)]
            if min_distance is None or d < min_distance:
                min_distance = d
                min_time = time
        # path = [(min_time, *end_pos)]
        # while True:
        #     prev = previous[path[-1]]
        #     if prev is None:
        #         break
        #     path.append(prev)
        return min_distance

    def path_there_and_back(self):
        graph = self.graph()
        there = self._path_from(graph, (0,-1,0), (self.height,self.width-1))
        back = self._path_from(graph, (there % self.repeat_time,self.height,self.width-1), (-1,0))
        there_again = self._path_from(graph, ((there+back) % self.repeat_time,-1,0), (self.height,self.width-1))
        return there + back + there_again


def main(second_flag):
    with open("input24.txt") as f:
        grid = Parse(f)
    if not second_flag:
        return grid.path()
    return grid.path_there_and_back()
