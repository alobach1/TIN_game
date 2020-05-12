import socket
import threading
from test1 import *
import struct
import pygame

class Network:
    def __init__(self,port):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.port = port
        self.host = socket.gethostbyname(socket.gethostname())
        self.addr = (self.host, self.port)
        self.t1 = threading.Thread(target=self.tcp_thread)
        self.t2 = threading.Thread(target=self.udp_thread)
        self.t3 = threading.Thread(target = self.tcp_sending)
        self.e = threading.Event()
        self.l = threading.Event()

        self.id = 0
        self.height = 0 
        self.weight = 0


    def connect(self):
        try:
            self.tcp.connect(self.addr)
        except socket.error as l:
            str(l)
        return self.tcp.recv(2)

    def set_arg(self, arg):
        self.arg = arg

    def udp_checking(self,id):
        i = id.decode('utf-8')
        print('Game id : {0}'.format(i))
        print(i[1])
        self.id = i[1]
        while not self.e.isSet():
            self.udp.sendto(i.encode('ascii'),self.addr)

    def tcp_thread(self):
        self.t3.start()
        while True:
            m = self.tcp.recv(5)
            s,d,y = struct.unpack('1s2s2s',m)
            
            #print(s.decode('ascii'))
            #print(d.decode('ascii'))
            if (s.decode('ascii')=="S"):
                self.height = int.from_bytes(d, byteorder='big')
                self.height = self.height /100
                self.weight = int.from_bytes(y, byteorder='big')
                self.weight = self.weight/100
               
                self.e.set()
            elif (str(s)=="E"):
                self.l.set()
                print("[Game stop]")
                self.tcp.close()
                break
            else:
                print(str(d))
                print("[ERROR]")
    

    def unpackeging(self,len,data):
        if(len==8):
            s = struct.Struct('1s 2s 1s  2s 2s')
            d ,nr ,i, x, y = s.unpack(data)
            i = int.from_bytes(i, byteorder='big')
            nr = int.from_bytes(nr, byteorder='big')
            x =int.from_bytes(x, byteorder='big')
            y = int.from_bytes(y, byteorder='big')
           
            return (d,nr,i,x,y)
        if(len==13):
            s = struct.Struct('1s 2s 1s 2s 2s 1s 2s 2s')
            d ,nr ,i, x, y , i1 ,x1,y1= s.unpack(data)
            i = int.from_bytes(i, byteorder='big')
            nr = int.from_bytes(nr, byteorder='big')
            x =int.from_bytes(x, byteorder='big')
            y = int.from_bytes(y, byteorder='big')
            i1 = int.from_bytes(i1, byteorder='big')
            x1 =int.from_bytes(x1, byteorder='big')
            y1 = int.from_bytes(y1, byteorder='big')
           
            return (d,nr,i,x,y,i1,x1,y1)
        else:
            s = struct.Struct('1s 2s 1s  2s 2s 1s 2s 2s 1s 2s 2s')
            d ,nr ,i, x, y, i1, x1,y1, i2,x2,y2 = s.unpack(data)
            i = int.from_bytes(i, byteorder='big')
            nr = int.from_bytes(nr, byteorder='big')
            x =int.from_bytes(x, byteorder='big')
            y = int.from_bytes(y, byteorder='big')
            i1 = int.from_bytes(i1, byteorder='big')
            x1 =int.from_bytes(x1, byteorder='big')
            y1 = int.from_bytes(y1, byteorder='big')
            i2 = int.from_bytes(i2, byteorder='big')
            x2 =int.from_bytes(x2, byteorder='big')
            y2 = int.from_bytes(y2, byteorder='big')
            
            return (d,nr,i,x,y,i1,x1,y1,i2,x2,y2)
        return
        
        


    def udp_thread(self):
        print("[GAME STARTED]")
        print("[STARTED UDP]")
        pygame.init()
        screen = pygame.display.set_mode((int(self.weight), int(self.weight)))
        sprites = pygame.sprite.Group(Player(0,0,0,'dodgerblue'))
        sprites1 = pygame.sprite.Group(Player(1,0,0,'yellow'))
        sprites2 = pygame.sprite.Group(Player(2,0,0,'green'))
        
        clock = pygame.time.Clock()
        dt = 0
        while not self.l.isSet():
            clock.tick(30)
        
            for i in sprites:
                if hasattr(i, 'x'):
                    print("X: {0} Y: {1}".format(str(i.x),str(i.y)))
                   
                    self.udp.sendto(i.get_packet(),self.addr)
                    
                else:
                    continue
                
            
            data, _ = self.udp.recvfrom(64)
            
            w = self.unpackeging(len(data),data)

            if len(data)>8:
                for sp in sprites1:
                    if hasattr(sp, 'x'):
                        sp.x = (w[6]/100)
                        sp.y = (w[7]/100)
                        sp.id = (w[5])
 
                    else:
                        continue


            if len(data) > 13:
                for sp in sprites2:
                    if hasattr(sp, 'x'):
                        sp.x = (w[9]/100)
                        sp.y = (w[10]/100)
                        sp.id = (w[8])

                    else:
                        continue


            for sp in sprites:
                if hasattr(sp, 'x'):
                    sp.x = (w[3]/100)
                    sp.y = (w[4]/100)
                    sp.id = (w[2])
                    
                    sp.drawing
                else:
                    continue

            
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    return 


            sprites.update(events, dt)
            sprites1.update(events, dt)
            sprites2.update(events, dt)

            screen.fill((30, 30, 30))
            sprites.draw(screen)
            sprites1.draw(screen)
            sprites2.draw(screen)

            pygame.display.update()
            
            
            
        
        self.udp.close()

    def tcp_sending(self):
        while True:
            data = b'[TCP CONNECTED TO SERVER]'
            self.tcp.send(data)
            if self.l.isSet():
                break