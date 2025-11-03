import socket
import json
import threading

class NetworkManager:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.server_host = "localhost"
        self.server_port = 8889
        self.player_id = None
        self.on_players_ready = None
        self.on_game_start = None
        self.on_game_update = None
        self.on_shot_result = None
        self.on_ship_sunk = None
        self.on_enemy_ship_sunk = None
        self.on_game_over = None
        self.on_server_disconnect = None
        
    def connect_to_server(self, host=None, port=None):
        if host:
            self.server_host = host
        if port:
            self.server_port = port
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.connected = True
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            return True
        except Exception:
            self.connected = False
            return False
    
    def disconnect(self):
        if self.socket:
            self.connected = False
            self.socket.close()
            self.socket = None
    
    def send_message(self, message_type, data=None):
        if not self.connected:
            return False
            
        try:
            message = {
                'type': message_type,
                'player_id': self.player_id,
                'data': data
            }
            message_json = json.dumps(message) + '\n'
            self.socket.send(message_json.encode('utf-8'))
            return True
        except (ConnectionResetError, ConnectionAbortedError):
            self.connected = False
            if self.on_server_disconnect:
                self.on_server_disconnect()
            return False
        except Exception:
            return False
    
    def receive_messages(self):
        buffer = ""
        while self.connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if data:
                    buffer += data
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if line.strip():
                            try:
                                message = json.loads(line.strip())
                                self.handle_server_message(message)
                            except json.JSONDecodeError:
                                pass
                else:
                    break
            except (ConnectionResetError, ConnectionAbortedError):
                break
                break
            except Exception:
                break
        
        self.connected = False
        if self.on_server_disconnect:
            self.on_server_disconnect()
    
    def handle_server_message(self, message):
        message_type = message.get('type')
        data = message.get('data', {})
        
        if message_type == 'player_connect':
            self.player_id = data.get('player_id')
        
        elif message_type == 'players_ready':
            if self.on_players_ready:
                self.on_players_ready(data)
        
        elif message_type == 'game_start':
            if self.on_game_start:
                self.on_game_start(data)
        
        elif message_type == 'game_update':
            if self.on_game_update:
                self.on_game_update(data)
        
        elif message_type == 'shot_result':
            if self.on_shot_result:
                self.on_shot_result(data)
        
        elif message_type == 'ship_sunk':
            if self.on_ship_sunk:
                self.on_ship_sunk(data)
        
        elif message_type == 'enemy_ship_sunk':
            if self.on_enemy_ship_sunk:
                self.on_enemy_ship_sunk(data)
        
        elif message_type == 'game_over':
            if self.on_game_over:
                self.on_game_over(data)
        
        elif message_type == 'player_disconnect':
            if self.on_server_disconnect:
                self.on_server_disconnect()
        
        elif message_type == 'error':
            pass
    
    def place_ships(self, ship_positions):
        return self.send_message('place_ships', {'ships': ship_positions})
    
    def make_shot(self, x, y):
        return self.send_message('shot', {'x': x, 'y': y})
    
    def start_game(self):
        if not self.connected:
            return False
            
        return self.send_message('start_game', {})
    
    def set_players_ready_callback(self, callback):
        self.on_players_ready = callback
    
    def set_game_start_callback(self, callback):
        self.on_game_start = callback
    
    def set_game_update_callback(self, callback):
        self.on_game_update = callback
    
    def set_shot_result_callback(self, callback):
        self.on_shot_result = callback
    
    def set_ship_sunk_callback(self, callback):
        self.on_ship_sunk = callback
    
    def set_enemy_ship_sunk_callback(self, callback):
        self.on_enemy_ship_sunk = callback
    
    def set_game_over_callback(self, callback):
        self.on_game_over = callback
    
    def set_server_disconnect_callback(self, callback):
        self.on_server_disconnect = callback