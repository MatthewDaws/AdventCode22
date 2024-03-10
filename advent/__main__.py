import sys, importlib, time

def fullrun(puzzle, secondflag):
    modulename = f".day{puzzle}"
    day = importlib.import_module(modulename, "advent")
    return day.main(secondflag)

def takeone(answer):
    try:
        num, *_ = answer
    except:
        return answer
    return num

def run(puzzle, secondflag):
    answer = fullrun(puzzle, secondflag)
    return takeone(answer)

def check10(a, b):
    assert b[1] == '########..########..######....######....######....########..########..########..\n##..............##..##....##..##....##..##....##..##..............##..##........\n######........##....######....##....##..######....######........##....######....\n##..........##......##....##..######....##....##..##..........##......##........\n##........##........##....##..##........##....##..##........##........##........\n##........########..######....##........######....##........########..##........'

def runall():
    answers = [(69693, 200945), (11150, 8295), (7817, 2444), (503, 827), ("ZWHVFWQWW", "HZFZCCWWV"),
               (1093, 3534), (1118405, 12545514), (1560 ,252000), (6376, 2607), (14720, "FZBPBFZF"),
               (64032, 12729522272), (517, 512)]
    specials = {10: check10}
    for day, (first, second) in enumerate(answers):
        start = time.perf_counter_ns()
        one = fullrun(day+1, False)
        t1 = (time.perf_counter_ns() - start) // 1000000
        start = time.perf_counter_ns()
        two = fullrun(day+1, True)
        t2 = (time.perf_counter_ns() - start) // 1000000
        if day+1 in specials:
            specials[day+1](one, two)
            one, two = takeone(one), takeone(two)
        assert one == first
        assert two == second
        print(f"Day {day+1} : {one} ({t1} ms) and {two} ({t2} ms).")

def parse_args(args):
    """return `(mode, puzzlenumber, secondflag)`
    
    or raises `SyntaxError`
    """
    if len(args) <= 1:
        raise SyntaxError()
    if len(args) == 2:
        if args[1] == "all":
            return ("all", None, None)
        try:
            return ("run", int(args[1]), False)
        except:
            raise SyntaxError()
    if len(args) > 3 or args[2] != "2nd":
        raise SyntaxError()
    try:
        return ("run", int(args[1]), True)
    except:
        raise SyntaxError()

def main():
    try:
        mode, puzzle, secondflag = parse_args(sys.argv)
    except:
        print("Usage: [{puzzle number} [2nd]] / [all]")
        print()
        print("python -m advent 5       : Solve the first part of puzzle 5")
        print("python -m advent 7 2nd   : Solve the second part of puzzle 7")
        print("python -m all            : Solve all the puzzles")
        exit(-1)
    if mode == "all":
        runall()
        exit(0)
    print(run(puzzle, secondflag))
          

if __name__ == "__main__":
    main()
