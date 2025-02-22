class Parse:
    def __init__(self, rows):
        self._input = [int(row.strip()) for row in rows]

    @property
    def numbers(self):
        return self._input
    
    def test_no_repeats(self):
        assert len(self._input) == len(set(self._input))

    def mix_all(self, decrypt=False, times=1):
        if decrypt:
            output = [(i,x*811589153) for i,x in enumerate(self._input)]
        else:
            output = list(enumerate(self._input))
        for _ in range(times):
            for index in range(len(self._input)):
                for i, x in enumerate(output):
                    if index == x[0]:
                        output = self.mix(output, i)
        return [x[1] for x in output]
    
    @staticmethod
    def at_index_with_wrap(input_list, index):
        return input_list[index % len(input_list)]

    def code_sum(self, decrypt=False, times=1):
        mixed = self.mix_all(decrypt, times)
        zero_index = mixed.index(0)
        return sum(self.at_index_with_wrap(mixed, zero_index+i) for i in [1000,2000,3000])

    @staticmethod
    def mix(current_list, index):
        final_index = len(current_list) - 1
        num = current_list[index]
        if num[1] == 0:
            return current_list
        current_list = current_list[:index] + current_list[index+1:]
        index = (index + num[1]) % final_index
        if index == 0:
            index = final_index
        current_list.insert(index, num)
        return current_list


def main(second_flag):
    with open("input20.txt") as f:
        nums = Parse(f)
    if not second_flag:
        return nums.code_sum()
    return nums.code_sum(True, 10)
