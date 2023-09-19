import socket
import random
import time

SOCKET_RECEIVE_PORT = 7501
LOCALHOST = '127.0.0.1'
BUFFER_SIZE = 1024

NUM_EVENTS = 10

red_players = []
green_players = []

# read in simple_database.txt
with open('simple_database.txt') as file:
	is_red = True
	for line in file:
		if line.strip() == 'red':
			is_red = True
		elif line.strip() == 'green':
			is_red = False
		elif line.strip() != '':
			name, id = line.strip().split(',')
			if is_red:
				red_players.append((name, int(id)))
			else:
				green_players.append((name, int(id)))

print('~~~~~ UDP Traffic Generator ver. 0 ~~~~~')
print('This program will generate some test traffic from the simple_database.txt and')
print('will include hits from both sides as well as base scoring\n')

print('Starting in 5 seconds...')
time.sleep(5)

print('Started!')

# Create datagram socket
socketTransmit = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# counter number of events, random player and order
for _ in range(NUM_EVENTS):
	red = random.choice(red_players)
	green = random.choice(green_players)
	select = random.randint(1, 4)
	if select == 1:
		message = str(red[1]) + ":" + str(green[1])
	elif select == 2:
		message = str(green[1]) + ":" + str(red[1])
	elif select == 3:
		message = "66:" + str(green[1])
	else:
		message = "148:" + str(red[1])

	print(message)
	socketTransmit.sendto(str.encode(str(message)), (LOCALHOST, SOCKET_RECEIVE_PORT))
	time.sleep(random.randint(1, 3))

print('UDP Test complete! Exiting now...')
socketTransmit.close()