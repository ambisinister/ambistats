#checks if assigned

import sqlite3
conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

txt = "-1"
while(txt != ""):
	txt = raw_input("Input person to check for character: ")
	c.execute('SELECT * FROM players WHERE tag LIKE (?)', ("%"+txt+"%", ))
	for row in c: print row
	print("")

exit()