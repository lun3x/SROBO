# Motor 0 is LEFT
# Motor 1 is RIGHT

# Servo 0 is BUMFLAP
# Servo 1 is LEFT PADDLE - smaller = more closed
# Servo 7 is RIGHT PADDLE - bigger = more closed
from sr import  *
import time
import basic_funcs

R = Robot()

#Initialising
token_list = []
facing_wall = 0
dist_from_wall = 0
tokens_in_robot = 0
num_main_repeats = 0
is_looking_home = False
home_zone = R.zone

#Constants
ROBO_LENGTH = 0.5
speed = 40.0
d_per_sec = 180.0 #degrees per second

m0_error_correct = 1.0 #multiplier of motor 0 speed
m1_error_correct = 1.05 #multiplier of motor 1 speed

m0_back_error_correct = 1.00 #multiplier of motor 0 speed backwards
m1_back_error_correct = 1.00 #multiplier of motor 1 speed backwards

#Primary functions
def find_token(max_turns): #find nearest token
	global token_list
	has_found = False
	num_turns = 0
	while has_found == False and num_turns < max_turns:
		if update_token_list() == True:
			has_found = True
			return True
		else:
			turn_left(30.0) #turn left
			time.sleep(1)
			num_turns = num_turns + 1
			print "Looking for tokens...", num_turns
	if num_turns >= max_turns:
		print "Can't find tokens"
		return False

def line_up(max_turns): #line up robot with token
	global token_list
	if token_list == []:
		print "token_list = []"
		return False

	lined_up = False
	num_turns = 0

	while lined_up == False and num_turns < max_turns:
		print "line_up(max_turns) - Searching for markers"
		num_turns = num_turns + 1
		markers = R.see()
		if markers == []:
			print "Can't see any markers"
			return False
		for m in markers:
			if m.info.offset == token_list[0].info.offset:
				if m.rot_y > 5:
					turn_right(10.0)
					print "Lining up with token ", m.info.offset, " attempt ", num_turns
				elif m.rot_y < -5:
					turn_left(10.0)
					print "Lining up with token ", m.info.offset, " attempt ", num_turns
				else:
					lined_up = True
					print "Lined up with near token."
					return True

def get_token(): #go to token and close paddles
	global token_list
	global tokens_in_robot
	global ROBO_LENGTH
	if token_list == []:
		print "get_token() - token_list = []"
		return False

	at_token = False

	markers = R.see()
	for m in markers:
		if m.info.offset == token_list[0].info.offset:
			if go_forward(m.dist + ROBO_LENGTH) == False:
				print "get_token() - Can't get token"
				return False
			shut_all()
			open_both()
			at_token = True
			tokens_in_robot = tokens_in_robot + 1
			print "get_token() - Taken in token."
			token_list = []
			return True

def locate_robot():
	global facing_wall
	global dist_from_wall

	markers = R.see()

	for m in markers:
		if m.info.marker_type == MARKER_ARENA:
			if m.info.offset >= 0 and m.info.offset <= 6:
				facing_wall = 0
				print "facing_wall = 0"
			elif m.info.offset >= 7 and m.info.offset <= 13:
				facing_wall = 1
				print "facing_wall = 1"
			elif m.info.offset >= 14 and m.info.offset <= 20:
				facing_wall = 2
				print "facing_wall = 2"
			elif m.info.offset >= 21 and m.info.offset <= 27:
				facing_wall = 3
				print "facing_wall = 3"
			dist_from_wall = m.dist
			return True
	return False

def turn_to_home(max_turns):
	global facing_wall
	global is_looking_home
	global home_zone

	num_turns = 0

	locate_robot()

	if facing_wall == home_zone:
		is_looking_home = True
		return True
	else:
		is_looking_home = False

	while is_looking_home == False and num_turns < max_turns:
		num_turns = num_turns + 1
		turn_left(45)
		time.sleep(0.5)
		if locate_robot() == False:
			print "cant see home"
		if facing_wall == home_zone:
			is_looking_home = True
			return True
		print "not facing home"
	return False

def go_home():
	global is_looking_home
	global dist_from_wall
	global ROBO_LENGTH
	num_turns = 0

	if turn_to_home(5) == True:
		print "go_home() - Is looking home, going home..."
		if go_forward(dist_from_wall - 0.5) == False:
			print "go_home() - Can't get home"
			return False
		return True
	else:
		print "go_home() - Not looking home"
		return False

def drop_off_tokens():
	global tokens_in_robot
	global ROBO_LENGTH
	turn_left(180) # 180 degrees
	print "Spinning"
	open_back()
	if go_forward(ROBO_LENGTH * 2) == False:
		print "drop_off_tokens() - Can't move away from tokens"
		turn_left(180)
		go_forward(3)
		return False
	close_back()
	print "Finished drop off"
	tokens_in_robot = 0
	return True

def follow_the_token():
	facing_token = False
	can_see_token = False

	while can_see_token == False:
		if update_token_list() == True:
			print "can_see_token = True"
			can_see_token = True

	if line_up(5) == True:
		facing_token = True
		update_token_list()
		old_rot_y = token_list[0].rot_y
		old_offset = token_list[0].rot_y
	else:
		facing_token = False
		return False

	while facing_token == True:
		if update_token_list() == True:
			if token_list[0].rot_y < old_rot_y + 5 and token_list[0].rot_y > old_rot_y - 5:
				go_straight()
				facing_token = True
			elif token_list[0].rot_y >= old_rot_y + 5:
				curve("right", 5)
			elif token_list[0].rot_y <= old_rot_y - 5:
				curve("left", 5)
		else:
			stop()
			can_see_token = False
			facing_token = False
			return False

def check_path_clear(distance):
	global token_list
	global ROBO_LENGTH
	markers = R.see()
	if markers != []:
		for m in markers:
			if m.info.marker_type == MARKER_ARENA or m.info.marker_type == MARKER_PEDESTAL:
				if m.dist < (ROBO_LENGTH):
					print "Detected wall."
					return False
				else:
					print "Path clear."
					return True
			elif m.info.marker_type == MARKER_ROBOT and m.dist < (ROBO_LENGTH):
				stop()
				print "Detected robot."
				return False
	print "Path clear."
	return True

#Secondary functions
def update_token_list():
	global token_list
	markers = R.see()
	for m in markers:
		if m.info.marker_type == MARKER_TOKEN:
			token_list.append(m)
			print "Found token ", m.info.offset, "! ", m.dist, "m away."
	if token_list != []:
		sort_tokens(token_list)
		token_list.reverse()
		return True
	else:
		return False

def get_dist(marker): #returns distance to marker
	return marker.dist

def sort_tokens(list): #sorts list of tokens by distance
	sorted(list, key=get_dist)
	
#Strategies
def dance(length):
	start_time = time.time()
	
	open_both()
	open_back()
	
	count = 0
	while time.time() - start_time < length:
		if count % 5 == 0:
			shut_all()
			
		elif count % 2 == 0:
			open_back()
			open_left()
			close_right()
			
		else:
			close_back()
			open_right()
			close_left()
		count = count + 1
		time.sleep(0.5)
		
def strategy_2():
	global token_list
	token_list = []
	open_both()

	if find_token(10) == True:
		print "about to line up with token", token_list[0].info.offset
		if line_up(10) == True:
			print "about to get token", token_list[0].info.offset
			if get_token() == True:
				print "got token"
			else:
				print "didn't get token", token_list[0].info.offset
		else:
			print "line_up(5) = False"
	else:
		print "find_token(5) = False"

	print "Completed strategy 2"

def main(): #start program
	global speed
	global num_main_repeats
	start_time = time.time()
	print time.time()
	close_back()
	open_both()
	
	while time.time() - start_time < 80.0:
		strategy_2()
		print time.time() - start_time
	print "test_strategy() - Going home."
	
	num_turns = 0
	while go_home() == False:
		if num_turns <= 2:
			turn_left(90)
		elif go_forward(1) == False or num_turns > 3:
			go_backward(3)
			num_turns = 0
		else:
			turn_right(90)

	while drop_off_tokens() == False:
		turn_left(20)

def test_strategy():
	start_time = time.time()
	while time.time() - start_time < 5.0:
		print time.time() - start_time
		strategy_2()
		
	print "test_strategy() - Going home."
	while go_home() == False:
		turn_left(90)
		if go_forward(1) == False:
			turn_right(90)

	while drop_off_tokens() == False:
		turn_left(20)
		
while True:
	main()