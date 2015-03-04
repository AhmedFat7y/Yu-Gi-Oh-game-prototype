from models.Card import Card
from models.Deck import Deck
from models.Graveyard import Graveyard
from models.MonstersZone import MonstersZone
from models.GameMat import GameMat
from models.Player import Player
import random


class GameEngine:
  DRAW_PHASE = 0
  STANDBY_PHASE = 1
  MAIN_PHASE_1 = 2
  BATTLE_PHASE = 3
  MAIN_PHASE_2 = 4
  END_PHASE = 5

  BATRTLE_PHASE_NONE_STEP = 0
  BATTLE_PHASE_START_STEP = 1
  BATTLE_PHASE_BATTLE_STEP = 2
  BATTLE_PHASE_DAMAGE_STEP = 3
  BATTLE_PHASE_END_STEP = 4

  def __init__(self):
    self.cards_used_this_turn = []
    self.game_running = False
    self.current_phase = GameEngine.DRAW_PHASE
    self.current_battle_Step = GameEngine.BATTLE_PHASE_START_STEP
    self.turns = 0
    self.deck1 = Deck(1)
    self.deck2 = Deck(2)
    self.game_mat = GameMat(self.deck1, self.deck2, self)
    self.player1 = Player(1, self.deck1, self)
    self.player1.goes_first()
    self.player2 = Player(2, self.deck2, self)
  
  def use_this_card(self, card):
    self.cards_used_this_turn.append(card)

  def is_first_turn(self):
    return self.turns == 0

  def current_player(self):
    if self.turns % 2 == 0:
      return self.player1
    else:
      return self.player2

  def skip_battle_phase(self):
    self.current_phase = GameEngine.MAIN_PHASE_2

  def battle_loop(self):
    if self.current_phase != GameEngine.BATTLE_PHASE:
      return False
    if self.current_battle_Step == GameEngine.BATTLE_PHASE_START_STEP:
      self.current_battle_Step = GameEngine.BATTLE_PHASE_BATTLE_STEP
    else:
      self.current_battle_Step = (((self.current_battle_Step - 2) + 1) % GameEngine.BATTLE_PHASE_BATTLE_STEP) + 2

  def goto_next_battle_step(self):
    if self.current_phase != GameEngine.BATTLE_PHASE:
      return False
    self.current_battle_Step = (self.current_battle_Step + 1) % (GameEngine.BATTLE_PHASE_END_STEP + 1)
  
  def enter_battle_phase(self):
    if self.current_phase == GameEngine.BATTLE_PHASE:
      self.current_battle_Step = GameEngine.BATTLE_PHASE_START_STEP

  def end_battle_phase(self):
    if self.current_phase == GameEngine.BATTLE_PHASE:
      self.current_battle_Step = GameEngine.BATTLE_PHASE_END_STEP

  def goto_next_phase(self):
    print '[phase-------] moving phases'
    print '--------------------------------------------------------------'
    if self.is_first_turn():
      if self.current_phase == GameEngine.MAIN_PHASE_1:
        self.skip_battle_phase()# if it's first turn skip battle phase
        return
    elif self.current_phase > GameEngine.MAIN_PHASE_1 and self.current_phase < GameEngine.MAIN_PHASE_2:
      self.skip_battle_phase()
      return
    if self.current_phase == GameEngine.END_PHASE:
      self.turns += 1
      self.current_phase = GameEngine.DRAW_PHASE
    self.current_phase = (self.current_phase + 1) % (GameEngine.END_PHASE) #go to next phase

  def start(self):
    self.game_running = True
    #player1.first_draw()
    #player2.first_draw()
  def check_battle_step(self):
    current_player = self.current_player()
    if self.current_battle_Step == GameEngine.BATTLE_PHASE_START_STEP:
      print '[Battle Phase] Start Step'
      print '[action------] Player-%i: Starts battle . . .' % current_player.id
    elif self.current_battle_Step == GameEngine.BATTLE_PHASE_BATTLE_STEP:
      print '[Battle Phase] Battle Step'
    elif self.current_battle_Step == GameEngine.BATTLE_PHASE_DAMAGE_STEP:
      print '[Battle Phase] Damage Step'
    elif self.current_battle_Step == GameEngine.BATTLE_PHASE_END_STEP:
      print '[Battle Phase] End Step'
      print '[action------] Player-%i: Ends battle . . .' % current_player.id
    elif self.current_battle_Step == GameEngine.BATRTLE_PHASE_NONE_STEP or self.current_phase != GameEngine.BATTLE_PHASE:
      print '[error-------] Not battle phase'
  def check_phase(self):
    current_player = self.current_player()
    if self.current_phase == GameEngine.DRAW_PHASE:
      print '[phase-------] DRAW_PHASE'
      print '[info--------] Player-%i: Draw a card. No spell or trap cards to activate . . .' % current_player.id
    elif self.current_phase == GameEngine.STANDBY_PHASE:
      print '[phase-------] STANDBY_PHASE'
      print '[info--------] Player-%i: No effects to resolve. No traps to activate? . . .' % current_player.id
    elif self.current_phase == GameEngine.MAIN_PHASE_1:
      print '[phase-------] MAIN_PHASE_1'
      print '[info--------] Player-%i: Summon or set a monster . . .' % current_player.id
      print '[info--------] Player-%i: Flip Summon or Special Summon a monster . . .' % current_player.id
      print '[info--------] Player-%i: change a monster position . . .' % current_player.id
      print '[info--------] Player-%i: No spell or trap cards to activate . . .' % current_player.id
      print '[info--------] Player-%i: No spell or trap cards to set . . .' % current_player.id
    elif self.current_phase == GameEngine.BATTLE_PHASE:
      print '[phase-------] BATTLE_PHASE'
    elif self.current_phase == GameEngine.MAIN_PHASE_2:
      print '[phase-------] MAIN_PHASE_2'
    elif self.current_phase == GameEngine.END_PHASE:
      print '[phase-------] END_PHASE'






#---------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
  game_engine = GameEngine()
  game_engine.start()
  turns = [('Battle Ox', 'set')]
  for turn in turns:
    player = game_engine.current_player()
    """ Draw Phase """
    player.draw_card(turn[0])
    game_engine.check_phase()
    game_engine.goto_next_phase()
    """ Standby Phase """
    game_engine.check_phase()
    game_engine.goto_next_phase()
    """ Main Phase 1 """
    game_engine.check_phase()
    player.play_card(turn[1])
    game_engine.goto_next_phase()
    """ Battle Phase """
    game_engine.enter_battle_phase()
    game_engine.battle_loop()
    game_engine.end_battle_phase()
    """ Main Phase 2 """
    game_engine.check_phase()
    game_engine.goto_next_phase()
    """ End Phase """
    game_engine.check_phase()
    game_engine.goto_next_phase()
    game_engine.game_mat.display()
