import random
import pickle

import game_constants
import towers

import map_manager
import play_build_order

# make up a build order, using a map_manager to avoid invalid tower placements
mm = map_manager.MapManager("occupancy_grid.png")
build_order = []
for i in range(1):
	#action_enum = random.randint(5 + 2*len(towers))
	action_enum = random.randint(0,5)
	#switch based on action type
	tower_type = towers.TowerTypes.DART
	x = random.randint(0, mm.shape[1] - 1)
	y = random.randint(game_constants.url_bar_height, mm.shape[0] - 1)
	while mm.is_occupied((x,y)):
		x = random.randint(0, mm.shape[1] - 1)
		y = random.randint(game_constants.url_bar_height, mm.shape[0] - 1)
	coords = (x, y)
	mm.add_object(coords, game_constants.tower_interference_radius)
	step = play_build_order.BuildOrderStep(tower_type, coords)
	build_order.append(step)

end_time, build_order_index, stats_list = play_build_order.play(build_order)

with open('data.pkl', 'wb') as f:
	data = (build_order, build_order_index, stats_list)
	pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


'''
t = 0
print("Build order:")
for i in range(len(build_order)):
	print('{:>10}'.format(round(t, 3)), "sec:", build_order[i])
	t += build_order_delays[i]
print(gm.get_stats())
'''

'''
here's how we can generate a build order
 - pick a random time to do a step
 - when that time arrives, pick a random type of step (out of 5 + 2*n options, where n is the current number of towers)
   - if we can't actually afford that option then choose another option
   - if we can't actually afford any options, then skip
   - if it's a tower, then pick a non-occupied place on the map, and add it to the occupancy grid
 - repeat
'''

'''
get round
get money
get lives
'''