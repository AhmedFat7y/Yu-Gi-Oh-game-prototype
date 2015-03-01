class Card:
  def __init__(self, name, attack, defence, level, monster_type):
    self.name = name
    self.attack = attack
    self.defence = defence
    self.level = level
    self.monster_type = monster_type
    self.position = "" #attk def
    self.face = "" #up #down

  def summon_set(self):
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
    level = 'N/A'
    if card_dict['level'] != 'N/A':
      level = int(card_dict['level'])
    attack = 'N/A'
    if card_dict['attack'] != 'N/A':
      attack = int(card_dict['attack'])
    defence = 'N/A'
    if card_dict['defence'] != 'N/A':
      defence = int(card_dict['defence'])
    return Card(card_dict['title'], attack,
      defence, level, card_dict['monster_type'])
  def __str__(self):
    return "name: %s, attack: %s, defece, %s" % (self.name, self.attack, self.defence)