import re, math

class Monkey:
    def __init__(self, items, operation, test, true_action, false_action, parent):
        self._items = list(items)
        self._op = self.parse_operation(operation)
        self._test, self._div = self.parse_test(test)
        self._actions = (true_action, false_action)
        self._parent = parent
        self._inspected_count = 0
        self._is_calm = False
        self._mod = None

    @property
    def items(self):
        return self._items
    
    @property
    def divisible_by(self):
        return self._div

    def calm(self):
        self._is_calm = True

    def set_mod(self, mod):
        self._mod = mod

    @property
    def inspected_count(self):
        return self._inspected_count
    
    def take_turn(self):
        for item in self._items:
            self._inspected_count += 1
            item = self._op(item)
            if not self._is_calm:
                item = item // 3
            if self._mod is not None:
                item = item % self._mod
            if self._test(item):
                self._parent.give_to_monkey(self._actions[0], item)
            else:
                self._parent.give_to_monkey(self._actions[1], item)
        self._items = list()

    def pass_item_to(self, item):
        self._items.append(item)

    @staticmethod
    def parse_test(test_string):
        # divisible by 23
        assert test_string[:13] == "divisible by "
        arg = int(test_string.strip()[13:])
        return lambda x : (x%arg==0), arg

    @staticmethod
    def parse_operation(operation_string):
        # new = old * 19
        assert operation_string[:10] == "new = old "
        op = operation_string[10]
        assert operation_string[11] == " "
        arg = operation_string.strip()[12:]
        if arg == "old":
            if op == "+":
                return lambda x : x+x
            if op == "*":
                return lambda x : x*x
            raise SyntaxError(operation_string)
        arg = int(arg)
        if op == "+":
            return lambda x : x+arg
        if op == "*":
            return lambda x : x*arg
        raise SyntaxError(operation_string)



class Monkeys:
    def __init__(self, rows):
        self._monkeys = dict()
        while True:
            num, monkey = Monkeys.parse_monkey(self, rows)
            if num is None:
                break
            self._monkeys[num] = monkey
            try:
                next(rows)
            except StopIteration:
                break
        num_monkeys = len(self._monkeys)
        assert set(self._monkeys.keys()) == set(range(num_monkeys))
        self._monkeys = [self._monkeys[k] for k in range(num_monkeys)]

    def calm(self):
        moduli = []
        for m in self._monkeys:
            m.calm()
            moduli.append(m.divisible_by)
        mod = 1
        for x in moduli:
            mod = mod * x
        mod //= math.gcd(*moduli)
        for m in self._monkeys:
            m.set_mod(mod)

    def give_to_monkey(self, monkey, item):
        self._monkeys[monkey].pass_item_to(item)

    def take_turn(self):
        for monkey in self._monkeys:
            monkey.take_turn()

    @property
    def monkey_business(self):
        counts = [m.inspected_count for m in self._monkeys]
        counts.sort(reverse=True)
        return counts[0] * counts[1]

    @property
    def monkeys(self):
        return self._monkeys

    @staticmethod
    def check_starts_with_give_rest(line, start):
        assert line.startswith(start)
        return line[len(start):]

    @staticmethod
    def parse_monkey(parent, rows):
        try:
            line = next(rows)
        except:
            return None, None
        if len(line.strip()) == 0:
            return None, None
        
        monkey_line = re.compile("Monkey (\\d+):")
        mo = monkey_line.match(line)
        if not mo:
            raise SyntaxError(line)
        monkey_number = int(mo.group(1))

        items = [int(x) for x in Monkeys.check_starts_with_give_rest(next(rows).rstrip(), "  Starting items: ").split(", ")]
        op = Monkeys.check_starts_with_give_rest(next(rows).rstrip(), "  Operation: ")
        test = Monkeys.check_starts_with_give_rest(next(rows).rstrip(), "  Test: ")
        true_monkey = int(Monkeys.check_starts_with_give_rest(next(rows).rstrip(), "    If true: throw to monkey "))
        false_monkey = int(Monkeys.check_starts_with_give_rest(next(rows).rstrip(), "    If false: throw to monkey "))
        return monkey_number, Monkey(items, op, test, true_monkey, false_monkey, parent)


def main(second_flag):
    with open("input11.txt") as f:
        m = Monkeys(f)
    if not second_flag:
        for _ in range(20):
            m.take_turn()
        return m.monkey_business
    m.calm()
    for _ in range(10000):
        m.take_turn()
    return m.monkey_business
