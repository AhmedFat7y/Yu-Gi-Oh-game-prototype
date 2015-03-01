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
  #BATTLE_PHASE = 4
  MAIN_PHASE_2 = 8
  END_PHASE = 9

  BATTLE_PHASE_START_STEP = 4
  BATTLE_PHASE_BATTLE_STEP = 5
  BATTLE_PHASE_DAMAGE_STEP = 6
  BATTLE_PHASE_END_STEP = 7

  def __init__(self):
    self.game_running = False
    self.current_phase = GameEngine.DRAW_PHASE
    self.turns = 0
    self.deck1 = Deck(1)
    self.deck2 = Deck(2)
    self.game_mat = GameMat(self.deck1, self.deck2)
    self.player1 = Player(1, self.deck1, self, self.game_mat)
    self.player1.goes_first()
    self.player2 = Player(2, self.deck2, self, self.game_mat)
  
  
  def is_first_turn(self):
    return self.turns == 0
  
  def current_turn_player(self):
    if self.turns % 2 == 0:
      return self.player1
    else:
      return self.player2

  def skip_battle_phase(self):
    self.current_phase = GameEngine.MAIN_PHASE_2

  def enter_battle_phase(self):
    self.current_phase = GameEngine.BATTLE_PHASE_START_STEP

  def end_battle_phase(self):
    self.current_phase = GameEngine.BATTLE_PHASE_END_STEP

  def goto_next_phase(self):
    print '[phase-------] moving phases'
    print '--------------------------------------------------------------'
    if self.is_first_turn():
      if self.current_phase ==GameEngine.MAIN_PHASE_1:
        self.skip_battle_phase()# if it's first turn skip battle phase
    elif self.current_phase > GameEngine.MAIN_PHASE_1 and self.current_phase < GameEngine.MAIN_PHASE_2:
      self.skip_battle_phase()
    self.current_phase = (self.current_phase + 1) % (GameEngine.END_PHASE + 1) #go to BATTLE_PHASE

  def start(self):
    self.game_running = True
    player1.first_draw()
    player2.first_draw()
  
  def check_phase(self):
    current_player = self.current_turn_player()
    if self.current_phase == game_engine.DRAW_PHASE:
      print '[phase-------] DRAW_PHASE'
      print '[action------] Player-%i: Draw a card. No spell or trap cards to activate . . .' % current_player.id
    elif self.current_phase == game_engine.STANDBY_PHASE:
      print '[phase-------] STANDBY_PHASE'
      print '[action------] Player-%i: No effects to resolve. No traps to activate? . . .' % current_player.id
    elif self.current_phase == game_engine.MAIN_PHASE_1:
      print '[phase-------] MAIN_PHASE_1'
      print '[action------] Player-%i: Summon or set a monster . . .' % current_player.id
      print '[action------] Player-%i: Flip Summon or Special Summon a monster . . .' % current_player.id
      print '[action------] Player-%i: change a monster position . . .' % current_player.id
      print '[action------] Player-%i: No spell or trap cards to activate . . .' % current_player.id
      print '[action------] Player-%i: No spell or trap cards to set . . .' % current_player.id











#---------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
  game_engine = GameEngine()
  player1 = game_engine.player1
  player2 = game_engine.player2
  game_engine.start()
  print 'deck 1: %s' % game_engine.deck1
  print 'deck 2: %s' % game_engine.deck2
  print 'current_player: %s' % (game_engine.current_turn_player())
  game_engine.check_phase()
  player1.draw_card()
  game_engine.goto_next_phase()
  print 'current_player: %s' % (game_engine.current_turn_player())
  game_engine.check_phase()
  if player1.play_card():
    game_engine.goto_next_phase()
  game_engine.check_phase()
  game_engine.goto_next_phase()
  game_engine.check_phase()
  player1.play_card()
  game_engine.goto_next_phase()
  game_engine.check_phase()
  game_engine.game_mat.display()