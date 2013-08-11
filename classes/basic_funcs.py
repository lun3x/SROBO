from sr import *

#Motor control
def go_straight():
	open_left()
	open_right()
	R.motors[0].target = speed * m0_error_correct
	R.motors[1].target = speed * m1_error_correct

def stop():
	R.motors[0].target = 0
	R.motors[1].target = 0

def curve(direction, increase): #curve to the right/left
	if direction == "right":
		R.motors[0].target = (speed * m0_error_correct) + increase
		R.motors[1].target = (speed * m1_error_correct)
	if direction == "left":
		R.motors[1].target = (speed * m1_error_correct) + increase
		R.motors[0].target = (speed * m0_error_correct)

def turn_left(degrees): #TODO work out what speed is needed for every degree
	print "Adjusting pincers"
	R.servos[0][1] = 95
	R.servos[0][7] = 65
	R.motors[0].target = -speed * m0_back_error_correct
	R.motors[1].target = speed * m1_error_correct
	time_to_sleep = float(degrees / d_per_sec)
	print "Turning for ", time_to_sleep, "s."
	time.sleep(time_to_sleep)
	stop()

def turn_right(degrees):
	print "Adjusting pincers"
	R.servos[0][1] = 25
	R.servos[0][7] = 5
	R.motors[0].target = speed * m0_error_correct
	R.motors[1].target = -speed * m1_back_error_correct
	time_to_sleep = float(degrees / d_per_sec)
	print "Turning for ", time_to_sleep, "s."
	time.sleep(time_to_sleep)
	stop()

def go_forward(distance):
	# if check_path_clear(distance) == False:
		# print "go_forward(distance) - Can't go that far"
		# return False
	open_left()
	open_right()
	R.motors[0].target = speed * m0_error_correct
	R.motors[1].target = speed * m1_error_correct
	time_to_sleep = float(distance)
	time.sleep(time_to_sleep)
	stop()

def go_backward(distance):
	R.motors[0].target = -speed * m0_back_error_correct
	R.motors[1].target = -speed * m1_back_error_correct
	time_to_sleep = float(distance)
	time.sleep(time_to_sleep)
	stop()

def quick_stop():
	R.motors[0].target = 0
	R.motors[1].target = 0

#---Servo control
#Bum flap
def close_back():
	R.servos[0][0] = 95
	time.sleep(1)

def open_back():
	R.servos[0][0] = 20
	time.sleep(1)

#--Pincers
#Close
def close_left():
	R.servos[0][1] = 45

def close_right():
	R.servos[0][7] = 45

#Open
def open_left():
	R.servos[0][1] = 70

def open_right():
	R.servos[0][7] = 20

def open_both():
	R.servos[0][1] = 70
	R.servos[0][7] = 20

#Shut
def shut_all():
	R.servos[0][1] = 0
	R.servos[0][7] = 95
	R.servos[0][0] = 95