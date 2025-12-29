import socket
import json
import time
import uuid
from datetime import datetime

class RPCClient:
    def __init__(self, server_host, server_port=5000):
        self.server_host = '172.31.9.14'
        self.server_port = server_port
        self.timeout = 2  # секунды
        self.max_retries = 3
    
    def call(self, method, params=None):
        """Вызов удаленного метода с повторными попытками"""
        if params is None:
            params = {}
        
        request_id = str(uuid.uuid4())[:8]
        request = {
            'request_id': request_id,
            'method': method,
            'params': params,
            'client_timestamp': datetime.now().isoformat()
        }
        
        print(f"\n{'='*50}")
        print(f" Calling: {method} with params: {params}")
        print(f" Target: {self.server_host}:{self.server_port}")
        print(f" Request ID: {request_id}")
        
        for attempt in range(1, self.max_retries + 1):
            print(f"\n Attempt {attempt}/{self.max_retries}")
            
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                
                start_time = time.time()
                sock.connect((self.server_host, self.server_port))
                
                sock.send(json.dumps(request).encode('utf-8'))
                
                response_data = sock.recv(1024).decode('utf-8')
                end_time = time.time()
                
                response = json.loads(response_data)
                
                print(f"Success! Response time: {(end_time - start_time):.2f}s")
                print(f" Response: {response}")
                
                sock.close()
                return response
                
            except socket.timeout:
                print(f" Timeout! No response after {self.timeout} seconds")
            except ConnectionRefusedError:
                print(f" Connection refused! Server may be down")
            except Exception as e:
                print(f" Error: {e}")
            
            if attempt < self.max_retries:
                print(f" Waiting 1 second before retry...")
                time.sleep(1)
        
        print(f"\n All {self.max_retries} attempts failed!")
        return None
    
    def test_connection(self):
        """Тестирование соединения с сервером"""
        print(f"\n Testing connection to {self.server_host}:{self.server_port}")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.server_host, self.server_port))
            sock.close()
            print("connection successful!")
            return True
        except Exception as e:
            print(f" Connection failed: {e}")
            return False

if __name__ == "__main__":
    SERVER_IP = '172.31.9.14'  
    
    client = RPCClient(SERVER_IP, 5000)
    
    # Тест соединения
    if not client.test_connection():
        print("\nCannot proceed without server connection")
        print("Please check:")
        print("1. Server is running (python3 server.py)")
        print("2. Security Group allows port 5000")
        print("3. Correct IP address")
        exit(1)
    
    # Тестовые вызовы
    print("\n" + "="*60)
    print("Starting RPC Tests")
    print("="*60)
    
    # 1. Получение времени с сервера
    print("\n1. Getting server time:")
    client.call('get_time')
    
    # 2. Сложение
    print("\n2. Adding numbers 15 + 25:")
    client.call('add', {'a': 15, 'b': 25})
    
    # 3. Умножение
    print("\n3. Multiplying 6 * 7:")
    client.call('multiply', {'a': 6, 'b': 7})
    
    # 4. Реверс строки
    print("\n4.  Reversing string 'Distributed Computing':")
    client.call('reverse', {'s': 'Distributed Computing'})
    
    print("\n" + "="*60)
    print(" All tests completed!")
    print("="*60)
