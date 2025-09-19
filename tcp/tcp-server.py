import socket
import threading
import argparse

# ---------------------------
# Command-line argument parsing
# ---------------------------
parser = argparse.ArgumentParser(description="TCP server")  # Description shown in --help
parser.add_argument('-H','--host', default='127.0.0.1', help="Server host (default: localhost)")
parser.add_argument('-p','--port', type=int, required=True, help="Server port to bind")
args = parser.parse_args()

# Store host and port from parsed arguments
host = args.host
port = args.port

# ---------------------------
# Create and start server
# ---------------------------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket (IPv4)
server.bind((host, port))  # Bind server to the specified host and port
server.listen(5)  # Listen for incoming connections (backlog of 5)
print(f"Listening on {host}:{port}")

# ---------------------------
# Function to handle each client connection
# ---------------------------
def handle_client(client):
    """
    Handles messages from a single client.
    Receives data, prints it, and allows interactive replies.
    """
    while True:
        try:
            # Receive message from client (max 1024 bytes)
            message = client.recv(1024).decode('utf-8')

            # If no message, client disconnected
            if not message:
                break

            # Print received message
            print(f"Message received: {message}")

            # Prompt server user for reply
            reply = str(input("Message to reply: "))

            # Send reply back to client (encode string to bytes)
            client.send(reply.encode('utf-8'))

        # Handle client disconnect or abrupt connection close
        except ConnectionResetError:
            print("\nConnection closed")
            client.close()

# ---------------------------
# Main server loop to accept connections
# ---------------------------
try:
    while True:
        # Accept new client connection
        client, address = server.accept()
        print(f"Connection created with {address[0]}:{address[1]}")

        # Start a new thread to handle the client
        handler = threading.Thread(target=handle_client, args=(client,))
        handler.start()

# Graceful shutdown on Ctrl+C
except KeyboardInterrupt:
    print("\nServer shutting down....")

# Ensure server socket is closed when exiting
finally:
    server.close()
