import pygame, time, random, csv, sys, threading, pygame.key, datetime, os
from pygame.locals import *
from datetime import date
from time import sleep

SID = raw_input("Please input subject ID: ")

# version 7.21.14
# author: B. Taylor Hilton
# email: hilton.taylor@gmail.com

#Condition 1: a = $0.00, b = $30.00.
#Condition 2: a = $5.00, b = $25.00.
#Condition 3: a = $10.00, b = $20.00.

pygame.init()
pygame.font.init()
pygame.display.init()

fpsClock = pygame.time.Clock()

# initializes timing, not final values for either
start = datetime.datetime.now()
stop = datetime.datetime.now()

def time_seconds(elapse):
	seconds = str(elapse.seconds) + '.' + str(elapse.microseconds)
	return seconds
	


# used for keeping track of when to switch players
current_trial = 1

# creates output csv file
output_name = '5_25outputSID%s.csv' % SID
csvout = open(output_name, "w")

dimension_x = 800  # horizontal dimension
dimension_y = 600  # vertical dimension

# creates the window object, comment/uncomment what is appropriate
windowSurfaceObj = pygame.display.set_mode((dimension_x,dimension_y)) # for testing

#windowSurfaceObj = pygame.display.set_mode((dimension_x,dimension_y), FULLSCREEN) # for scanner


# load images
blue_smile = pygame.image.load('blueface.png')
purple_smile = pygame.image.load('purpleface.png')
fixation = pygame.image.load('fixation.jpg')

# color definitions
red = pygame.Color(255, 0, 0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)

screen = 0  # value to keep track of what stage the program is at

# sets font type, monospace is good for formatting purposes
fontObj = pygame.font.SysFont("monospace", 30, bold = True)

# for testing purposes, set to False for experimenting
no_wait = False

# timing, initializes values so they can be used in the correct sequence later
face_time = datetime.datetime.now()
decision_phase = datetime.datetime.now()
decision_made = datetime.datetime.now()
decision_shown = datetime.datetime.now()
decision_actual = ''
keepFinal = 0
giveFinal = 0


def readInput():
	# reads from csv input
	cr = csv.reader(open("input5_25.csv", "rU"), dialect=csv.excel_tab)
	while True:
		try:  # reads values into array until exception occurs
			input.append( int(next(cr)[0]) )
		except StopIteration:
			break
	random.shuffle(input)
	
def roundNum(floatNum):
	newNum = floatNum*100
	newNum = newNum%10
	if newNum < 5:
		return floatNum-newNum/100
	else:
		return floatNum+(10-newNum)/100
	
def approx_equal(a, b):
     return abs(a - b) < .001
	
# True if rejected
def unDecision(giveValue):
	randgen = random.randint(1,100)
	if giveValue >= 7:
		return False
	elif giveValue == 0:
		return True
	elif giveValue == 1:
		return randgen < 40
	elif giveValue == 2:
		return randgen < 31
	elif giveValue == 3:
		return randgen < 18
	elif giveValue == 4:
		return randgen < 9
	elif giveValue == 5 or giveValue == 6:
		return randgen < 2	
	else:
		print 'improper function'
	
	
input = []
readInput()
iterator = iter(input)

# values to initialize 
maxKeep = iterator.next()  # reads from input to determine pie
keepValue = maxKeep  # sets current keep value
giveValue = 0 # sets current give value to 0
decision = False # used in logic structures for accept/reject
iteration = 0 # used in iterative processes
wait = 0 # time in milliseconds for loop to wait

rangeMin = 5 # lower range for this run, not currently used in logic
rangeMax = 25 # upper range for this run, just used for text on screen

# used in logic structure to note if a user is pressing the 1 key for the first time in a trial
firstDecision = True

# boolean that tells us if the scanner has responded at least once (keypress 5)
first_scan = True

# initial text values
keepmsg = 'KEEP: '
givemsg = 'GIVE: '
instrmsg ='       Decide how much to give someone '
instr_2 = '       and keep yourself.  They are only aware '
instr_3 = '       of the range, not the amount to split.'
instr_4 = '       Press 1 to change values, Press 2 to submit.'
instr_5 = '                 Press 1 to continue...'
rangemsg = 'Range: $' + str(rangeMin) + '-$' + str(rangeMax)
splitmsg = 'Amount to split in this run: ' + str(maxKeep)
roundmsg = 'round complete'
operatormsg = '{operator press spacebar to exit}'
responsemsg = ''

keepmsg = keepmsg + '$' + str(keepValue)
givemsg = givemsg + '$' + str(giveValue)
			

# "infinite" loop, contains pygame control structures
while True:
	if no_wait == True:
		wait = 0
	pygame.time.wait(wait)  # waits if a time was set earlier
	wait = 0
	
    #background color
	windowSurfaceObj.fill(black)
	
	# blank screen between rounds
	if screen == 2:
		windowSurfaceObj.fill(black)
		if iteration == 0:
			wait = 4000
			iteration = iteration +1
		else:
			screen = 5
			iteration = 0
	# decision phase
	elif screen == 3:
		if iteration == 0:
			responsemsg = '  ?'
			wait = 8000
		elif iteration == 1:
			if decision == False:
				responsemsg = 'ACCEPT'
			elif decision == True:
				responsemsg = 'REJECT'
			wait = 4000
		elif iteration == 2:
			try:
				maxKeep = iterator.next()
				keepValue = maxKeep
				giveValue = 0
				pygame.display.update()
				keepmsg = 'KEEP: $' + str(keepValue)
				givemsg = 'GIVE: $' + str(giveValue)
				splitmsg = 'Amount to split in this run: $' + str(maxKeep)
				screen = 2
			except:
				screen = 6
		# updates iterator	
		if iteration < 2:
			iteration = iteration + 1
		else:
			iteration = 0
	
	# fixation between trials		
	elif screen == 5:
		windowSurfaceObj.fill(black)
		windowSurfaceObj.blit(fixation, (dimension_x/2 - 250,dimension_y/2 - 150))
		pygame.display.flip()
		if iteration < 1:
			screen = 5
			iteration = iteration + 1
			wait = 4000 + random.randint(0,300)
		elif iteration == 1:
			screen = 4
			iteration = 0
			csvout.write(str(current_trial) + ',')
			csvout.write('n/a,')
			csvout.write(face_time+ ',')
			csvout.write(decision_phase+ ',')
			csvout.write(str(keepFinal)+ ',')
			csvout.write(str(giveFinal)+ ',')
			csvout.write(decision_actual+ ',')
			csvout.write(decision_made+ ',')
			csvout.write(decision_shown+ ',')
			csvout.write('\n')
			
			current_trial = current_trial + 1
			firstDecision = True
			
			stop = datetime.datetime.now()
			elapsed = stop-start
			face_time = time_seconds(elapsed)
			
	# round complete screen
	elif screen == 6:
		windowSurfaceObj.fill(black)
		roundSurface = fontObj.render(roundmsg, False, white)
		roundRect = roundSurface.get_rect()
		roundRect.topleft = (dimension_x/3 - 150, dimension_y/2) 
		windowSurfaceObj.blit(roundSurface, roundRect)
		
		operatorSurface = fontObj.render(operatormsg, False, white)
		operatorRect = operatorSurface.get_rect()
		operatorRect.topleft = (dimension_x/3-150, dimension_y/2+30) 
		windowSurfaceObj.blit(operatorSurface, operatorRect)
	# first fixation
	elif screen == 7:
		windowSurfaceObj.fill(black)
		windowSurfaceObj.blit(fixation, (dimension_x/2 - 250,dimension_y/2 - 150))
		pygame.display.flip()
		if iteration < 1:
			iteration = iteration + 1
			wait = 4000 + random.randint(0,300)
		elif iteration == 1:
			iteration = 0
			screen = 4
			stop = datetime.datetime.now()
			elapsed = stop-start
			face_time = time_seconds(elapsed)
		
		pygame.display.flip()
	# main trial screen objects
	if screen == 4 or screen == 3:
		windowSurfaceObj.fill(black)
		if screen == 4:
			responsemsg = ''
    	# puts images on screen
		windowSurfaceObj.blit(blue_smile, (dimension_x/5,dimension_y/3))
		windowSurfaceObj.blit(purple_smile, ((3*dimension_x/5),dimension_y/3))
	
    	# puts text in Surface object
		keepSurface = fontObj.render(keepmsg, False, white)
		giveSurface = fontObj.render(givemsg, False, white)
		splitSurface = fontObj.render(splitmsg, False, white)
		rangeSurface = fontObj.render(rangemsg, False, white)
		responseSurface = fontObj.render(responsemsg, False, white)
		
    	# sets positions of text
		keepRect = keepSurface.get_rect()
		keepRect.topleft = (dimension_x/5+20,dimension_y/3+210)
	
    
		giveRect = giveSurface.get_rect()
		giveRect.topleft = (dimension_x/5+20,dimension_y/3 + 240)
		
		rangeRect = rangeSurface.get_rect()
		rangeRect.topleft = (dimension_x/2-150, 50)
		splitRect = splitSurface.get_rect()
		splitRect.topleft = (dimension_x/2 - 300,80)
		
		responseRect = responseSurface.get_rect()
		responseRect.topleft = (2*dimension_x/3 ,3*dimension_y/5 + 40)
	
		# puts text on the screen
		windowSurfaceObj.blit(keepSurface, keepRect)
		windowSurfaceObj.blit(giveSurface, giveRect)
		windowSurfaceObj.blit(rangeSurface, rangeRect)
		windowSurfaceObj.blit(splitSurface, splitRect)
		windowSurfaceObj.blit(responseSurface, responseRect)
		if responsemsg == 'ACCEPT' or responsemsg == 'REJECT':
			stop = datetime.datetime.now()
			elapsed = stop-start
			decision_shown = time_seconds(elapsed)
	
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN: #key was pressed 
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if screen == 4:  # trial session behavior
				keepmsg = 'KEEP: '
				givemsg = 'GIVE: '
				if event.key == K_1:
					if keepValue > 0:
						keepValue = keepValue - 1
						giveValue = giveValue + 1
					elif keepValue == 0:
						keepValue = maxKeep
						giveValue = 0
					if firstDecision == True:
						stop = datetime.datetime.now()
						elapsed = stop-start
						decision_phase = time_seconds(elapsed)
						firstDecision = False
				elif event.key == K_2:
					if firstDecision == True:
						stop = datetime.datetime.now()
						elapsed = stop-start
						decision_phase = time_seconds(elapsed)
						firstDecision = False
					giveFinal = giveValue
					keepFinal = keepValue
					
					decision = unDecision(giveFinal)
					
					if decision == True:
						decision_actual = 'rejected'
					elif decision == False:
						decision_actual = 'accepted' 
					csvout.flush()  # writes to text file
					screen = 3
					stop = datetime.datetime.now()
					elapsed = stop-start
					decision_made = time_seconds(elapsed)
					
				keepmsg = keepmsg + '$' + str(keepValue)
				givemsg = givemsg + '$' + str(giveValue)
			elif screen == 0:
				if event.key == K_5:  # waits for scanner initialization
					if first_scan == True:
						start = datetime.datetime.now()  # for use of TR values, set again later
						first_scan = False
					else:
						elapsed = datetime.datetime.now() - start
						csvout.write('TR: ' + time_seconds(elapsed) + '\n')
						
					if iteration < 7:  # seven times without response
						iteration = iteration + 1
					else:
						screen = 7
						iteration = 0
						start = datetime.datetime.now() # true time zero set here
						csvout.write('Subject ID: ' + SID + '\n')
						csvout.write('trial, personality, faces shown (t), beginning of decision phase (t), proposer kept, proposer gave,')
						csvout.write('decision, decision made (t), decision shown (t)\n')
			elif screen == 6:
				if event.key == K_SPACE:
					pygame.quit()
					sys.exit()
			
			
	#refreshes display
	pygame.display.update()
	fpsClock.tick(30)