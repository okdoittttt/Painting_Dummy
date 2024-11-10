import socket

# Setup socket to receive signal
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(('localhost', 12345))

print("Listening for red detection signal...")

while True:
    message, _ = receiver_socket.recvfrom(1024)
    print(message.decode())  # Display the received message with coordinates and distance
