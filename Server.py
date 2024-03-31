class Server:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port

    def __repr__(self):
        return f'server on {self.ip} port {self.port}'
