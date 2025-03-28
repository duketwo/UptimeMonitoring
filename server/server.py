import socket
import threading
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="server_log.txt",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class UptimeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.clients = {}  # Dictionary to track connected clients

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        logging.info(f"Server started on {self.host}:{self.port}")
        print(f"Server started on {self.host}:{self.port}")
        
        try:
            while self.running:
                client_socket, address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            logging.error(f"Server error: {e}")
            print(f"Server error: {e}")
            self.stop()

    def handle_client(self, client_socket, address):
        client_id = f"{address[0]}:{address[1]}"
        self.clients[client_id] = client_socket
        
        # Log new connection
        connection_time = datetime.now()
        logging.info(f"New connection from {client_id}")
        
        try:
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # Simple protocol: client sends "KEEPALIVE", server responds "OK"
                if data.strip() == b"KEEPALIVE":
                    client_socket.send(b"OK")
                    # No logging for normal keepalives
        except Exception as e:
            # Log disconnection with error
            disconnect_time = datetime.now()
            duration = (disconnect_time - connection_time).total_seconds()
            logging.info(
                f"Connection lost from {client_id} after {duration:.3f} seconds. Error: {e}"
            )
        finally:
            # Clean up
            if client_id in self.clients:
                del self.clients[client_id]
            client_socket.close()
            
            # Log disconnection
            disconnect_time = datetime.now()
            duration = (disconnect_time - connection_time).total_seconds()
            logging.info(
                f"Client {client_id} disconnected after {duration:.3f} seconds"
            )

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        # Close all client connections
        for client_socket in self.clients.values():
            client_socket.close()
        
        logging.info("Server stopped")
        print("Server stopped")


if __name__ == "__main__":
    import os
    
    host = os.environ.get("SERVER_HOST", "0.0.0.0")
    port = int(os.environ.get("SERVER_PORT", 5000))
    
    server = UptimeServer(host, port)
    server.start()
