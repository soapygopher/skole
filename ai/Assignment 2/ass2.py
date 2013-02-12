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

def valuefromcell(board, x, y, direction):
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
	logging.info("Right value is " + str(rightcell))
	logging.info("Front value is " + str(frontcell))
	logging.info("Left value is " + str(leftcell))
	avg = (0.7 * frontcell) + (0.2 * leftcell) + (0.1 * rightcell)
	logging.info("Weighted average = " + str(0.7 * frontcell) + " + " + str(0.2 * leftcell) + " + " + str(0.1 * rightcell) + " = " + str(avg))
	return (0.7 * frontcell) + (0.2 * leftcell) + (0.1 * rightcell)

def valueiteration():
	epsilon = 0.0001
	delta = 0
	reward = -0.04
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
		print "iteration", iterationnumber
		print prettyprint(board)
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
				northval = valuefromcell(board, x, y, "N")
				southval = valuefromcell(board, x, y, "S")
				westval = valuefromcell(board, x, y, "W")
				eastval = valuefromcell(board, x, y, "E")
				newvalue = reward + gamma * max(eastval, westval, southval, northval)
				delta = max(delta, newvalue - nextiterboard[y][x])
				#print "delta ", delta
				nextiterboard[y][x] = newvalue
		board = nextiterboard
		convergence = delta < epsilon * (1 - gamma) / gamma
		iterationnumber += 1

def policyiteration():
	epsilon = 0.0001
	delta = 0
	reward = -0.04
	gamma = 0.9
	board = [
		[reward, reward, None,   reward],
		[reward, reward, reward, reward],
		[reward, None,   reward,     -1],
		[reward, reward, reward,      1]
	]
	policyboard = [
		["N", "N", "N", "N"],
		["N", "N", "N", "N"],
		["N", "N", "N", "N"],
		["N", "N", "N", "N"]
	]
	iterationnumber = 1
	convergence = False
	unchanged = True
	while not convergence:
		delta = 0
		print "iteration", iterationnumber
		print prettyprint(board)
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
				northval = valuefromcell(board, x, y, "N")
				southval = valuefromcell(board, x, y, "S")
				westval = valuefromcell(board, x, y, "W")
				eastval = valuefromcell(board, x, y, "E")
				newvalue = reward + gamma * max(eastval, westval, southval, northval)
				delta = max(delta, newvalue - nextiterboard[y][x])
				#print "delta ", delta
				nextiterboard[y][x] = newvalue
		board = nextiterboard
		convergence = delta < epsilon * (1 - gamma) / gamma
		iterationnumber += 1

valueiteration()
#policyiteration()
