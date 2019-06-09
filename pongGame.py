import pygame
from pygame.locals import *
import sys
import random
import math

SIZE = width, height = 800, 600
WHITE = (255,255,255)

def calculate_new_xy(old_xy,speed,angle_in_radians):
    new_x = old_xy[0] + (speed*math.sin(angle_in_radians))
    new_y = old_xy[1] + (speed*math.cos(angle_in_radians))
    new_x = math.ceil(new_x)
    new_y = math.ceil(new_y)
    return new_x, new_y

def predictBall(angle,x,y):
    #if direction > 135 than ball is moving toward AI.
    # if direction < -135 ball is moving toward AI
    isNeg = False
    #angle = 180 - angle
    angle = math.radians(angle)
    side = x*math.tan(angle)


    if angle < 0:
        return side + y
    elif angle > 0:
        return side + y
        
        
    


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20,100])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = height//2
        self.speed = 1
        self.width = 100
        
        #self.rect.x = 500



class Player(Paddle):
    def __init__(self):
        super(Player,self).__init__()
        self.rect.x = width-20
    
    def move(self,direction):
        if self.rect.y >= (height-100):
            self.rect.y = (height-101)
        elif self.rect.y <= 0:
            self.rect.y = 1
        else:
            self.rect.y += direction*self.speed
class CPU(Paddle):
    def __init__(self):
        super(CPU,self).__init__()
        self.rect.x = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([20,20])
        self.width = 20
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.direction = 0
        self.speed = 2

        self.x = 0
        self.y = 0
        self.reset()

    def reset(self):
        self.speed = 1
        self.x = self.screenwidth // 2
        #self.rect.y = random.randrange(100,self.screenheight-100)
        #self.speed*=1.1
        self.y = self.screenheight // 2
        #self.direction = random.randrange(-45,45)
        
        self.direction = -200
        #if random.randrange(2) == 0:
        #   self.direction +=180
        print("\nDirection:"+str(self.direction))
        print("Prediction:"+str(predictBall(self.direction,self.x,self.y)))
        
    
    def update(self):
        self.directionRad = math.radians(self.direction)
        #self.rect.center = calculate_new_xy(self.rect.center,self.speed,self.directionRad)
        self.y -= (self.speed*math.sin(self.directionRad))
        self.x += (self.speed*math.cos(self.directionRad))

        self.rect.y = self.y
        self.rect.x = self.x

        if self.rect.x == self.screenwidth or self.rect.x == 0:
            print("Result: "+str(self.y))
            self.reset()

        if self.rect.y >= self.screenheight-10 or self.rect.y <= 0:
            self.direction*=-1

    def paddleCollide(self,c):
        self.direction = (180-self.direction)%360
        self.direction -= c
        print(self.direction)
 
        self.speed *= 1.1






def main():
    screen = pygame.display.set_mode(SIZE)

    BallGroup = pygame.sprite.Group()
    Paddles = pygame.sprite.Group()
    
    ball = Ball()
    player = Player()
    cpu = CPU()
    
    BallGroup.add(ball)
    
    Paddles.add(player)
    Paddles.add(cpu)
    clock = pygame.time.Clock()
    
    
    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            
        if pygame.sprite.spritecollide(player, BallGroup, False):
             contact = (player.rect.y + player.width/2) - (ball.rect.y+ball.width/2)
             ball.paddleCollide(contact)

        if pygame.sprite.spritecollide(cpu, BallGroup, False):
             contact = (player.rect.y + player.width/2) - (ball.rect.y+ball.width/2)
             #ball.paddleCollide(contact)

        #Handle Player movement
        keystate = pygame.key.get_pressed()
        if keystate[K_RIGHT]:
            player.move(-1)
        
        elif keystate[K_LEFT]:
            player.move(1)
        
        
        ball.update()
        Paddles.draw(screen)
        BallGroup.draw(screen)
        
        
        pygame.display.flip()
        clock.tick(240)
main()