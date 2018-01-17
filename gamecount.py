import requests
import sqlite3
import csv
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

'''
winscore_20_all = 0
winscore_21_all = 0
winscore_30_all = 0
winscore_31_all = 0
winscore_32_all = 0

c.execute('SELECT * FROM matches WHERE winscore = 2 AND losescore = 0')
for row in c: winscore_20_all += 1
c.execute('SELECT * FROM matches WHERE winscore = 2 AND losescore = 1')
for row in c: winscore_21_all += 1
c.execute('SELECT * FROM matches WHERE winscore = 3 AND losescore = 0')
for row in c: winscore_30_all += 1
c.execute('SELECT * FROM matches WHERE winscore = 3 AND losescore = 1')
for row in c: winscore_31_all += 1
c.execute('SELECT * FROM matches WHERE winscore = 3 AND losescore = 2')
for row in c: winscore_32_all += 1

labels = '2-0', '2-1', '3-0', '3-1', '3-2'
sizes = [winscore_20_all, winscore_21_all, winscore_30_all, winscore_31_all, winscore_32_all]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')
plt.title('Wins by Gamecount')
plt.show()
'''

'''
winscore_20_all = 0
winscore_21_all = 0
winscore_30_all = 0
winscore_31_all = 0
winscore_32_all = 0

c.execute('SELECT * FROM matches JOIN players p1 JOIN players P2 ON p1.tag = matches.winner AND p2.tag = matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 2 AND losescore = 0')
for row in c: winscore_20_all += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players P2 ON p1.tag = matches.winner AND p2.tag = matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 2 AND losescore = 1')
for row in c: winscore_21_all += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players P2 ON p1.tag = matches.winner AND p2.tag = matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 3 AND losescore = 0')
for row in c: winscore_30_all += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players P2 ON p1.tag = matches.winner AND p2.tag = matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 3 AND losescore = 1')
for row in c: winscore_31_all += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players P2 ON p1.tag = matches.winner AND p2.tag = matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 3 AND losescore = 2')
for row in c: winscore_32_all += 1

#print(float(winscore_30_all) / (winscore_30_all+winscore_31_all+winscore_32_all))

labels = '2-0', '2-1', '3-0', '3-1', '3-2'
sizes = [winscore_20_all, winscore_21_all, winscore_30_all, winscore_31_all, winscore_32_all]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')
plt.title('Wins by Gamecount')
plt.show()

'''

'''

winscore_30_foxwins = 0
winscore_31_foxwins = 0
winscore_32_foxwins = 0
winscore_30_sheikwins = 0
winscore_31_sheikwins = 0
winscore_32_sheikwins = 0

c.execute('SELECT * FROM matches WHERE winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik"))
for row in c: winscore_30_foxwins += 1
c.execute('SELECT * FROM matches WHERE winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik"))
for row in c: winscore_31_foxwins += 1
c.execute('SELECT * FROM matches WHERE winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik"))
for row in c: winscore_32_foxwins += 1

c.execute('SELECT * FROM matches WHERE winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?)', ("%sheik", "%fox%"))
for row in c: winscore_30_sheikwins += 1
c.execute('SELECT * FROM matches WHERE winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?)', ("%sheik", "%fox%"))
for row in c: winscore_31_sheikwins += 1
c.execute('SELECT * FROM matches WHERE winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?)', ("%sheik", "%fox%"))
for row in c: winscore_32_sheikwins += 1

labels = '3-0', '3-1', '3-2'
N = 3
sizesf = [float(winscore_30_foxwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_foxwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_foxwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
sizess = [float(winscore_30_sheikwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_sheikwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_sheikwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars
fig1, ax1 = plt.subplots()
rects1 = ax1.bar(ind, sizesf, width, color='r', edgecolor=('k', 'k', 'k'))
rects2 = ax1.bar(ind+width, sizess, width, color='b', edgecolor=('k', 'k', 'k'))
ax1.set_ylabel('Win Percentage')
ax1.set_title('Win Percentage in Fox vs Sheik By Gamecount')
ax1.set_xticks(ind + width / 2)
ax1.set_xticklabels(labels)
ax1.legend((rects1[0], rects2[0]), ('Fox', 'Sheik'))
plt.show()

'''

'''

winscore_30_foxwins = 0
winscore_31_foxwins = 0
winscore_32_foxwins = 0
winscore_30_sheikwins = 0
winscore_31_sheikwins = 0
winscore_32_sheikwins = 0

c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik"))
for row in c: winscore_30_foxwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik"))
for row in c: winscore_31_foxwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik"))
for row in c: winscore_32_foxwins += 1

c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?)', ("%sheik", "%fox%"))
for row in c: winscore_30_sheikwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?)', ("%sheik", "%fox%"))
for row in c: winscore_31_sheikwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?)', ("%sheik", "%fox%"))
for row in c: winscore_32_sheikwins += 1

labels = '3-0', '3-1', '3-2'
N = 3
sizesf = [float(winscore_30_foxwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_foxwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_foxwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
sizess = [float(winscore_30_sheikwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_sheikwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_sheikwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars
fig1, ax1 = plt.subplots()
rects1 = ax1.bar(ind, sizesf, width, color='r', edgecolor=('k', 'k', 'k'))
rects2 = ax1.bar(ind+width, sizess, width, color='b', edgecolor=('k', 'k', 'k'))
ax1.set_ylabel('Win Percentage')
ax1.set_title('Win Percentage in Fox vs Sheik By Gamecount (Tiered Players)')
ax1.set_xticks(ind + width / 2)
ax1.set_xticklabels(labels)
ax1.legend((rects1[0], rects2[0]), ('Fox', 'Sheik'))
plt.show()

'''
'''
winscore_30_foxwins = 0
winscore_31_foxwins = 0
winscore_32_foxwins = 0
winscore_30_sheikwins = 0
winscore_31_sheikwins = 0
winscore_32_sheikwins = 0

c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND p1.tier - p2.tier <= 1 AND p1.tier - p2.tier >= -1 AND winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik"))
for row in c: winscore_30_foxwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND p1.tier - p2.tier <= 1 AND p1.tier - p2.tier >= -1 AND winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik"))
for row in c: winscore_31_foxwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND p1.tier - p2.tier <= 1 AND p1.tier - p2.tier >= -1 AND winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik"))
for row in c: winscore_32_foxwins += 1

c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND p1.tier - p2.tier <= 1 AND p1.tier - p2.tier >= -1 AND winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?)', ("%sheik", "%fox%"))
for row in c: winscore_30_sheikwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND p1.tier - p2.tier <= 1 AND p1.tier - p2.tier >= -1 AND winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?)', ("%sheik", "%fox%"))
for row in c: winscore_31_sheikwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier != -1 AND p2.tier != -1 AND p1.tier - p2.tier <= 1 AND p1.tier - p2.tier >= -1 AND winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?)', ("%sheik", "%fox%"))
for row in c: winscore_32_sheikwins += 1

print(float(winscore_30_foxwins+winscore_31_foxwins+winscore_32_foxwins) / (winscore_30_foxwins+winscore_31_foxwins+winscore_32_foxwins+winscore_30_sheikwins+winscore_31_sheikwins+winscore_32_sheikwins))

labels = '3-0', '3-1', '3-2'
N = 3
sizesf = [float(winscore_30_foxwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_foxwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_foxwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
sizess = [float(winscore_30_sheikwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_sheikwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_sheikwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars
fig1, ax1 = plt.subplots()
rects1 = ax1.bar(ind, sizesf, width, color='r', edgecolor=('k', 'k', 'k'))
rects2 = ax1.bar(ind+width, sizess, width, color='b', edgecolor=('k', 'k', 'k'))
ax1.set_ylabel('Win Percentage')
ax1.set_title('Win Percentage in Fox vs Sheik By Gamecount (Closely Tiered Players)')
ax1.set_xticks(ind + width / 2)
ax1.set_xticklabels(labels)
ax1.legend((rects1[0], rects2[0]), ('Fox', 'Sheik'))
plt.show()
'''

'''
winscore_30_foxwins = 0
winscore_31_foxwins = 0
winscore_32_foxwins = 0
winscore_30_sheikwins = 0
winscore_31_sheikwins = 0
winscore_32_sheikwins = 0

c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik%"))
for row in c: winscore_30_foxwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik%"))
for row in c: winscore_31_foxwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?)', ("%fox%", "%sheik%"))
for row in c: 
	print row
	winscore_32_foxwins += 1

print("***")

c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?)', ("%sheik%", "%fox%"))
for row in c: winscore_30_sheikwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?)', ("%sheik%", "%fox%"))
for row in c: winscore_31_sheikwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?)', ("%sheik%", "%fox%"))
for row in c: 
	print row
	winscore_32_sheikwins += 1

print(float(winscore_30_foxwins+winscore_31_foxwins+winscore_32_foxwins) / (winscore_30_foxwins+winscore_31_foxwins+winscore_32_foxwins+winscore_30_sheikwins+winscore_31_sheikwins+winscore_32_sheikwins))

labels = '3-0', '3-1', '3-2'
N = 3
sizesf = [float(winscore_30_foxwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_foxwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_foxwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
sizess = [float(winscore_30_sheikwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_sheikwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_sheikwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars
fig1, ax1 = plt.subplots()
rects1 = ax1.bar(ind, sizesf, width, color='r', edgecolor=('k', 'k', 'k'))
rects2 = ax1.bar(ind+width, sizess, width, color='b', edgecolor=('k', 'k', 'k'))
ax1.set_ylabel('Win Percentage')
ax1.set_title('Win Percentage in Fox vs Sheik By Gamecount (Highest Tier Players)')
ax1.set_xticks(ind + width / 2)
ax1.set_xticklabels(labels)
ax1.legend((rects1[0], rects2[0]), ('Fox', 'Sheik'))
plt.show()

'''

winscore_30_foxwins = 0
winscore_31_foxwins = 0
winscore_32_foxwins = 0
winscore_30_sheikwins = 0
winscore_31_sheikwins = 0
winscore_32_sheikwins = 0

c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?) AND loser NOT LIKE (?) AND loser NOT LIKE (?) AND loser NOT LIKE (?)', ("%fox%", "%sheik%", "%mew2king%", "%shroomed%", "%plup%"))
for row in c: winscore_30_foxwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?) AND loser NOT LIKE (?) AND loser NOT LIKE (?) AND loser NOT LIKE (?)', ("%fox%", "%sheik%", "%mew2king%", "%shroomed%", "%plup%"))
for row in c: winscore_31_foxwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?) AND loser NOT LIKE (?) AND loser NOT LIKE (?) AND loser NOT LIKE (?)', ("%fox%", "%sheik%", "%mew2king%", "%shroomed%", "%plup%"))
for row in c: 
	print row
	winscore_32_foxwins += 1

print("****")

c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 0 AND wchar like (?) AND lchar like (?) AND winner NOT LIKE (?) AND winner NOT LIKE (?) AND winner NOT LIKE (?)', ("%sheik%", "%fox%", "%mew2king%", "%shroomed%", "%plup%"))
for row in c: winscore_30_sheikwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 1 AND wchar like (?) AND lchar like (?) AND winner NOT LIKE (?) AND winner NOT LIKE (?) AND winner NOT LIKE (?)', ("%sheik%", "%fox%", "%mew2king%", "%shroomed%", "%plup%"))
for row in c: winscore_31_sheikwins += 1
c.execute('SELECT * FROM matches JOIN players p1 JOIN players p2 ON p1.tag=matches.winner AND p2.tag=matches.loser WHERE p1.tier = 0 AND p2.tier = 0 AND winscore = 3 AND losescore = 2 AND wchar like (?) AND lchar like (?) AND winner NOT LIKE (?) AND winner NOT LIKE (?) AND winner NOT LIKE (?)', ("%sheik%", "%fox%", "%mew2king%", "%shroomed%", "%plup%"))
for row in c: 
	print row
	winscore_32_sheikwins += 1

print(float(winscore_30_foxwins+winscore_31_foxwins+winscore_32_foxwins) / (winscore_30_foxwins+winscore_31_foxwins+winscore_32_foxwins+winscore_30_sheikwins+winscore_31_sheikwins+winscore_32_sheikwins))


labels = '3-0', '3-1', '3-2'
N = 3
sizesf = [float(winscore_30_foxwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_foxwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_foxwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
sizess = [float(winscore_30_sheikwins) / (winscore_30_foxwins+winscore_30_sheikwins), float(winscore_31_sheikwins) / (winscore_31_foxwins+winscore_31_sheikwins), float(winscore_32_sheikwins) / (winscore_32_foxwins+winscore_32_sheikwins)]
ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars
fig1, ax1 = plt.subplots()
rects1 = ax1.bar(ind, sizesf, width, color='r', edgecolor=('k', 'k', 'k'))
rects2 = ax1.bar(ind+width, sizess, width, color='b', edgecolor=('k', 'k', 'k'))
ax1.set_ylabel('Win Percentage')
ax1.set_title('Win Percentage in Fox vs Sheik By Gamecount (Highest Tier Players, no M2K/Plup/Shroomed)')
ax1.set_xticks(ind + width / 2)
ax1.set_xticklabels(labels)
ax1.legend((rects1[0], rects2[0]), ('Fox', 'Sheik'))
plt.show()
