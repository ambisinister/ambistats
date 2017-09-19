import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()
players = []
players_old = []

# c.execute('DROP TABLE IF EXISTS players')
# c.execute('CREATE TABLE players (tag TEXT, character TEXT, elo NUMERIC)')
c.execute('SELECT DISTINCT tag FROM players')
for row in c: players_old.append(row[0])

c.execute('SELECT DISTINCT winner FROM matches')
for row in c: 
	if row not in players_old:
		players.append(row[0])
c.execute('SELECT DISTINCT loser FROM matches')
for row in c: 
	if row in players:
		continue
	if row not in players_old:
		players.append(row[0])

for player in players:
	chars = []
	c.execute('SELECT DISTINCT wchar FROM matches WHERE winner = (?)', (player, ))
	for row in c: chars.append(row[0])
	c.execute('SELECT DISTINCT lchar FROM matches WHERE loser = (?)', (player, ))
	for row in c: 
		if row[0] in chars:
			continue
		else:
			chars.append(row[0])
	p_char = "?"
	for row in chars:
		if (row != '?'):
			if (p_char == "?"):
				p_char = row
			else:
				p_char = p_char + "/" + row
	c.execute('INSERT INTO players VALUES (?, ?, ?)', (player, p_char, -1))

zz = raw_input("press enter to check")
c.execute('SELECT * FROM players')
for row in c: print row
zz = raw_input("press enter to exit")

conn.commit()
conn.close()


