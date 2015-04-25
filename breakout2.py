import math
import pygame
import random

#set screen width/height
#as a matter of practice, always use x-axis first, y-axis next
_W=800
_H=600

background_image_filename="space_big.jpg"
game_over_image_filename="gameover.png"
ball_image_filename="ball.gif"

backgroundColor=(0,0,0)
paddleColor=(255,255,255)
paddleColor2=(50,50,50)
normalBrickColor=(0,0,200)
angryBrickColor=(200,0,0)
fairyBrickColor=(230,230,0)

brickWidth=23
brickHeight=15

class Block(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super(Block,self).__init__()

        self.image=pygame.Surface([brickWidth,brickHeight])

        self.image.fill(color)

        self.rect=self.image.get_rect()

        self.rect.x=x
        self.rect.y=y

class Ball(pygame.sprite.Sprite):
    speed=10.0

    #Ball's point of origin
    #possible problem
    x=0.0
    y=180.0

    direction=200

    width=10
    height=10

    def __init__(self):
        super(Ball,self).__init__()

        self.image=pygame.image.load(ball_image_filename).convert_alpha()
        self.rect=self.image.get_rect()
        self.screenheight=pygame.display.get_surface().get_height()
        self.screenwidth=pygame.display.get_surface().get_width()

    def bounce(self,diff):
        self.direction=(180-self.direction) % 360
        self.direction -=diff

    def update(self):
        direction_radians=math.radians(self.direction)

        self.x +=self.speed * math.sin(direction_radians)
        self.y -=self.speed * math.cos(direction_radians)
        self.rect.x=self.x
        self.rect.y=self.y

        if self.y <=0:
            self.bounce(0)
            self.y=1
        if self.x <=0:
            self.direction =(360-self.direction)%360
            self.x=1
        if self.x > self.screenwidth - self.width:
            self.direction = (360-self.direction)%360
            self.x = self.screenwidth - self.width - 1

        if self.y > _H:
            return True
        else:
            return False

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player,self).__init__()

        self.width=75
        self.height=15
        self.image=pygame.Surface([self.width,self.height])
        self.image.fill((paddleColor))

        self.rect=self.image.get_rect()
        self.screenheight=pygame.display.get_surface().get_height()
        self.screenwidth=pygame.display.get_surface().get_width()

        self.rect.x=0
        self.rect.y=self.screenheight-self.height

    def update(self,color):
        self.image.fill(color)
        pos=pygame.mouse.get_pos()
        self.rect.x=pos[0]
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x=self.screenwidth - self.width
pygame.init()

screen=pygame.display.set_mode([_W,_H])
pygame.display.set_caption("Breakout")
pygame.mouse.set_visible(0)

background=pygame.image.load(background_image_filename).convert()
#background=pygame.transform.scale(background, (1600,1200))
gameOverBackground=pygame.image.load(game_over_image_filename).convert_alpha()
blocks=pygame.sprite.Group()
balls=pygame.sprite.Group()
allSprites=pygame.sprite.Group()
player=Player()
allSprites.add(Player)
ball=Ball()
allSprites.add(ball)
balls.add(ball)

#level map

top=80
blockCount=32

levelMap=[
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,0,1,0,0,0,1,0,1,1,0,0,1,1,1,1,1,0,1,1,1,1,0,0,1,0,0],
    [0,0,1,0,0,1,0,1,0,0,0,1,0,1,1,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0],
    [0,0,1,1,1,1,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,0,1,1,1,1,0,0,1,0,0],
    [0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

rowCounter=0
columnCounter=0
outerListItem= -1
innerListItem = -1
while rowCounter < len(levelMap):
    columnCounter=0
    while columnCounter < 32:
        outerListItem=levelMap[rowCounter]
        innerListItem=outerListItem[columnCounter]
        if innerListItem==0:
            bColor=normalBrickColor
            block=Block(normalBrickColor,columnCounter * (brickWidth +2)+2,top)
            blocks.add(block)
            allSprites.add(block)
        elif innerListItem ==1:
            bColor=random.choice([angryBrickColor,fairyBrickColor])
            block=Block(bColor,columnCounter * (brickWidth +2)+2, top)
            blocks.add(block)
            allSprites.add(block)
        columnCounter+=1
    top+=brickHeight
    rowCounter+=1


#################
clock=pygame.time.Clock()
game_over=False
exit_program=False

brokenBrickCount=0

#game loop
while exit_program != True:
    clock.tick(30)
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            exit_program=True

    if not game_over:
        if brokenBrickCount==10:
            player.update(paddleColor2)
        elif brokenBrickCount > 10:
            player.update(paddleColor)
        else:
            player.update(paddleColor)
        game_over=ball.update()

    if game_over:
        screen.blit(gameOverBackground, (_W/2 -200, _H/2 -50))

    if pygame.sprite.spritecollide(player,balls,False):
        diff=(player.rect.x + player.width/2)-(ball.rect.x + ball.width/2)

        ball.rect.y=screen.get_height() - player.rect.height-ball.rect.height-1
        ball.bounce(diff)
    deadblocks=pygame.sprite.spritecollide(ball,blocks,True)

    if len(deadblocks)>0:
        brokenBrickCount +=len(deadblocks)
        ball.bounce(0)
        if len(blocks)==0:
            game_over= True


    allSprites.draw(screen)
    pygame.display.flip()
pygame.quit