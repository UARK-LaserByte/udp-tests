"""
src/tests/traffic_generator_e2e.py

This test works with the game start/end codes to have a full e2e test with the game
For fixed amounts, use traffic_generator.py

by Alex Prosser
10/22/2023
"""

import socket
import random
import time
import common

# read in players from simple_database.txt
players = common.read_players(common.PLAYER_FILENAME)

print('~~~~~ UDP Traffic Generator - End to End (E2E) ~~~~~')
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
		red = random.choice(list(filter(lambda p: p.team == common.RED_TEAM, players)))
		green = random.choice(list(filter(lambda p: p.team == 'Green', players)))
		select = random.randint(1, 4)

		if select == 1:
			message = str(red.equipment_id) + ':' + str(green.equipment_id)
		elif select == 2:
			message = str(green.equipment_id) + ':' + str(red.equipment_id)
		elif select == 3:
			message = str(green.equipment_id) + ':' + str(common.UDP_RED_BASE_SCORED)
		else:
			message = str(red.equipment_id) + ':' + str(common.UDP_GREEN_BASE_SCORED)

		# Send message to port 7501 and wait for next message
		print('Sent message: ' + message)
		socket_receive.sendto(str.encode(str(message)), (common.URL_LOCALHOST, common.PORT_SOCKET_RECEIVE))
		time.sleep(random.randint(1, 3))

print('UDP Test complete! Exiting now...')
socket_receive.close()
socket_broadcast.close()
