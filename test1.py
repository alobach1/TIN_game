import pygame
import struct
import zlib 


class Player(pygame.sprite.Sprite):
    def __init__(self,id,x,y,angle,color):
        super().__init__()
        self.id = id
        self.points = 0
        self.size = 32  
        self.visible = False
        self.angle = angle
        self.x = x
        self.y = y
        self.color = (255,255,255)

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.polygon(self.image, color, ((0, 0), (self.size, self.size/2), (0, self.size)))
        self.org_image = self.image.copy()
        
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.pos = pygame.Vector2(self.rect.center)
        crc = self.coun_crc(struct.pack('cB',b'T',0))
        self.packet = struct.pack('cBI',b'T',0,crc)
        
    def coun_crc(self, t):
        crc = zlib.crc32(t)
        return crc

    def update(self, events, dt):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    crc = self.coun_crc(struct.pack('cB',b'Z',int(self.angle*255/360)))
                    self.packet = struct.pack('cBI',b'Z',int(self.angle*255/360),crc)
                    
            if e.type == pygame.KEYUP:
                crc = self.coun_crc(struct.pack('cB',b'T',0))
                self.packet = struct.pack('cBI',b'T',0,crc)


        pressed = pygame.key.get_pressed()  # :
        if pressed[pygame.K_w] and self.y > 0 :
            self.angle = 270
            crc = self.coun_crc(struct.pack('cB',b'T',1))
            self.packet = struct.pack('cBI',b'T',1,crc)
            
            if pressed[pygame.K_d]:
                self.angle = 315
                crc = self.coun_crc(struct.pack('cB',b'T',2))
                self.packet = struct.pack('cBI',b'T',2,crc)

            elif pressed[pygame.K_a]:
                self.angle = 225
                crc = self.coun_crc(struct.pack('cB',b'T',8))
                self.packet = struct.pack('cBI',b'T',8,crc)     
            


        if pressed[pygame.K_a] and self.x > 0 :
            self.angle = 180
            crc = self.coun_crc(struct.pack('cB',b'T',7))
            self.packet = struct.pack('cBI',b'T',7,crc)



        if pressed[pygame.K_d] and self.x < 600:
            self.angle = 0
            crc = self.coun_crc(struct.pack('cB',b'T',3))
            self.packet =struct.pack('cBI',b'T',3,crc)
        



        if pressed[pygame.K_s] and self.y < 600:
            self.angle = 90
            crc = self.coun_crc(struct.pack('cB',b'T',5))
            self.packet = struct.pack('cBI',b'T',5,crc)
            
            if pressed[pygame.K_d]:
                self.angle = 45
                crc = self.coun_crc(struct.pack('cB',b'T',4))
                self.packet = struct.pack('cBI',b'T',4,crc)

            elif pressed[pygame.K_a]:
                self.angle = 135
                crc = self.coun_crc(struct.pack('cB',b'T',6))
                self.packet = struct.pack('cBI',b'T',6,crc)

            

        if pressed[pygame.K_LEFT] and self.angle < 360:
            self.angle += 3
            crc = self.coun_crc(struct.pack('cB',b'T',0))
            self.packet = struct.pack('cBI',b'T',0,crc)
           
        
        if pressed[pygame.K_RIGHT] and self.angle > 0 :
            self.angle -= 3
            crc = self.coun_crc(struct.pack('cB',b'T',0))
            self.packet = struct.pack('cBI',b'T',0,crc)
         
        self.drawing()
        
            
    def drawing(self):
        self.image = pygame.transform.rotate(self.org_image, 360 - self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
   

    def get_packet(self):
        return self.packet



class Projectile(pygame.sprite.Sprite):
    def __init__(self, ident,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((8, 8))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, pygame.Color('orange'), (4, 4), 4)
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.id = ident
        
    def update(self, events, dt):
        self.rect.center = (self.x, self.y)


    def get_packet(self):
        packet = self.packet
        return packet
