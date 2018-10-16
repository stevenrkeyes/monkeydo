# takes a generation of build orders, runs them all, and saves their stats

import sys
import pickle

import game_constants
import towers
import play_build_order

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print()
		print("You must pass the name of the generation to run. Example:")
		print("   $ python run_build_orders.py gen_3")
		print()
		sys.exit()

	filename = sys.argv[1] + ".pkl"
	with open(filename, 'rb') as f:
		build_orders = pickle.load(f)

	for i in range(len(build_orders)):
		build_order = build_orders[i]
		end_time, build_order_index, stats_list = play_build_order.play(build_order)
		filename = sys.argv[1] + "_" + str(i) + "_stats" + ".pkl"
		data = (build_order, build_order_index, stats_list)
		with open(filename, 'wb') as f:
			pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

