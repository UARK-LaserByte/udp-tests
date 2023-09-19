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
# 9/19/2023

import socket
import time
import udp_test_common as common

# Constants
GAME_LENGTH = 60

# Read players from 'simple_database.txt' 
players = common.read_players(common.PLAYER_FILENAME)

# Create a UDP sockets
socketReceive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socketReceive.settimeout(1)

# Bind the receive socket to the right port
socketReceive.bind((common.URL_LOCALHOST, common.PORT_SOCKET_RECEIVE))

print('Starting UDP Server...')
print('Game starting in 5 seconds...')
time.sleep(5)

# Start game
print('Game has started!')
game_running = True
start_time = time.time()
socketBroadcast.sendto(str.encode(str(common.UDP_GAME_START)), (common.URL_LOCALHOST, common.PORT_SOCKET_BROADCAST))

while game_running:
	try:
		# Receive any data that might have come in
		data, _ = socketReceive.recvfrom(common.SOCKET_BUFFER_SIZE)
		id_transmit, id_hit = map(lambda id: int(id), data.decode().split(':'))
		hitter = common.get_player_by_id(players, id_transmit)
		hittee = common.get_player_by_id(players, id_hit)

        # Check if a green player has scored on red base
		if id_hit == common.UDP_RED_BASE_SCORED and not hitter[2]:
			print('The green player ' + hitter[0] + ' has scored on Red Base!')
		# Check if a red player has scored on green base
		elif id_hit == common.UDP_GREEN_BASE_SCORED and hitter[2]:
			print('The red player ' + hitter[0] + ' has scored on Green Base!')
		# Normal tag
		else:
			print('The player ' + hitter[0] + ' has tagged the player ' + hittee[0] + '!')

		socketBroadcast.sendto(str.encode(str(id_hit)), (common.URL_LOCALHOST, common.PORT_SOCKET_BROADCAST))
	except socket.timeout:
		# No data has come in, try again
		pass

	# Check if the desired duration has passed
	elapsed_time = time.time() - start_time
	if elapsed_time >= GAME_LENGTH:
		game_running = False

# Game has ended
print('Game is over!')
for _ in range(3):
	socketBroadcast.sendto(str.encode(str(common.UDP_GAME_END)), (common.URL_LOCALHOST, common.PORT_SOCKET_BROADCAST))

# Close the sockets
socketReceive.close()
socketBroadcast.close()