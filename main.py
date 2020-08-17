import os
os.system('python persion.py')
import pygame
import time
from pygame.locals import *
pygame.init()
canvas=pygame.display.set_mode((1200,667))
pygame.display.set_caption("防疫大作战")
bg=pygame.image.load("images/3.png")
bglost=pygame.image.load("images/bglost.png")
bgstart=pygame.image.load("images/5.png")
bgwin=pygame.image.load("images/bgwin.png")
ehead=pygame.image.load("images/ememyhead.png")
ebullet=pygame.image.load("images/enemybullet.png")
hero1=pygame.image.load("images/hero1.png")
hero2=pygame.image.load("images/hero2.png")
hhead=pygame.image.load("images/herohead.png")
hbullet=pygame.image.load("images/herobullet.png")
bgko=pygame.image.load("images/ko2.png")
monster1=pygame.image.load("images/monster01.png")
monster2=pygame.image.load("images/monster02.png")
#设置音乐播放
pygame.key.set_repeat(1)
bg_music=pygame.mixer.Sound("music/bg_music.wav")
KO_music=pygame.mixer.Sound('music/KO.wav')
bg_hero=pygame.mixer.Sound('music/bgHero.wav')
bg_enemy=pygame.mixer.Sound('music/bgEnemy.wav')
bg_music.set_volume(0.1)
bg_hero.set_volume(0.08)
bg_enemy.set_volume(0.1)
KO_music.set_volume(0.3)
bg_music.play()
bgend_music=pygame.mixer.Sound('music/bgStart.wav')
bgend_music.set_volume(0.3)
bgend2=pygame.mixer.Sound('music/bg222.wav')
bgend2.set_volume(0.3)
def close():
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if GameVar.startes==GameVar.STARTES["READY"]:
                GameVar.startes=GameVar.STARTES["START"]
        if  event.type==KEYDOWN and event.key==K_UP  :
            GameVar.hero.y-=10
        if  event.type==KEYDOWN and event.key==K_DOWN :
            GameVar.hero.y+=10
        if  event.type==KEYDOWN and event.key==K_RIGHT  :
            GameVar.hero.x+=10
        if  event.type==KEYDOWN and event.key==K_LEFT :
            GameVar.hero.x-=10
        if event.type == KEYDOWN and event.key == K_SPACE:
            if GameVar.hero.img == hero1:
                GameVar.hero.img = hero2
            if GameVar.startes==GameVar.STARTES["START"]:
                GameVar.hero.shoot()
        if event.type == KEYUP and event.key == K_SPACE:
            DressHero()
        if GameVar.hero.y < 100:
            GameVar.hero.y += 10
        if GameVar.hero.y > 410:
            GameVar.hero.y -= 10
        if GameVar.hero.x < 577:
            GameVar.hero.x += 10
        if GameVar.hero.x > 1000:
            GameVar.hero.x -= 10
#定义时间间隔的方法
def isActionTime(lastTime, interval):
    if lastTime == 0:
        return True
    currentTime = time.time()
    return currentTime - lastTime >= interval
#形参   形式参数   没有具体的值   无实际的意义
#创建敌人类
class Enemy():
    def __init__(self,head,img,x,y,width,height,life):
        self.head=head
        self.img=img
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.life=life
        self.enemyLastTime=0
        self.enemyInterval=0.7
        self.shootLastTime=0
        self.shootInterval=2
        self.n=3
    def draw(self):
        canvas.blit(self.head,(20,20))
        canvas.blit(self.img,(self.x,self.y))
    def EnemyLife(self):
        pygame.draw.rect(canvas,(100,255,0),(120, 50, self.life, 30))
    def shoot(self):
        if not isActionTime(self.shootLastTime,self.shootInterval):
                return
        self.shootLastTime = time.time()
        GameVar.bulletEnemy.append(Bullet(self.x+200, self.y+120, 75, 30, ebullet))
        bg_enemy.play()
    def step(self,hero_bullet):
        self.x = 80
        max_y = 425
        min_y = 225
        if hero_bullet >= self.y and 0 < (hero_bullet - self.y) < 320:
            y_len = hero_bullet - self.y
            max_len = max_y - hero_bullet
            min_len = hero_bullet - min_y
            if max_len > min_len:
                if self.y <= max_y + 40 and self.y >= min_y:
                    self.y += 120
                else:
                    if self.y > max_y:
                        self.y = max_y
                    elif self.y < min_y:
                        self.y = min_y
            else:
                if self.y >= min_y and self.y < max_y:
                    self.y -= 120
    def changeEnemy(self):
        if not isActionTime(self.enemyLastTime,self.enemyInterval):
                return
        self.enemyLastTime = time.time()
        if self.n%3==0:
            self.img=monster1
        if self.n%3==1 or self.n%3==2:
            self.img=monster2
        self.n+=1
    def Hit(self,component):
        e=component
        return   e.x>self.x and e.x<self.x+self.width-50 and e.y>self.y and e.y<self.y+self.height/2
    def bang(self):
        self.life -= 10
        if self.life <= 0:
            self.life = 0
#创建英雄类i
class Hero():
    def __init__(self,head,img,x,y,width,height,life):
        self.head = head
        self.img = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.life = life
        self.blood=1
        self.shootLastTime=0
        self.shootInterval=0.5
    def draw(self):
        canvas.blit(self.head,(750,20))
        canvas.blit(self.img,(self.x,self.y))
    def HeroLife(self):
        pygame.draw.rect(canvas,(100,255,0),(762-self.blood, 50, 315+self.blood, 30))
    def shoot(self):
        if not isActionTime(self.shootLastTime, self.shootInterval):
            return
        self.shootLastTime=time.time()
        GameVar.bulletHero.append(Bullet(self.x+50, self.y+120, 75, 30, hbullet))
        bg_hero.play()

    def Hit(self,component):
        h=component
        return h.x+h.width>self.x+self.width/3 and h.x+h.width<self.x+self.width*(2/3) and h.y>self.y  and h.y<self.y+self.height
    def bang(self):
        self.blood -= 5
        if self.blood <= -315:
            self.blood = 0
            self.life = 0
#创建子弹类
class Bullet():
    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
    def Paint(self):
        canvas.blit(self.img,(self.x,self.y))
    def Herostep(self):
        self.x-=7
    def Enemystep(self):
        self.x+=5
#定义画子弹的方法
def drawBullet():
    if not isActionTime(GameVar.paintLastTime,GameVar.paintInterval):
        return
    GameVar.paintLastTime=time.time()
    for bullet in GameVar.bulletHero:
        bullet.Paint()
    for bullet in GameVar.bulletEnemy:
        bullet.Paint()
#定义子弹移动的方法
def MoveBullet():
    for bullet in GameVar.bulletHero:
        bullet.Herostep()
    for bullet in GameVar.bulletEnemy:
        bullet.Enemystep()
    for i in GameVar.bulletHero:
        if i.x<80:
            continue
        elif i.x>80:
            GameVar.enemy.step(i.y)
            break
def DressHero():
    if  GameVar.hero.img==hero2:
                  GameVar.hero.img=hero1
#创建游戏类
class GameVar():
    #实参   实际参数    具有实际的值
    enemy=Enemy(ehead,monster1,200,300,288,200,315)
    hero=Hero(hhead,hero1,550,300,380,320,315)
    STARTES={"READY":1,"START":2,"OVER":3}
    startes=STARTES["READY"]
    bulletHero=[]
    bulletEnemy=[]
    paintLastTime = 0.5
    paintInterval = 0.01
def changeHit():
    for bullet in GameVar.bulletHero:
        if GameVar.enemy.Hit(bullet):
            GameVar.enemy.bang()
    for bullet2 in GameVar.bulletEnemy:
        if GameVar.hero.Hit(bullet2):
            GameVar.hero.bang()
def deleteComponent():
    for i in range(len(GameVar.bulletEnemy)-1,-1,-1):
        b2=GameVar.bulletEnemy[i]
        if b2.x >1340 or b2.x  >GameVar.hero.x+GameVar.hero.width/6 and b2.x <=GameVar.hero.x+GameVar.hero.width  :
            if  b2.y <=GameVar.hero.y+GameVar.hero.height and b2.y >GameVar.hero.y :
             GameVar.bulletEnemy.remove(b2)

    for i in range(len(GameVar.bulletHero)-1,-1,-1):
        b = GameVar.bulletHero[i]
        if b.x < -120 or b.x <= GameVar.enemy.x + GameVar.enemy.width / 2 and b.x > GameVar.enemy.x:
            if b.y <= GameVar.enemy.y + GameVar.enemy.height and b.y > GameVar.enemy.y:
                GameVar.bulletHero.remove(b)
def Lost():
    if GameVar.enemy.life<=0 or GameVar.hero.life<=0:
        GameVar.startes=GameVar.STARTES["OVER"]
xt=0
run=False
def GameOver():
    global xt, run
    if GameVar.enemy.life <= 0 or GameVar.hero.life <= 0:
        bg_music.stop()
        bg_hero.stop()
        bg_enemy.stop()
        run = True
        canvas.blit(bgko, (0, 0))
        if xt == 10:
            KO_music.play()
        if run==True:
            xt+=1
    if GameVar.hero.blood <= 0 and xt > 200:
        canvas.blit(bglost, (0, 0))
        bgend2.play()

    if GameVar.enemy.life <= 0 and xt > 200:
        canvas.blit(bgwin, (0, 0))
        bgend_music.play()
 #封装    三大特征  继承   多态   封装   面向对象
#定义封装的方法
def StatusContral():
    if GameVar.startes==GameVar.STARTES["READY"]:
        canvas.blit(bgstart,(0,0))
    if GameVar.startes==GameVar.STARTES["START"]:
        canvas.blit(bg,(0,0))
        GameVar.enemy.EnemyLife()
        GameVar.enemy.draw()
        GameVar.enemy.changeEnemy()
        GameVar.enemy.shoot()
        GameVar.hero.HeroLife()
        GameVar.hero.draw()
        drawBullet()
        MoveBullet()
        deleteComponent()
        changeHit()
        Lost()
    if GameVar.startes==GameVar.STARTES["OVER"]:
            GameOver()
while True:
    #调用封装方法
    StatusContral()
    pygame.display.update()
    close()
    pygame.time.delay(10)