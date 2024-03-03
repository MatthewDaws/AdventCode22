import enum, dataclasses, typing

class Commands(enum.Enum):
    NOOP = 1
    ADDX = 2


@dataclasses.dataclass
class Command:
    cmd: Commands
    data: 'typing.Any' = None


class RegisterMachine:
    def __init__(self, commands):
        self._X = 1
        self._waiting = 0
        self._index = 0
        self._current_command = None
        self._pixel = 0

        self._cmds = []
        for row in commands:
            row = row.strip()
            if row == "noop":
                self._cmds.append( Command(cmd=Commands.NOOP) )
            elif row[:5] == "addx ":
                self._cmds.append( Command(cmd=Commands.ADDX, data=int(row[5:])) )

    @property
    def X(self):
        return self._X
    
    @property
    def commands(self):
        return self._cmds
    
    def step(self):
        self._pixel += 1
        if self._waiting > 0:
            self._waiting -= 1
            if self._waiting == 0:
                if self._current_command.cmd == Commands.ADDX:
                    self._X += self._current_command.data
            return
        if self._index == len(self._cmds):
            raise StopIteration()
        self._current_command = self._cmds[self._index]
        self._index += 1
        if self._current_command.cmd == Commands.ADDX:
            self._waiting = 1
        
    def steps(self, number_steps):
        for _ in range(number_steps):
            self.step()

    def sum_signal_strengths(self, steps):
        self.steps(steps[0]-1)
        count = steps[0] * self.X
        for i in range(1, len(steps)):
            delta = steps[i] - steps[i-1]
            self.steps(delta)
            count += steps[i] * self.X
        return count
    
    def determine_pixel(self):
        row = self._pixel % 40
        if abs(row - self._X) <= 1:
            return "#"
        return "."

    def compute_screen(self):
        rows = []
        for _ in range(6):
            row = ""
            for _ in range(40):
                row += self.determine_pixel()
                self.step()
            rows.append(row)
        return rows
    
def main(second_flag):
    with open("input10.txt") as f:
        rm = RegisterMachine(f)
    if not second_flag:
        return rm.sum_signal_strengths([20,60,100,140,180,220])
    rows = rm.compute_screen()
    def dbl(row):
        out = []
        for x in row:
            out.append(x)
            out.append(x)
        return "".join(out)
    #print("\n".join(dbl(x) for x in rows))
    return "FZBPBFZF", "\n".join(dbl(x) for x in rows)
