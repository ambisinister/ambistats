import sqlite3
conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()
person = "."

while(person != ""):
	person = raw_input("Choose person to get matches of: ")
	print("matches for {}".format(person))
	print("wins")
	c.execute('SELECT * FROM matches WHERE (winner LIKE (?) AND lchar = "Marth")', ("%"+person+"%",))
	for row in c: print row

	print("losses")
	c.execute('SELECT * FROM matches WHERE (loser LIKE (?) AND wchar = "Marth")', ("%"+person+"%",))
	for row in c: print row

	print("")