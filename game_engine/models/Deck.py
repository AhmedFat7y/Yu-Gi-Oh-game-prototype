import os
import json
from Card import Card
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Deck:
  # def __init__(self, cards):
  #   self.cards = cards

  def __init__(self, id):
    self.cards = []
    if id == 1:
      self.load_kaiiba_cards()
    elif id == 2:
      self.load_yugi_cards()
    else:
      raise Exception('unknown deck id')
    self.clean_cards()


  #remove any card that is not normal monster
  def clean_cards(self):
    temp_cards = list(self.cards)
    for card in temp_cards:
      if card.card_type != 'N/A':
        self.cards.remove(card)
    random.shuffle(self.cards)

      #deck_path relaative to game engine.
  def load_deck_cards_json(self, deck_path):
    with open(os.path.join(BASE_DIR, deck_path)) as json_f:
      self.cards = json.loads(json_f.read(), object_hook=Card.card_loader)

  def load_kaiiba_cards(self):
    self.load_deck_cards_json('data/kaiiba_cards.json')

  def load_yugi_cards(self):
    self.load_deck_cards_json('data/yugi_cards.json')

  def draw_card(self):
    return self.cards.pop()

  def __str__(self):
    return str(len(self.cards))