import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()
players = []
variates = []
group = raw_input("Input player: ")

while(group != "go"):
	players.append(group)
	group = raw_input("Input player: ")
	

for row in players:
	temp = row.split(',')
	print(temp[0])
	prob_tag = "%" + temp[0] + "%"
	prob_tier = int(temp[1])
	temp2 = []
	print(prob_tier)
	print("***")
	c.execute('SELECT * FROM players WHERE tag LIKE (?)', (prob_tag, ))
	for rowa in c:
		temp2.append(rowa)
	if len(temp2) == 1:
		c.execute('UPDATE players SET tier=(?) WHERE tag LIKE (?)', (prob_tier, prob_tag))
		print('ASSIGNING TIER {} TO {}'.format(prob_tier, temp2[0]))
		print("***")
	else:
		variates.append(row)

print("UNASSIGNED:")

for row in variates:
	tmp = row.split(',')
	ideas = []
	tr = int(tmp[1])
	print('matches for: {}'.format(tmp[0]))
	c.execute('SELECT * FROM players WHERE tag LIKE (?)', ("%" + tmp[0] + "%", ))

	for x in c: ideas.append(x)
	counter = 1

	for x in ideas:
		print("{}: {}".format(counter, x[0]))
		counter += 1

	select = int(raw_input("Choice?: "))
	if (select > len(ideas)): 
		print("go back here")
		continue
	if select == 0:
		continue
	else:
		c.execute('UPDATE players SET tier=(?) WHERE tag=(?)', (tr, ideas[select-1][0]))
		print('ASSIGNING TIER {} TO {}'.format(tr, ideas[select-1][0]))
		print("***")

conn.commit()
conn.close()