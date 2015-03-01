import random
class Player:
  def __init__(self, id, deck, game_engine, game_mat):
    self.id = id
    self.first_turn = False
    self.deck = deck
    self.cards_in_hand = []
    self.game_engine = game_engine
    self.game_mat = game_mat

  def first_draw(self):
    for i in range(5):
      self.cards_in_hand.append(self.deck.draw_card())

  def draw_card(self):
    temp =self.deck.draw_card()
    self.cards_in_hand.append(temp)
    return temp

  #test method
  def play_card(self):
    if self.game_engine.current_phase != self.game_engine.MAIN_PHASE_1:
      print '[error-------] only trap cards are allowed'
      return False
    rand_card = random.choice(self.cards_in_hand)
    if rand_card.attack < 1800:
      if rand_card.defence < 1200:
        rand_card.summon_set()
      else:
        rand_card.summon_def()
    else:
      rand_card.summon()
      
    print 'player %i played card %s' % (self.id, rand_card)
    self.game_mat.monstersZone1.add_monster(rand_card)
    return True

  def goes_first(self):
    self.first_turn = True

  def __str__(self):
    return "id: %i, deck: %s" % (self.id, self.deck.__str__())