# Uptime Monitoring Server and Client

This project consists of a server and client application to monitor uptime and keepalive signals using sockets in Python. The server logs incoming client connections and monitors keepalive messages, while the client sends periodic keepalive signals to the server.

## Features
- Real-time connection monitoring
- Server logs client connection and disconnection times
- Client attempts to reconnect automatically if disconnected
- Uses multi-threading for handling multiple clients
- Docker support for easy deployment

## Project Structure
```
.
├── server/
│   └── uptime_server.py
├── client/
│   └── uptime_client.py
├── dockerfile.server
├── dockerfile.client
└── docker-compose.yml
```

## Prerequisites
- Python 3.x
- Docker

## Setup

### Clone the repository
```
git clone https://github.com/yourusername/uptime-monitor.git
cd uptime-monitor
```

### Run using Docker
1. Build and start the containers:
```
docker-compose up --build
```
2. To stop the containers:
```
docker-compose down
```

### Run without Docker
#### Server:
```
python3 server/uptime_server.py
```
#### Client:
```
python3 client/uptime_client.py
```

## Configuration
You can configure the server and client through environment variables in the Docker Compose file or directly in the Python scripts.

### Environment Variables
| Variable          | Description                     | Default      |
|------------------|---------------------------------|--------------|
| SERVER_HOST       | Host IP address of the server    | 0.0.0.0      |
| SERVER_PORT       | Port on which the server listens | 5000         |
| KEEPALIVE_INTERVAL| Interval between keepalives      | 0.25 seconds |

## Logging
- Server logs are stored in `server_log.txt`.
- Client logs are stored in `client_log.txt`.

## Example Output
```
Server started on 0.0.0.0:5000
New connection from 192.168.1.5:60000
Client 192.168.1.5:60000 disconnected after 45.123 seconds
```

## License
This project is licensed under the MIT License.

