# generates an inital generation of build orders
# and saves it to a specified filename

import sys
import random
import pickle

import game_constants
import towers
import map_manager
import play_build_order
import evolutionary_constants

def generate_build_order():
	# make up a build order, using a map_manager to avoid invalid tower placements
	mm = map_manager.MapManager("occupancy_grid.png")
	build_order = []
	for i in range(evolutionary_constants.BUILD_ORDER_LENGTH):
		#action_enum = random.randint(5 + 2*len(towers))
		action_enum = random.randint(0,4)

		tower_type = towers.TowerTypes(action_enum)
		x = random.randint(0, mm.shape[1] - 1)
		y = random.randint(game_constants.url_bar_height, mm.shape[0] - 1)
		while mm.is_occupied((x,y)):
			x = random.randint(0, mm.shape[1] - 1)
			y = random.randint(game_constants.url_bar_height, mm.shape[0] - 1)
		coords = (x, y)
		mm.add_object(coords, game_constants.tower_interference_radius)
		step = play_build_order.BuildOrderStep(tower_type, coords)
		build_order.append(step)
	return build_order

def generate_build_orders(num_to_generate):
	build_orders = []
	for i in range(num_to_generate):
		build_order = generate_build_order()
		build_orders.append(build_order)
	return build_orders

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print()
		print("You must pass a name for the generation file. Example:")
		print("   $ python generate_build_orders.py gen_0")
		print()
		sys.exit()

	build_orders = generate_build_orders(evolutionary_constants.NUM_TO_GENERATE)

	pretested_build_order_results = []

	filename = sys.argv[1] + ".pkl"
	with open(filename, 'wb') as f:
		pickle.dump((pretested_build_order_results, build_orders), f, pickle.HIGHEST_PROTOCOL)
