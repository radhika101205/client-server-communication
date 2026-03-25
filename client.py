import socket
import threading
import os

# Configuration (Must match the server)
HOST = '127.0.0.1'  # The server's IP address
PORT = 65432        # The server's Port

def receive_messages(client_socket):
    """Handles receiving messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            # Check for termination commands or lost connection
            if not message or message.lower() in ['exit', 'quit']:
                print("\n[Server has disconnected. Press Enter to exit.]")
                client_socket.close()
                os._exit(0)
            
            # Print the received message
            print(f"\nServer: {message}")
        except ConnectionResetError:
            print("\n[Connection closed by server.]")
            os._exit(0)
        except Exception as e:
            print(f"\n[An error occurred: {e}]")
            os._exit(1)

def start_client():
    # 1. Create the socket (IPv4, TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 2. Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
    except ConnectionRefusedError:
        print("[Error: Server is not running or unreachable.]")
        return

    # Start a background thread to listen for incoming messages
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    recv_thread.daemon = True
    recv_thread.start()
    
    # Main thread handles sending messages
    while True:
        try:
            message = input()
            if message.lower() in ['exit', 'quit']:
                client_socket.send(message.encode('utf-8'))
                print("[Closing connection...]")
                break
            
            # Send the message to the server
            client_socket.send(message.encode('utf-8'))
        except EOFError:
            break

    # Clean up
    client_socket.close()
    os._exit(0)

if __name__ == "__main__":
    start_client()