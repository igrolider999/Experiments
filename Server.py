import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 9999))
server.listen(1)

client, addr = server.accept()
print(f"\033[32mConnected to {addr}\n\n\033[37m")

while True:
    client.send(input("You: ").encode())  
    print(f"[Client]: {client.recv(1024).decode()}")
