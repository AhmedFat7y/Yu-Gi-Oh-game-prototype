from Card import Card


class MonstersZone:
  def __init__(self):
    self.cards = []

  def get_card(self, card_name):
    return Card.get_card_by_name(self.cards, card_name)

  def remove_card(self, card):
    try:
      self.cards.remove(card)
    except ValueError:
      print card.name, [c.name for c in self.cards]
      raise

  def add_monster(self, card):
    self.cards.append(card)