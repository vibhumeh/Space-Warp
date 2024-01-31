from curses import KEY_A1
from tkinter import E
import pygame
import sys
import time
import random as rand
import logging
#import simpleaudio as sa
from pygame.locals import *
pygame.init()
Portals= pygame.sprite.Group()
gamers = pygame.sprite.Group()
bullets = pygame.sprite.Group()
Explosion=pygame.sprite.Group()
Landmines=pygame.sprite.Group()
ELandmines=pygame.sprite.Group()
w=1400
h=750
screen = pygame.display.set_mode((w,h))

pygame.mixer.music.load("sound_effects/game_music.wav")#play music later
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

boom = pygame.mixer.Sound('sound_effects/DeathFlash.wav')
gunshot=pygame.mixer.Sound('sound_effects/gunshot.wav')




def rot_center(image, angle):

    #rotate an image while keeping its center and size
    orig_rect = (image.get_rect())
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    #rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


path="images/"
image1=pygame.image.load(path+'space-invaders.png').convert_alpha()
image2=pygame.image.load(path+'space-invaders_2.png').convert_alpha()

image_b=pygame.image.load(path+"bullet.png").convert_alpha()
image_mine=[pygame.image.load(path+"Landmine0.png").convert_alpha(),pygame.image.load(path+"Landmine1.png").convert_alpha()]

image_expM=pygame.image.load(path+"explosion_M/exp2.png").convert_alpha()
myfont = pygame.font.SysFont(None,50)

sheet_width, sheet_height = image_expM.get_size()
num_sprites = 12  # Number of frames in the sprite sheet
frame_width = sheet_width //4
frame_height = sheet_height//4

# Separating the frames
frames = []
k=0
p=0
for i in range(num_sprites+3):
  
    # Define a rectangle to cut out the right frame
    frame_rect = pygame.Rect(p * frame_width, frame_height*k, frame_width,frame_height)
    try:
        frame = image_expM.subsurface(frame_rect)
        frames.append(frame)

    except:
        p-=5
        k+=1
    p+=1
    
image_mine+=frames



waiting=True
maxhp=100
dmg=20
speed=1.5
rot=1.5#in radians
portalsize=[300,200]
#Start game func


def start_screen():
    screen.fill((0,100,100))
    text = myfont.render("Press SPACE to Start", True, (0,0,0))
    text_rect = text.get_rect(center=(w // 2, h // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    global waiting
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                pygame.mixer.music.set_volume(0.6)
def End_gamescreen():
    global winner
    screen.fill((150,150,100))
    text = myfont.render(f"Winner is {winner}", True, (0,0,0))
    text_rect = text.get_rect(center=(w // 2, h // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    global waiting

class portal(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.pos=(x,y)
        self.rect=pygame.Rect(x,y,portalsize[0],portalsize[1])
    def draw(self):
        x,y=self.pos
        pygame.draw.rect(screen,(0,0,92.5),(x,y,portalsize[0],portalsize[1]))

    
class health_bar():
    def _init_(self,playername):
        self.owner=playername
        
    def draw(self):
        self.ratio=self.owner.hp/maxhp
        if(not self.ratio<=0):
            
            if self.ratio<0:
                self.ratio=0
            x,y=self.owner.pos
            y+=30
            x-=45
            
            pygame.draw.rect(screen,"red",(x,y,100,10))
            pygame.draw.rect(screen,"green",(x,y,100*self.ratio,10))

class Player(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        super().__init__() 
        self.reloading=False
        self.timer=0
        self.bcount=5
        self.hp=maxhp
        self.delangle=False
        self.angle = 0
        self.pos = pygame.math.Vector2(x, y)
        self.move = pygame.math.Vector2()
        try:
            self.image =image1# pygame.image.load('space-invaders.png')
           
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 0))
        self.image=rot_center(image1,self.angle)
        self.rect = self.image.get_rect(midbottom = (round(self.pos.x ), round(self.pos.y)))

    def update(self):
        #adjustment=#pygame.math.Vector2(-self.image.get_width()/200000,-self.image.get_height()/200000)
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            self.delangle=True
            self.angle+=rot
            self.image=rot_center(image1,self.angle)
            #self.pos=self.pos+adjustment
        if pressed[K_RIGHT]:
            self.delangle=True
            self.angle+=-rot
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
        if self.pos.y > h:
            self.pos.y = h
        if self.pos.y < 45:
            self.pos.y = 45

        self.rect =self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.right > w:
            self.rect.right = w
            self.pos.x = self.rect.centerx
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>h:
            self.rect.bottom=h
class Player2(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        super().__init__()
        self.reloading=False
        self.timer=0
        self.bcount=5 
        self.hp=maxhp
        self.delangle=False
        self.angle =180
        
        self.pos = pygame.math.Vector2(x, y)
        self.move = pygame.math.Vector2()
        try:
            self.image =image2 #pygame.image.load('space-invaders_2.png')
           
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 0))
        self.image=rot_center(image2,self.angle)
        self.rect = self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_a]:
            self.delangle=True
            self.angle+=rot
            self.image=rot_center(image2,self.angle)
            
        if pressed[K_d]:
            self.delangle=True
            self.angle+=-rot
            self.image=rot_center(image2,self.angle)
        if pressed[K_w]:
            self.move=pygame.math.Vector2(0,speed)
            self.move.rotate_ip(self.angle)#+30)
            delangle=False
            self.move.y*=-1


        self.pos = self.pos + self.move * time_passed
        self.move.x *= 0.2# slow down (decrease progressively)
        self.move.y *= 0.2

        if self.pos.y > h:
            self.pos.y = h
        if self.pos.y < 45:
            self.pos.y = 45

        self.rect =self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.right > w:
            self.rect.right = w
            self.pos.x = self.rect.centerx
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>h:
            self.rect.bottom=h

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player) -> None:
        super().__init__()
        self.pos = player.pos
        self.move = pygame.math.Vector2(0,0)
        self.image = image_b
        self.owner=player
        self.isready=False
        self.rect = self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))
    def bullet_ready(self):
        #global bullet_bool1
        #global bullet_bool2
        player=self.owner
        mv=pygame.math.Vector2(0,40)
        self.angle=player.angle
        mv.rotate_ip(-self.angle)
        self.image=rot_center(image_b,self.angle)
        self.pos=self.pos-mv
        self.isready=True
    
    def update(self):
        player=self.owner
        self.move=pygame.math.Vector2(0,speed+2)
        self.move.rotate_ip(-self.angle)
        self.pos= self.pos-self.move*time_passed
        self.rect =self.image.get_rect(midbottom = (round(self.pos.x), round(self.pos.y)))   
        if(i.pos.y>h or i.pos.y<0 or i.pos.x<0 or i.pos.x>w):
            self.kill() 
class Landmine(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.time=time.time()
        self.pos = player.pos
        self.index=0
        self.image = image_mine[self.index]
        self.owner=player
        self.isready=False
        self.boom=False
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
        self.counter=0
        
    def update(self):
        if(time.time()-self.time>=5):
            self.isready=True
    def Explode(self):
        self.boom=True
        explosion_speed=6
        self.counter+=1

        if self.counter>=explosion_speed and self.index<len(image_mine):
            self.counter=0
            self.image=image_mine[self.index]
            self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
            self.index+=1
        if self.index>=len(image_mine):
            self.kill()



class P_explosion(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.images=[]
        self.pos=player.pos
        for i in range(5,10):
            img=pygame.image.load(path+f"explosion_p/filer/tile00{i}.png")
            self.images.append(img)
        self.counter=0
        self.index=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect(center = (round(self.pos.x ), round(self.pos.y)))
    def update(self):
        explosion_speed=6
        self.counter+=1
        if self.counter>=explosion_speed and self.index<len(self.images):
            self.counter=0
            
            self.image=self.images[self.index]
            self.index+=1
        if self.index>=len(self.images):
            self.kill()




    


check=0
gg=False
bullet_bool1=False
bullet_bool2=False

collisions=[]
x,y=(rand.randint(0+portalsize[0],w-portalsize[0]),rand.randint(0+portalsize[1],h-portalsize[1]))
potol=portal(x,y)

player = Player(w/2, h-100)
player2=Player2(w/2,0)
gamers.add(player)
gamers.add(player2)


clock = pygame.time.Clock()

HP1=health_bar()
HP1._init_(player)
HP2=health_bar()
HP2._init_(player2)
gamerl=gamers.sprites()
sl=[gamers,HP1,HP2,Explosion,bullets]
sus=[]
while True: 
    if waiting:
        start_screen()
    time_passed = clock.tick(120)/10
    
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if(event.key==K_r) and not player2.reloading:
                player2.reloading=True
                player2.timer=time.time()
                b2=player2.bcount
            if(event.key==K_m) and not player.reloading:
                player.reloading=True
                player.timer=time.time()    
                b1=player.bcount
            if(event.key==K_SPACE and len(gamerl)>1):
                
                if not player.reloading:  
                    gunshot.play()
                    player.bcount-=1
                    bullet_bool1=True
            if(event.key==K_1):
                landm=Landmine(player2)
                Landmines.add(landm)
            if(event.key==K_SLASH):
                landm=Landmine(player)
                Landmines.add(landm)
            if(event.key==K_q and len(gamerl)>1):
                if not player2.reloading:
                    gunshot.play()
                    player2.bcount-=1
                    bullet_bool2=True
    sus+=bullets.sprites()+gamerl#makes list of owner sprites objects
    #reloading of player//may remove reload feature
    if not player.reloading and player.bcount==0:
         player.reloading=True
         player.timer=time.time()
         b1=0
    elif player.reloading and time.time()-player.timer>=5-b1:
        player.bcount=5
        player.reloading=False
    if not player2.reloading and player2.bcount==0:
        player2.reloading=True
        player2.timer=time.time()
        b2=0
    elif player2.reloading and time.time()-player2.timer>=5-b2:
        player2.bcount=5
        player2.reloading=False
    #gamers.update()
    screen.fill((0,0,90))
    potol.draw()
    for sprite in sl:
        try:
            sprite.update()
        except:
            pass
        try:
            if(sprite== gamers):
                player2.rect = player2.image.get_rect(center=((player2.pos.x), (player2.pos.y)))
                player.rect = player.image.get_rect(center=((player.pos.x), (player.pos.y)))
            sprite.draw(screen)
        except:
            sprite.draw()
    ELandmines.draw(screen)
    Landmines.update()
    for i in Landmines.sprites():
        collisions2=pygame.sprite.spritecollide(i,[gamers for gamers in gamerl],False)
        if(i.isready and len(collisions2) and not i.boom):
            ELandmines.add(i)
            for k in collisions2:
                if(k==player):
                    player.hp-=100
                elif(k==player2):
                    player2.hp-=100
            collisions2=[]
    for i in ELandmines.sprites():
        i.Explode()
            
    tp=pygame.sprite.spritecollide(potol,sus,False)
    if tp:
        tp=list(set(tp))
        for k in tp:
            x,y=(rand.randint(0,w),rand.randint(0,h))
            k.pos=(pygame.math.Vector2(x,y))
    #bullets
    if bullet_bool1:
        bull1=Bullet(player)
        bull1.bullet_ready()
        bullets.add(bull1)
        bullet_bool1=False
    if bullet_bool2:
        bull2=Bullet(player2)
        bull2.bullet_ready()
        bullets.add(bull2)
        bullet_bool2=False
    

    for i in bullets.sprites():
        if(i.owner!=player) and not gg:

             collisions=pygame.sprite.spritecollide(i,[gamerl[0]],False)
             if len(collisions):
                i.kill()

        if(i.owner!=player2) and not gg:
            collisions=pygame.sprite.spritecollide(i,[gamerl[1]],False )
            if len(collisions):
                i.kill()

        for k in collisions:
            if(k==player2):
                player2.hp-=dmg
            if(k==player):
                player.hp-=dmg
        
    
   
    if player2.hp<=0 and not gg:
        winner="player1"
        expl=P_explosion(player2)
        Explosion.add(expl)
        gamers.remove(player2)
        gamerl.remove(player2)
        t=time.time()
        boom.play()
        gg=True
    if player.hp<=0 and not gg:
        winner="player2"
        expl=P_explosion(player)
        Explosion.add(expl)
        gamers.remove(player)
        gamerl.remove(player2)
        t=time.time()
        boom.play()
        gg=True
    if gg and not Explosion and time.time()-t>=5:
         if i:
             time.sleep(1)
             End_gamescreen()
         check+=1
#player 1 has advantage when draw!!!! 
#remove landmines after kill.
    pygame.display.flip()