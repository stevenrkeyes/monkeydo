# generates a the next generation of build orders based on how the current generation did

import sys
import random
import pickle
import numpy
import copy

import game_constants
import towers
import map_manager
import play_build_order
import evolutionary_constants

def fitness(build_order_stats):
	# the fitness will be defined as a function of the last round acheieved,
	# with ties broken by how much money is left over
	build_order, build_order_index, stats_list = build_order_stats
	last_t, last_stats = stats_list[-1]
	last_round = last_stats[0]
	last_money = last_stats[1]
	return float(last_round) + 0.000001 * float(last_money)

def randint_except(a, b, except_n):
	r = list(range(a, except_n)) + list(range(except_n + 1, b))
	return random.choice(r)

def concise_str(build_order):
	return ' '.join([str(step) for step in build_order])

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print()
		print("You must pass names for the generations. Example:")
		print("   $ python generate_build_orders.py gen_3 gen_4")
		print()
		sys.exit()

	parent_generation_filename = sys.argv[1] + ".pkl"
	child_generation_filename = sys.argv[2] + ".pkl"

	with open(parent_generation_filename, 'rb') as f:
		build_orders1, build_orders2 = pickle.load(f)
	num_parents = len(build_orders1) + len(build_orders2)

	# the stats for each build order
	list_of_build_order_stats = []
	for i in range(num_parents):
		filename = sys.argv[1] + "_" + str(i) + "_stats" + ".pkl"
		with open(filename, "rb") as f:
			data = pickle.load(f)
		list_of_build_order_stats.append(data)

	print()
	print("Parent Generation:")
	print()

	for i in range(len(list_of_build_order_stats)):
		build_order_stats = list_of_build_order_stats[i]
		parent_build_order = build_order_stats[0]
		print(sys.argv[1] + "_" + str(i))
		print(concise_str(parent_build_order))
		print(fitness(build_order_stats))
		print()

	print()
	print("Generating next generation...")
	print()

	num_elite_survivors = round(evolutionary_constants.ELITIST_FRACTION * num_parents)
	num_fit_survivors = round(evolutionary_constants.SURVIVAL_FRACTION * num_parents)
	num_to_generate = num_parents - num_elite_survivors - num_fit_survivors

	sorted_list_of_build_order_stats = list(reversed(sorted(list_of_build_order_stats, key = fitness)))

	surviving_build_order_results = []

	print("Sending elite build orders on to the next generation:")
	for elite_survivor_stats in sorted_list_of_build_order_stats[:num_elite_survivors]:
		elite_survivor_build_order = elite_survivor_stats[0]
		surviving_build_order_results.append(elite_survivor_stats)
		print("    " + concise_str(elite_survivor_build_order))
		print("    with fitness " + str(fitness(elite_survivor_stats)))
	print()

	sorted_remaining_build_order_stats = sorted_list_of_build_order_stats[num_elite_survivors:]
	num_remaining = len(sorted_remaining_build_order_stats)

	# p is the probability for each possible survivor to be picked, based on going over the
	# survivors in fitness rank order and picking one with probability SURVIVAL_PROBABILITY
	p = []
	for i in range(num_remaining - 1):
		p_none_previous_chosen = (1 - evolutionary_constants.SURVIVAL_PROBABILITY)**i
		p_this_one_chosen = p_none_previous_chosen * evolutionary_constants.SURVIVAL_PROBABILITY
		p.append(p_this_one_chosen)
	p_last = (1 - evolutionary_constants.SURVIVAL_PROBABILITY)**(num_remaining - 1)
	p.append(p_last)

	chosen_survivor_indices = numpy.random.choice(range(num_remaining), size=num_fit_survivors, replace=False, p=p)

	print("Randomly picking other fit build orders to send on to the next generation:")
	for i in chosen_survivor_indices:
		chosen_survivor_stats = sorted_remaining_build_order_stats[i]
		chosen_survivor_build_order = chosen_survivor_stats[0]
		surviving_build_order_results.append(chosen_survivor_stats)
		print("    " + concise_str(chosen_survivor_build_order))
		print("    with fitness " + str(fitness(chosen_survivor_stats)))


	generated_build_orders = []

	num_survivors = num_elite_survivors + num_fit_survivors
	max_survivor_index = num_survivors - 1

	surviving_build_orders = [b[0] for b in surviving_build_order_results]

	for i in range(num_to_generate):
		parent_build_order_index = random.randint(0, max_survivor_index)
		new_build_order = copy.deepcopy(surviving_build_orders[parent_build_order_index])
		# todo: figure out a way to do crossover that won't cause towers to collide
		#if random.uniform(0, 1) < CROSSOVER_PROBABILITY:
		#	crossed_parent_index = randint_except(0, max_survivor_index, parent_build_order_index)
		#	crossed_parent_build_order = copy.deepcopy(child_build_orders[crossed_parent_index])
		#	crossover_index = random.randint(1, len(new_build_order) - 2)
		#	new_build_order[crossover_index:] = crossed_parent_build_order[crossover_index:]

		mm = map_manager.MapManager("occupancy_grid.png")
		for i in range(len(new_build_order)):
			step = new_build_order[i]
			if random.uniform(0, 1) < evolutionary_constants.POSITION_MUTATION_PROBABILITY:
				x, y = step.coords
				dx = random.randint(-evolutionary_constants.POSITION_MUTATION_STEP_SIZE, \
					evolutionary_constants.POSITION_MUTATION_STEP_SIZE)
				dy = random.randint(-evolutionary_constants.POSITION_MUTATION_STEP_SIZE,
					evolutionary_constants.POSITION_MUTATION_STEP_SIZE)
				new_x = x + dx
				new_y = y + dy
				new_x = min(max(0, new_x), mm.shape[1] - 1)
				new_y = min(max(game_constants.url_bar_height, new_y), mm.shape[0] - 1)
				while mm.is_occupied((new_x, new_y)):
					dx = random.randint(-evolutionary_constants.POSITION_MUTATION_STEP_SIZE,
						evolutionary_constants.POSITION_MUTATION_STEP_SIZE)
					dy = random.randint(-evolutionary_constants.POSITION_MUTATION_STEP_SIZE,
						evolutionary_constants.POSITION_MUTATION_STEP_SIZE)
					new_x = x + dx
					new_y = y + dy
					new_x = min(max(0, new_x), mm.shape[1] - 1)
					new_y = min(max(game_constants.url_bar_height, new_y), mm.shape[0] - 1)
				step.coords = (new_x, new_y)
			mm.add_object(step.coords, game_constants.tower_interference_radius)
			if random.uniform(0, 1) < evolutionary_constants.TOWER_MUTATION_PROBABILITY:
				# mutate the tower
				new_tower_type = randint_except(0, towers.TowerTypes.SUPER, step.tower_type)
				step.tower_type = new_tower_type
		generated_build_orders.append(new_build_order)

	print("Generated new child build orders:")
	for build_order in generated_build_orders:
		print("    " + concise_str(build_order))

	with open(child_generation_filename, 'wb') as f:
		pickle.dump((surviving_build_order_results, generated_build_orders), f, pickle.HIGHEST_PROTOCOL)

