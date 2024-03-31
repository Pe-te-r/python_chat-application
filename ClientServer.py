import socket
import select
import threading

class ClientServer:

    '''Please enter a Doc String...'''
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print("Connected to server.")
            self.connected = True
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
        except ConnectionRefusedError:
            print("Connection refused. Server may be unavailable.")

    def receive_messages(self):
        while self.connected:
            try:
                ready = select.select([self.socket], [], [], 1)  # Timeout set to 1 second
                if ready[0]:
                    data = self.socket.recv(1024).decode()
                    if data == 'exit':
                        print('done')
                        self.socket.close()
                    if not data:
                        print("no data")
                        break
                    print(data)
            except ConnectionError:
                print("Connection with server closed unexpectedly.")
                self.connected = False
                break

    def send_message(self, message):
        if self.connected:
            try:
                self.socket.sendall(message.encode())
                # print("Message sent to server.")
            except ConnectionError:
                print("Failed to send message. Connection lost.")
                self.connected = False

    def disconnect(self):
        if self.connected:
            self.socket.close()
            print("Disconnected from server.")
            self.connected = False

if __name__ == "__main__":
    host = '192.168.88.232'
    port = 5000
    client = ClientServer(host, port)
    client.connect()

    print("(type 'exit' to disconnect): ")
    try:
        while client.connected:
            print()
            message=input()
            if message.lower() == 'exit':
                client.send_message('exit')
                # client.disconnect()
            else:
                if len(message.strip())<1:
                    continue
                client.send_message(message)
    except:
        client.disconnect()
