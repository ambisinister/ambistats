import requests, bs4
import sqlite3
import csv

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

players = []
group = raw_input("Input player: ")

while(group != "go"):
	players.append(group)
	group = raw_input("Input player: ")
	group = group.encode('ascii', 'ignore').strip()

#print("PLAYERS TIERED BEFORE")
#print("===========================")


#for row in players:
#	zzz = "%" + row + "%"
#	c.execute('SELECT DISTINCT tag FROM players WHERE tag like (?) AND tier != -1', (zzz, ))
#	for z in c: 
#		c.execute('SELECT tier FROM players WHERE tag=(?)', (z[0], ))
#		for v in z:
#			print("{} = {}: {}".format(zzz, z[0], v))


print("===========================")

print("PLAYERS WITH WINS ON ONES")

for row in players:
	zzz = "%" + row + "%"
	c.execute('SELECT DISTINCT m1.winner FROM matches m1 JOIN players s1 ON s1.tag=m1.loser WHERE m1.winner LIKE (?) and s1.tier = 2', (zzz, ))
	for z in c:
		c.execute('SELECT tier FROM players WHERE tag=(?)', (z[0], ))
		for v in z:
			print("{} = {}: {}".format(zzz, z[0], v))


