"""
traffic_generator_1.py

This test works with the game start/end codes to have a full e2e test with the game
Prefer to use this over traffic_generator_0.py as it tests all UDP codes

by Alex Prosser
10/9/2023
"""

import socket
import random
import time
import udp_test_common as common

# read in players from simple_database.txt
players = common.read_players(common.PLAYER_FILENAME)

print('~~~~~ UDP Traffic Generator ver. 1 ~~~~~')
print('This program will generate some test traffic from the simple_database.txt and')
print('will include hits from both sides as well as base scoring\n')
print('Waiting for game start...')

# Create datagram socket
socket_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socket_broadcast.settimeout(1)
socket_broadcast.bind((common.URL_LOCALHOST, common.PORT_SOCKET_BROADCAST))

game_started = False
game_over_count = 0

while True:
	try:
		data, _ = socket_broadcast.recvfrom(common.SOCKET_BUFFER_SIZE)
		
		if int(data.decode()) == common.UDP_GAME_START:
			print('Game started!')
			game_started = True
		elif int(data.decode()) == common.UDP_GAME_END:
			game_over_count += 1
			if game_over_count == 3:
				print('Game is over!')
				break
		else:
			print('Received message: ' + data.decode())
	except socket.timeout:
		pass

	if game_started:
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

print('UDP Test complete! Exiting now...')
socket_receive.close()
socket_broadcast.close()
