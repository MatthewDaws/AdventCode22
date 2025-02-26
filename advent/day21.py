import re
# from collections import namedtuple

class Value:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value


class Op:
    def __init__(self, parent, one, op, two):
        self._parent = parent
        self._data = (one, op, two)

    def clone(self, new_parent):
        return Op(new_parent, *self._data)

    @property
    def one(self):
        return self._data[0]

    @property
    def two(self):
        return self._data[2]

    @property
    def op(self):
        return self._data[1]

    @property
    def value(self):
        one = self._parent.var(self._data[0])
        two = self._parent.var(self._data[2])
        if one is not None and two is not None:
            if self._data[1] == "+":
                return one + two
            if self._data[1] == "-":
                return one - two
            if self._data[1] == "*":
                return one * two
            if self._data[1] == "/":
                return one // two
            raise ValueError()
        return None

    def __repr__(self):
        return f"Op{self._data}"
    

class Parse:
    def __init__(self, rows):
        prog = re.compile("(.*?):\\s(.*?)\\s(.)\\s(.*)")
        self._variables = dict()
        self._know = set()
        self._cache = dict()
        for row in rows:
            row = row.strip()
            m = prog.match(row)
            if not m:
                self._variables[ row[:4] ] = Value( int(row[6:]) )
                self._know.add( row[:4] )
            else:
                self._variables[ m.group(1) ] = Op(self, m.group(2), m.group(3), m.group(4))

    @property
    def variables(self):
        return self._variables
    
    def var(self, name):
        if name in self._cache:
            return self._cache[name]
        v = self._variables[name].value
        if v is not None:
            self._cache[name] = v
        return v

    # def solve(self):
    #     unknown = { name for name in self._variables if name not in self._know }
    #     print(unknown)
    #     raise AssertionError()
    #     while "root" in unknown:
    #         for name in unknown:
    #             v = self._variables[name].value
    #             if v is not None:
    #                 self._know.add(name)
    #                 unknown.remove(name)
    #                 self._cache[name] = v
    #     return self.var("root")

class Solver:
    def __init__(self, parser):
        self._levels = [ {name:val for name,val in parser.variables.items() if type(val) == Value} ]
        not_seen = {name for name,val in parser.variables.items() if type(val) != Value}
        while len(not_seen) > 0:
            level = dict()
            for name in not_seen:
                op = parser.variables[name]
                if op.one not in not_seen and op.two not in not_seen:
                    level[name] = op.clone(self)
            for name in level:
                not_seen.remove(name)
            self._levels.append(level)

    def simplify(self):
        self._cache = {name:op.value for name,op in self._levels[0].items()}
        del self._cache["humn"]
        index = 1
        while index < len(self._levels):
            level = self._levels[index]
            new_level = dict()
            for name, op in level.items():
                if op.one in self._cache and op.two in self._cache:
                    self._cache[name] = op.value
                else:
                    new_level[name] = op
            if len(level) == len(new_level):
                index += 1
            else:
                self._levels[index] = new_level
        self._levels[0] = {name:Value(val) for name,val in self._cache.items()}

    @property
    def levels(self):
        return self._levels
    
    def var(self, name):
        return self._cache[name]

    def __call__(self, human_value):
        self._levels[0]["humn"] = Value(human_value)
        self._cache = {name:op.value for name,op in self._levels[0].items()}
        for level in self._levels[1:]:
            for name, op in level.items():
                self._cache[name] = op.value
                if op.value is None:
                    raise ValueError(name, op)
        op = self._levels[-1]["root"]
        return self._cache[op.one], self._cache[op.two]
    
    def check_divs(self):
        for level in self._levels[1:]:
            for name, op in level.items():
                if op.op == "/":
                    assert op.two in self._levels[0]

    def binary_search(self, negate=False):
        # There is no particular reason this should work, but it does
        ev = self
        if negate:
            def ev(x):
                a, b = self(x)
                return -a, -b
        low = 0
        high = 200
        while True:
            a, b = ev(high)
            if a-b < 0:
                break
            low, high = high, high + high
        # Invariant: a,b=ev(low) has a>b
        while True:
            mid = (low + high) // 2
            if low == mid:
                raise AssertionError()
            a, b = ev(mid)
            if a==b:
                return mid
            if a < b : 
                high = mid
            else:
                low = mid
            

def main(second_flag):
    with open("input21.txt") as f:
        prog = Parse(f)
    if not second_flag:
        return prog.var("root")
    solver = Solver(prog)
    # solver.simplify()
    # solver.check_divs()
    # So no singularities, and hence continuous
    return solver.binary_search()
