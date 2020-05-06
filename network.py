import socket
import threading
import game

class Network:
    def __init__(self,port):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.port = port
        self.host = socket.gethostbyname(socket.gethostname())
        self.addr = (self.host, self.port)
        self.t1 = threading.Thread(target=self.tcp_thread)
        self.arg = b'0'
        self.t2 = threading.Thread(target=self.udp_thread)
        self.t3 = threading.Thread(target = self.tcp_sending)
        self.e = threading.Event()
        self.l = threading.Event()


    def connect(self):
        try:
            self.tcp.connect(self.addr)
        except socket.error as l:
            str(l)
        return self.tcp.recv(6).decode()

    def set_arg(self, arg):
        self.arg = arg

    def udp_checking(self,id):
        print('Game id : {0}'.format(id))
        while not self.e.isSet():
            self.udp.sendto(id,self.addr)

    def tcp_thread(self):
        self.t3.start()
        while True:
            m = self.tcp.recv(5).decode()
            if str(m)=="start":
                self.e.set()
            elif (str(m)=="stop"):
                self.l.set()
                print("[Game stop]")
                self.tcp.close()
                break
            else:
                print("[ERROR]")
    
    def udp_thread(self):
        print("[GAME STARTED]")
        print("[STARTED UDP]")
        gam = game.Player() 
        while not self.l.isSet():
            
            self.arg = gam.get_state()
            self.udp.sendto(str(self.arg).encode(),self.addr)
            print('Sending state {0} ...'.format(str(self.arg)))
            data, _ = self.udp.recvfrom(4096)
            print('Receiving state {0}'.format(str(data)))
            self.arg = gam.set_state(int(data))
            
        self.udp.close()

    def tcp_sending(self):
        while True:
            data = b'[TCP CONNECTED TO SERVER]'
            self.tcp.send(data)
            if self.l.isSet():
                break