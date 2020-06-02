import socket
import threading
from test1 import *
import struct
import pygame
import numpy as np
import random
import codecs
import parsing
import crypt
import zlib 
import crcmod
import binascii
import sys

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
        self.height = 600 
        self.weight = 600 # width
        self.points = 0 # max points
        self.score = 0  # score of player
        self.winner = 0 # who wins in game
        self.key = 0
        
    def connect(self):
        try:
            self.tcp.connect(self.addr)
        except socket.error as l:
            str(l)
        return self.tcp.recv(2)


    def udp_checking(self,ide):
        #ide = ide.decode()
        #print(type(ide))
        #i = struct.unpack('1s1s')
        #print('Game id : {0}'.format(i))
        #print(i[1])
        #self.id = i[1]
        #print(type(crc))
        #print(type(i[0]))
        #print(type(i[1]))
        #packet = bytearray(ide)
        s = struct.Struct('cc')
        p,l = s.unpack(ide)
        print(len(ide))
        print(p)
        print(l)
        crc = binascii.crc32(struct.pack('cc',p,l))
        crc = crc % (1<<32)
        print(sys.getsizeof(crc))
        #print(len(hex(crc)))
        #packet = ide.join(crc)
        #print(len(packet))
        #print(str(len(crc)))
        packet = struct.pack('ccI',p,l,crc)
        #struct.unpack('ccI', packet)
        print(sys.getsizeof(packet))
        while not self.e.isSet():
            self.udp.sendto(hex(crc),self.addr)

    def tcp_thread(self):
        self.t3.start()
        while not self.q.isSet():
            m = self.tcp.recv(2)
            print(m)            
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
                print("[ERROR]")
        self.tcp.close()


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
            players.add(Player(i,-20,-20,0,self.rand_color()))
        for i in range(8):
            projectiles.add(Projectile(i,-20,-20))


        clock = pygame.time.Clock()
        s = False
        dt = 0
        while not s:

        #while not self.l.isSet():
            # if someone wins , print winner and players are resetted 
            

            for i in players:
                if hasattr(i,'x'):
                    print("X: {0} Y: {1}".format(str(i.x),str(i.y)))
                    self.udp.sendto(i.get_packet(),self.addr)
                    break
                  
            data, _ = self.udp.recvfrom(64)
            
            w, number_player, number_pr = parsing.unpackeging(len(data),data)  # parsing 
            
            # writting received coordinates and player id from server
            # '1s 2s 1s 1s 2s 2s 1s '
            i = 0
            self.gamerid = parsing.b_int(w[2])
            self.score = parsing.b_int(w[3])

            for sp in players:
                if number_player == 0:
                    i = i + 2
                    break
                else:
                    sp.id = parsing.b_int(w[i+2])
                    sp.score = parsing.b_int(w[i+3])
                    sp.x = parsing.b_int(w[i+4])/100
                    sp.y = parsing.b_int(w[i+5])/100
                    number_player = number_player - 1
                    i= i + 4 # + 5
                  
            for pr in projectiles:
                if number_pr == 0:
                    break
                pr.x = parsing.b_int(w[i+1])/100
                pr.y = parsing.b_int(w[i+2])/100
                i = i + 2
                number_pr = number_pr -1
                
          
            # gets events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    s = True
                    return 

            # player.id = w[2] and projectile.id = w[2] -> event update
            for p in players:
                p.update(events, dt)
            for p in projectiles:
                p.update(events,dt)
        
            # draw players
            screen.fill((30, 30, 30))
            
            players.draw(screen)
            projectiles.draw(screen)

            text = score.render("Score : "+ str(self.score), 1, (255,255,255), True)
            screen.blit(text, (self.weight - 110 , 10))
            if self.l.isSet():
                text = font.render("Wins "+ str(self.winner), 1, (255,255,255), True)
                screen.blit(text, (self.weight/2 -100, self.height/2 - 50))
                i = 0
                for p in players:
                    p.id = i 
                    p.x = -20
                    p.y = -20
                    i = i + 1
            pygame.display.update()
            dt = clock.tick(30)
            
                
        self.q.set()           
        self.udp.close()

    def tcp_sending(self):
        while True:
            data = b'[TCP CONNECTED TO SERVER]'
            self.tcp.send(data)
            if self.q.isSet():
                break