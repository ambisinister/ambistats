import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

winrates = []

w_count = 0
l_count = 0

for x in range(0,14):
	sub_wr = []
	for y in range(0,14):
		c.execute('SELECT matches.winner, p1.tier, matches.loser, p2.tier FROM matches JOIN players p1 JOIN players p2 ON p1.tag = matches.winner AND p2.tag = matches.loser WHERE p1.tier=(?) AND p2.tier=(?) ORDER BY p1.tier', (x, y))
		for row in c: w_count += 1
		c.execute('SELECT matches.winner, p1.tier, matches.loser, p2.tier FROM matches JOIN players p1 JOIN players p2 ON p1.tag = matches.winner AND p2.tag = matches.loser WHERE p1.tier=(?) AND p2.tier=(?) ORDER BY p1.tier', (y, x))
		for row in c: l_count += 1
		if l_count == 0:
			if w_count == 0:
				if (x > y):
					winrate = 0
				else:
					winrate = 1
			else:
				winrate = 1
		else:
			winrate = float(w_count) / (float(l_count)+float(w_count))
		sub_wr.append(winrate)
		w_count = 0
		l_count = 0

	winrates.append(sub_wr)

for row in winrates:
	print(row)

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.mlab import bivariate_normal

Z = winrates

# Dogshit view
#plt.plot(winrates)
#plt.title('Winrate vs MS Rough Tiering')
#plt.ylabel("winrate")
#plt.xlabel("Opponent Tier")
#plt.show()

# The Good View
plt.pcolor(Z, cmap='RdYlGn')
plt.title('Winrate vs MS Rough Tiering')
cbar = plt.colorbar()
plt.ylabel("Tier")
plt.xlabel("Opponent Tier")
cbar.set_label('winrate', rotation=270)
plt.show()