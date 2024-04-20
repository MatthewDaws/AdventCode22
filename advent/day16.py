from . import util
import itertools
from collections import namedtuple

class Parse:
    def __init__(self, rows):
        self._data = []
        for row in rows:
            row = row.strip()
            assert row[:6] == "Valve "
            name = row[6:8]
            assert row[8:23] == " has flow rate="
            i = row[23:].find(";")
            rate = int( row[23:23+i] )
            row = row[24+i:]
            if row[:24] == " tunnels lead to valves ":
                neighbours = [x.strip() for x in row[24:].split(",")]
            elif row[:23] == " tunnel leads to valve ":
                neighbours = [ row[23:] ]
            else:
                raise AssertionError()                
            self._data.append( (name, rate, neighbours) )

    @property
    def data(self):
        return self._data
    
    def full_graph(self):
        graph = util.Graph()
        for vertex, _, _ in self._data:
            graph.add_vertex(vertex)
        for vertex, _, neighbours in self._data:
            for v in neighbours:
                graph.add_directed_edge(vertex, v)
        return graph
    
    def flow_rate(self, value):
        for name, r, _ in self._data:
            if name == value:
                return r
        raise KeyError()

    def reduced_graph(self):
        g = self.full_graph()
        graph = util.WeightedGraph()
        for v, r, _ in self._data:
            if r > 0:
                graph.add_vertex(v)
        vertices = set(graph.vertices)
        for v in vertices:
            distances, _ = util.shortest_path_unweighted(g, v)
            for dest, distance in distances.items():
                if dest in vertices:
                    graph.add_directed_edge(v, dest, distance)
        from_start, _ = util.shortest_path_unweighted(g, "AA")
        return ReducedNetwork(self, graph, from_start)
    

class ReducedNetwork:
    def __init__(self, parent, graph, from_start):
        self._parent = parent
        self._graph = graph
        self._from_start = from_start
        self._rate = { name:rate for name, rate, _ in parent.data }

    @property
    def graph(self):
        return self._graph
    
    @property
    def from_start(self):
        return self._from_start
    
    @property
    def rate(self):
        return self._rate

    def total_flow(self, route, start_time=30):
        current_node = route[0]
        current_time = start_time - 1 - self._from_start[current_node]
        if current_time < 0:
            return 0
        flow = current_time * self._rate[current_node]

        for name in route[1:]:
            for n,d in self._graph.weighted_neighbours_of(current_node):
                if n == name:
                    distance = d
            current_node = name
            current_time -= 1 + distance
            if current_time <= 0:
                return flow
            flow += current_time * self._rate[current_node]

        return flow

    def search_best_flow(self, start_time=30):
        vertices = list(self._graph.vertices)
        best_flow = None
        for option in itertools.permutations(vertices):
            flow = self.total_flow(option, start_time)
            if best_flow is None or best_flow < flow:
                best_flow = flow
                best_route = option
        return best_flow, best_route
    
    def to_backtrack(self):
        distances_dict = dict()
        for v in self._graph.vertices:
            distances_dict[v] = {n:d for n,d in self._graph.weighted_neighbours_of(v)}
        return BackTrack(self._rate, self._from_start, distances_dict)


class BackTrack:
    def __init__(self, rates, distances_from_start, distances_dict):
        self._rates = rates
        self._distances_from_start = distances_from_start
        self._distances_dict = distances_dict

    Agent = namedtuple("Agent", ["movingto", "arrivaltime"])
    PS2 = namedtuple("PS2", ["used_nodes", "agents", "total_rate", "unusedrates"])

    def multisolve(self, starttime=26, agents=2):
        self._todo = []
        for dests in itertools.combinations(self._distances_dict, agents):
            agents = [self.Agent(movingto=d, arrivaltime=starttime-1-self._distances_from_start[d]) for d in dests]
            used_nodes = set(dests)
            total_rate = sum(self._rates[a.movingto] * a.arrivaltime for a in agents)
            unusedrates = sum(self._rates[d] for d in self._distances_dict if d not in used_nodes)
            self._todo.append(self.PS2(used_nodes=used_nodes, agents=agents, total_rate=total_rate, unusedrates=unusedrates))
        self._best_rate = 0
        while len(self._todo) > 0:
            self._next_multi_step()
        return self._best_rate
    
    def _next_multi_step(self):
        current = self._todo.pop()
        index, first_time = 0, current.agents[0].arrivaltime
        for i, a in enumerate(current.agents):
            if a.arrivaltime > first_time:
                first_time = a.arrivaltime
                index = i
        agents = current.agents[:index] + current.agents[index+1:]
        agent = current.agents[index]
        new_agent = []
        for node in self._distances_dict:
            if node in current.used_nodes:
                continue
            arrivaltime = agent.arrivaltime - 1 - self._distances_dict[agent.movingto][node]
            if arrivaltime <= 0:
                continue
            new_total_rate = current.total_rate + arrivaltime * self._rates[node]
            new_unusedrates = current.unusedrates - self._rates[node]
            new_agent.append((self.Agent(movingto=node, arrivaltime=arrivaltime), new_total_rate, new_unusedrates))
        if len(new_agent) == 0:
            if all(a.movingto is None for a in agents):
                self._best_rate = max(self._best_rate, current.total_rate)
                return
            new_agent.append((self.Agent(movingto=None, arrivaltime=0), current.total_rate, current.unusedrates))
        for agent, new_total_rate, new_unusedrates in new_agent:
            new_agents = agents + [agent]
            new_used_nodes = current.used_nodes | {agent.movingto}
            first_time = max(a.arrivaltime for a in new_agents)
            best_possible = new_total_rate + first_time * new_unusedrates
            if best_possible > self._best_rate:
                self._todo.append(self.PS2(used_nodes=new_used_nodes, agents=new_agents, total_rate=new_total_rate, unusedrates=new_unusedrates))

    PartialSoln = namedtuple("PartialSoln", ["visited", "at", "rates", "time", "other_rates_sum"])

    def solve(self, starttime=30):
        self._todo = []
        total_rates = sum(self._rates.values())
        for node in self._distances_dict:
            time = starttime - 1 - self._distances_from_start[node]
            rate = self._rates[node]
            entry = self.PartialSoln(visited={node}, at=node, time=time,
                        rates=time*rate, other_rates_sum=total_rates-rate)
            self._todo.append(entry)
        self._best_rate = 0
        while len(self._todo) > 0:
            self._next_steps()
        return self._best_rate

    def _next_steps(self):
        current = self._todo.pop()
        flag = False
        for node in self._distances_dict:
            if node in current.visited:
                continue
            time = current.time - 1 - self._distances_dict[current.at][node]
            if time <= 0:
                continue
            rate = current.rates + time * self._rates[node]
            total_rates = current.other_rates_sum - self._rates[node]
            if time * total_rates + rate <= self._best_rate:
                continue
            entry = self.PartialSoln(visited={node} | current.visited, at=node, time=time,
                             rates=rate, other_rates_sum=total_rates)
            self._todo.append(entry)
            flag = True
        if not flag:
            if current.rates > self._best_rate:
                self._best_rate = current.rates


def main(second_flag):
    with open("input16.txt") as f:
        p = Parse(f)
    reduced_network = p.reduced_graph()
    back_track = reduced_network.to_backtrack()
    if not second_flag:
        return back_track.solve()
    return back_track.multisolve()
