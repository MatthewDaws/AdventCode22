class Parse:
    def __init__(self, rows):
        self._loads = []
        current = []
        for line in rows:
            line = line.strip()
            if len(line) == 0:
                if len(current) > 0:
                    self._loads.append(current)
                    current = []
                else:
                    break
            else:
                current.append(int(line))
        if len(current) > 0:
            self._loads.append(current)

    @property
    def loads(self):
        return self._loads
    
    def maximum_sum(self):
        return max(sum(load) for load in self.loads)

    def sumtop(self, n):
        sums = [sum(load) for load in self.loads]
        sums.sort(reverse=True)
        return sum(sums[:n])


def main(second_flag):
    with open("input1.txt") as f:
        loads = Parse(f)
    if not second_flag:
        return loads.maximum_sum()
    return loads.sumtop(3)
