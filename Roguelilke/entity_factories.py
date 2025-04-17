from components.ai import HostileEnemy
from components.consumables import HealingConsumable
from components.fighter import Fighter
from entity import Actor, Item

""" PLAYER """
player = Actor(
  char="@",
  color=(255, 255, 255),
  name="Player",
  ai_cls=HostileEnemy,
  fighter=Fighter(hp=30, defense=2, power=5),
)

""" ENEMIES """
goblin = Actor(
  char="G",
  color=(63, 127, 63),
  name="Goblin",
  ai_cls=HostileEnemy,
  fighter=Fighter(hp=10, defense=0, power=3),
)

troll = Actor(
  char="T",
  color=(0, 127, 0),
  name="Troll",
  ai_cls=HostileEnemy,
  fighter=Fighter(hp=16, defense=1, power=4),
)

""" CONSUMABLES """
health_potion = Item(
  char="!",
  color=(127, 0, 255),
  name="Healing Potion",
  consumable=HealingConsumable(amount=4),
)