"""
traffic_generator_0.py

The first test when trying out UDP connections and how the server should respond
You should probably use traffic_generator_1.py for actual testing
This has the same functionality as https://github.com/jstrother123/team15_spring2023/blob/main/python_trafficgenarator.py

by Alex Prosser
10/9/2023
"""

import socket
import random
import time
import udp_test_common as common

# Constants
NUM_EVENTS = 10

players = common.read_players(common.PLAYER_FILENAME)

print('~~~~~ UDP Traffic Generator ver. 0 ~~~~~')
print('This program will generate some test traffic from the simple_database.txt and')
print('will include hits from both sides as well as base scoring\n')

print('Starting in 5 seconds...')
time.sleep(5)
print('Started!')

# Create datagram socket
socket_receive = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# counter number of events, random player and order
for _ in range(NUM_EVENTS):
	# Randomly choose a red and green player and an action to happen
	red = random.choice(list(filter(lambda p: p[2], players)))
	green = random.choice(list(filter(lambda p: not p[2], players)))
	select = random.randint(1, 4)

	if select == 1:
		message = str(red[1]) + ':' + str(green[1])
	elif select == 2:
		message = str(green[1]) + ':' + str(red[1])
	elif select == 3:
		message = str(green[1]) + ':' + str(common.UDP_RED_BASE_SCORED)
	else:
		message = str(red[1]) + ':' + str(common.UDP_GREEN_BASE_SCORED)

	# Send message to port 7501 and wait for next message
	print('Sent message: ' + message)
	socket_receive.sendto(str.encode(str(message)), (common.URL_LOCALHOST, common.PORT_SOCKET_RECEIVE))
	time.sleep(random.randint(1, 3))

# Clean up code and exit safely
print('UDP Test complete! Exiting now...')
socket_receive.close()
