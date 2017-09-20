import sqlite3
conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

# c.execute('DROP TABLE IF EXISTS tourneys')
# c.execute('CREATE TABLE tourneys (event TEXT, date INT)')

events = []

c.execute('SELECT DISTINCT event FROM matches')
for row in c: events.append(row[0])

num = 0

for event in events:

	# check if event in tourneys
	testvar = False
	c.execute('SELECT DISTINCT event FROM tourneys WHERE event=(?)', (event, ))
	for row in c: testvar = True
	if(testvar):
		continue

	# if event is not in tourneys, input a date for the tourney
	dt = raw_input("What date was {}? ".format(event))
	dt = "2017" + dt
	num += 1
	c.execute('INSERT INTO tourneys VALUES (?, ?)', (event, dt))

	# stop if num >= 20 because I don't want to do all of these at once lol
	if(num>=20):
		break

conn.commit()
conn.close()