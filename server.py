import socket
import threading
import os

# Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def receive_messages(conn):
    """Handles receiving messages from the client."""
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            # Check for termination commands or lost connection
            if not message or message.lower() in ['exit', 'quit']:
                print("\n[Client has disconnected. Press Enter to exit.]")
                conn.close()
                os._exit(0) # Exits the entire program cleanly
            
            # Print the received message
            print(f"\nClient: {message}")
        except ConnectionResetError:
            print("\n[Connection closed by client.]")
            os._exit(0)
        except Exception as e:
            print(f"\n[An error occurred: {e}]")
            os._exit(1)

def start_server():
    # 1. Create the socket (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow the port to be reused immediately after restart
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 2. Bind the socket to the IP and Port
    server_socket.bind((HOST, PORT))
    
    # 3. Listen for incoming connections
    server_socket.listen()
    print(f"Server is listening on {HOST}:{PORT}...")
    
    # 4. Accept a client connection
    conn, addr = server_socket.accept()
    print(f"Connected to client at {addr}")
    
    # Start a background thread to listen for incoming messages
    recv_thread = threading.Thread(target=receive_messages, args=(conn,))
    recv_thread.daemon = True
    recv_thread.start()
    
    # Main thread handles sending messages
    while True:
        try:
            message = input()
            if message.lower() in ['exit', 'quit']:
                conn.send(message.encode('utf-8'))
                print("[Closing connection...]")
                break
            
            # Send the message to the client
            conn.send(message.encode('utf-8'))
        except EOFError:
            break

    # Clean up
    conn.close()
    server_socket.close()
    os._exit(0)

if __name__ == "__main__":
    start_server()