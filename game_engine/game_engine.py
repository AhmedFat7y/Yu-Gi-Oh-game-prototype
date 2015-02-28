from models.Card import Card
from models.Deck import Deck
from models.Graveyard import Graveyard
from models.MonstersZone import MonstersZone
from models.GameMat import GameMat
from models.Player import Player
import random


class GameEngine:
  DRAW_PHASE = 1
  STANDBY_PHASE = 2
  MAIN_PHASE_1 = 3
  BATTLE_PHASE = 4
  MAIN_PHASE_2 = 5
  END_PHASE = 6

  BATTLE_PHASE_START_STEP = 1
  BATTLE_PHASE_BATTLE_STEP = 2
  BATTLE_PHASE_DAMAGE_STEP = 3
  BATTLE_PHASE_END_STEP = 4

  def __init__(self):
    self.current_phase = GameEngine.DRAW_PHASE
    self.turns = 0
    self.deck1 = Deck(1)
    self.deck2 = Deck(2)
    self.player1 = Player(1, self.deck1)
    self.player1.goes_first()
    self.player2 = Player(2, self.deck2)
    self.game_mat = GameMat(self.deck1, self.deck2)
  
  def is_first_turn(self):
    return self.turns == 0
  
  def current_turn_player(self):
    if self.turns % 2 == 0:
      return self.player1
    else:
      return self.player2

if __name__ == '__main__':
  game_engine = GameEngine()
  print 'deck 1: %s' % game_engine.deck1
  print 'deck 2: %s' % game_engine.deck2
  print 'current_player: %s' % (game_engine.current_turn_player())