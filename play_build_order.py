import time

import game_manager
import game_constants
import towers

class BuildOrderStep:
	def __init__(self, tower_type, coords):
		self.tower_type = tower_type
		self.coords = coords

	# I'm using __str__ as the concise representation
	def __str__(self):
		return ["Dart", "Tack", "Ice", "Bomb", "Super"][self.tower_type]

	# __repr__ is the unambiguous representation
	def __repr__(self):
		return self.__str__() + " Tower at " + str(self.coords[0]) + ", " + str(self.coords[1])

# build_order is a list of build_order_step
# this function returns the time at which the game ended, the index of the last build order
# step, and a list of tuples containing the stats of the game over time
def play(build_order):
	start_time = time.time()
	stats_list = []
	gm = game_manager.GameManager()
	gm.start()
	lives = 40
	build_order_index = 0
	while lives > 0 and build_order_index < len(build_order):
		step = build_order[build_order_index]
		if gm.can_afford_tower(step.tower_type):
			gm.build_tower(step.tower_type, step.coords)
			build_order_index += 1
			print(step)
		time.sleep(0.1)
		gm.click_start_round()
		stats = gm.get_stats()
		lives = stats[2]
		stats_list.append((time.time() - start_time, stats))
	while lives > 0:
		time.sleep(0.1)
		gm.click_start_round()
		stats = gm.get_stats()
		lives = stats[2]
		stats_list.append((time.time() - start_time, stats))
		print(lives)
	gm.end()
	end_time = stats_list[-1][0]
	return end_time, build_order_index, stats_list
