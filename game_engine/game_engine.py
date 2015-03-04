from models.Card import Card
from models.Deck import Deck
from models.Graveyard import Graveyard
from models.MonstersZone import MonstersZone
from models.GameMat import GameMat
from models.Player import Player
from turn import Turn
import os
import json
import random
import pdb


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
    self.battles = []
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
  def opposing_player(self):
    if self.turns % 2 == 1:
      return self.player1
    else:
      return self.player2

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
      return True
    return False

  def end_battle_phase(self):
    if self.current_phase == GameEngine.BATTLE_PHASE:
      self.current_battle_Step = GameEngine.BATTLE_PHASE_END_STEP
  def send_to_opposing_graveyard(self, card):
    self.game_mat.opposing_graveyard().add_card(card)
    self.game_mat.opposing_monstersZone().remove_card(card)
  
  def send_to_current_graveyard(self, card):
    self.game_mat.current_graveyard().add_card(card)
    self.game_mat.current_monstersZone().remove_card(card)

  def modify_current_player_life_points(self, val):
    self.current_player().life_points += val
  def modify_opposing_player_life_points(self, val):
    self.opposing_player().life_points += val
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
    self.current_phase = (self.current_phase + 1) % (GameEngine.END_PHASE + 1) #go to next phase
  
  def _damage_calculation_set_case_(self, attacker, target):
    result = target.defence - attacker.attack
    if result < 0:
      self.send_to_opposing_graveyard(target)
      self.modify_opposing_player_life_points(result)

  
  def _damage_calculation_def_case_(self, attacker, target):
    result = target.defence - attacker.attack
    if result < 0:
      self.send_to_opposing_graveyard(target)
      self.modify_opposing_player_life_points(result)
  
  def _damage_calculation_attk_case_(self, attacker, target):
    result = attacker.attack - target.attack
    if result > 0:
      self.send_to_opposing_graveyard(target)
      self.modify_opposing_player_life_points(-1 * result)
    elif result == 0:
      self.send_to_opposing_graveyard(target)
      self.send_to_current_graveyard(attacker)
    else:
      self.send_to_current_graveyard(attacker)
      self.modify_current_player_life_points(result) #because result is -ve already

  def fight(self, attacker_name, target_name):
    attacker = self.game_mat.current_monstersZone().get_card(attacker_name)
    target = self.game_mat.opposing_monstersZone().get_card(target_name)
    print '[action------] Monster: %s is attacking Monster: %s' % (attacker.name, target.name)
    if target.is_set():
      target.flip_summon()
    self.battles.append([attacker, target])
  
  def damage_calculation(self):
    for battle in self.battles:
      if battle[-1].is_set():
        self._damage_calculation_set_case_(battle[0], battle[1])
      elif battle[-1].is_def():
        self._damage_calculation_def_case_(battle[0], battle[1])
      elif battle[-1].is_attk():
        self._damage_calculation_attk_case_(battle[0], battle[1])
    self.battles = []

  def start(self):
    self.game_running = True
    #player1.first_draw()
    #player2.first_draw()

  def check_battle_step(self):
    current_player = self.current_player()
    if self.current_phase != GameEngine.BATTLE_PHASE:
      print '[error-------] Not battle phase'
    elif self.current_battle_Step == GameEngine.BATTLE_PHASE_START_STEP:
      print '[Battle Phase] Start Step'
      print '[action------] Player-%i: Starts battle . . .' % current_player.id
    elif self.current_battle_Step == GameEngine.BATTLE_PHASE_BATTLE_STEP:
      print '[Battle Phase] Battle Step'
    elif self.current_battle_Step == GameEngine.BATTLE_PHASE_DAMAGE_STEP:
      print '[Battle Phase] Damage Step'
    elif self.current_battle_Step == GameEngine.BATTLE_PHASE_END_STEP:
      print '[Battle Phase] End Step'
      print '[action------] Player-%i: Ends battle . . .' % current_player.id
    else:
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
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def load_turns():
  turns = []
  turns_path = 'data/turns.json'
  with open(os.path.join(BASE_DIR, turns_path)) as json_f:
    turns = json.loads(json_f.read(), object_hook=Turn.loader)
  return turns



if __name__ == '__main__':
  game_engine = GameEngine()
  game_engine.start()
  turns = load_turns()

  for turn in turns:
    attacks = zip(turn.cards_to_attack, turn.cards_to_target)
    game_engine.check_phase()
    player = game_engine.current_player()
    """ Draw Phase """
    player.draw_card(turn.card_to_draw)
    game_engine.goto_next_phase()
    """ Standby Phase """
    game_engine.check_phase()
    game_engine.goto_next_phase()
    """ Main Phase 1 """
    game_engine.check_phase()
    player.play_card(turn.card_to_play, turn.card_state)
    game_engine.goto_next_phase()
    """ Battle Phase """
    battle = game_engine.enter_battle_phase()
    game_engine.check_battle_step()
    for attack in attacks:
      game_engine.battle_loop()
      game_engine.check_battle_step()
      result = game_engine.fight(attack[0], attack[1])
      game_engine.battle_loop()
      game_engine.damage_calculation()
      game_engine.check_battle_step()
    game_engine.end_battle_phase()
    game_engine.check_battle_step()
    if battle: 
      game_engine.goto_next_phase()
    """ Main Phase 2 """
    game_engine.check_phase()
    game_engine.goto_next_phase()
    """ End Phase """
    game_engine.check_phase()
    game_engine.goto_next_phase()
    game_engine.game_mat.display()
    print '####################################################'
    print ''
  print game_engine.player1
  print game_engine.player2
