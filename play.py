import time
import random

import game_manager
import game_constants
import towers

gm = game_manager.game_manager()
gm.start()

print("hi")
print(gm.window_height)
time.sleep(1)

'''
for i in range(60):
	gm.print_relative_mouse_position()
	time.sleep(1)
'''

print(gm.get_stats())


max_wait = 8

towers_build = []
build_order = []
build_order_delays = []

for i in range(30):
	#action_enum = random.randint(5 + 2*len(towers))
	action_enum = random.randint(0,5)
	#switch based on action type
	tower_type = towers.tower_types.DART
	x = random.randint(0, game_constants.map_width-1)
	y = random.randint(game_constants.url_bar_height, gm.window_height-1)
	while gm.is_occupied((x,y)):
		x = random.randint(0, game_constants.map_width-1)
		y = random.randint(game_constants.url_bar_height, gm.window_height-1)
	gm.build_tower(tower_type, (x, y))
	build_order.append(tower_type)

	time.sleep(0.2)

	wait_time = random.uniform(0, max_wait)
	build_order_delays.append(wait_time)
	gm.click_start_round()

	time.sleep(wait_time)

t = 0
print("Build order:")
for i in range(len(build_order)):
	print('{:>10}'.format(round(t, 3)), "sec:", build_order[i])
	t += build_order_delays[i]
print(gm.get_stats())

'''
here's how we can generate a build order
 - pick a random time to do a step
 - when that time arrives, pick a random type of step (out of 5 + 2*n options, where n is the current number of towers)
   - if we can't actually afford that option then choose another option
   - if we can't actually afford any options, then skip
   - if it's a tower, then pick a non-occupied place on the map, and add it to the occupancy grid
 - repeat
'''



time.sleep(3)

print("bye")
gm.end()


'''
get round
get money
get lives
'''