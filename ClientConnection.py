class ClientConnection:
    def __init__(self,address,client_handle):
        self.address=address
        self.socket=client_handle
        self.nick_name=None
    
    def __repr__(self):
        return f'address {self.address} client handler {self.client_handle}'
    

    
    def receive(self,server):
        
        while True:
            try:
                data = self.socket.recv(1024).decode()

                if not data or data == 'exit':
                    break
                if self.nick_name == None:
                    self.nick_name=data
                    continue


                final=(f"\n{self.nick_name}: {data}\n")
                print(final)
                server.send_to_all_clients_except(final, self.address)
            except ConnectionError:
                print(f"Connection with {self.address} closed unexpectedly.")
                server.remove_client(self)
                break

            except Exception as e:
                print(f'error occured {e}')

    def send_alone(self,data):
        self.socket.sendall(data.encode())

    def send_data(self, data):
        self.socket.sendall(data.encode())

    def close(self):
        self.socket.close()

