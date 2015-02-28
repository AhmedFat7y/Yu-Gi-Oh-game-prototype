from models.Card import Card
from models.Deck import Deck
from models.Graveyard import Graveyard
from models.MonstersZone import MonstersZone


class GameMat:
  def __init__(self, deck1, deck2):
    self.deck1 = deck1
    self.monstersZone1 = MonstersZone()
    self.graveyard1 = Graveyard()
    self.deck2 = deck2
    self.monstersZone2 = MonstersZone()
    self.graveyard2 = Graveyard()

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
    print  '_' * 10
    for card in monstersZone1.cards:
      if card.is_def():
        print '_'
      elif card.is_attk():
        print '|'
      elif card.is_set():
        print '\\'