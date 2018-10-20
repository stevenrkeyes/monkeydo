import sys
import pickle

import game_constants
import towers
import play_build_order

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print()
		print("You must pass the name of the generation and build order to run. Example:")
		print("   $ python run_build_orders.py gen_3 7")
		print()
		sys.exit()

	filename = sys.argv[1] + ".pkl"
	with open(filename, 'rb') as f:
		pretested_build_order_results, build_orders = pickle.load(f)

	pretested_build_orders = [b[0] for b in pretested_build_order_results]

	build_orders = pretested_build_orders + build_orders

	i = int(sys.argv[2])

	print(build_orders[i])

	print("Running build order " + sys.argv[1] + "_" + str(i))
	build_order = build_orders[i]
	end_time, build_order_index, stats_list = play_build_order.play(build_order)
	print("End time: " + str(end_time))
	if build_order_index < len(build_order):
		print("Last step reached: " + str(build_order_index) + ", " + repr(build_order[build_order_index]))
	else:
		print("Got to end of build order.")

