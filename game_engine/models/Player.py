import random
from Errors import NO_ERROR, NO_ENOUGH_SACRIFICES, MONSTERS_ZONE_IS_FULL

def check_error_message(error_code):
  if error_code == NO_ERROR:
    return 'No Error'
  elif error_code == NO_ENOUGH_SACRIFICES:
    return 'No enough sacrifices available'
  elif error_code == MONSTERS_ZONE_IS_FULL:
    return 'No place in monster zone'

def print_error(card, error_code):
  print '[error-------] Cannot summon %s' % (card)
  print '[phase-------] Reson: %s' % check_error_message(error_code)

def print_sucess_summon(card, sacrifices):
  summoning_message = 'No sacrifices needed'
  if len(sacrifices) > 0:
    summoning_message = '%i card(s) were tributed.' % len(sacrifices)
  print '[success-----] %s was successfully summoned.' % card
  print '[success-----] %s' % summoning_message

class Player:
  def __init__(self, id, deck, game_engine):
    self.id = id
    self.first_turn = False
    self.deck = deck
    self.cards_in_hand = []
    self.game_engine = game_engine
    self.game_mat = game_engine.game_mat

  def first_draw(self):
    for i in range(5):
      self.cards_in_hand.append(self.deck.draw_card())

  def draw_card(self, card_name=None):
    temp =self.deck.draw_card(card_name)
    self.cards_in_hand.append(temp)
    return temp

  def normal_summon(self, card, monstersZone):
    sacrifices = []
    if len(monstersZone.cards) == 5:
      return False, MONSTERS_ZONE_IS_FULL, sacrifices
    if card.level == 5 or card.level == 6:
      if len(monstersZone.cards) > 0:
        sacrifices.append(monstersZone.cards.pop())
      else:
        return False, NO_ENOUGH_SACRIFICES, sacrifices
    elif card.level >= 7:
      if len(monstersZone.cards) > 1:
        sacrifices.append(monstersZone.cards.pop())
        sacrifices.append(monstersZone.cards.pop())
      else:
        return False, NO_ENOUGH_SACRIFICES, sacrifices
    monstersZone.add_monster(card)
    return True, NO_ERROR, sacrifices

  def pick_card(self, monstersZone):
    card = self.cards_in_hand[-1]
    return card

  def send_to_graveyard(self, cards):
    for card in cards:
      self.game_mat.current_graveyard().add_card(card)

  def remove_card_from_hand(self, card):
    self.cards_in_hand.remove(card)
    return True

  #test method
  def play_card(self, card_state):
    if self.game_engine.current_phase != self.game_engine.MAIN_PHASE_1:
      print '[error-------] only trap cards are allowed'
      return False
    monstersZone = self.game_mat.current_monstersZone()
    card = self.pick_card(monstersZone)
    card.set_position(card_state)
    result = self.normal_summon(card, monstersZone)
    if result and result[0]:
      self.remove_card_from_hand(card)
      print_sucess_summon(card, result[2])
    else:
      print_error(card, result[1])
      card.reset()
    self.send_to_graveyard(result[-1])
    print '[action------] player %i played card %s' % (self.id, card)
    return True

  def goes_first(self):
    self.first_turn = True

  def __str__(self):
    return "id: %i, deck: %s" % (self.id, self.deck.__str__())