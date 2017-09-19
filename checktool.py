import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

targets = []
challengers = []
aa = ""

while(aa != "go"):
	aa = raw_input("Provide list of people to scan for wins against: ")
	if (aa == "go"): 
		break
	else:
		targets.append("%"+aa+"%")

aa = ""

while(aa != "go"):
	aa = raw_input("Provide list of people to search for: ")
	if (aa == "go"):
		break
	else:
		challengers.append("%"+aa+"%")

for target in targets:
	print("People who might have beaten {}".format(target.translate(None, '%')))
	for challenger in challengers:
		c.execute('SELECT * FROM matches WHERE winner LIKE (?) AND loser LIKE (?)', (challenger, target))
		count = 0
		for row in c:
			count += 1
			if (count == 1):
				print("{}, assuming {} is {} and {} is {}".format(challenger.translate(None, '%'), row[0], challenger.translate(None, '%'), row[3], target.translate(None, '%')))
	print("")
