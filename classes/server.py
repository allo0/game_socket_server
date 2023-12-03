# import json
# import socket
# from _thread import *
#
# from classes.Player import Player
#
# from configs import logConf
# from configs.appConf import Settings
#
# logger = logConf.logger
#
#
# class Server():
#     def __init__(self) -> None:
#         self.server_ip = Settings.SERVER_IP
#         self.port = Settings.SERVER_PORT
#         self.server_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.current_player = 0
#         self.connected_players = {}  # Dictionary to dynamically store connected players
#         self.player_instance = None
#         try:
#             self.server_init.bind((self.server_ip, self.port))
#         except socket.error as e:
#             logger.error(str(e))
#
#         self.server_init.listen()
#         logger.info("Server started... waiting patiently for connections")
#
#     def threaded_client(self, conn, player_index):
#         try:
#             reply = ""
#             previous_data = None
#             # initial_data = self.connected_players[player_index].get_player_data()
#             # conn.sendall(json.dumps(initial_data).encode('utf-8'))  # Send initial player data
#             # logger.info("Sent initial data to client")
#
#             while True:
#                 try:
#
#                     data = json.loads(conn.recv(2048).decode('utf-8'))
#                     logger.info(f"Received data from client: {data}")
#
#                     ##########
#                     if self.player_instance is None:
#                         # Receive the Player instance from the client
#                         self.player_instance = Player(id=data['id'], x=data['x'], y=data['y'], health=data['health'])
#
#                         self.connected_players[player_index] = self.player_instance
#
#                     # Send initial player data using JSON
#                     # initial_data_json = json.dumps(player_instance.get_player_data()).encode('utf-8')
#                     # conn.sendall(initial_data_json)
#                     ######
#
#                     self.connected_players[player_index].update_from_data(data)  # Update player state
#
#                     if not data:
#                         logger.info("Disconnected")
#                         break
#
#                     elif data != previous_data:
#                         # Update other player's position based on received data
#                         other_player = self.connected_players[player_index]
#                         reply = other_player.get_player_data()
#
#                         conn.sendall(json.dumps(reply).encode('utf-8'))
#                         logger.info("Sending reply to client: %s", reply)
#                         previous_data = data
#                         del data
#
#                 except Exception as e:
#                     logger.exception(f"Error in threaded_client: {e}")
#                     break
#         except Exception as e:
#             logger.exception(f"Connection Error: {e}")
#         finally:
#             conn.close()
#
#     def start_server(self):
#         while True:
#             conn, addr = self.server_init.accept()
#             logger.info(f"Connection from: {addr}")
#
#             player_index = self.current_player
#             try:
#                 # # Receive the Player instance from the client
#                 # initial_data = json.loads(conn.recv(2048).decode('utf-8'))
#                 # player_instance = Player(x=initial_data['x'], y=initial_data['y'])
#                 # logger.info(f"Received player data: {initial_data}")
#                 #
#                 # self.connected_players[player_index] = player_instance
#                 #
#                 # # Send initial player data using JSON
#                 # initial_data_json = json.dumps(player_instance.get_player_data()).encode('utf-8')
#                 # conn.sendall(initial_data_json)
#
#                 start_new_thread(self.threaded_client, (conn, 1))
#                 self.current_player += 1
#             except Exception as e:
#                 logger.exception(f"Error receiving or sending player data: {e}")
#                 conn.close()

import json
import socket
from _thread import *

from configs import logConf
from configs.appConf import Settings

logger = logConf.logger


class Server:
    def __init__(self) -> None:
        self.server_ip = Settings.SERVER_IP
        self.port = Settings.SERVER_PORT
        self.server_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_player = 0
        self.connected_players = {}  # Dictionary to dynamically store connected players

        try:
            self.server_init.bind((self.server_ip, self.port))
        except socket.error as e:
            logger.error(str(e))

        self.server_init.listen()
        logger.info("Server started... waiting patiently for connections")

    def threaded_client(self, conn, player_index):
        try:
            reply = ""
            previous_data = None

            while True:
                try:
                    data = json.loads(conn.recv(2048).decode('utf-8'))
                    logger.info(f"Received data from client: {data}")

                    self.connected_players[player_index] = (conn, data)  # Update player state

                    if not data:
                        logger.info(f"Client {data['id']} disconnected")
                        break

                    elif data != previous_data:
                        # Update other player's position based on received data
                        other_player = self.connected_players[player_index]
                        reply = other_player[1]  # Echo the data received from one client to others

                        # Send reply to all connected clients
                        for other_player_index, (other_conn, _) in self.connected_players.items():
                            # if other_player_index != player_index:
                            other_conn.sendall(json.dumps(reply).encode('utf-8'))

                        logger.info(f"Sending reply to all clients: {reply}")
                        previous_data = data
                        del data

                except Exception as e:
                    logger.exception(f"Error in threaded_client: {e}")
                    break
        except Exception as e:
            logger.exception(f"Connection Error: {e}")
        finally:
            conn.close()

    def start_server(self):
        while True:
            conn, addr = self.server_init.accept()
            logger.info(f"Connection from: {addr}")

            player_index = self.current_player
            try:
                start_new_thread(self.threaded_client, (conn, player_index))
                self.current_player += 1
            except Exception as e:
                logger.exception(f"Error receiving or sending player data: {e}")
                conn.close()
