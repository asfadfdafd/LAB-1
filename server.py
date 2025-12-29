import socket
import json
import time
from datetime import datetime
import threading

class RPCServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        
    def handle_request(self, data):
        """Обработка RPC запроса"""
        try:
            request = json.loads(data)
            method = request.get('method', '')
            params = request.get('params', {})
            
            if method == 'add':
                result = params.get('a', 0) + params.get('b', 0)
            elif method == 'get_time':
                result = datetime.now().isoformat()
            elif method == 'reverse':
                result = params.get('s', '')[::-1]
            elif method == 'multiply':
                result = params.get('a', 0) * params.get('b', 0)
            else:
                result = f"Unknown method: {method}"
            
            response = {
                'request_id': request.get('request_id', 'unknown'),
                'result': result,
                'status': 'OK',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            response = {
                'request_id': request.get('request_id', 'unknown'),
                'error': str(e),
                'status': 'ERROR'
            }
        
        return json.dumps(response)
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        
        print(f"RPC Server started on {self.host}:{self.port}")
        print("Waiting for connections...")
        
        while True:
            client, addr = server.accept()
            print(f" Connection from {addr[0]}:{addr[1]}")
            
            try:
                data = client.recv(1024).decode('utf-8')
                if data:
                    print(f"Received: {data[:100]}...")
                    response = self.handle_request(data)
                    print(f" Sending: {response}")
                    client.send(response.encode('utf-8'))
            except Exception as e:
                print(f" Error: {e}")
            finally:
                client.close()

if __name__ == "__main__":

    
    server = RPCServer('0.0.0.0', 5000)
    server.start()
