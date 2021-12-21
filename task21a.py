print('Hello, world!')
import random

class Game:
  
  def __init__(self, position1, position2, dice):
    self.turn = 1
    self.score1 = 0
    self.score2 = 0
    self.position1 = position1
    self.position2 = position2
    self.dice = dice
    
  def play_turn(self, rolls):
    roll_list = [self.dice.roll() for i in range(rolls)]
    move = sum(roll_list)
    
    if self.turn == 1:
      self.position1 = (self.position1 + move - 1 ) % 10 + 1
      self.score1 += self.position1
      self.turn = 2
    elif self.turn == 2:
      self.position2 = (self.position2 + move - 1 ) % 10 + 1
      self.score2 += self.position2
      self.turn = 1
      
  def is_win(self):
    if self.score1 >= 1000:
      return 1
    elif self.score2 >= 1000:
      return 2
    else:
      return 0
  
  def get_nof_rolls(self):
    return self.dice.nof_rolls
      
class Dice:
  def __init__(self):
    self.current = 1
    self.nof_rolls = 0
    
  def roll(self):
    roll = self.current
    self.nof_rolls += 1
    self.current = (self.current + 1 - 1) % 100 + 1
    return roll

g = Game(9, 3, Dice())

while True:
  g.play_turn(3)
  winner = g.is_win()
  if winner != 0:
    print("winner", winner, g.score1)
    print("rolls", g.get_nof_rolls())
    print("player1", g.score1, g.score1 * g.get_nof_rolls())
    print("player2", g.score2, g.score2 * g.get_nof_rolls())
    break
  
 