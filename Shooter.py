from pygame import * 
from pygame.sprite import Group
from random import randint 
#звук 

player = [image.load('s1.png'), image.load('s2.png'),image.load('s1.png'), image.load('s2.png'),image.load('s1.png'), image.load('s2.png')]
player_scaled = [transform.scale(img, (90, 100)) for img in player]


mixer.init() 
clock= time.Clock()
fire = mixer.Sound("shoot.ogg") 

class GameSprite(sprite.Sprite): 

    def __init__(self, player_image , player_x , player_y, size_x, syze_y, player_speed): 
        sprite.Sprite.__init__(self) 
        self.image = transform.scale(image.load(player_image),(size_x, syze_y))  
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
    def reset (self): 
        window.blit(self.image,(self.rect.x , self.rect.y)) 
class Bullet(GameSprite):
    def update(self):
        self.rect.x -= self.speed 
        #зникає дійдучи до краю екрану
        if self.rect.x < 0:
            self.kill() 

class Player(GameSprite): 
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] :
            self.rect.x -= self.speed
            self.left = True
            self.right = False

        elif keys[K_RIGHT] :
            self.left = False
            self.right = True
            self.rect.x += self.speed
        else:
            self.right = self.left = False
 
 
    def fire(self): 
        pass
        
        bullet = Bullet(ammo_img, self.rect.x+30, self.rect.y+30, 20, 30, -20)
        bullets.add(bullet)

    def animation(self):
        if self.left:
            self.count = (self.count + 1) % len(player)  
            window.blit(player_scaled[self.count], (self.rect.x, self.rect.y))
        elif self.right:
            self.count = (self.count + 1) % len(player)  
            window.blit(player_scaled[self.count], (self.rect.x, self.rect.y))
        else:
            self.count=0
            window.blit(player_scaled[self.count], (self.rect.x, self.rect.y))

bullets = sprite.Group()

score = 0 


class Enemy(GameSprite): 
    def update(self): 
        self.rect.x -= self.speed 
        global lost  

        if self.rect.y > win_height: 
            self.rect.x = randint(80, win_width - 80) 
            self.rect.y = 0 
            lost = lost + 1 
win_width = 900
win_height = 700 
window = display.set_mode((win_width, win_height)) 
display.set_caption("Shooter Game") 
background = transform.scale(image.load("background.png"), (win_width, win_height))

font.init() 
font2 = font.Font(None, 36) 
font1 = font.Font(None,100)

game = True
finish = False
FPS = 60

font.init() 
font2 = font.Font(None, 36) 
font1 = font.Font(None,100)

ammo_img = 'bullet.png'
soilder_img = 's1.png'
soilder2_img = 's2.png'
soilder3_img = 's3.png'
monster_img = 'monster.png'



monsters = sprite.Group() 
for i in range(1, 10): 
    monster = Enemy(monster_img  , randint(win_height - 200, win_width - 80), 490, 160, 90, randint(1, 7)) 
    monsters.add(monster)

bullets = sprite.Group()

soilder = Player(soilder_img, 50, 490, 90, 100, 5)

jumping = False
jump_count = 7
jump_height = 7

run = True 
lose = font1.render("YOU lose", True, (182,21,21))
while run: 
    

    for e in event.get(): 
        if e.type == QUIT: 
            run = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                soilder.fire()

    if not finish:
        window.blit(background,(0,0))
        # soilder.reset()
        soilder.update()
        soilder.animation()
        bullets.draw(window)
        monsters.draw(window)
        
        bullets.update()
        monsters.update()
        keys = key.get_pressed()

        text = font2.render("Рахунок:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        if not jumping:
            if keys[K_UP]:
                jumping = True

    
        else:
            if jump_count >= -jump_height:
                neg = 1
                if jump_count <= 0:
                    neg = -1
                soilder.rect.y -= (jump_count ** 2)  * neg
                jump_count -= 1
            else:
                jumping = False
                jump_count = jump_height

        if sprite.spritecollide(soilder,monsters, False):
            window.blit(lose, (200, 200))
            finish = True

        collides = sprite.groupcollide(monsters,bullets, True, True)
        
        for c in collides:
            monster = Enemy(monster_img  , randint(win_height-200, win_width - 80), 490, 160, 90, randint(1, 7)) 
            monsters.add(monster) 
            score = score + 1


        collidesds = sprite.groupcollide(monsters,bullets, True, True)


    display.update()
    clock.tick(40)