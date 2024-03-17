class MyList:
    def __init__(self, string=None):
        if string is None:
            return
        if string[0] == "[":
            assert string[-1] == "]"
            self._content = list(MyList(part) for part in self.split(string[1:-1]))
        else:
            self._content = int(string)

    def __str__(self):
        if type(self._content) == int:
            return str(self._content)
        return "[" + ",".join(str(x) for x in self._content) + "]"
    
    @property
    def content(self):
        return self._content
    
    def aslist(self):
        if type(self._content) == int:
            nl = MyList()
            nl._content = [self]
            return nl
        raise TypeError()

    def __lt__(self, other):
        if type(self._content) == int:
            if type(other._content) == int:
                return self._content < other._content
            return self.aslist() < other
        if type(other._content) == int:
            return self < other.aslist()
        for x, y in zip(self._content, other._content):
            if x < y:
                return True
            if not(x == y):
                return False
        return len(self._content) < len(other._content)

    def __eq__(self, other):
        if type(self._content) == int:
            if type(other._content) == int:
                return self._content == other._content
            return self.aslist() == other
        if type(other._content) == int:
            return self == other.aslist()
        if len(self._content) != len(other._content):
            return False
        return all(x==y for x, y in zip(self._content, other._content))

    @staticmethod
    def split(string):
        inbracket = 0
        part = ""
        for x in string:
            if x == "," and inbracket == 0:
                yield part
                part = ""
                continue
            elif x == "[":
                inbracket += 1
            elif x == "]":
                inbracket -= 1
                assert inbracket >= 0
            part = part + x
        if len(part) > 0:
            yield part


class Parts:
    def __init__(self, rows):
        self._rows = list()
        while True:
            row1 = next(rows).strip()
            if len(row1) == 0:
                break
            row2 = next(rows).strip()
            self._rows.append( (row1, row2) )
            try:
                next(rows)
            except StopIteration:
                break

    @property
    def pairs(self):
        return self._rows
    
    @property
    def pairs_as_lists(self):
        for x,y in self._rows:
            yield MyList(x), MyList(y)

    def compare_all(self):
        return [x<y for x,y in self.pairs_as_lists]
    
    def indices_of_correct(self):
        index = 1
        for order in self.compare_all():
            if order:
                yield index
            index += 1

    def as_one_list(self):
        out = []
        for x,y in self.pairs_as_lists:
            out.append(x)
            out.append(y)
        return out
    
    def places_of_dividers(self):
        li = self.as_one_list()
        li.append(MyList("[[2]]"))
        li.append(MyList("[[6]]"))
        li.sort()
        places = []
        index = 1
        for x in li:
            s = str(x)
            if s == "[[2]]" or s == "[[6]]":
                places.append(index)
            index += 1
        return places
    
    
def main(secondflag):
    with open("input13.txt") as f:
        parts = Parts(f)
    if not secondflag:
        return sum(parts.indices_of_correct())
    x, y = parts.places_of_dividers()
    return x*y
