import random, logging, copy, numpy

logging.basicConfig(level=logging.CRITICAL)

dirs = {
	"N": (-1, 0),
	"E": (0, 1),
	"S": (1, 0),
	"W": (0, -1)
}

def prettyprint(board):
	if type(board[0][0]) is float:
		board = [[round(x, 3) if x else "[   ]" for x in row] for row in board]
	else:
		board = [[x if x else " " for x in row] for row in board]
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
		# stored as tuple for purposes of policy iteration
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
	#print "Value iteration"
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
	logging.warning("Convergence in iteration " + str(iterationnumber - 1))
	#print prettyprint(board)
	return board
	

def policyiteration(reward, getvalues=False):
	#print "Policy iteration"
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
		logging.debug("iteration", iterationnumber)
		logging.debug(board)
		nextiterboard = copy.deepcopy(board)
		for y, line in enumerate(board):
			for x, cell in enumerate(line):
				if (x == 3 and y == 3) or (x == 3 and y == 2):
					logging.debug("Cell " + str(x) + str(y) + " is a terminal")
					continue
				elif (x == 2 and y == 0) or (x == 1 and y == 2):
					logging.debug("Cell " + str(x) + str(y) + " is useless")	
					continue
				
				oldvalue, oldpolicy = board[y][x]
				
				northval = valuefromcell(board, x, y, "N", policy=True)
				southval = valuefromcell(board, x, y, "S", policy=True)
				westval = valuefromcell(board, x, y, "W", policy=True)
				eastval = valuefromcell(board, x, y, "E", policy=True)
				newvalue, newpolicy = max((eastval, "E"), (westval, "W"), (southval, "S"), (northval, "N"))
				logging.debug("newval", newvalue, "newpol", newpolicy)
				if newpolicy != oldpolicy:
				#if newvalue > oldvalue:
					nextiterboard[y][x] = (newvalue, newpolicy)
					logging.debug("change in ", x, y)
					logging.debug("was", oldpolicy, "now", newpolicy)
					logging.debug("was", oldvalue, "now", newvalue)
					change = True
		
		board = nextiterboard
		iterationnumber += 1
	
	logging.warning("Convergence in iteration " + str(iterationnumber - 1))
	p = [[x[1] for x in row] for row in board] # policies
	v = [[x[0] for x in row] for row in board] # values
	logging.debug("\n".join("\t".join(map(str, row)) for row in p))
	logging.debug("\n".join("\t".join(map(str, row)) for row in v))
	if getvalues: # for problem 1.4
		return v
	else:
		return p

def linalgiterate(reward):
	a = [[0.8, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0.7, 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0.7, 0.1, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0.7, 0.1, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0.1, 0, 0, 0, 0.7, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0.1, 0, 0, 0, 0.7, 0, 0, 0, 0.2, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0.1, 0, 0, 0.7, 0.2, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0.1, 0, 0, 0, 0.7, 0, 0, 0, 0.2, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.1, 0, 0, 0, 0.2, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0.1, 0, 0, 0.7, 0, 0, 0, 0, 0.2, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0, 0, 0.7, 0.2, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.3]]
	x = [reward,reward,reward,reward,reward,0,reward,reward,reward,reward,reward,0,1,-1,reward,reward]
		
	rewards = numpy.array([1 if i == reward else 0 for i in x])
	rewards.shape = (16, 1)
		
	tempa = numpy.array(numpy.copy(a)) # dimensions (16x16)
	tempa = numpy.hstack((rewards, tempa)) # dimensions (16x17)
		
	x = numpy.array(x) # dimension (16x1)
		
	for n in range(1000): # more than enough iterations
		x = numpy.hstack(([reward], x)).transpose() # x has dimensions (17x1)
		x = numpy.dot(tempa, x) # (16x17) x (17x1) = (16x1)
			
	tempx = x.ravel()
	tempx.shape = (4,4) # dimension (4x4) for display
	return tempx.transpose()[::-1]

def problem11():
	print "Problem 1.1"
	reward = -0.04
	print "Value iteration"
	print prettyprint(valueiteration(reward))
	print
	print "Policy iteration"
	print prettyprint(policyiteration(reward))

def problem12():
	print "Problem 1.2"
	print linalgiterate(-0.02)
	print linalgiterate(-0.04)

def problem14():
	print "Problem 1.4"
	print "r\t(3, 2)\t(2, 1)\t(4, 4)"
	steps = 100
	for reward in range(-4 * steps, 1, 7):
		reward /= float(steps)
		v = linalgiterate(reward) # using the policy "n", going south all the time
		state32 = v[2][2]
		state21 = v[3][1]
		state44 = v[0][3]
		print "\t".join(map(str, [reward, state32, state21, state44]))

def problem15():
	print "Problem 1.5"
	print "r\t State (2, 3)\t State (3, 3)\t State (3, 2)"
	steps = 1000
	for reward in range(-4 * steps, 1, 1):
		reward /= float(steps)
		state23 = valueiteration(reward)[1][1]
		state33 = valueiteration(reward)[1][2]
		state32 = valueiteration(reward)[2][2]
		print "\t".join(map(str, [reward, state23, state33, state32]))

def problem24():
	#board = [0, 0, -1, 0, 1, 0, -1, 0, 0]
	board = range(9)
	def jump(start, direction, magnitude): 
		# returns an index
		# jump into left wall from square 1 with magnitude 2, bounce off and land in 2
		if start == 0 and direction == -1 and magnitude == 2: 
			return 1
		# jump into left wall from square 1 with magnitude 1, bounce off and land in same spot
		elif start == 0 and direction == -1 and magnitude == 1:
			return 0 # to square 1
		# jump into left wall from square 2 with magnitude 2, bounce off and land in 1
		elif start == 1 and direction == -1 and magnitude == 2:
			return 0
		# jump into right wall from square 9 with magnitude 2, bounce off and land in 8
		elif start == 8 and direction == 1 and magnitude == 2:
			return 7
		# jump into right wall from square 9 with magnitude 1, bounce off and land in same spot
		elif start == 8 and direction == 1 and magnitude == 1:
			return 8
		# jump into right wall from square 8 with magnitude 2, bounce off and land in 9
		elif start == 7 and direction == 1 and magnitude == 2:
			return 8
		# all other cases
		else:
			return start + (direction * magnitude)
	
	# testing
	# for i in range(9):
	# 	for d in [-1, 1]:
	# 		for m in [0, 1, 2]:
	# 			idx = jump(i, d, m)
	# 			s = "Jumping from %d to the %s with magnitude %d lands you in %d" 
	# 			s %= (i + 1, "left" if d == -1 else "right", m, board[idx] + 1)
	# 			logging.debug(s)
	
	def valueit(reward):
		convergence = False
		gamma = 0.9
		epsilon = 0.01
		startboard = [float("-inf"), float("-inf"), -1, float("-inf"), 1, float("-inf"), -1, float("-inf"), float("-inf")]
		utilities = zip(startboard, [0 for i in range(9)])
		while not convergence:
			delta = 0
			newutilities = copy.deepcopy(utilities)
			for i, (oldutility, oldpolicy) in enumerate(utilities):
				
				logging.debug(str(i) + " old " + str(oldutility) + " " + str(oldpolicy))
				if i == 2 or i == 6:
					logging.debug("skip "  + str(i))
					continue # terminals
				
				jump2left =   (utilities[jump(i, -1, 2)][0], -2)
				jump1left =   (utilities[jump(i, -1, 1)][0], -1)
				jumpinplace = (utilities[jump(i, 1, 0)][0], 0)
				jump1right =  (utilities[jump(i, 1, 1)][0], 1)
				jump2right =  (utilities[jump(i, 1, 2)][0], 2)
				
				logging.debug("jumps" + str([jump2left, jump1left, jumpinplace, jump1right, jump2right]))
				
				# restictions on what moves are allowed, depending on the previous move
				if oldpolicy == -2: 
					bestutility, bestmove = max(jump2left, jump1left)
				elif oldpolicy == -1: 
					bestutility, bestmove = max(jump2left, jump1left, jumpinplace)
				elif oldpolicy == 0: 
					bestutility, bestmove = max(jump1left, jumpinplace, jump1right)
				elif oldpolicy == 1: 
					bestutility, bestmove = max(jumpinplace, jump1right, jump2right)
				elif oldpolicy == 2: 
					bestutility, bestmove = max(jump1right, jump2right)
				
				logging.debug("bestutility, bestmove " + str(bestutility) + " " + str(bestmove))
				
				newutility = reward + gamma * bestutility # bellman update
				if newutility > oldutility:
					newutilities[i] = (newutility, bestmove)
					delta = abs(oldutility - newutility)
			
			utilities = newutilities
			convergence = delta < epsilon * (1 - gamma) / gamma
		print [round(x[0], 3) for x in utilities]
		
		def polstr(d):
			if d == -2:
				return "<--"
			elif d == -1:
				return "<-"
			elif d == 0:
				return "^"
			elif d == 1:
				return "->"
			elif d == 2:
				return "-->"
		
		print [polstr(x[1]) for x in utilities]
	
	for r in [-0.04, -0.5, -1]:
		print "r =", r
		valueit(r)
		print

problem24()
