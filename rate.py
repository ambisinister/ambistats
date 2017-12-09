import sqlite3, math
conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

# functions adapted from sublee's github 

def scale_down(rating, sigma, vol, ratio=173.7178):
	mu = (rating-1500) / ratio
	sig = sigma / ratio
	return [mu, sig, vol]

def scale_up(rating, sigma, vol, ratio=173.7178):
	mu = (rating*ratio) + 1500
	sig = sigma * ratio
	return [mu, sig, vol]

def reduce_impact(rating, sigma, vol):
	#g(RD)
	return 1 / math.sqrt(1 + (3 * sigma ** 2) / (math.pi ** 2))

def expect_score(myrate, oprate, impact):
	return 1./ (1 + math.exp(-impact * (myrate - oprate)))

def determine_volatility(rating, sig, vol, difference, variance):
        sigma = sig
        tau = 1
        epsilon = 0.000001
        min_delta=0.0001
        difference_squared = difference ** 2

        # 1. Let a = ln(s^2), and define f(x)
        alpha = math.log(vol ** 2)
        def f(x):
            """This function is twice the conditional log-posterior density of
            sigma, and is the optimality criterion.
            """
            tmp = sigma ** 2 + variance + math.exp(x)
            a = math.exp(x) * (difference_squared - tmp) / (2 * tmp ** 2)
            b = (x - alpha) / (tau ** 2)
            return a - b

        # 2. Set the initial values of the iterative algorithm.
        a = alpha
        if difference_squared > sigma ** 2 + variance:
            b = math.log(difference_squared - sigma ** 2 - variance)
        else:
            k = 1
            while f(alpha - k * math.sqrt(tau ** 2)) < 0:
                k += 1
            b = alpha - k * math.sqrt(tau ** 2)

        # 3. Let fA = f(A) and f(B) = f(B)
        f_a, f_b = f(a), f(b)

        # 4. While |B-A| > e, carry out the following steps.
        # (a) Let C = A + (A - B)fA / (fB-fA), and let fC = f(C).
        # (b) If fCfB < 0, then set A <- B and fA <- fB; otherwise, just set
        #     fA <- fA/2.
        # (c) Set B <- C and fB <- fC.
        # (d) Stop if |B-A| <= e. Repeat the above three steps otherwise.
        while abs(b - a) > epsilon and abs(b - a) > min_delta:
            c = a + (a - b) * f_a / (f_b - f_a)
            f_c = f(c)
            if f_c * f_b < 0:
                a, f_a = b, f_b
            else:
                f_a /= 2
            b, f_b = c, f_c

        # 5. Once |B-A| <= e, set s' <- e^(A/2)
        return math.exp(1) ** (a / 2)	

# calculates ELO by each match
def rate(match):
	#get ELOs
	welo = -1
	lelo = -1
	wrd = -1
	lrd = -1
	wvl = -1
	lvl = -1

	c.execute('SELECT * FROM players WHERE tag = (?)', (match[0], ))
	for row in c: 
		welo = row[2]
		wrd = row[3]
		wvl = row[4]

	c.execute('SELECT * FROM players WHERE tag = (?)', (match[3], ))
	for row in c: 
		lelo = row[2]
		lrd = row[3]
		lvl = row[4]

	#2
	wrating = scale_down(welo, wrd, wvl)
	lrating = scale_down(lelo, lrd, lvl)

	#3
	wimpact = reduce_impact(lrating[0], lrating[1], lrating[2])
	limpact = reduce_impact(wrating[0], wrating[1], wrating[2])
	ew = expect_score(wrating[0], lrating[0], wimpact)
	el = expect_score(lrating[0], wrating[0], limpact)

	wvariance = 1. / (wimpact**2 * ew * (1-ew))
	lvariance = 1. / (limpact**2 * el * (1-el))

	#4
	wdifference = wvariance*wimpact*(1-ew)
	ldifference = lvariance*limpact*(-ew)

	#5
	new_wvol = determine_volatility(wrating[0], wrating[1], wrating[2], wdifference, wvariance)
	new_lvol = determine_volatility(lrating[0], lrating[1], lrating[2], ldifference, lvariance)

	#6-7
	sigma_star_w = math.sqrt(wrating[1]**2 + wrating[2]**2)
	wrating[1] = 1 / math.sqrt(1 / sigma_star_w ** 2 + 1 / wvariance)
	wrating[0] = wrating[0] + wrating[1] ** 2 * (wdifference / wvariance)

	sigma_star_l = math.sqrt(lrating[1]**2 + wrating[2]**2)
	lrating[1] = 1. / math.sqrt(1. / sigma_star_l ** 2 + 1. / lvariance)
	lrating[0] = lrating[0] + lrating[1] ** 2 * (ldifference / lvariance)

	#8
	wrating = scale_up(wrating[0], wrating[1], wrating[2])
	lrating = scale_up(lrating[0], lrating[1], lrating[2])

	c.execute('UPDATE players SET elo=(?), RD=(?), volatility=(?) WHERE tag=(?)', (wrating[0], wrating[1], wrating[2], match[0]))
	c.execute('UPDATE players SET elo=(?), RD=(?), volatility=(?) WHERE tag=(?)', (lrating[0], lrating[1], lrating[2], match[3]))

def init_ratings():
	# arbitrarily set all elos to 1600 - don't like this idea since it
	# super undervalues early wins but just wanna see what kind of results it gives
	c.execute('UPDATE players SET elo=1500 WHERE tag LIKE "%"')
	c.execute('UPDATE players SET RD=350 WHERE tag LIKE "%"')
	c.execute('UPDATE players SET volatility=0.06 WHERE tag LIKE "%"')

def rate_all_games():
	games = []
	c.execute('SELECT * FROM matches INNER JOIN tourneys ON matches.event=tourneys.event ORDER BY tourneys.date ASC')
	for row in c: games.append(row)

	init_ratings()

	for game in games:
		rate(game)

	c.execute('SELECT * FROM players ORDER BY (elo-3*RD) DESC')
	sample = 0
	for row in c:
		sample += 1
		print("{}: {: >15} {: >15} {: >15} {: >15} {: >15}".format(sample, *row))
		if sample >= 999:
			break

rate_all_games()