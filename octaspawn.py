from copy import deepcopy

from easyAI import TwoPlayersGame
from timeit import default_timer as timer
from random import randint

# Convert D7 to (3,6) and back...
to_string = lambda move: " ".join(["ABCDEFGHIJ"[move[i][0]] + str(move[i][1] + 1)
                                   for i in (0, 1)])
to_tuple = lambda s: ("ABCDEFGHIJ".index(s[0]), int(s[1:]) - 1)


class Hexapawn(TwoPlayersGame):
    """
    A nice game whose rules are explained here:
    http://fr.wikipedia.org/wiki/Hexapawn
    """

    def __init__(self, players, size = (4, 4)):
        self.size = M, N = size
        p = [[(i, j) for j in range(N)] for i in [0, M - 1]]

        for i, d, goal, pawns in [(0, 1, M - 1, p[0]), (1, -1, 0, p[1])]:
            players[i].direction = d
            players[i].goal_line = goal
            players[i].pawns = pawns

        self.players = players
        random_player = randint(1,2)
        self.nplayer = random_player
        
    def play(self, nmoves=1000, verbose=True):

        history = []
        times = []

        if verbose:
            self.show()

        for self.nmove in range(1, nmoves + 1):
            start = timer()
            if self.is_over():
                break

            move = self.player.ask_move(self)
            history.append((deepcopy(self), move))
            self.make_move(move)

            # a = randint() * 10

            if verbose:
                print("\nMove #%d: player %d plays %s :" % (
                      self.nmove, self.nplayer, str(move)))
                self.show()

            self.switch_player()

            time = round(timer() - start, 5)

            print("Time to take move = ", time)
            if time < 5:
                times.append(time)
        times.append(time)
        history.append(deepcopy(self))
        return history, times


    def possible_moves(self):
        moves = []
        opponent_pawns = self.opponent.pawns
        d = self.player.direction
        for i, j in self.player.pawns:
            if (i + d, j) not in opponent_pawns:
                moves.append(((i, j), (i + d, j)))
            if (i + d, j + 1) in opponent_pawns:
                moves.append(((i, j), (i + d, j + 1)))
            if (i + d, j - 1) in opponent_pawns:
                moves.append(((i, j), (i + d, j - 1)))

        return list(map(to_string, [(i, j) for i, j in moves]))

    def make_move(self, move):
        move = list(map(to_tuple, move.split(' ')))
        ind = self.player.pawns.index(move[0])
        self.player.pawns[ind] = move[1]
        if move[1] in self.opponent.pawns:

            self.opponent.pawns.remove(move[1])

    def lose(self):
        return (any([i == self.opponent.goal_line
                for i, j in self.opponent.pawns])
                or (self.possible_moves() == []))

    def is_over(self):
        return self.lose()

    def show(self):
        f = lambda x: '1' if x in self.players[0].pawns else (
            '2' if x in self.players[1].pawns else '.')
        print("\n".join([" ".join([f((i, j))
                                   for j in range(self.size[1])])
                         for i in range(self.size[0])]))


if __name__ == "__main__":
    from easyAI import AI_Player, Human_Player, Negamax
    import matplotlib.pyplot as plt
    import numpy as np
    wins = []

    for i in range(10):

        scoring = lambda game: -100 if game.lose() else 0
        ai = Negamax(10, scoring)
        game = Hexapawn([AI_Player(ai), AI_Player(ai)])
        play_game = game.play()
        history, times = play_game

        player1_time = []
        player2_time = []
        couter = 1
        for item in times:
            if couter % 2 == 0:
                player2_time.append(item)
            else:
                player1_time.append(item)

            couter += 1

        if i == 1:
            plt.figure(1)
            plt.plot(player1_time)
            plt.xlabel("Move")
            plt.ylabel("Time [s]")
            plt.title("Time needed for AI to make move Player 1")

            plt.figure(2)
            plt.plot(player2_time)
            plt.xlabel("Move")
            plt.ylabel("Time [s]")
            plt.title("Time needed for AI to make move Player 2")
            plt.show()

        print("player %d wins after %d turns " % (game.nopponent, game.nmove))

        if game.nopponent == 1:
            wins.append(1)
        else:
            wins.append(2)

    print(wins)
