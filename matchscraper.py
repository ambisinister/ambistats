import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

# c.execute('DROP TABLE IF EXISTS matches ')
# c.execute('CREATE TABLE matches (winner TEXT, winscore INT, wchar TEXT, loser TEXT, losescore INT, lchar TEXT, event TEXT)')

res = []

url = raw_input("Input URL: ")

while(url != "go"):
	res.append(requests.get(url))
	url = raw_input("Input URL: ")

for page in range(0, len(res)):
	res[page].raise_for_status()
	soup = bs4.BeautifulSoup(res[page].text)

	if("smash.gg" in soup.strings):
		event = soup.head.meta.get('content').strip() 
		print("Smash.gg bracket - {}".format(event))

		games = soup.find_all('div', class_="match-affix-wrapper")

		for game in games:
			
			## Winner
			w_log = game.find('div', class_="match-player entrant winner")
			if(w_log == None): w_log = game.find('div', class_="match-player entrant winner missing")
			if(w_log == None):
				print("Match has no winner?")
				print(game)
				continue
			w_namegrab = w_log.find('div', class_="flex-item-grower text-ellipsis")
			w_score = w_log.find('div', class_="match-player-stocks")
			if(w_score != None):
				w_score = w_score.text.strip()
			else:
				w_score = "1"
			w_char = w_log.find('div', class_="match-character winner")
			if(w_char != None):
				w_char = w_char.img.get('src').strip()
			else:
				w_char = "?"
			winner = w_namegrab.span.getText().encode('ascii', 'ignore').strip()

			## Loser
			l_log = game.find('div', class_="match-player entrant loser")
			if(l_log == None): l_log = game.find('div', class_="match-player entrant loser missing")
			if(l_log == None): l_log = game.find('div', class_="match-player entrant loser missing dq")
			if(l_log == None): 
				print("Panic! At the Disco")
				continue
			l_namegrab = l_log.find('div', class_="flex-item-grower text-ellipsis")
			l_score = l_log.find('div', class_="match-player-stocks")
			if(l_score != None):
				l_score = l_score.text.strip()
			else:
				l_score = "0"
			l_char = l_log.find('div', class_="match-character loser")
			if(l_char != None):
				l_char = l_char.img.get('src').strip()
			else:
				l_char = "?"
			loser = l_namegrab.span.getText().encode('ascii', 'ignore').strip()

			if(l_score == 'DQ'): continue
			if(w_score == 'DQ'): continue

			## img_to_char
			if (w_char == "https://images.smash.gg/images/character/6/image-55b92279973dc72a6e2ae99b2e22a21c.png"): w_char = "Fox"
			if (w_char == "https://images.smash.gg/images/character/23/image-696cf22872b76795f6350dcde8494a70.png"): w_char = "Sheik"
			if (w_char == "https://images.smash.gg/images/character/5/image-325f30eee6631a6989a345e98da764e2.png"): w_char = "Falco"
			if (w_char == "https://images.smash.gg/images/character/18/image-d2f96f79292d23ede1d456607ca33384.png"): w_char = "Peach"
			if (w_char == "https://images.smash.gg/images/character/9/image-d985265ef0d8fc9d1c8952132dd99a29.png"): w_char = "Puff"
			if (w_char == "https://images.smash.gg/images/character/2/image-b3c33a1a600b53fd7d0750d38f37e665.png"): w_char = "Falcon"
			if (w_char == "https://images.smash.gg/images/character/8/image-4466e095b8d678180a3b825eb30d5428.png"): w_char = "ICs"
			if (w_char == "https://images.smash.gg/images/character/14/image-8c91c208bb2d4215c1428a7254454cff.png"): w_char = "Marth"
			if (w_char == "https://images.smash.gg/images/character/22/image-e6d3acbe1b82a1d2ec3c5ea616283997.png"): w_char = "Samus"
			if (w_char == "https://images.smash.gg/images/character/7/image-d9b5589528a705cfacdc7b7e38144302.png"): w_char = "Ganon"
			if (w_char == "https://images.smash.gg/images/character/13/image-dfcb808542da6ba2bf41a24e9494f8df.png"): w_char = "Mario"
			if (w_char == "https://images.smash.gg/images/character/4/image-afe3635350c115deca38e09e01adfce0.png"): w_char = "Doc"
			if (w_char == "https://images.smash.gg/images/character/12/image-f583318c7efb80b6fa7a3f5e45657670.png"): w_char = "Luigi"
			if (w_char == "https://images.smash.gg/images/character/12/image-f583318c7efb80b6fa7a3f5e45657670.png"): w_char = "G&W"
			if (w_char == "https://images.smash.gg/images/character/20/image-6232a3460eaf76d10c03f5f5724cee19.png"): w_char = "Pikachu"

			if (l_char == "https://images.smash.gg/images/character/6/image-55b92279973dc72a6e2ae99b2e22a21c.png"): l_char = "Fox"
			if (l_char == "https://images.smash.gg/images/character/23/image-696cf22872b76795f6350dcde8494a70.png"): l_char = "Sheik"
			if (l_char == "https://images.smash.gg/images/character/5/image-325f30eee6631a6989a345e98da764e2.png"): l_char = "Falco"
			if (l_char == "https://images.smash.gg/images/character/18/image-d2f96f79292d23ede1d456607ca33384.png"): l_char = "Peach"
			if (l_char == "https://images.smash.gg/images/character/9/image-d985265ef0d8fc9d1c8952132dd99a29.png"): l_char = "Puff"
			if (l_char == "https://images.smash.gg/images/character/2/image-b3c33a1a600b53fd7d0750d38f37e665.png"): l_char = "Falcon"
			if (l_char == "https://images.smash.gg/images/character/8/image-4466e095b8d678180a3b825eb30d5428.png"): l_char = "ICs"
			if (l_char == "https://images.smash.gg/images/character/14/image-8c91c208bb2d4215c1428a7254454cff.png"): l_char = "Marth"
			if (l_char == "https://images.smash.gg/images/character/22/image-e6d3acbe1b82a1d2ec3c5ea616283997.png"): l_char = "Samus"
			if (l_char == "https://images.smash.gg/images/character/7/image-d9b5589528a705cfacdc7b7e38144302.png"): l_char = "Ganon"
			if (l_char == "https://images.smash.gg/images/character/13/image-dfcb808542da6ba2bf41a24e9494f8df.png"): l_char = "Mario"
			if (l_char == "https://images.smash.gg/images/character/4/image-afe3635350c115deca38e09e01adfce0.png"): l_char = "Doc"
			if (l_char == "https://images.smash.gg/images/character/12/image-f583318c7efb80b6fa7a3f5e45657670.png"): l_char = "Luigi"
			if (l_char == "https://images.smash.gg/images/character/16/image-612796e66ce5c8dacb6693c240fe7665.png"): l_char = "G&W"
			if (l_char == "https://images.smash.gg/images/character/20/image-6232a3460eaf76d10c03f5f5724cee19.png"): l_char = "Pikachu"

			c.execute('INSERT INTO matches VALUES (?, ?, ?, ?, ?, ?, ?);', (winner, w_score, w_char, loser, l_score, l_char, event))
			print("{} beats {} {}-{}".format(winner, loser, w_score, l_score))

	if("Support Challonge development" in soup.strings):
		print("Challonge currently unsupported")

	else:
		print("???")

zzz = raw_input("Press enter to view")
c.execute('SELECT * FROM matches')
for row in c: print row
zzz = raw_input("Press Enter to exit")
conn.commit()
conn.close()