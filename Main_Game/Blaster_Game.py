import pygame
#import time
from pygame.locals import *
pygame.init()
gamers = pygame.sprite.Group()
bullets = pygame.sprite.Group()
screen = pygame.display.set_mode((800, 600))
def rot_center(image, angle):

    #rotate an image while keeping its center and size
    orig_rect = (image.get_rect())
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    #rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
def rot_center2(image, angle, x, y):
    #orig_rect = (image.get_rect())
    rot_image = pygame.transform.rotate(image, angle)
    #rot_rect = orig_rect.copy()
    rot_rect = rot_image.get_rect(center=(x-image.get_width()/2,y-image.get_height()))

    #rot_rect.center = rot_image.get_rect().center
    #rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image,rot_rect

path="images/"
image1=pygame.image.load(path+'space-invaders.png')
image2=pygame.image.load(path+'space-invaders_20.png')
speed=1
class Player(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        super().__init__() 
        self.delangle=False
        self.angle = 0
        self.pos = pygame.math.Vector2(x, y)
        self.move = pygame.math.Vector2()
        try:
            self.image =image1# pygame.image.load('space-invaders.png')
           
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom = (round(self.pos.x ), round(self.pos.y)))

    def update(self):
        #adjustment=#pygame.math.Vector2(-self.image.get_width()/200000,-self.image.get_height()/200000)
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            self.delangle=True
            self.angle+=1.1
            self.image=rot_center(image1,self.angle)
            #self.pos=self.pos+adjustment
        if pressed[K_RIGHT]:
            self.delangle=True
            self.angle+=-1.1
            self.image=rot_center(image1,self.angle)
        if pressed[K_UP]:
            self.move=pygame.math.Vector2(0,speed)
            self.move.rotate_ip(self.angle)#+30)
            delangle=False
            self.move.y*=-1

        self.pos = self.pos + self.move * time_passed
        
        self.move.x *= 0.2# slow down (decrease progressively)
        self.move.y *= 0.2
        #makes sure we stay within boundries of screen
        if self.pos.y > 600:
            self.pos.y = 600
        if self.pos.y < 45:
            self.pos.y = 45

        self.rect =self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.right > 800:
            self.rect.right = 800
            self.pos.x = self.rect.centerx
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>600:
            self.rect.bottom=600
#class computer(pygame.sprite.Sprite):
class Player2(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        super().__init__() 
        self.delangle=False
        self.angle = 0
        self.pos = pygame.math.Vector2(x, y)
        self.move = pygame.math.Vector2()
        try:
            self.image =image2 #pygame.image.load('space-invaders_2.png')
           
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_a]:
            self.delangle=True
            self.angle+=1
            self.image=rot_center(image2,self.angle)
            
        if pressed[K_d]:
            self.delangle=True
            self.angle+=-1
            self.image=rot_center(image2,self.angle)
        if pressed[K_w]:
            self.move=pygame.math.Vector2(0,speed)
            self.move.rotate_ip(self.angle)#+30)
            delangle=False
            self.move.y*=-1


        self.pos = self.pos + self.move * time_passed
        self.move.x *= 0.2# slow down (decrease progressively)
        self.move.y *= 0.2

        if self.pos.y > 600:
            self.pos.y = 600
        if self.pos.y < 45:
            self.pos.y = 45

        self.rect =self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.right > 800:
            self.rect.right = 800
            self.pos.x = self.rect.centerx
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>600:
            self.rect.bottom=600
image_b=pygame.image.load(path+"bullet.png")
class Bullet(pygame.sprite.Sprite):
    def __init__(self,player) -> None:
        super().__init__()
        self.pos = player.pos
        self.move = pygame.math.Vector2(0,0)
        self.image = image_b
        self.owner=player
        self.isready=False
        self.rect = self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))
    def bullet_ready(self,player):
        #global bullet_bool1
        #global bullet_bool2
        mv=pygame.math.Vector2(0,40)
        self.angle=player.angle
        mv.rotate_ip(-self.angle)
        self.image=rot_center(image_b,self.angle)
        self.pos=self.pos-mv
        self.isready=True
    
    def update(self,player):
        
        self.move=pygame.math.Vector2(0,speed+2)
        self.move.rotate_ip(-self.angle)
        self.pos= self.pos-self.move*time_passed
        self.rect =self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))    
player = Player(400, 600)
player2=Player2(300,200)
allSprites =[pygame.sprite.Group(player),pygame.sprite.Group(player2)]
bullet_bool1=False
bullet_bool2=False
bullet_L=[]
bullet_L1=[]
collisions=[]
clock = pygame.time.Clock()
appender2=False
while True:
    time_passed = clock.tick(120)/10
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if(event.key==K_SPACE):
                appender1=True
                bullet_bool1=True
            if(event.key==K_q):
                
                appender2=True
                bullet_bool2=True
                
    allSprites[0].update()
    allSprites[1].update()
    screen.fill((220, 220, 0))
    #makes turning smooth
    player2.rect = player2.image.get_rect(center=((player2.pos.x), (player2.pos.y)))
    player.rect = player.image.get_rect(center=((player.pos.x), (player.pos.y)))
    allSprites[0].draw(screen)
    allSprites[1].draw(screen)
    winner=""
    #replacing seperate bullets with looped bullets
    for k,i in zip(bullet_L,bullet_L1):
        k.update(i.owner)
        k.draw(screen)
        if(i.pos.y>600 or i.pos.y<0 or i.pos.x<0 or i.pos.x>800):
            #bullet_bool1=False
            bullet_L.remove(k)
            bullet_L1.remove(i)
        
            #bullet_bool1=False

    #bullets
    if(bullet_bool1):
        if(appender1):
            bullet1=Bullet(player) 
            bul1=(pygame.sprite.Group(bullet1))
            appender1=False
            bullet1.bullet_ready(player)
            bullet_L.append(bul1)
            bullet_L1.append(bullet1)
    if(bullet_bool2):
        if(appender2):
            bullet2=Bullet(player2)
            
            bul2=(pygame.sprite.Group(bullet2))
            appender2=False
            bullet2.bullet_ready(player2)
            bullet_L.append(bul2)
            bullet_L1.append(bullet2)
       
    for i in bullet_L1:
        if(i.owner!=player):

             collisions=pygame.sprite.spritecollide(i,allSprites[0], True)

        if(i.owner!=player2):

            collisions=(pygame.sprite.spritecollide(i,allSprites[1], True))

        for k in collisions:
            if(k==player2):
                winner="player1"
                print(f"The winner is {winner} ")
                
                quit()
            if(k==player):
                winner="player2"
                print(f"The winner is {winner} ")
                quit()     

    pygame.display.flip()


