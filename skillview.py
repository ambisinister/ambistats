import requests
import sqlite3
import csv
import matplotlib.pyplot as plt
import numpy as np
import numpy.polynomial.polynomial as poly

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

#popuate wins/losses for each character, winloss = 0 for wins, = 1 for losses
def fill(games, winloss, anime_tiddies):
	for row in games:
		#this is disgustingly bad but I'm sleep deprived so as long as it shits out graphs correctly
		anime_tiddies[ ((row[9]-row[12]) +13)] += 1
	return anime_tiddies

char_games = []

important_characters = ["Fox", "Falco", "Marth", "Sheik", "Puff", "Samus", "ICs", "Falcon", "Peach"]
#important_characters = []
#c.execute('SELECT DISTINCT character FROM players WHERE character NOT LIKE "%/%" AND character NOT LIKE "?"')
#for row in c:
#	important_characters.append(row[0])

total_players = 0
total_matches = 0
players_bychar = []
players_bymatch = []

'''
#bellum omnum contra omnius
char_games = []
c.execute('SELECT * FROM matches m1 JOIN players p1 JOIN players p2 ON p1.tag=m1.winner AND p2.tag=m1.loser WHERE p1.tier > -1 AND p2.tier > -1' )
for row in c:
	char_games.append(row)

char_tier_wins = [0] * 27
char_tier_wins = fill(char_games, 0, char_tier_wins)
char_games = []

c.execute('SELECT * FROM matches m1 JOIN players p1 JOIN players p2 ON p1.tag=m1.loser AND p2.tag=m1.winner WHERE p1.tier > -1 AND p2.tier > -1' )
for row in c:
	char_games.append(row)

char_tier_loss = [0] * 27
char_tier_loss = fill(char_games, 1, char_tier_loss)

print(char_tier_wins)
print(char_tier_loss)

if(char_tier_wins[13]+char_tier_loss[13] == 0):
	print("NO DATA")
else:
	print(float(char_tier_wins[13]) / (char_tier_wins[13]+char_tier_loss[13]))


final_winrate = []
fw_index = []
	
for m in range (0,27):
	if(char_tier_wins[m]+char_tier_loss[m] == 0):
		continue
	else:
		final_winrate.append(float(char_tier_wins[m]) / (char_tier_wins[m]+char_tier_loss[m]))
		fw_index.append(int(m-13))
print fw_index
print final_winrate


fig, ax = plt.subplots()
z = np.polyfit(fw_index, final_winrate, 3)
f = np.poly1d(z)
x_new = np.linspace(fw_index[0], fw_index[-1], 50)
y_new = f(x_new)
plt.plot(fw_index, final_winrate,'o', x_new, y_new)
plt.ylabel('Winrate')
plt.xlabel('Skill Difference')
plt.title('%s vs %s' % ("All", "All"))
plt.xlim([-13,13])
plt.ylim([0,1])
plt.savefig("./characters/%s_vs_%s" % ("All", "All"))
'''


#generate character skill-adherence charts
'''
with open('bluh.csv', 'wb') as csvfile:
	bookkeeper = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
	bookkeeper.writerow(["character", "derivative", "upsetting", "upsetted", "error"])

	for xchar in important_characters:
		char_games = []
		print("{} vs all".format(xchar))
		c.execute(
			'SELECT * FROM matches m1 JOIN players p1 JOIN players p2 ON p1.tag=m1.winner AND p2.tag=m1.loser WHERE p1.character=(?) AND p1.tier > -1 AND p2.tier > -1', (
			xchar, ))
		for row in c:
			char_games.append(row)

		P1TIER_INDEX = 9
		P2TIER_INDEX = 12

		char_tier_wins = [0] * 27

		char_tier_wins = fill(char_games, 0, char_tier_wins)
		char_games = []

		c.execute(
			'SELECT * FROM matches m1 JOIN players p1 JOIN players p2 ON p1.tag=m1.loser AND p2.tag=m1.winner WHERE p1.character=(?) AND p1.tier > -1 AND p2.tier > -1', (
			xchar, ))
		for row in c:
			char_games.append(row)

		char_tier_loss = [0] * 27
		char_tier_loss = fill(char_games, 1, char_tier_loss)

		
		print(char_tier_wins)
		print(char_tier_loss)

		
		if(char_tier_wins[13]+char_tier_loss[13] == 0):
			print("NO DATA")
		else:
			print(float(char_tier_wins[13]) / (char_tier_wins[13]+char_tier_loss[13]))
		

		final_winrate = []
		fw_index = []
		
		for m in range (0,27):
			if(char_tier_wins[m]+char_tier_loss[m] == 0):
				continue
			else:
				final_winrate.append(float(char_tier_wins[m]) / (char_tier_wins[m]+char_tier_loss[m]))
				fw_index.append(int(m-13))
		#print fw_index
		#print final_winrate


		fig, ax = plt.subplots()
		z = np.polyfit(fw_index, final_winrate, 3)
		f = np.poly1d(z)
		f_durr = np.polyder(f)
		x_new = np.linspace(fw_index[0], fw_index[-1], 50)
		y_new = f(x_new)
		#plt.plot(fw_index, final_winrate,'o', x_new, y_new)
		#plt.ylabel('Winrate')
		#plt.xlabel('Skill Difference')
		#plt.title('%s vs %s' % (xchar, "All"))
		#plt.xlim([-13,13])
		#plt.ylim([0,1])
		#plt.savefig("./characters/%s_vs_%s" % (xchar, "All"))

		print(z)
		#print(f_durr)
		error_calc = np.sum((np.polyval(f, fw_index) - final_winrate) ** 2)
		print("(integral from -13 to 0 of {}x^3 + {}x^2 + {}x + {})/13".format(z[0], z[1], z[2], z[3]))
		print("(integral from 0 to 13 of {}x^3 + {}x^2 + {}x + {})/13".format(z[0], z[1], z[2], z[3]))
		print("")
		print("***")
		print("")
		bookkeeper = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
		bookkeeper.writerow([xchar, np.polyval(f_durr, 0), 0, 0, error_calc])

'''





#generate matchup charts
with open('bluh.csv', 'wb') as csvfile:
	bookkeeper = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
	bookkeeper.writerow(["matchup", "derivative", "upsetting", "upsetted", "error"])
	for xchar in important_characters:
		for ychar in important_characters:
			char_games = []
			matchup = "{} vs {}".format(xchar, ychar)
			print matchup
			c.execute(
				'SELECT * FROM matches m1 JOIN players p1 JOIN players p2 ON p1.tag=m1.winner AND p2.tag=m1.loser WHERE p1.character=(?) AND p2.character=(?) AND p1.tier > -1 AND p2.tier > -1', (
					xchar, ychar))
			for row in c:
				char_games.append(row)

			P1TIER_INDEX = 9
			P2TIER_INDEX = 12

			char_tier_wins = [0] * 27

			char_tier_wins = fill(char_games, 0, char_tier_wins)
			char_games = []

			c.execute(
				'SELECT * FROM matches m1 JOIN players p1 JOIN players p2 ON p1.tag=m1.loser AND p2.tag=m1.winner WHERE p1.character=(?) AND p2.character=(?) AND p1.tier > -1 AND p2.tier > -1', (
					xchar, ychar))
			for row in c:
				char_games.append(row)

			char_tier_loss = [0] * 27
			char_tier_loss = fill(char_games, 1, char_tier_loss)

			print(char_tier_wins)
			print(char_tier_loss)

			if(char_tier_wins[13]+char_tier_loss[13] == 0):
				print("NO DATA")
			else:
				print(float(char_tier_wins[13]) / (char_tier_wins[13]+char_tier_loss[13]))


			final_winrate = []
			fw_index = []
			
			for m in range (0,27):
				if(char_tier_wins[m]+char_tier_loss[m] == 0):
					continue
				else:
					final_winrate.append(float(char_tier_wins[m]) / (char_tier_wins[m]+char_tier_loss[m]))
					fw_index.append(int(m-13))
			print fw_index
			print final_winrate


			fig, ax = plt.subplots()
			z = np.polyfit(fw_index, final_winrate, 3)
			f = np.poly1d(z)
			f_durr = np.polyder(f)
			x_new = np.linspace(fw_index[0], fw_index[-1], 50)
			y_new = f(x_new)
			#plt.plot(fw_index, final_winrate,'o', x_new, y_new)
			#plt.ylabel('Winrate')
			#plt.xlabel('Skill Difference')
			#plt.title('%s vs %s' % (xchar, ychar))
			#plt.xlim([-13,13])
			#plt.ylim([0,1])
			#plt.savefig("./matchups/%s_vs_%s" % (xchar, ychar))

			print(z)
			#print(f_durr)
			error_calc = np.sum((np.polyval(f, fw_index) - final_winrate) ** 2)
			print("(integral from -13 to 0 of {}x^3 + {}x^2 + {}x + {})/13".format(z[0], z[1], z[2], z[3]))
			print("(integral from 0 to 13 of {}x^3 + {}x^2 + {}x + {})/13".format(z[0], z[1], z[2], z[3]))
			print("")
			print("***")
			print("")
			bookkeeper = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
			bookkeeper.writerow([matchup, np.polyval(f_durr, 0), 0, 0, error_calc])




