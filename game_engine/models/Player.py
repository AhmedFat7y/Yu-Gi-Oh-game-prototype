class Player:
  def __init__(self, id, deck):
    self.id = id
    self.first_turn = False
    self.deck = deck

  def goes_first(self):
    self.first_turn = True
  def __str__(self):
    return "id: %i, deck: %s" % (self.id, self.deck.__str__())