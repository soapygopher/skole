import random, logging, copy
logging.basicConfig(level=logging.CRITICAL)

dirs = {
	"N": (-1, 0),
	"E": (0, 1),
	"S": (1, 0),
	"W": (0, -1)
}

def prettyprint(board):
	board = [[round(x, 3) if x else "[   ]" for x in row] for row in board]
	return "\n".join("\t".join(map(str, row)) for row in board)

def rotate(forward, rotation):
	if forward == "N":
		return "W" if rotation == "left" else "E"
	elif forward == "E":
		return "N" if rotation == "left" else "S"
	elif forward == "S":
		return "E" if rotation == "left" else "W"
	else:
		return "S" if rotation == "left" else "N"

def move(intended):
	rand = random.random()
	if rand < 0.7: # 70% of cases
		direction = intended
	elif rand < 0.9: # 20% of cases
		direction = rotate(intended, "left")
	else: # 10% of cases
		direction = rotate(intended, "right")
	return direction

def valuefromcell(board, x, y, direction, policy=False):
	logging.info("Looking at position " + str(x) + str(y))
	dy, dx = dirs[direction]
	ldy, ldx = dirs[rotate(direction, "left")]
	rdy, rdx = dirs[rotate(direction, "right")]
	logging.info("Intended direction " + direction + " -> dx = " + str(dx) + ", dy = " + str(dy) + " to " + str(x + dx) + str(y + dy))
	frontcell = leftcell = rightcell = board[y][x]
	if (0 <= x + dx <= 3) and (0 <= y + dy <= 3):
		frontcell = board[y + dy][x + dx]
		frontcell = frontcell if frontcell else board[y][x]
	if (0 <= x + ldx <= 3) and (0 <= y + ldy <= 3):
		leftcell = board[y + ldy][x + ldx]
		leftcell = leftcell if leftcell else board[y][x]
	if (0 <= x + rdx <= 3) and (0 <= y + rdy <= 3):
		rightcell = board[y + rdy][x + rdx]
		rightcell = rightcell if rightcell else board[y][x]
	# logging.info("Right value is " + str(rightcell))
	# logging.info("Front value is " + str(frontcell))
	# logging.info("Left value is " + str(leftcell))
	# avg = (0.7 * frontcell) + (0.2 * leftcell) + (0.1 * rightcell)
	# logging.info("Weighted average = " + str(0.7 * frontcell) + " + " + str(0.2 * leftcell) + " + " + str(0.1 * rightcell) + " = " + str(avg))
	if policy:
		if frontcell[0] is None:
			frontcell = (0, frontcell[1])
		if leftcell[0] is None:
			leftcell = (0, leftcell[1])
		if rightcell[0] is None:
			rightcell = (0, rightcell[1])
		#print x, y, "f", frontcell, "l", leftcell, "r", rightcell
		return (0.7 * frontcell[0]) + (0.2 * leftcell[0]) + (0.1 * rightcell[0])
	else:
		return (0.7 * frontcell) + (0.2 * leftcell) + (0.1 * rightcell)

def valueiteration(reward):
	print "Value iteration:"
	epsilon = 0.0001
	gamma = 0.9
	board = [
		[reward, reward, None,   reward],
		[reward, reward, reward, reward],
		[reward, None,   reward,     -1],
		[reward, reward, reward,      1]
	]
	iterationnumber = 1
	convergence = False
	while not convergence:
		delta = 0
		nextiterboard = copy.deepcopy(board)
		for y, line in enumerate(board):
			for x, cell in enumerate(line):
				if (x == 3 and y == 3) or (x == 3 and y == 2):
					logging.info("Cell " + str(x) + str(y) + " is a terminal")
					continue
				elif (x == 2 and y == 0) or (x == 1 and y == 2):
					logging.info("Cell " + str(x) + str(y) + " is useless")	
					continue
				northval = valuefromcell(board, x, y, "N")
				southval = valuefromcell(board, x, y, "S")
				westval = valuefromcell(board, x, y, "W")
				eastval = valuefromcell(board, x, y, "E")
				newvalue = reward + gamma * max(eastval, westval, southval, northval)
				delta = max(delta, newvalue - nextiterboard[y][x])
				nextiterboard[y][x] = newvalue
		board = nextiterboard
		convergence = delta < epsilon * (1 - gamma) / gamma
		iterationnumber += 1
	print "Convergence in iteration", iterationnumber - 1
	print prettyprint(board)
	

def policyiteration(reward):
	print "Policy iteration"
	epsilon = 0.0001
	gamma = 0.9
	board = [
		[(reward, "N"), (reward, "N"), (None, ""),   (reward, "N")],
		[(reward, "N"), (reward, "N"), (reward, "N"), (reward, "N")],
		[(reward, "N"), (None, ""),   (reward, "N"), (-1, "")],
		[(reward, "N"), (reward, "N"), (reward, "N"), (1, "")]
	]
	iterationnumber = 1
	change = True
	while change:
		change = False
		print "iteration", iterationnumber
		print (board)
		print
		nextiterboard = copy.deepcopy(board)
		for y, line in enumerate(board):
			for x, cell in enumerate(line):
				if (x == 3 and y == 3) or (x == 3 and y == 2):
					logging.info("Cell " + str(x) + str(y) + " is a terminal")
					continue
				elif (x == 2 and y == 0) or (x == 1 and y == 2):
					logging.info("Cell " + str(x) + str(y) + " is useless")	
					continue
				oldvalue, oldpol = board[y][x]
				northval = valuefromcell(board, x, y, "N", policy=True)
				southval = valuefromcell(board, x, y, "S", policy=True)
				westval = valuefromcell(board, x, y, "W", policy=True)
				eastval = valuefromcell(board, x, y, "E", policy=True)
				# directionvalues = [valuefromcell(board, x, y, d, policy=True) for d in dirs]
				# print "dv", directionvalues
				newvalue, newpol = max((eastval, "E"), (westval, "W"), (southval, "S"), (northval, "N"))
				newvalue = reward + gamma * newvalue
				# print "newval", newvalue
				# print "newpol", newpol
				if newvalue > oldvalue or newpol != oldpol:
				# if newpol != oldpol:
					nextiterboard[y][x] = (newvalue + reward, newpol)
					print "change in ", x, y
					print "was", oldpol, "now", newpol
					change = True
				#newvalue = reward + gamma * max(eastval, westval, southval, northval)
				#delta = max(delta, newvalue - nextiterboard[y][x])
				#print "delta ", delta
				#nextiterboard[y][x] = newvalue
		board = nextiterboard
		#convergence = delta < epsilon * (1 - gamma) / gamma
		iterationnumber += 1
	print "Convergence in iteration", iterationnumber - 1
	#print prettyprint(board)
	p = [[x[1] for x in row] for row in board]
	v = [[x[0] for x in row] for row in board]
	print "\n".join("\t".join(map(str, row)) for row in p)
	print "\n".join("\t".join(map(str, row)) for row in v)
	
	print board

reward = -0.04
#valueiteration(reward)
policyiteration(reward)
