from Tcp import Tcp

def main():
    ip='192.168.88.232'
    tcp=Tcp(ip=ip,port=5000)
    try:
       tcp.get_connections()
    #    tcp.get_clients()
    except Exception as error:
        print(error)
    finally:
        tcp.close_connection()

if __name__=='__main__':
    main()
