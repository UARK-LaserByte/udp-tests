# server.py
#
# This is a test server to see how we can implement the code necessary to run the laser system
#
# Broadcast Socket Port: 7500
# Receive Socket Port:   7501
# Reserved Transmit IDs:
# - 202 (1x): Game start
# - 221 (3x): Game end
# - 66  (1x): Red base scored
# - 148 (1x): Green base scored
#
# Chain of events:
# - Player 0 shoots Player 1 which sends 0:1 to UDP port 7501
# - Server receives it and displays a message
# - Server broadcasts 1 on UDP port 7500 to indicate to Player 1 that it was hit
#
# by Alex Prosser
# 9/18/2023

import socket
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

GAME_LENGTH = 60

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

def get_player(id):
	for player in green_players:
		if player[1] == id:
			return player
		
	for player in red_players:
		if player[1] == id:
			return player
		
	return None

# Create a UDP sockets
socketReceive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socketReceive.settimeout(1)

# Bind the sockets to the right ports
socketReceive.bind((LOCALHOST, SOCKET_RECEIVE_PORT))

print('Starting UDP Server...')
print('Game starting in 5 seconds...')
time.sleep(5)

print('Game has started!')
game_running = True
start_time = time.time()
socketBroadcast.sendto(str.encode(str(GAME_START)),
					   (LOCALHOST, SOCKET_BROADCAST_PORT))

while game_running:
	try:
		data, _ = socketReceive.recvfrom(BUFFER_SIZE)
		id_transmit, id_hit = map(lambda id: int(id), data.decode().split(':'))
		hitter = get_player(id_transmit)
		hittee = get_player(id_hit)

		if id_transmit == RED_BASE_SCORED:
			print('The green player ' + hittee[0] + ' has scored on Red Base!')
		elif id_transmit == GREEN_BASE_SCORED:
			print('The red player ' + hittee[0] + ' has scored on Green Base!')
		else:
			print('The player ' + hitter[0] + ' has tagged the player ' + hittee[0] + '!')

		socketBroadcast.sendto(str.encode(str(id_hit)), (LOCALHOST, SOCKET_BROADCAST_PORT))
	except socket.timeout:
		pass

	# Check if the desired duration has passed
	elapsed_time = time.time() - start_time
	if elapsed_time >= GAME_LENGTH:
		game_running = False

# Game has ended
print('Game is over!')
for _ in range(3):
	socketBroadcast.sendto(str.encode(str(GAME_END)), (LOCALHOST, SOCKET_BROADCAST_PORT))

# Close the sockets
socketReceive.close()
socketBroadcast.close()
