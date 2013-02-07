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

def valuefrom(board, x, y, direction):
	logging.info("Looking at position " + str(x) + str(y))
	dy, dx = dirs[direction]
	ldy, ldx = dirs[rotate(direction, "left")]
	rdy, rdx = dirs[rotate(direction, "right")]
	logging.info("Intended direction " + direction + " -> dx = " + str(dx) + ", dy = " + str(dy) + " to " + str(x + dx) + str(y + dy))
	frontcell, leftcell, rightcell = 0, 0, 0
	if (0 <= x + dx <= 3) and (0 <= y + dy <= 3):
		frontcell = board[y + dy][x + dx]
		frontcell = frontcell if frontcell and (0 <= x + dx <= 3) and (0 <= y + dy <= 3) else 0
	if (0 <= x + ldx <= 3) and (0 <= y + ldy <= 3):
		leftcell = board[y + ldy][x + ldx]
		leftcell = leftcell if leftcell else 0
	if (0 <= x + rdx <= 3) and (0 <= y + rdy <= 3):
		rightcell = board[y + rdy][x + rdx]
		rightcell = rightcell if rightcell else 0
	logging.info("Right value is " + str(rightcell))
	logging.info("Front value is " + str(frontcell))
	logging.info("Left value is " + str(leftcell))
	avg = (0.7 * frontcell) + (0.2 * leftcell) + (0.1 * rightcell)
	logging.info("Weighted average = " + str(0.7 * frontcell) + " + " + str(0.2 * leftcell) + " + " + str(0.1 * rightcell) + " = " + str(avg))
	return (0.7 * frontcell) + (0.2 * leftcell) + (0.1 * rightcell)

def valueiteration():
	r = -0.04
	gamma = 0.9
	board = [
		[r, r,    None, r],
		[r, r,    r,    r],
		[r, None, r,   -1],
		[r, r,    r,    1]
	]
	print prettyprint(board)
	print
	convergence = False
	while not convergence:
		nextiterboard = copy.deepcopy(board)
		for y, line in enumerate(board):
			for x, cell in enumerate(line):
				if (x == 3 and y == 3) or (x == 3 and y == 2):
					logging.info("Cell " + str(x) + str(y) + " is a terminal")
					continue
				elif (x == 2 and y == 0) or (x == 1 and y == 2):
					logging.info("Cell " + str(x) + str(y) + " is useless")	
					continue
				northval = valuefrom(board, x, y, "N")
				southval = valuefrom(board, x, y, "S")
				westval = valuefrom(board, x, y, "W")
				eastval = valuefrom(board, x, y, "E")
				cell += gamma * max(eastval, westval, southval, northval)
				nextiterboard[y][x] = cell
		board = nextiterboard
		print prettyprint(board)
		print

valueiteration()
