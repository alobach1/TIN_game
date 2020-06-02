import pygame
import struct

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,angle,color):
        super().__init__()
        self.id = 0
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
        
        #self.direction = pygame.Vector2(1, 0) 
        # self.direction = [1,0]# i guess i should make someting different
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.pos = pygame.Vector2(self.rect.center)
        self.packet = struct.pack('cB',b'T',0)
        


    def update(self, events, dt):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.packet = struct.pack('cB',b'Z',int(self.angle*255/360))
                    
                    
                    #self.projectile.append(Projectile(self.id, self.rect.center, self.packet ,self.direction))
            if e.type == pygame.KEYUP:
                self.packet = struct.pack('cB',b'T',0)


        pressed = pygame.key.get_pressed()  # :
        if pressed[pygame.K_w] and self.y > 0 :
            self.angle = 270
            #print(int(self.angle*255/360))
            self.packet = struct.pack('cB',b'T',1)
            '''
            if pressed[pygame.K_d]:
                self.angle = 45
                self.packet = struct.pack('cB',b'T',2)

            elif pressed[pygame.K_a]:
                self.angle = 135
                self.packet = struct.pack('cB',b'T',8)     
            '''


        if pressed[pygame.K_a] and self.x > 0 :
            self.angle = 180
            self.packet = struct.pack('cB',b'T',7)



        if pressed[pygame.K_d] and self.x < 600:
            self.angle = 0
            self.packet =struct.pack('cB',b'T',3)
        



        if pressed[pygame.K_s] and self.y < 600:
            self.angle = 90
            self.packet = struct.pack('cB',b'T',5)
            '''
            if pressed[pygame.K_d]:
                self.angle = 315
                self.packet = struct.pack('cB',b'T',4)

            elif pressed[pygame.K_a]:
                self.angle = 225
                self.packet = struct.pack('cB',b'T',6)

            '''

        if pressed[pygame.K_LEFT] and self.angle < 360:
            self.angle += 3
            self.packet = struct.pack('cB',b'T',0)
           
        
        if pressed[pygame.K_RIGHT] and self.angle > 0 :
            self.angle -= 3
            self.packet = struct.pack('cB',b'T',0)
         
        self.drawing()
        
            
    def drawing(self):
        # self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
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
        #self.direction = direction  # gets from server pos
        #self.packet = packet
        
    def update(self, events, dt):
          # without dt
        self.rect.center = (self.x, self.y)
        #if not pygame.display.get_surface().get_rect().contains(self.rect):
            #self.kill()

    def get_packet(self):
        packet = self.packet
        return packet
