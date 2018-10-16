import enum

class TowerTypes(enum.IntEnum):
	DART = 0
	TACK = 1
	ICE = 2
	BOMB = 3
	SUPER = 4

class Tower:
	def __init__(self, coords, tower_type):
		self.coords = coords
		self.tower_type = tower_type

	def __repr__(self):
		s = ["Dart", "Tack", "Ice", "Bomb", "Super"][self.tower_type]
		return s + " Tower at " + str(coords[0]) + ", " + str(coords[1])
