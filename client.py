import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

while True:
    print(f"[Server]: {client.recv(1024).decode()}")
    client.send(input("You: ").encode())
