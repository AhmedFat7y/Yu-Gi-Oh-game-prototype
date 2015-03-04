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

  def summon_attk(self):
    self.position = 'attk'
    self.face = 'up'

  def summon_def(self):
    self.position = 'def'
    self.face = 'up'

  def flip_summon(self):
    self.summon_def()

  def is_def(self):
    return self.position == 'def' and self.face == 'up'

  def is_attk(self):
    return self.position == 'attk'

  def is_set(self):
    return self.position == 'def' and self.face == 'down'

  def set_position(self, state):
    if state == 'set':
      self.summon_set()
    elif state == 'def':
      self.summon_def()
    elif state == 'attk':
      self.summon_attk()
    elif state == 'flip':
      self.flip_summon()
    else:
      raise Exception ('UnKnown State . . .')

  def reset(self):
    self.position = ''
    self.face = ''

  @staticmethod
  def get_card_by_name(cards, card_name):
    for card in cards:
      if card.name == card_name:
        return card
    err_msg = 'Wrong Card Name "%s"\nAvailble cards: %s' % (card_name, [card.name for card in cards ])
    raise Exception(err_msg)

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
  def __unicode__(self):
    return self.__str__()
  def __str__(self):
    return "(name: %s, level: %s, attack: %s, defece, %s)" % (self.name, self.level, self.attack, self.defence)