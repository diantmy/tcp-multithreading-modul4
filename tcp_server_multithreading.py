import socket
import threading

# Simpan informasi klien dengan format: {client_socket: client_name}
clients = {}

def handle_client(client_socket, client_address):
    print(f"Client {client_address} connected.")
    
    # Terima nama klien saat terhubung
    client_name = client_socket.recv(1024).decode("utf-8")
    clients[client_socket] = client_name
    print(f"Client name: {client_name}")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"Received message from {client_name} ({client_address}): {message}")
            # Kirim pesan ke semua klien lain
            broadcast(f"{client_name}: {message}", client_socket)
        except ConnectionResetError:
            break
    
    print(f"Client {client_name} ({client_address}) disconnected.")
    client_socket.close()
    remove_client(client_socket)

def broadcast(message, current_client_socket):
    for client_socket in clients:
        if client_socket != current_client_socket:
            try:
                client_socket.send(message.encode("utf-8"))
            except:
                continue

def remove_client(client_socket):
    if client_socket in clients:
        del clients[client_socket]

def start_server(host="0.0.0.0", port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
