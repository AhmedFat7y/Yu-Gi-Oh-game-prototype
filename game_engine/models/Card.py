class Card:
  def __init__(self, name, attack, defence, level, card_type):
    self.name = name
    self.attack = attack
    self.defence = defence
    self.level = level
    self.card_type = card_type
    self.position = "" #attk def
    self.face = "" #up #down
  def set(self):
    self.position = 'def'
    self.face = 'down'

  def summon(self):
    self.position = 'attk'
    self.face = 'up'

  def summon_def(self):
    self.position = 'def'
    self.face = 'up'

  def flip_summon(self):
    summon_def(self)

  def is_def(self):
    return self.position == 'def'

  def is_attk(self):
    return self.position == 'attk'

  def is_set(self):
    return self.is_def() and self.face == 'down'

  @staticmethod
  def card_loader(card_dict):
    # print card_dict
    return Card(card_dict['title'], card_dict['attack'],
      card_dict['defence'], card_dict['level'], card_dict['card_type'])
