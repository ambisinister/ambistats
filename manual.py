# manualassign characters (low hanging fruit)

import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

players = []

c.execute('SELECT * FROM players WHERE character = "?"')
for row in c: players.append(row)

counts = []

for player in players:
	c.execute('SELECT * FROM matches WHERE winner = (?) OR loser = (?)', (player[0], player[0]))
	num = 0
	for row in c: num += 1
	counts.append([player, num])

counts.sort(key=lambda tup: tup[1])
counts = counts[::-1]

num = 0
for row in counts: 
	if(row[1] > 5):
		num += 1
		print row
		p_chr = raw_input("Input Character: ")
		c.execute('UPDATE players SET character=(?) WHERE tag=(?)', (p_chr, row[0][0]))
	if num >= 40:
		break

conn.commit()
conn.close()