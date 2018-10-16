import random
import pickle

import game_constants
import towers
import map_manager
import play_build_order
import generate_build_orders

build_order = generate_build_orders.generate_build_order()

for step in build_order:
	print(step)

end_time, build_order_index, stats_list = play_build_order.play(build_order)

with open('data.pkl', 'wb') as f:
	data = (build_order, build_order_index, stats_list)
	pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
