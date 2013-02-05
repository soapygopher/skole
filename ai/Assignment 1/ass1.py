#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: python ass1.py [args]
# See submitted report for details.

import string, copy, time, argparse, random

# Tuples of (dy, dx) for all directions
directions = {
	"N": (-1, 0),
	"E": (0, 1),
	"S": (1, 0),
	"W": (0, -1)
}

# Used for counting states, problem 1.1
statesvisited = 0

# Used for the search algorithms.
class Node:
	def __init__(self, board, player, command):
		self.board = board
		self.player = player
		self.value = fancyheuristic(board, player) if fancy else simpleheuristic(board, player)
		self.command = command # The move made to generate this state

# Dummy classes for representing the players.
class Black: 
	def __init__(self): 
		self.piece = "X"

class White: 
	def __init__(self): 
		self.piece = "O"

# Generates a list of all possible successor states to the given board position.
def successors(board, player):
	succs = []
	for y, line in enumerate(board):
		for x, char in enumerate(line):
			if char == player.piece:
				# Try all possible moves: xyN, xyE, xyS, xyW
				for cmd in (str(x + 1) + str(y + 1) + d for d in directions): 
					try:
						candidate = move(cmd, board, player)
						succs.append(Node(candidate, player, cmd))
					except (ValueError, IndexError) as e:
						# ValueError: attempted move was illegal, e.g. trying to move to an occupied square
						# IndexError: try to move outside of the board
						continue
	# Used for problem 1.2, for determining whether varying the evaluation order matters
	if args.shuffle:
		random.shuffle(succs)
	return succs

def alphabeta(player, node, depth, alpha, beta):
	if countingstates:
		global statesvisited
		statesvisited += 1
	succs = successors(node.board, player)
	otherplayer = white if player is black else black
	# Cut off and return heuristic value if we are too deep down
	if depth == cutoff or len(succs) == 0:
		return node.value
	# White is maxplayer (arbitrary pick)
	elif player is white: 
		for childnode in succs:
			alpha = max(alpha, alphabeta(otherplayer, childnode, depth + 1, alpha, beta))
			if alpha >= beta:
				return beta
		return alpha
	# Black is minplayer
	else: 
		for childnode in succs:
			beta = min(beta, alphabeta(otherplayer, childnode, depth + 1, alpha, beta))
			if alpha >= beta:
				return alpha
		return beta

def minmax(player, node, depth):
	otherplayer = white if player is black else black
	if countingstates:
		global statesvisited
		statesvisited += 1
	if depth == cutoff or not successors(node.board, player):
		return node.value
	elif node.player is black: # Arbitrary pick
		return min(minmax(otherplayer, child, depth + 1) for child in successors(node.board, player))
	else:
		return max(minmax(otherplayer, child, depth + 1) for child in successors(node.board, player))

# Returns a comma-separated board of X-es and O-s to be printed to console.
def prettyprint(board):
	b = "\n".join(",".join(map(str, row)) for row in board)
	return b.replace("None", " ")

# Check if any consecutive n entries in a row are X-es or O-s, and
# return the number of n-in-a-row instances on the board for the given player.
def horizontal(board, n, player):
	piece = player.piece
	connected = 0
	for line in board:
		for i, char in enumerate(line):
			if line[i : i + n] == [piece] * n:
				connected += 1
	return connected

# Checking verticals is equivalent to checking horizontals in the transposed matrix.
def vertical(board, n, player):
	return horizontal(map(list, zip(*board)), n, player)

# All downward diagonals must start in the upper-left 4x4 submatrix, and similarly, all upward diagonals must start in the lower-left 4x4 submatrix.
# Somewhat inelegant, but it works.
def diagonal(board, n, player):
	piece = player.piece
	connected = 0
	for i in range(n):
		for j in range(n):
			# Count four down(up)ward from the upper (lower) left quadrant.
			if (all(board[i + k][j + k] == piece for k in range(n)) 
			or all(board[6 - i - k][j + k] == piece for k in range(n))):
				connected += 1
	return connected

# Indicate the winner (if any) in the given board state.
# Used, among other things, for the main game loop, which runs as long as there is no winner.
def winner(board):
	if horizontal(board, 4, white) or vertical(board, 4, white) or diagonal(board, 4, white):
		return white
	elif horizontal(board, 4, black) or vertical(board, 4, black) or diagonal(board, 4, black):
		return black
	else:
		return None

# Indicated whether the player has managed to thwart the opponent's play by blocking three of their pieces, thus preventing a loss.
# Used by the advanced utility function.
def sabotage(board, player):
	goal = "OOOX" if player is black else "XXXO"
	# This is a terrible, terrible hack, and I'm ashamed of it.
	# Map the elements in the matrix to strings, concatenate,
	auxboard = [map(str, l) for l in copy.deepcopy(board)]
	auxboard = ["".join(l) for l in auxboard]
	auxtransp = ["".join(l) for l in map(list, zip(*auxboard))]
	# then look up XXXO and OOOX and their reverses in that string.
	hor = any(goal in line or goal[::-1] in line for line in auxboard)
	vert = any(goal in line or goal[::-1] in line for line in auxtransp)
	# The diagonal is a bit more tricky, but the same reasoning applies as in the horizontal(board, n, player) function.
	# All interesting diagonals start in the upper or lower left quandrants, so we make a list of them, join each of them up and look for the OOOX and XXXO strings and their reverses there.
	diags = []
	for i in range(4):
		for j in range(4):
			diags.append([board[i + k][j + k] for k in range(4)])
			diags.append([board[6 - i - k][j + k] for k in range(4)])
	# Map elements to string and concatenate with empty string.
	diags = ["".join(l) for l in [map(str, l) for l in diags]]
	diag = any(goal in line or goal[::-1] in line for line in diags)
	return hor or vert or diag

# As given in problem 1.
def simpleheuristic(board, player):
	otherplayer = white if player is black else black
	if winner(board) is player:
		return 1
	elif winner(board) is otherplayer:
		return -1
	else:
		return 0

# A somewhat more advanced heuristic, used for part 2 of the assignment and actual gameplay. See the submitted report for details and discussion.
def fancyheuristic(board, player):
	otherplayer = white if player is black else black
	score = 0
	for i in [4, 3, 2]:
		h = horizontal(board, i, player)
		v = vertical(board, i, player)
		d = diagonal(board, i, player)
		score += (10 ** i) * (h + v + d)
	if sabotage(board, player):
		score += 9999
	elif sabotage(board, otherplayer):
		score -= 9999
	return score

# Builds a matrix from an input string, in case we want to specify an initial board layout.
def parseboard(boardstring):
	boardstring = string.replace(boardstring, ",", "")
	board, line = [], []
	for char in boardstring:
		if char == " ":
			line.append(None)
		elif char == "\n":
			board.append(line)
			line = []
		else: 
			line.append(char)
	if line:
		board.append(line) # Last line, if there is no newline at the end
	return board

# Performs a move according to a given command, and returns the new game state.
def move(command, board, player):
	# Takes indices and a direction, e.g. "43W" or "26N".
	x, y, d = tuple(command)
	# The board is a zero-indexed array, adjust accordingly
	x, y = int(x) - 1, int(y) - 1
	dy, dx = directions[d.upper()]
	# Does the piece fall within the bounds?
	if ((0 <= x + dx <= 7) and (0 <= y + dy <= 7)
	# ...and is it our piece?
	and board[y][x] == player.piece
	# ...and is the destination square empty?
	and not board[y + dy][x + dx]):
		# ...then it's okay
		successor = copy.deepcopy(board)
		successor[y + dy][x + dx] = successor[y][x]
		successor[y][x] = None
		return successor
	else:
		raise ValueError("The move " + command + " by " + player.__class__.__name__ + " is not legal")

# Parse command-line arguments. See submitted report for summary of usage.
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cutoff", help="Cutoff depth")
parser.add_argument("-i", "--input", help="Input game board")
parser.add_argument("-u", "--human", choices=["w", "b"], help="Play with a human opponent")
parser.add_argument("-a", "--alg", choices=["mm", "ab"], help="Minmax or alpha-beta algorithm")
parser.add_argument("-l", "--log", help="Write a game log on exit", action="store_true")
parser.add_argument("-s", "--shuffle", help="Shuffle successor list", action="store_true")
parser.add_argument("-k", "--count", help="Count states visited", action="store_true")
parser.add_argument("-f", "--fancy", help="Fancy heuristic function", action="store_true")
parser.add_argument("-t", "--time", help="Timeout limit in seconds")
args = parser.parse_args()

cutoff = int(args.cutoff) if args.cutoff else 3
useab = not (args.alg == "mm") # Alpha-beta by default
logthegame = args.log
countingstates = args.count
fancy = args.fancy
timeout = float(args.time) if args.time else float("inf")

# If we give an input file, parse it and set up the initial board layout accordingly.
if args.input:
	with open(args.input, "r") as inputfile:
		initstr = inputfile.read()
	board = parseboard(initstr)
else: # If not, default to the starting position from the assignment.
	board = [
		["O", None, None, None, None, None, "X"],
		["X", None, None, None, None, None, "O"],
		["O", None, None, None, None, None, "X"],
		["X", None, None, None, None, None, "O"],
		["O", None, None, None, None, None, "X"],
		["X", None, None, None, None, None, "O"],
		["O", None, None, None, None, None, "X"]
	]

# Player instances
white = White()
black = Black()

# Designate a human player to a color if one is given, else let the computer play against itself.
if args.human == "w":
	human = white
	computer = black
elif args.human == "b":
	human = black
	computer = white
else:
	human = None
	computer = black # Arbitrary choice

# Other administrivia
currentplayer = white
log = ["Initial state:"]
movenumber = 1

# Main loop. Runs as long as there is no winner, or until interrupted.
while winner(board) is None:
	# Print informative stuff at the beginning of each round.
	playername = currentplayer.__class__.__name__
	p = prettyprint(board)
	print p
	print "\nMove #%s:" % movenumber
	print "It's %s's turn." % playername
	if logthegame:
		log.append(p)
		log.append("\nMove #%s:" % movenumber)
		log.append("It's %s's turn." % playername)
		
	cmd = "" # Command string, e.g. 11E or 54N
	
	try: # In case of keyboard interrupts
		# Show a list of options to human players:
		if currentplayer is human:
			print "Possible moves:"
			for s in successors(board, currentplayer):
				print s.command
			cmd = raw_input() 
		# Otherwise, have the computer calculate its move using the given algorithm.
		else:
			t = time.time() # Time limit is 20 seconds
			succs = successors(board, currentplayer) # Successors of this state
			# Take the first move, pick something better later on if we can find it.
			bestmove = succs[0].command
			bestutility = 0
			
			# Pick algorithm according to --alg argument.
			if useab: # Alpha-beta pruning
				for succ in succs:
					# Initialize with alpha = -inf, beta = inf
					u = alphabeta(currentplayer, succ, 0, float("-inf"), float("inf"))
					if u > bestutility:
						bestutility = u
						bestmove = succ.command
					if time.time() - t > timeout:
						print "Time limit cutoff"
						break
			else: # Minmax
				for succ in succs:
					u = minmax(currentplayer, succ, 0)
					if u > bestutility:
						bestutility = u
						bestmove = succ.command
					if time.time() - t > timeout:
						print "Time limit cutoff"
						break
			
			cmd = bestmove
			print "The computer makes the move", cmd
			print "Thinking took", time.time() - t, "seconds"
			if logthegame:
				log.append("Thinking took " + str(time.time() - t) + " seconds")
		
		# May raise a ValueError if input is ill-formed.
		board = move(cmd, board, currentplayer)
		
		if countingstates:
			print statesvisited
			raise Exception("Counting states only, stopping here")
		if logthegame:
			log.append("%s plays %s" % (playername, cmd))
		
		# Move to next round
		currentplayer = white if currentplayer is black else black
		playername = currentplayer.__class__.__name__
		movenumber += 1
	
	# Catch errors made by user when entering a command:
	except ValueError: 
		print "Illegal move."
	# Possibility for interrupting computation it takes too long.
	except KeyboardInterrupt:
		if logthegame:
			log.append("Game cancelled.")
		break

# Post-game formalities: print the board one last time, logging
print prettyprint(board)

if winner(board):
	s = "%s won the match" % winner(board).__class__.__name__
	print s
	if logthegame:
		log.append(s)
else:
	print "It's a draw"
	if logthegame:
		log.append("It's a draw")

if logthegame:
	log.append(prettyprint(board))
	logname = time.strftime("./connect4-%H-%M-%S.log")
	with open(logname, "w+") as logfile:
		logfile.write("\n".join(log))

