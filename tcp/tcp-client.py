import socket
import argparse

# ---------------------------
# Command-line argument parsing
# ---------------------------
parser = argparse.ArgumentParser(description="TCP client")  # Description shown in --help
parser.add_argument('-H','--host', default="127.0.0.1", help="Server host (default: localhost)")
parser.add_argument('-p','--port', type=int, required=True, help="Server port to connect to")
args = parser.parse_args()

# Store host and port from parsed arguments
host = args.host
port = args.port

# ---------------------------
# TCP client connection function
# ---------------------------
def connection(host, port):
    """
    Establish a TCP connection to the given host and port.
    Allows sending messages interactively and prints server replies.
    """
    # Create a TCP socket (IPv4)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to the server
    connection.connect((host, port))

    try:
        # Main interactive loop
        while True:
            # Prompt user for input message
            message = str(input("Enter message to send: "))

            # Send message to server (encode string to bytes)
            connection.send(message.encode('utf-8'))

            # Receive response from server (decode bytes to string)
            receive = (connection.recv(1024)).decode('utf-8')
            print(f"Reply: {receive}")

    # Handle case when server is not reachable
    except ConnectionRefusedError:
        print(f"Cannot connect to {host}:{port}. Is the server running?")

    # Handle user pressing Ctrl+C to exit
    except KeyboardInterrupt:
        print("\nConnection closed")
        connection.close()

# ---------------------------
# Run the client
# ---------------------------
connection(host, port)
