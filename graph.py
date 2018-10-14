import pickle
import matplotlib.pyplot as plt

f = open("data.pkl", "rb")
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