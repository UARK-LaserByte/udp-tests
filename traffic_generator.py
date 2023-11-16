"""
traffic_generator.py

A test for trying out a fixed amount of responses for UDP connections and how the server should respond
Use traffic_generator_e2e.py for actual testing as it tests all UDP codes
This has the same functionality as https://github.com/jstrother123/team15_spring2023/blob/main/python_trafficgenarator.py

by Alex Prosser
11/16/2023
"""

import socket
import random
import time
import common

# Constants
NUM_EVENTS = 10

players = common.read_players(common.PLAYER_FILENAME)

print("~~~~~ UDP Traffic Generator - Fixed Amount ~~~~~")
print("This program will generate some test traffic from the simple_database.txt and")
print("will include hits from both sides as well as base scoring\n")

print("Starting in 5 seconds...")
time.sleep(5)
print("Started!")

# Create datagram socket
socket_receive = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# counter number of events, random player and order
for _ in range(NUM_EVENTS):
    # Randomly choose a red and green player and an action to happen
    red = random.choice(list(filter(lambda p: p.team == common.RED_TEAM, players)))
    green = random.choice(list(filter(lambda p: p.team == common.GREEN_TEAM, players)))
    select = random.randint(1, 4)

    if select == 1:
        message = str(red.equipment_id) + ":" + str(green.equipment_id)
    elif select == 2:
        message = str(green.equipment_id) + ":" + str(red.equipment_id)
    elif select == 3:
        message = str(green.equipment_id) + ":" + str(common.UDP_RED_BASE_SCORED)
    else:
        message = str(red.equipment_id) + ":" + str(common.UDP_GREEN_BASE_SCORED)

    # Send message to port 7501 and wait for next message
    print("Sent message: " + message)
    socket_receive.sendto(
        str.encode(str(message)), (common.URL_LOCALHOST, common.PORT_SOCKET_RECEIVE)
    )
    time.sleep(random.randint(1, 3))

# Clean up code and exit safely
print("UDP Test complete! Exiting now...")
socket_receive.close()
