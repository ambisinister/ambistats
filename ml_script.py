import requests, bs4
import sqlite3
from sklearn import tree
import numpy as np

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

def guess(clf):

	c.execute('SELECT DISTINCT matches.winner FROM matches JOIN players s1 JOIN players s2 ON matches.winner=s1.tag AND matches.loser=s2.tag WHERE s2.tier>-1 AND s1.tier=-1')
	unknowns = []
	for row in c: unknowns.append(row[0])

	#Probably do this 13 times starting from fill 0s and refilling backwards
	#That way you don't miss good wins as you go further down
	for tier in range(0,14):
		for choice in unknowns:

			checker = 99
			c.execute('SELECT tier FROM players WHERE tag=(?)', (choice, ))
			for row in c: checker=row[0]

			if(checker != -1):
				print("skipping {} because he's already tier {}".format(choice, checker))
				continue

			# Establish format for features
			myplayer_features = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

			# Get each value for features
			for x in range(0,14):
				c.execute('SELECT * FROM matches JOIN players s1 ON s1.tag=matches.loser WHERE matches.winner=(?) AND s1.tier=(?)', (choice, x))
				for row in c: myplayer_features[2*x] += 1
				c.execute('SELECT * FROM matches JOIN players s1 ON s1.tag=matches.winner WHERE matches.loser=(?) AND s1.tier=(?)', (choice, x))
				for row in c: myplayer_features[(2*x)+1] += 1

			vector = np.array(myplayer_features).reshape(1, -1)
			prediction = clf.predict(vector)
			if prediction <= tier:
				print("Guessing {} is tier {}".format(choice, prediction))
				c.execute('UPDATE players SET tier=(?) WHERE tag=(?)', (prediction[0], choice))

	conn.commit()
	conn.close()

def generateTrainingSet():
	# Kind of convoluted but I'm gonna roughly do the following
	# tier: wins on 0s, losses on 0s, wins on 1s, losses on 1s, etc
	# So I'll have 26 features for every label
	# Since I'm only using this as a tagger I think it should be fine to not have char data

	# Gets currently skill-tiered players
	playerpool = []
	c.execute('SELECT DISTINCT tag FROM players WHERE tier IS NOT -1')
	for row in c: playerpool.append(row[0])

	# List of features, list of labels
	features = []
	labels = []

	# Goes through and fills out features and labels
	for player in playerpool:
		# Get assigned label for player
		c.execute('SELECT tier FROM players WHERE tag=(?)', (player, ))
		for row in c: myplayer_label = row[0]

		# Establish format for features
		myplayer_features = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		# Get each value for features
		for x in range(0,14):
			c.execute('SELECT * FROM matches JOIN players s1 ON s1.tag=matches.loser WHERE matches.winner=(?) AND s1.tier=(?)', (player, x))
			for row in c: myplayer_features[2*x] += 1
			c.execute('SELECT * FROM matches JOIN players s1 ON s1.tag=matches.winner WHERE matches.loser=(?) AND s1.tier=(?)', (player, x))
			for row in c: myplayer_features[(2*x)+1] += 1

		features.append(myplayer_features)
		labels.append(myplayer_label)

	features = np.array(features)
	labels = np.array(labels)
	clf=tree.DecisionTreeClassifier()
	clf=clf.fit(features, labels)

	guess(clf)

generateTrainingSet()




#c.execute('SELECT DISTINCT matches.winner FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p2.tier IS NOT -1 AND p1.tier IS -1')

#people = []
#results = []
#for row in c:
#	people.append(row[0])

#for row in people:
#	c.execute('SELECT matches.winner, p1.tier, matches.loser, p2.tier FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND matches.winner=(?) AND p2.tag=matches.loser WHERE p2.tier IS NOT -1 AND p1.tier IS -1 ORDER BY p2.tier', (row, ))
#	for x in c: print x