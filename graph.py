import sys
import pickle
import matplotlib.pyplot as plt


if len(sys.argv) > 2:
	print()
	print("Ignoring extra parameters")
	print()

	build_orders = generate_build_orders(NUM_TO_GENERATE)

# default filename
filename = "data.pkl"

if len(sys.argv) == 2:
	user_specified_filename = sys.argv[1]
	if user_specified_filename.endswith(".pkl"):
		filename = user_specified_filename
	else:
		filename = user_specified_filename + ".pkl"

f = open(filename, "rb")
data = pickle.load(f)
f.close()

build_order, build_order_index, stats_list = data

t = [d[0] for d in stats_list]
stats = [d[1] for d in stats_list]
lives = [s[2] for s in stats]
money = [s[1] for s in stats]

fix, axes = plt.subplots(2, 1)

axis_lives = plt.subplot(211)
plt.plot(t, lives)
plt.ylabel("Lives")

axis_money = plt.subplot(212, sharex=axis_lives)
plt.plot(t, money)
plt.ylabel("Money")
plt.xlabel("Time (s)")

plt.show()