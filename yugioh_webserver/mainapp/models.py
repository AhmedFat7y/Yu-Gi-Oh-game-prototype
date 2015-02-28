from django.db import models
# Create your models here.

# class CardBase(models.Model):
#   name = models.CharField(max=500)
#   description = models.TextField(max=1000)
#   card_type = models.ForeignKey('CardType')
#   class Meta:
#     abstract = True

# class Card(CardBase):
#   effect = models.ManyToMany('CardEffect')
#   attribute = models.ForeignKey('CardAttribute')
#   level = models.IntegerField()
#   attack = models.IntegerField()
#   defence = models.IntegerField()
#   pass

# class IconCard(CardBase):
#   icon = models.ForeignKey('IconType')

class CardType(models.Model):
  """
  Normal Monsters, Fusion, Ritual, Trap, Spell, Field
  """
  name = models.CharField(max=500)

class IconType(models.Model):
  name = models.CharField(max=500)

class CardEffect(models.Model):
  name = models.CharField(max=100)

class CardAttribute(models.Model):
  name = models.CharField(max=100)