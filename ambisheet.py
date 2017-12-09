import requests, bs4
import sqlite3
import csv

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()
players = []
variates = []
group = raw_input("Input player: ")

while(group != "go"):
	variates.append(group)
	group = raw_input("Input player: ")

for row in variates:
	probtag = "%" + row + "%"
	c.execute('SELECT DISTINCT tag FROM players WHERE tag LIKE (?)', (probtag, ))
	tmp = []
	for row in c: tmp.append(row)
	if len(tmp) == 1:
		players.append(tmp[0])
	else:
		number = 1
		print("Select correct tag for {}: ".format(probtag))
		for p in tmp:
			print("{}: {}".format(number, tmp[number-1]))
			number += 1
		selection = int(raw_input("choice: "))
		if selection == 0: players.append("Poop")
		else: players.append(tmp[selection-1])

print("")
print("********")
print(players)
print("********")
print("")

records = []
for player in players:
	myrec = []
	myrec.append(player[0])
	for otherplayer in players:
		if player == otherplayer:
			myrec.append("x")
		else:
			wins = 0
			losses = 0
			c.execute('SELECT * FROM matches WHERE winner=(?) AND loser=(?)', (player[0], otherplayer[0]))
			for row in c: wins += 1
			c.execute('SELECT * FROM matches WHERE winner=(?) AND loser=(?)', (otherplayer[0], player[0]))
			for row in c: losses += 1
			rec = str(wins) + " & " + str(losses)
			myrec.append(rec)

	records.append(myrec)

with open('h2h.csv', 'wb') as csvfile:
	bookkeeper = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
	bookkeeper.writerow(players)
	for record in records:
		bookkeeper.writerow(record)