import requests, bs4
import sqlite3
from sklearn import tree
import numpy as np

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

allp = []

c.execute('SELECT * FROM players WHERE tier=-1')
for row in c: allp.append(row[0])

for player in allp:
	counter = 0
	c.execute('SELECT * FROM matches WHERE winner=(?)', (player, ))
	for row in c: counter += 1
	if counter > 15:
		print("{}: {} games and tier -1". format(player, counter))
	counter = 0
