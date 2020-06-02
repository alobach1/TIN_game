import socket
import threading
from test1 import *
import struct
import pygame
import numpy as np
import random
import codecs

class Network:
    def __init__(self,port):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.port = port
        self.host = socket.gethostbyname(socket.gethostname())  #  serwer ip address
        self.addr = (self.host, self.port)  # socket

        self.t1 = threading.Thread(target=self.tcp_thread) # tcp inicialization
        self.t2 = threading.Thread(target=self.udp_thread) # udp game
        self.t3 = threading.Thread(target = self.tcp_sending) # tcp connection  
        self.e = threading.Event() # udp checking event
        self.l = threading.Event() # game end event
        self.q = threading.Event() # game quit

        self.id = 0  # client id of connection
        self.gamerid = 0 # gamer id
        self.number_player = 0
        self.number_pr = 0
        self.height = 600 
        self.weight = 600 # width
        self.points = 0 # max points
        self.score = 0  # score of player
        self.winner = 0 # who wins in game
        self.velocity = 0 # projectile speed
        

    def connect(self):
        try:
            self.tcp.connect(self.addr)
        except socket.error as l:
            str(l)
        return self.tcp.recv(2)

    '''
    def set_arg(self, arg):
        self.arg = arg
    '''

    def udp_checking(self,id):
        i = id.decode('utf-8')
        print('Game id : {0}'.format(i))
        print(i[1])
        self.id = i[1]
        while not self.e.isSet():
            self.udp.sendto(i.encode('ascii'),self.addr)

    def tcp_thread(self):
        self.t3.start()
        while not self.q.isSet():
            m = self.tcp.recv(6)
            
            
            if len(m) == 2:
                s, w = struct.unpack('1s1s',m)

            print(len(m))
            #print(s.decode('ascii'))
            #print(d.decode('ascii'))

            if (s.decode('ascii')=="S"):
                print(len(m))
                self.points = int.from_bytes(w,byteorder='big')
                self.e.set()

            elif (s.decode('ascii')=="E"):
                # napisz id zwyciezcy 
                self.winner = int.from_bytes(w, byteorder = 'big') 
                self.l.set()
                # reset ?
                print("[Game reset]")

            else:
                # get gamer score
                #self.score = int.from_bytes(m, byteorder = 'big')
                
                print("[ERROR]")

    def unpack_pr(self, data):
        print(data)
        l = len(data)/4
        print(l)
        self.number_pr = int(l)
        o = ' 2s 2s'
        o = '1s'+ o*int(l)
        #print(o)
        return o

    def searching(self,data):
        start = 0
        n = []
        while True:
            start = data.find(b'\x00', start)
            if start == -1:
                break
            n.append(start)
            start += len(b'\x00')
        print(n)
        for i in n:
            if (i == 9) or (i == 15) or (i== 21) or (i ==27) or (i == 33) or (i == 39) or (i== 45) or (i == 51):
                o = self.unpack_pr(data[i+1:])
                l = i+1
        return data, l, o

    # parsing received udp message
    def unpackeging(self,l,data):
        strct = '1s 2s 1s 1s 2s 2s ' # +id + pointy
        s = '1s 1s 2s 2s' 
        o = '1s'
         # + direction for projectile
        print(data)
        data, l , o = self.searching(data)
        
        if(l==10):
            s = struct.Struct(strct+o)
            # d ,nr ,i, x, y = s.unpack(data)
            # i = int.from_bytes(i, byteorder='big')
            self.number_player = 1
            pack = s.unpack(data)
        if(l==16):
            self.number_player = 2
            s = struct.Struct(strct +s + o) #+o
            pack = s.unpack(data) 
        if(l == 22):
            self.number_player = 3
            s = struct.Struct(strct + (s)*2 + o) #+o
            pack = s.unpack(data)
        if (l == 28):
            self.number_player = 4
            s = struct.Struct(strct + (s)*3 + o) #+o
            pack = s.unpack(data)
        if (l == 34):
            self.number_player = 5
            s = struct.Struct(strct + (s)*4 + o) #+o
            pack = s.unpack(data)
        if (l == 40):
            self.number_player = 6
            s = struct.Struct(strct + (s)*5 + o) #+o
            pack = s.unpack(data)
        if (l == 46):
            self.number_player = 7
            s = struct.Struct(strct + (s)*6 + o) #+o
            pack = s.unpack(data)
        if (l == 52):
            self.number_player = 8
            s = struct.Struct(strct + (s)*7 + o) #+o
            pack = s.unpack(data)
        return pack

    # convert bytes to int    
    def b_int(self,i):
        i = int.from_bytes(i, byteorder='big')
        return i

    # generate random color
    def rand_color(self):
        r = random.randint(1,255)
        g = random.randint(1,255)
        b = random.randint(1,255)
        return (r,g,b)

    def udp_thread(self):
        print("[GAME STARTED]")
        print("[STARTED UDP]")
        pygame.init()
        screen = pygame.display.set_mode((int(self.weight), int(self.weight)))
        font = pygame.font.SysFont("comicsans", 80)
        score = pygame.font.SysFont("comicsans", 30, True)
        # visibility ?
        # szyfrowanie ?
        
        projectiles = pygame.sprite.Group()
        players = pygame.sprite.Group()
        for i in range(8):
            players.add(Player(i,0,0,self.rand_color()))
        for i in range(8):
            projectiles.add(Projectile(i,0,0))


        clock = pygame.time.Clock()
        
        dt = 0
        #while True:
        while not self.l.isSet():
            '''
            if self.l.isSet():
                text = font.render("Wins "+ str(self.winner), 1, (255,255,255), True)
                screen.blit(text, (self.weight/2 - 40, self.height/2 - 40))
                i = 0
                for p in players:
                    p.id = i
                    p.reset()
                    i = i + 1
                # reset Players?
            '''    
            # put some winner here
            # for reset: if self.winner not null -> font blit 
            for i in players:
                if hasattr(i,'x'):
                    print("X: {0} Y: {1}".format(str(i.x),str(i.y)))
                    self.udp.sendto(i.get_packet(),self.addr)
                    break
                  
            data, _ = self.udp.recvfrom(64)
            
            w = self.unpackeging(len(data),data)  # parsing 
            
            # writting received coordinates and player id from server
            # '1s 2s 1s 1s 2s 2s 1s '
            i = 0
            self.gamerid = self.b_int(w[2])
            #print(self.gamerid)
            self.score = self.b_int(w[3])
            #print(self.b_int(w[6]))
            for sp in players:
                
                if self.number_player == 0:
                    i = i + 2
                    break
                else:
                    sp.id = self.b_int(w[i+2])
                    sp.score = self.b_int(w[i+3])
                    sp.x = self.b_int(w[i+4])/100
                    sp.y = self.b_int(w[i+5])/100
                    self.number_player = self.number_player - 1
                    i= i + 4 # + 5
                   
                
            
            print(i)                    
            for pr in projectiles:
                try:
                    print(self.b_int(w[i+1]))
                    print(self.b_int(w[i+2]))
                    pr.x = self.b_int(w[i+1])/100
                    pr.y = self.b_int(w[i+2])/100
                    i = i + 2
                except IndexError:
                    break
          
            # gets events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.q.set()
                    self.udp.close()
                    self.tcp.close()
                    return 

            # player.id = w[2] and projectile.id = w[2] -> event update
            for p in players:
                p.update(events, dt)
            for p in projectiles:
                p.update(events,dt)
        
            # draw players
            screen.fill((30, 30, 30))

            # if player is connected -> draw player
            # waiting for players if len(data) == 43 -> waiting for players
            
            
            players.draw(screen)
            projectiles.draw(screen)

            text = score.render("Score : "+ str(self.score), 1, (255,255,255), True)
            screen.blit(text, (self.weight - 110 , 10))
            text = font.render("Wins "+ str(self.winner), 1, (255,255,255), True)
            screen.blit(text, (self.weight/2 -100, self.height/2 - 50))
            pygame.display.update()
            dt = clock.tick(30)
            
            
        
        self.udp.close()

    def tcp_sending(self):
        while True:
            data = b'[TCP CONNECTED TO SERVER]'
            self.tcp.send(data)
            if self.l.isSet():
                break