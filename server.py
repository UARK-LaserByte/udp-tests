"""
server.py

This is a test server to see how we can implement the code necessary to run the laser system

Broadcast Socket Port: 7500
Receive Socket Port:   7501
Reserved UDP codes:
- Broadcasted
  - 202 ~ Game start
  - 221 (3x) ~ Game end
- Received
  - [id]:66 ~ Red base scored
  - [id]:148 ~ Green base scored

Chain of events:
- Player 0 tags Player 1
  - Player 0 shoots Player 1 which sends 0:1 to UDP port 7501
  - Server receives it and displays a message and awards Player 0 10 points
  - Server broadcasts 1 on UDP port 7500 to indicate to Player 1 that it was hit
- Player 0 on red team tags Green Base
  - Player 0 hits Green Base which sends 0:66 to UDP port 7501
  - Server receives it and displays a "B" next to Player 0 and awards 100 points
- Player 1 on green team tags Green Base
  - Player 1 hits Green Base which sends 1:66 to UDP port 7501
  - Server receives it and does nothing as green player can't tag green base

by Alex Prosser
9/20/2023
"""

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
		
		if hitter == None or hittee == None:
			print('Invalid message sent. Ignoring for now...')
		else:
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