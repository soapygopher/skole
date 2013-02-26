from numpy import *

a = [[0.8, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0.7, 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0.7, 0.1, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0.7, 0.1, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0.1, 0, 0, 0, 0.7, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0,      1     , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0.1, 0, 0, 0, 0.7, 0, 0, 0, 0.2, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0.1, 0, 0, 0.7, 0.2, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0.1, 0, 0, 0, 0.7, 0, 0, 0, 0.2, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.1, 0, 0, 0, 0.2, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0.1, 0, 0, 0.7, 0, 0, 0, 0, 0.2, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,      1    , 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,       1      , 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,         1      , 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0, 0, 0.7, 0.2, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.3]]

#reward = -0.02

def iterate(reward, alt=False):
	x = [reward,reward,reward,reward,reward,0,reward,reward,reward,reward,reward,0,1,-1,reward,reward]
	
	if alt:
		regulars = array([1 if i == reward else 0 for i in x])
		regulars.shape = (16, 1)
	
	global a
	locala = copy(a)
	locala = array(locala) # dimensions (16x16)
	if alt:
		locala = hstack((regulars, locala)) # dimensions (16x17)
	
	x = array(x) # dimension (16x1)
	
	for n in range(1000): # more than enough iterations
		if alt:
			x = hstack(([reward], x)).transpose() # x has dimensions (17x1)
		x = dot(locala, x) # (16x17) x (17x1) = (16x1)
	
	tempx = x.ravel()
	tempx.shape = (4,4) # dimension (4x4) for display
	print "Reward", reward, "alt =", alt
	print tempx.transpose()[::-1]
	print

iterate(-0.02, alt=True)
iterate(-0.04, alt=True)
iterate(-0.02, alt=False)
iterate(-0.04, alt=False)