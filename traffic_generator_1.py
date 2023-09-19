import socket
import random
import time

# UDP codes
GAME_START = 202
GAME_END = 221
RED_BASE_SCORED = 66
GREEN_BASE_SCORED = 148

SOCKET_BROADCAST_PORT = 7500
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

print('~~~~~ UDP Traffic Generator ver. 1 ~~~~~')
print('This program will generate some test traffic from the simple_database.txt and')
print('will include hits from both sides as well as base scoring\n')
print('Waiting for game start...')

# Create datagram socket
socketReceive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socketBroadcast.settimeout(1)
socketBroadcast.bind((LOCALHOST, SOCKET_BROADCAST_PORT))

game_started = False
game_over_count = 0

while True:
	try:
		data, _ = socketBroadcast.recvfrom(BUFFER_SIZE)
		
		if int(data.decode()) == GAME_START:
			print('Game started!')
			game_started = True
		elif int(data.decode()) == GAME_END:
			game_over_count += 1
			if game_over_count == 3:
				print('Game is over!')
				break
		else:
			print('Received message: ' + data.decode())
	except socket.timeout:
		pass

	if game_started:
		red = random.choice(red_players)
		green = random.choice(green_players)
		select = random.randint(1, 4)
		if select == 1:
			message = str(red[1]) + ':' + str(green[1])
		elif select == 2:
			message = str(green[1]) + ':' + str(red[1])
		elif select == 3:
			message = str(RED_BASE_SCORED) + ':' + str(green[1])
		else:
			message = str(GREEN_BASE_SCORED) + ':' + str(red[1])

		print('Sent message: ' + message)
		socketReceive.sendto(str.encode(str(message)),
								(LOCALHOST, SOCKET_RECEIVE_PORT))
		time.sleep(random.randint(3, 5))

print('UDP Test complete! Exiting now...')
socketReceive.close()
socketBroadcast.close()
