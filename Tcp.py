import socket
import threading
from Server import Server
from ClientConnection import ClientConnection

class Tcp(Server):
    def __init__(self,ip,port):
        super().__init__(ip,port)
        self.lock = threading.Lock()
        self.connections=4
        self.clients=[]
        self.tcp_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print(f'\t\t{self}')
        self.tcp_server.bind((self.ip,self.port))

    def handle_client(self,client):
        client.send_data('Nickname:')
        client.receive(self)
    
    def send_to_all_clients(self, data):
        for client in self.clients:
            client.send_data(data)
    
    def send_to_all_clients_except(self, data, sender_address):
        for client in self.clients:
            if client.address != sender_address:
                client.send_data(data)
        
    def add_client(self, client):
        with self.lock:
            self.clients.append(client)

    def remove_client(self, client):
        with self.lock:
            if client in self.clients:
                self.clients.remove(client)
                client.close()
                print(f"Client {client.address} disconnected.")    

    def get_connections(self):
        self.tcp_server.listen(self.connections)
        print(f'\n\tlistenig for {self.connections} connection today' )
        while True:
            self.client_connection,self.client_ip=self.tcp_server.accept()
            print(f'got connection from {self.client_ip}')
            client=ClientConnection(self.client_ip,self.client_connection)
            self.add_client(client)
            client_thread=threading.Thread(target=self.handle_client,args=(client,))
            client_thread.start()
            


    def close_connection(self):
        self.tcp_server.close()
