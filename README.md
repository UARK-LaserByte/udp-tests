# Photon Laser System UDP tester

This repository tests the functionality of the UDP server that works with the laser tag system. It has an isolated server that sends and receives commands to check if the server works for the main application.

#### Created by Alex Prosser
##### Last updated: 10/9/2023

## How to run
To run `traffic_generator_0.py`, first start `server.py`, then start the test. It will send a number of events to the server without regards to the server timing (that means it can send before or after the game is over).

To run `traffic_generator_1.py`, start the test, then start `server.py`. The test will listen to the server to start and stop the game.

Files include:
- [server.py](https://github.com/UARK-LaserByte/udp-tests/blob/main/server.py)
```
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
```
- [traffic_generator_0.py](https://github.com/UARK-LaserByte/udp-tests/blob/main/traffic_generator_0.py)
```
The first test when trying out UDP connections and how the server should respond
You should probably use traffic_generator_1.py for actual testing
This has the same functionality as https://github.com/jstrother123/team15_spring2023/blob/main/python_trafficgenarator.py
```
- [traffic_generator_1.py](https://github.com/UARK-LaserByte/udp-tests/blob/main/traffic_generator_1.py)
```
This test works with the game start/end codes to have a full e2e test with the game
Prefer to use this over traffic_generator_0.py as it tests all UDP codes
```
- [udp_test_common.py](https://github.com/UARK-LaserByte/udp-tests/blob/main/udp_test_common.py)
```
Common methods and functions between the testing files
```
- [simple_database.txt](https://github.com/UARK-LaserByte/udp-tests/blob/main/simple_database.txt)
```
The simple database that runs with the testing files

The path is defined in udp_test_common.py under PLAYERS_FILENAME

The format for this "database" is:
   red
   name,id
   name,id
   name,id

   green
   name,id
   name,id
   name,id
```