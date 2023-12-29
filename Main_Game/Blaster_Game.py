import pygame
import sys
import time
import simpleaudio as sa
from pygame.locals import *
pygame.init()
gamers = pygame.sprite.Group()
bullets = pygame.sprite.Group()
screen = pygame.display.set_mode((800, 600))

pygame.mixer.music.load("sound_effects/game_music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

boom = sa.WaveObject.from_wave_file('sound_effects/muffled_explosion.wav')
gunshot=sa.WaveObject.from_wave_file('sound_effects/gunshot.wav')




def rot_center(image, angle):

    #rotate an image while keeping its center and size
    orig_rect = (image.get_rect())
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    #rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


path="images/"
image1=pygame.image.load(path+'space-invaders.png')
image2=pygame.image.load(path+'space-invaders_2.png')

image_b=pygame.image.load(path+"bullet.png")
#image_mine=pygame.image.load(path+"explosion_p/filer/tile000.png")

myfont = pygame.font.SysFont(None,50)





waiting=True
maxhp=100
dmg=20
speed=1
#Start game func


def start_screen():
    screen.fill((0,100,100))
    text = myfont.render("Press SPACE to Start", True, (0,0,0))
    text_rect = text.get_rect(center=(800 // 2, 600 // 2))
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
                pygame.mixer.music.set_volume(1)
def End_gamescreen():
    global winner
    screen.fill((150,150,100))
    text = myfont.render(f"Winner is {winner}", True, (0,0,0))
    text_rect = text.get_rect(center=(800 // 2, 600 // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    global waiting


class health_bar():
    def _init_(self,playername):
        self.owner=playername
        
    def draw(self):
        self.ratio=self.owner.hp/maxhp
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
### SPAM REMOVES RELOAD TIME OF BULLET ->resolved
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
class Landmines(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.pos = player.pos
        #self.image = image_mine
        self.owner=player
        self.isready=False
        self.rect = pygame.Rect(10, 10, 200, 200)

class P_explosion(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.images=[]
        self.pos=player.pos
        for i in range(6,10):
            img=pygame.image.load(path+f"explosion_p/filer/tile00{i}.png")
            self.images.append(img)
        self.counter=0
        self.index=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect(center = (round(self.pos.x ), round(self.pos.y)))
    def update(self):
        explosion_speed=8
        self.counter+=1
        if self.counter>=explosion_speed and self.index<len(self.images):
            self.counter=0
            
            self.image=self.images[self.index]
            self.index+=1
        if self.index>=len(self.images):
            self.kill()




    



gg=False
bullet_bool1=False
bullet_bool2=False
bullet_L=[]
bullet_L1=[]
collisions=[]


player = Player(400, 500)
player2=Player2(400,0)
gamers.add(player)
gamers.add(player2)
Explosion=pygame.sprite.Group()

#allSprites =[pygame.sprite.Group(player),pygame.sprite.Group(player2)]
clock = pygame.time.Clock()

HP1=health_bar()
HP1._init_(player)
HP2=health_bar()
HP2._init_(player2)
gamerl=gamers.sprites()
while True:
    
    if waiting:
        start_screen()
    time_passed = clock.tick(120)/10
    if player.reloading and k==0:
        k=1
        t=time.time
    
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
                
            if(event.key==K_SPACE and len(gamerl)>1):
                
                if not player.bcount==0:  
                    gunshot.play()
                    player.bcount-=1
                    appender1=True
                    bullet_bool1=True
                elif not player.reloading and player.bcount==0:
                    player.reloading=True
                    player.timer=time.time()
                elif time.time()-player.timer>=5:
                    player.bcount=5
                    player.reloading=False
            if(event.key==K_q and len(gamerl)>1):
                if not player2.bcount==0:
                    gunshot.play()
                    player2.bcount-=1
                    appender2=True
                    bullet_bool2=True
                
                elif not player2.reloading:
                    player2.reloading=True
                    player2.timer=time.time()
                elif time.time()-player2.timer>=5:
                    player2.bcount=5
                    player2.reloading=False
    
                
    gamers.update()
    screen.fill((0,0,90))
   
    HP1.draw()
    HP2.draw()
    #makes turning smooth
    player2.rect = player2.image.get_rect(center=((player2.pos.x), (player2.pos.y)))
    player.rect = player.image.get_rect(center=((player.pos.x), (player.pos.y)))
    gamers.draw(screen)
    Explosion.update()
    Explosion.draw(screen)

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

    for p,i in enumerate(bullet_L1):
        if(i.owner!=player):

             collisions=pygame.sprite.spritecollide(i,[gamerl[0]],False)
             if len(collisions)>0:
                bullet_L1.remove(i)
                bullet_L.pop(p)

        if(i.owner!=player2):
            collisions=pygame.sprite.spritecollide(i,[gamerl[1]],False )
            if len(collisions)>0:
                bullet_L1.remove(i)
                bullet_L.pop(p)

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
        boom.play()
        gg=True
    if player.hp<=0 and not gg:
        winner="player2"
        expl=P_explosion(player)
        Explosion.add(expl)
        gamers.remove(player)
        boom.play()
        gg=True
    if gg and len(Explosion.sprites())==0:
        End_gamescreen()
    
    pygame.display.flip()