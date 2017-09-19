import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

allc = 0
cc = 0
hc = 0

c.execute('SELECT * FROM matches')
for row in c: allc += 1

c.execute('SELECT * FROM matches WHERE wchar != "?" AND lchar != "?"')
for row in c: cc += 1

c.execute('SELECT * FROM matches WHERE wchar != "?" OR lchar != "?"')
for row in c: hc += 1

print("Currently, you have {} sets with {} complete cases and {} half-complete cases".format(allc, cc, hc))