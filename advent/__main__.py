import sys, importlib

def runall():
    pass



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
    modulename = f"day{puzzle}"
    day = importlib.import_module(modulename)
    output = day.main(secondflag)
    print(output)

if __name__ == "__main__":
    main()
