"""
common.py

Common methods and functions between the testing files

by Alex Prosser
11/16/2023
"""


# Player model
class Player:
    def __init__(self, player_id: int, equipment_id: int, codename: str, team: str):
        self.player_id = player_id
        self.equipment_id = equipment_id
        self.codename = codename
        self.team = team


# UDP constants
UDP_GAME_START = 202
UDP_GAME_END = 221
UDP_RED_BASE_SCORED = 53
UDP_GREEN_BASE_SCORED = 43

# Other constants
PORT_SOCKET_BROADCAST = 7500
PORT_SOCKET_RECEIVE = 7501
URL_LOCALHOST = "127.0.0.1"
SOCKET_BUFFER_SIZE = 1024
PLAYER_FILENAME = "simple_database.txt"
RED_TEAM = "Red"
GREEN_TEAM = "Green"


def read_players(filename: str) -> list[Player]:
    """
    Reads all players from a database

    Args:
            filename: path to database

    Returns:
            list of players from database file
    """
    players = []
    with open(filename) as file:
        current_team = ""
        for line in file:
            if line.strip() == "red":
                current_team = RED_TEAM
            elif line.strip() == "green":
                current_team = GREEN_TEAM
            elif line.strip() != "":
                name, player_id, equipment_id = line.strip().split(",")
                players.append(
                    Player(int(player_id), int(equipment_id), name, current_team)
                )
    return players


def get_player_by_id(players: list[Player], id: int) -> Player | None:
    """
    Get a player from id number with players array

    Args:
            players: list of players from database
            id: id of needed player

    Returns:
            if player found, return player; else return None
    """
    for player in players:
        if player.equipment_id == id:
            return player

    return None
