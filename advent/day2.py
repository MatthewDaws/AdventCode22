class Parse:
    play_scores = {"A": 1, "B": 2, "C": 3}
    opplay_mapping = {"X":"A", "Y":"B", "Z":"C"}

    def __init__(self, lines):
        self._plays = []
        for row in lines:
            row = row.strip()
            if len(row) == 0:
                break
            play, opplay = row.split()
            if play not in self.play_scores:
                raise ValueError()
            if opplay not in self.opplay_mapping:
                raise ValueError()
            opplay = self.opplay_mapping[opplay]
            play, opplay = opplay, play
            self._plays.append( (play, self.play_scores[play], opplay, self.score(play, opplay)) )

    @property
    def plays(self):
        return self._plays
    
    @staticmethod
    def score(play, opponent):
        if play == opponent:
            return 3
        # rock, scissors
        if play == "A" and opponent == "C":
            return 6
        # paper, rock
        if play == "B" and opponent == "A":
            return 6
        # scissors, paper
        if play == "C" and opponent == "B":
            return 6
        return 0

    def sum_scores(self):
        return sum(x[1]+x[3] for x in self._plays)
    
    lose_map = {"A": "C", "B":"A", "C":"B"}
    win_map = {"A":"B", "B":"C", "C":"A"}

    @staticmethod
    def solve_game(play, outcome):
        # A = lose
        if outcome == "A":
            return Parse.lose_map[play]
        # B = draw
        if outcome == "B":
            return play
        # C = win
        return Parse.win_map[play]

    @staticmethod
    def scores_with_solve(row):
        outcome, _, opplay, _ = row
        play = Parse.solve_game(opplay, outcome)
        play_score = Parse.play_scores[play]
        score = Parse.score(play, opplay)
        return score + play_score

    def all_scores_with_solve(self):
        return sum(self.scores_with_solve(row) for row in self._plays)


def main(second_flag):
    with open("input2.txt") as f:
        games = Parse(f)
    if not second_flag:
        return games.sum_scores()
    return games.all_scores_with_solve()
