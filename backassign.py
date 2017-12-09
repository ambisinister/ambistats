# backassign characters (low hanging fruit)
# Scans through matches, checks if player has a main in the database
# If they have a single main, set all matches with that player to that main

import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

players = []

#c.execute('DROP TABLE IF EXISTS players')
c.execute('SELECT * FROM players WHERE character != "?"')
for row in c: players.append(row)

for row in players:
	if '/' not in row[1]:
		c.execute('UPDATE matches SET wchar = (?) WHERE wchar = "?" AND winner = (?)', (row[1], row[0]))
		c.execute('UPDATE matches SET lchar = (?) WHERE lchar = "?" AND loser = (?)', (row[1], row[0]))

# zz = raw_input("Check, cancel out if bad")
# c.execute('SELECT * FROM matches WHERE wchar != "?" OR lchar != "?"')
# for row in c: print row
# zz = raw_input("Looks good?")

conn.commit()
conn.close()