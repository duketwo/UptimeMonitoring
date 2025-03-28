import socket
import time
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    filename="client_log.txt",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class UptimeClient:
    def __init__(self, server_host, server_port, keepalive_interval=0.25):
        self.server_host = server_host
        self.server_port = server_port
        self.keepalive_interval = keepalive_interval
        self.socket = None
        self.connected = False
        self.connection_time = None
        self.reconnect_delay = 1  # Constant 1-second reconnect delay

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.connected = True
            self.connection_time = datetime.now()
            
            # Log successful connection
            logging.info(
                f"Connected to server at {self.server_host}:{self.server_port}"
            )
            print(
                f"Connected to server at {self.server_host}:{self.server_port}"
            )
            return True
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            print(f"Connection failed: {e}")
            return False

    def send_keepalive(self):
        if not self.connected:
            return False
        
        try:
            self.socket.send(b"KEEPALIVE")
            response = self.socket.recv(1024)
            
            if response != b"OK":
                logging.error(f"Unexpected response: {response}")
                self.disconnect("Unexpected server response")
                return False
            
            return True
        except Exception as e:
            self.disconnect(f"Keepalive failed: {e}")
            return False

    def disconnect(self, reason="Client disconnected"):
        if self.connected:
            self.connected = False
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
            
            # Calculate connection duration
            if self.connection_time:
                duration = (datetime.now() - self.connection_time).total_seconds()
                logging.info(
                    f"Disconnected from server after {duration:.3f} seconds. Reason: {reason}"
                )
                print(
                    f"Disconnected from server after {duration:.3f} seconds. Reason: {reason}"
                )

    def run(self):
        while True:
            if not self.connected:
                if not self.connect():
                    # Always wait exactly 1 second before trying to reconnect
                    logging.info(f"Will attempt to reconnect in {self.reconnect_delay} second")
                    time.sleep(self.reconnect_delay)
                    continue
            
            # Send keepalive
            if not self.send_keepalive():
                # Wait exactly 1 second before reconnecting
                time.sleep(self.reconnect_delay)
                continue
            
            # Wait for next keepalive interval
            time.sleep(self.keepalive_interval)


if __name__ == "__main__":
    server_host = os.environ.get("SERVER_HOST", "localhost")
    server_port = int(os.environ.get("SERVER_PORT", 5000))
    keepalive_interval = float(os.environ.get("KEEPALIVE_INTERVAL", 0.25))
    
    client = UptimeClient(server_host, server_port, keepalive_interval)
    
    try:
        client.run()
    except KeyboardInterrupt:
        client.disconnect("User interrupted")
    except Exception as e:
        logging.error(f"Client error: {e}")
        client.disconnect(f"Error: {e}")
