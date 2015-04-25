import pygame
import math
import pickle
import random
"""
TODO

[x]ball constructor is different, background, game over text(image load)
[x]find and load image for bricks
[x]change images for background, ball and game over, add power to player at 10 DB
[]speed up player for a turn at (x)
[]add replay functionality using 'r', whole loop inside while replay==1, game_over modified with replay
"""




#setting colors

screenW=800
screenH=600

background_image_filename='space_big.jpg'
game_over_image_filename='gameover.png'
ball_image_filename='ball.gif'
brick_image_filename='brick.jpg'
alien_brick_image_filename='alien.gif'


score_color1=(255,255,255)
score_color2=(200,0,0)

background_color=(0,0,0)

paddle_color=(255,255,255)
paddle_color2=(50,50,50)

ball_color=(255,255,255)
normal_block=(0,0,200)
gBlock_width=23 ^ (1+(screenW/800))
gBlock_height=15 ^ (1+(screenH/600))
block_width=23
block_height=15
pColor=paddle_color


rowCounter=0
columnCounter=0
outerListItem=-1
innerListItem=-1
levelMap1=[
    [0,0,0,1,1,1,0,0,1,1,1,1,0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0]
]

highScore=0
score=0
highScoreLoad=pickle.load(open('save.p','rb'))
print(highScoreLoad)
#creating the block class

class Block(pygame.sprite.Sprite):
    def __init__(self,power,x,y):
        super(Block,self).__init__()
        self.power=power
        if power=='alien':
            self.image=pygame.image.load(alien_brick_image_filename).convert()
        else:
            self.image=pygame.image.load(brick_image_filename).convert()
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class Ball(pygame.sprite.Sprite):
    #properties of the ball before __init__
    speed=10.0
    x=screenW/2
    y=screenH/2
    direction=190
    width=10
    height=10
    #creating template for instances of Ball
    def __init__(self):
        super(Ball,self).__init__()
        self.image=pygame.image.load(ball_image_filename).convert_alpha()
        self.rect=self.image.get_rect()
        self.screenheight=pygame.display.get_surface().get_height()
        self.screenwidth=pygame.display.get_surface().get_width()
    #making the ball bounce when the direction is manipulated
    def bounce(self,diff):
        #switching the direction of the ball when you bounce
        self.direction=(180 - self.direction)%360
        self.direction-=diff

    def update(self):
        direction_radians=math.radians(self.direction)

        self.x +=self.speed * math.sin(direction_radians)
        self.y -=self.speed * math.cos(direction_radians)
        #setting the positions of the rectangles(x and y)?
        self.rect.x=self.x
        self.rect.y=self.y
        #when the ball reaches y=0, the ball will bounce

        if self.y <=0:
            self.bounce(0)
            self.y=1

        #horizontal direction swap?
        if self.x <=0:
            self.direction=(360-self.direction)%360
            self.x=1

        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction)%360
            self.x=self.screenwidth - self.width - 1

        #if y exceeds the resolution of the game screen
        if self.y>screenH:
            return True
        else:
            return False
    #configuring paddle

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        #properties of the paddle
        self.width=75
        self.height=15
        self.image=pygame.Surface([self.width,self.height])
        self.image.fill((paddle_color))
        #creating a rectangle with a position
        self.rect = self.image.get_rect()
        self.screenheight=pygame.display.get_surface().get_height()
        self.screenwidth=pygame.display.get_surface().get_width()
        #placing the rectangle at the bottom of the screen?
        self.rect.x=0
        self.rect.y=self.screenheight - self.height
    #updating the position of the paddle when the mouse moves
    def update(self,color):
        self.image.fill(color)
        pos=pygame.mouse.get_pos()
        self.rect.x=pos[0]
        if self.rect.x>self.screenwidth-self.width:
            self.rect.x = self.screenwidth-self.width
    def color_change(self,color):
        player.image.fill(color)

pygame.init()
screen=pygame.display.set_mode([screenW,screenH])
#caption the screen window
pygame.display.set_caption("Breakout!")
#the mouse is not visible
pygame.mouse.set_visible(0)
font=pygame.font.Font(None,36)
background=pygame.image.load(background_image_filename).convert()
gameOverBackground=pygame.image.load(game_over_image_filename).convert_alpha()


blocks = pygame.sprite.Group()
balls=pygame.sprite.Group()
allSprites=pygame.sprite.Group()
#object player is being created and added to allSprites
player=Player()
allSprites.add(player)
#object Ball is being created and added to allSprites and (balls)
ball=Ball()

allSprites.add(ball)
balls.add(ball)
top=80
#blockCount measures how many blocks are added to the game
blockCount=32

#creating blocks in rows(5) and columns within the rows

while rowCounter < len(levelMap1):
    columnCounter=0
    while columnCounter < 32:
        outerListItem=levelMap1[rowCounter]
        innerListItem=outerListItem[columnCounter]
        if innerListItem ==0:
            bPower='normal'
            block=Block(bPower,columnCounter*(block_width+2)+2,top)
            blocks.add(block)
            allSprites.add(block)
        elif innerListItem == 1:
            bPower='alien'
            block=Block(bPower, columnCounter * (block_width + 2)+2,top)
            blocks.add(block)
            allSprites.add(block)
        columnCounter+=1
    top += block_height
    rowCounter+=1


clock=pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('space_music.wav')
pygame.mixer.music.play(-1)

game_over=False
deadBlockCounter=0
exit_program=False
font=pygame.font.Font(None,32)

while exit_program != True:
    clock.tick(30)
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        #if you quit the game via window closure, exit_program is TRUE
        if event.type ==pygame.QUIT:
            exit_program=True

    if not game_over:
        player.update(pColor)
        game_over=ball.update()
        score=font.render("Score: " + str(deadBlockCounter),True, (255,255,255))
        scorePos=screenW-100,20
        screen.blit(score,scorePos)

    if deadBlockCounter > highScoreLoad:
        highScore=deadBlockCounter
        pickle.dump(highScore,open('save.p','wb'))

    highScoreText=font.render("High Score: "+str(highScoreLoad),True, (255,255,255))
    highScorePos=screenW/2,20
    screen.blit(highScoreText,highScorePos)

    if game_over:
        screen.blit(gameOverBackground,(screenW/2-200,screenH/2-50))
        pickle.dump(highScore,open('save.p','wb'))

    if pygame.sprite.spritecollide(player,balls,False):
        diff=(player.rect.x + player.width/2)-(ball.rect.x + ball.width/2)

        ball.rect.y=screen.get_height() - player.rect.height-ball.rect.height-1
        ball.bounce(diff)

    #when the sprites of (ball) and (block) collide, deadBlocks will become True
    deadBlocks=pygame.sprite.spritecollide(ball,blocks,True)

    #the ball will not bounce on dead blocks
    if len(deadBlocks)>0:
        s=pygame.mixer.Sound('hit.wav')
        s.play()
        for b in deadBlocks:
            if b.power == 'alien':
                pColor=paddle_color2
            else:
                pColor=paddle_color
        deadBlockCounter+= len(deadBlocks)
        ball.bounce(0)

        if len(blocks)==0:
            game_over=True

    allSprites.draw(screen)
    pygame.display.flip()

pygame.quit()