from dataclasses import dataclass

class Parse:
    def __init__(self, rows):
        self.parse_first(rows)
        next(rows)
        self.parse_second(rows)

    @property
    def stacks(self):
        return self._cols

    @property
    def commands(self):
        return self._cmds

    def parse_first(self, lines):
        rows = []
        for line in lines:
            try:
                rows.append( self.parse_line(line) )
            except ValueError:
                break
        expected_columns = line.split()
        self._cols = [list() for _ in expected_columns]
        for row in rows:
            for entry, li in zip(row, self._cols):
                if entry is not None:
                    li.append(entry)
        for li in self._cols:
            li.reverse()

    def parse_second(self, lines):
        self._cmds = []
        for line in lines:
            if len(line.strip()) == 0:
                break
            self._cmds.append( self.parse_command(line) )
            
    @dataclass
    class Command:
        source: int
        target: int
        number_to_move: int

    @staticmethod
    def parse_command(cmd):
        """"move 1 from 2 to 1"
        parsed to a `Command` object"""
        parts = cmd.split()
        assert parts[0] == "move"
        assert parts[2] == "from"
        assert parts[4] == "to"
        return Parse.Command(number_to_move=int(parts[1]), source=int(parts[3]), target=int(parts[5]))

    @staticmethod
    def _parse_fragment(frag):
        if len(frag) < 3:
            return None
        if frag[0] == "[" and frag[2] == "]":
            name = frag[1]
        elif all(c==" " for c in frag[:3]):
            if len(frag)==3:
                return None, None
            return None, frag[4:]
        else:
            raise ValueError()
        if len(frag) <= 4:
            return name, None
        return name, frag[4:]

    @staticmethod
    def parse_line(line):
        row = []
        rest = line
        while rest is not None:
            x = Parse._parse_fragment(rest)
            if x is None:
                break
            name, rest = x
            row.append(name)
        return row
    
    def run(self):
        stacks = [list(x) for x in self.stacks]
        def move(src, tgt):
            x = stacks[src-1].pop()
            stacks[tgt-1].append(x)
        for cmd in self.commands:
            for _ in range(cmd.number_to_move):
                move(cmd.source, cmd.target)
        return stacks
    
    def run2(self):
        stacks = [list(x) for x in self.stacks]
        for cmd in self.commands:
            top = stacks[cmd.source-1][-cmd.number_to_move:]
            stacks[cmd.source-1] = stacks[cmd.source-1][:-cmd.number_to_move]
            stacks[cmd.target-1].extend(top)
        return stacks

    def resulting_tops(self):
        stacks = self.run()
        return "".join(s[-1] for s in stacks)

    def resulting_tops_2nd(self):
        stacks = self.run2()
        return "".join(s[-1] for s in stacks)


def main(second_flag):
    with open("input5.txt") as f:
        p = Parse(f)
    if not second_flag:
        return p.resulting_tops()
    return p.resulting_tops_2nd()
