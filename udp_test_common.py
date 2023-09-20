"""
udp_test_common.py

Common methods and functions between the testing files

by Alex Prosser
9/20/2023
"""

# UDP constants
UDP_GAME_START = 202
UDP_GAME_END = 221
UDP_RED_BASE_SCORED = 66
UDP_GREEN_BASE_SCORED = 148

# Other constants
PORT_SOCKET_BROADCAST = 7500
PORT_SOCKET_RECEIVE = 7501
URL_LOCALHOST = '127.0.0.1'
SOCKET_BUFFER_SIZE = 1024
PLAYER_FILENAME = 'simple_database.txt'

# Type definitions
Player = tuple[str, int, bool]

def read_players(filename: str) -> list[Player]:
	"""Reads all players from a database

	Args:
		filename: path to database

	Returns:
		list of players from database file
	"""
	players = []
	with open(filename) as file:
		is_red = True
		for line in file:
			if line.strip() == 'red':
				is_red = True
			elif line.strip() == 'green':
				is_red = False
			elif line.strip() != '':
				name, id = line.strip().split(',')
				players.append((name, int(id), is_red))
	return players

def get_player_by_id(players: list[Player], id: int) -> Player | None:
	"""Get a player from id number with players array

	Args:
		players: list of players from database
		id: id of needed player

	Returns:
		if player found, return player; else return None
	"""
	for player in players:
		if player[1] == id:
			return player

	return None