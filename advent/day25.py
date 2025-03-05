class Snafu:
    def __init__(self, value):
        if type(value) == int:
            self._from_int(value)
            return
        if not all(v in "012-=" for v in value):
            raise ValueError()
        self._value = value

    def _from_int(self, num):
        if num <= 0:
            raise ValueError()
        carry = 0
        base = 1
        self._value = ""
        while num > 0:
            b = num % 5
            num //= 5
            if b == 4:
                s = "-"
                carry = 1
            elif b == 3:
                s = "="
                carry = 1
            else:
                s = str(b)
                carry = 0
            num += carry
            self._value = s + self._value

    def __int__(self):
        base = 1
        num = 0
        for v in self._value[::-1]:
            if v == "-":
                num -= base
            elif v == "=":
                num -= base + base
            else:
                num += int(v) * base
            base *= 5
        return num
    
    def __str__(self):
        return self._value


class Parse:
    def __init__(self, rows):
        self._numbers = [row.strip() for row in rows]

    @property
    def data(self):
        return self._numbers
    
    def sum(self):
        sum_of_numbers = sum(int(Snafu(v)) for v in self._numbers)
        return str(Snafu(sum_of_numbers))


def main(second_flag):
    with open("input25.txt") as f:
        console = Parse(f)
    if not second_flag:
        return console.sum(), None
