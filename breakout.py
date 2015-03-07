import pygame
import math
#setting colors
black=(0,0,0)
white=(255,255,255)
blue=(0,0,200)
block_width=23
block_height=15
#creating the block class
class Block(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super(Block,self).__init__()
        self.image=pygame.Surface([block_width,block_height])
        #filling the sprite with color (white)
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
class Ball(pygame.sprite.Sprite):
    #properties of the ball before __init__
    speed=10.0
    x=0.0
    y=180.0
    direction=200
    width=10
    height=10
    #creating template for instances of Ball
    def __init__(self):
        super(Ball,self).__init__()
        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(white)
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
        if self.y>600:
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
        self.image.fill((white))
        #creating a rectangle with a position
        self.rect = self.image.get_rect()
        self.screenheight=pygame.display.get_surface().get_height()
        self.screenwidth=pygame.display.get_surface().get_width()
        #placing the rectangle at the bottom of the screen?
        self.rect.x=0
        self.rect.y=self.screenheight - self.height
    #updating the position of the paddle when the mouse moves
    def update(self):
        pos=pygame.mouse.get_pos()
        self.rect.x=pos[0]
        if self.rect.x>self.screenwidth-self.width:
            self.rect.x = self.screenwidth-self.width

pygame.init()
screen=pygame.display.set_mode([800,600])
#caption the screen window
pygame.display.set_caption("Breakout!")
#the mouse is not visible
pygame.mouse.set_visible(0)
font=pygame.font.Font(None,36)
background=pygame.Surface(screen.get_size())
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
for row in range(5):
    for column in range(0,blockCount):
        #modifying the positions of the blocks?
        block=Block(blue,column*(block_width+2)+1,top)
        blocks.add(block)
        allSprites.add(block)
    top +=block_height+2

clock=pygame.time.Clock()

game_over=False

exit_program=False

while exit_program != True:
    clock.tick(30)

    screen.fill(black)
    for event in pygame.event.get():
        #if you quit the game via window closure, exit_program is TRUE
        if event.type ==pygame.QUIT:
            exit_program=True

    if not game_over:
        #when the game isn't over, the paddle position and ball position will be updated
        player.update()
        game_over=ball.update()

    if game_over:
        text=font.render("Game Over",True,white)
        textPos=text.get_rect(centerx=background.get_width()/2)
        textPos.top=300
        screen.blit(text,textPos)

    if pygame.sprite.spritecollide(player,balls,False):
        diff=(player.rect.x+player.width/2)-(ball.rect.x+ball.width/2)

        ball.rect.y=screen.get_height()-player.rect.height-ball.rect.height-1
        ball.bounce(diff)
    #when the sprites of (ball) and (block) collide, deadBlocks will become True
    deadBlocks=pygame.sprite.spritecollide(ball,blocks,True)

    #the ball will not bounce on dead blocks
    if len(deadBlocks)>0:
        ball.bounce(0)

        if len(blocks)==0:
            game_over=True

    allSprites.draw(screen)
    pygame.display.flip()
pygame.quit()