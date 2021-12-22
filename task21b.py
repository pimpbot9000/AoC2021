import itertools as it
import copy
from collections import Counter


class Game:

    def __init__(self, position1, position2, win=21):
        self.win = win
        self.turn = 1
        self.score1 = 0
        self.score2 = 0
        self.position1 = position1
        self.position2 = position2

    def play_turn(self, move):
        new_game = copy.copy(self)

        if self.turn == 1:
            new_game.position1 = (new_game.position1 + move - 1) % 10 + 1
            new_game.score1 += new_game.position1
            new_game.turn = 2
        elif self.turn == 2:
            new_game.position2 = (new_game.position2 + move - 1) % 10 + 1
            new_game.score2 += new_game.position2
            new_game.turn = 1
        return new_game

    def get_state(self):
        return (self.position1, self.position2, self.score1, self.score2, self.turn)

    def is_win(self):
        if self.score1 >= self.win:
            return 1
        elif self.score2 >= self.win:
            return 2
        else:
            return 0

class Play:

    def __init__(self, game, throws):
        self.game = game
        self.throws = throws
        self.states = {}

    def play(self, player=1):

        states = {}
        # state: (player, p1score, p2score, p1position, p2position)

        def recurse(game, N):
            nonlocal player
            nonlocal states

            if player == 1:

              if game.is_win() == 1 and player == 1:
                  return N
              elif game.is_win() == 2:
                  return 0

            elif player == 2:

              if game.is_win() == 1:
                  return 0
              elif game.is_win() == 2:
                  return N
            
            if game.get_state() in states:
                return N * states[game.get_state()]
            else:
                wins = 0
                new_games = [(game.play_turn(throw), n) for throw, n in self.throws.items()]
                for new_game, n in new_games:
                    wins += recurse(new_game, n)

                states[game.get_state()] = wins 
                
                return wins * N

        return recurse(self.game, 1)    

throws = list(it.product(*[[1, 2, 3] for _ in range(3)]))
sums = [sum(x) for x in throws]
throws = Counter(sums)

# Initialize with puzzle input
game = Game(9, 3)

p = Play(game, throws)
print(p.play(player=1))
print(p.play(player=2))
