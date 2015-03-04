from models.Card import Card
from models.Deck import Deck
from models.Graveyard import Graveyard
from models.MonstersZone import MonstersZone


class GameMat:
  def __init__(self, deck1, deck2, game_engine):
    self.deck1 = deck1
    self.monstersZone1 = MonstersZone()
    self.graveyard1 = Graveyard()
    self.deck2 = deck2
    self.monstersZone2 = MonstersZone()
    self.graveyard2 = Graveyard()
    self.game_engine = game_engine

  def opposing_monstersZone(self):
    if self.game_engine.current_player().id == 2:
      return self.monstersZone1
    else:
      return  self.monstersZone2

  def current_monstersZone(self):
    if self.game_engine.current_player().id == 1:
      return self.monstersZone1
    else:
      return  self.monstersZone2

  def opposing_graveyard(self):
    if self.game_engine.current_player().id == 2:
      return self.graveyard1
    else:
      return  self.graveyard2

  def current_graveyard(self):
    if self.game_engine.current_player().id == 1:
      return self.graveyard1
    else:
      return  self.graveyard2

  def display(self):
    """
     _______________________________
    |                               |
    |                               |
    |                               |
    |                               |
    |                               |
    |                               |
    |                               |
    |                               |
    |                               |
    |                               |
    |_______________________________|
    """
    print  '', '_' * 17
    temp_str = '|  '
    i = 0
    for card in self.monstersZone1.cards:
      if card.is_def():
        temp_str += '_'
      elif card.is_attk():
        temp_str += '|'
      elif card.is_set():
        temp_str += '/'
      i += 1
      temp_str += '  '
    if i < 5:
        temp_str += '#  ' * (5-i)
    print (temp_str + '|')
    print '|                 |'
    print '|                 |'
    i=0
    temp_str = "|  "
    for card in self.monstersZone2.cards:
      if card.is_def():
        temp_str += '_'
      elif card.is_attk():
        temp_str += '|'
      elif card.is_set():
        temp_str += '/'
      i += 1
      temp_str += '  '
    if i < 5:
      temp_str += '#  ' * (5-i)
    print (temp_str + '|')
    print  '', '_' * 17
    