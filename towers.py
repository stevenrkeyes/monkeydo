import enum

class TowerTypes(enum.Enum):
	DART = 1
	TACK = 2
	ICE = 3
	BOMB = 4
	SUPER = 5

class Tower:
	def __init__(self, coords, tower_type):
		self.coords = coords
		self.tower_type = tower_type
