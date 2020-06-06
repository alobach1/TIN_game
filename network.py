import socket
import threading
from test1 import *
import struct
import pygame
import numpy as np
import random
import parsing
import crypt
import zlib 
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
        self.q = threading.Event() # game quit

        self.id = 0  # client id of connection
        self.gamerid = 0 # gamer id
        self.height = 600 
        self.weight = 600 # width
        self.points = 0 # max points
        # self.score = 0  # score of player
        self.winner = -1 # who wins in game
        self.key = 0
        self.quit = True
        self.num = 0
        
    def connect(self):
        try:
            self.tcp.connect(self.addr)
        except socket.error as l:
            str(l)
        return self.tcp.recv(2)


    def udp_checking(self,ide):
        print('Game id : {0}'.format(ide.decode()))
        crc = zlib.crc32(ide)
        crc = crc % (1<<32)
        packet = struct.pack('!2sI',ide,crc)
        while not self.e.isSet():
            self.udp.sendto(packet,self.addr)

    def tcp_thread(self):
        self.t3.start()
        s = True
        while True :
            if self.q.isSet():
                self.tcp.close()
                break
                        
            m = self.tcp.recv(6)
 
            if(len(m))==6: 
                m = (m[:-4])          
            if len(m) == 2:
                s, w = struct.unpack('1s1s',m)
            if len(m) == 0:
                if self.q.isSet():
                    self.tcp.close()
                    break

            if (s.decode('ascii')=="S"):
                #print(len(m))
                self.points = int.from_bytes(w,byteorder='big')
                self.e.set()

            elif (s.decode('ascii')=="E"):
                # napisz id zwyciezcy 
                self.winner = int.from_bytes(w, byteorder = 'big') 
                print(self.winner)
                
                
                print("[Game reset]")
            else:              
                print("[ERROR]")
        

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
        score = pygame.font.SysFont("comicsans", 25, True)
        projectiles = pygame.sprite.Group()
        players = pygame.sprite.Group()

        for i in range(8):
            players.add(Player(i,-20,-20,0,self.rand_color()))
        for i in range(16):
            projectiles.add(Projectile(i,-20,-20))


        clock = pygame.time.Clock()
        dt = 0
        s = True

        while s: 
            
            for i in players:
                if hasattr(i,'x'):
                    #print("X: {0} Y: {1}".format(str(i.x),str(i.y)))
                    self.udp.sendto(i.get_packet(),self.addr)
                    break
                  
            data, _ = self.udp.recvfrom(64)
            
            w, number_player, number_pr = parsing.unpackeging(len(data),data)  # parsing 
            
            # writting received params for players and projectiles
            self.num = number_player
            i = 0
            for sp in players:
                if number_player == 0:
                    i = i + 2
                    break
                else:
                    sp.id = parsing.b_int(w[i+2])
                    sp.score = parsing.b_int(w[i+3])
                    sp.render()
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
                    self.udp.close()
                    self.q.set()
                    s = False
                    print("Closing ...")     
                    return
                    

            if s:
                # update plyers and projectiles
                for p in players:
                    p.update(events, dt)
                for p in projectiles:
                    p.update(events,dt)
            
                # draw players
                screen.fill((30, 30, 30))

                players.draw(screen)
                projectiles.draw(screen)

                # draw winner
                text = score.render(str(self.winner) + "  wins", 1, (255,255,255), False)
                screen.blit(text, (self.weight - 110 , 10))

                # draw score
                y = 10
                i = self.num
                for s in players:
                    if i == 0:
                        break
                    screen.blit(s.text, (self.weight - 80 , y + 20))
                    y = y + 20
                    i = i -1

                pygame.display.update()
                
                
                dt = clock.tick(30)
                
   
        

    def tcp_sending(self):
        
        while True:
            data = b'[TCP CONNECTED TO SERVER]'
            if self.q.isSet():
                break
            self.tcp.send(data)
            