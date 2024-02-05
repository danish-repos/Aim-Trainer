import math
import random
import time
import pygame
pygame.init()

# height and width of the window of our game
Width= 800
Height = 600

# making a window 
Window = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Aim Trainer")

# time after each target will appear 
targetIncrement = 500
targetEvent = pygame.USEREVENT
targetPadding = 30

# R-G-B
backgroundColor = (0 , 25, 40)

# Top-Bar things
topBarColor = "grey"
topBarHeight = 50
topBarTextColor = "black"

labelFont = pygame.font.SysFont("comicsans",24)

# No of misses you can do
lives = 3

class Target:

    # target will grow up to this size
    maxSize = 30
    growthRate = 0.2
    color = "red"
    secondColor = "white"

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    # keeps growing untip it reaches a max size
    def update(self):
        if self.size + self.growthRate >= self.maxSize:
            self.grow = False
        
        if self.grow:
            self.size += self.growthRate
        else:
            self.size -= self.growthRate

    # draws a target
    def draw(self, Window):
        pygame.draw.circle(Window,self.color,(self.x,self.y),self.size)
        pygame.draw.circle(Window,self.secondColor,(self.x,self.y),self.size * 0.8)
        pygame.draw.circle(Window,self.color,(self.x,self.y),self.size * 0.6)
        pygame.draw.circle(Window,self.secondColor,(self.x,self.y),self.size * 0.4)

    # using the distance formula, it will detect a collison
    def collison(self, x, y):
        distance = math.sqrt((self.x - x )** 2 + (self.y - y )** 2)
        return distance <= self.size

def drawingTargets(Window,targets):
    Window.fill(backgroundColor)

    for target in targets:
        target.draw(Window)

# takes seconds and convet into a 'min:sec:millisecs' format
def formatTime(secs):
    milliSeconds = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60,1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}:{milliSeconds}"

def drawTopBar(Window, elapsedTime, targetPressed , misses):
    pygame.draw.rect(Window, topBarColor, (0,0, Width , topBarHeight))
    timeLabel = labelFont.render(f"Time : {formatTime(elapsedTime)}",1, topBarTextColor)

    speed = round(targetPressed / elapsedTime, 1)
    speedLabel = labelFont.render(f"Speed : {speed} t/s" , 1 , topBarTextColor)

    hitsLabel = labelFont.render(f"Hits : {targetPressed}" , 1 , topBarTextColor)
    
    livesLabel = labelFont.render(f"Lives : {lives - misses}" , 1 , topBarTextColor)

    Window.blit(timeLabel,(5,5))
    Window.blit(speedLabel,(200,5))
    Window.blit(hitsLabel,(400,5))
    Window.blit(livesLabel,(600,5))

def endScreen(Window, elapsedTime, targetPressed , clicks):
    Window.fill(backgroundColor)

    timeLabel = labelFont.render(f"Time : {formatTime(elapsedTime)}",1, "white")

    speed = round(targetPressed / elapsedTime, 1)
    speedLabel = labelFont.render(f"Speed : {speed} t/s" , 1 , "white")

    hitsLabel = labelFont.render(f"Hits : {targetPressed}" , 1 , "white")
    
    accuracy = round(targetPressed/clicks,1)
    accuracyLabel = labelFont.render(f"Accuracy : {accuracy}" , 1 , "white")
    
    Window.blit(timeLabel,(getMiddle(timeLabel),100))
    Window.blit(speedLabel,(getMiddle(speedLabel),200))
    Window.blit(hitsLabel,(getMiddle(hitsLabel),300))
    Window.blit(accuracyLabel,(getMiddle(accuracyLabel),400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def getMiddle(surface):
    return Width / 2 - surface.get_width()/2

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targetPressed = 0
    clicks = 0
    misses = 0
    startTime = time.time()

    pygame.time.set_timer(targetEvent,targetIncrement)

    # main game loop
    while run:

        # setting frame rate
        clock.tick(60)
        click = False

        mousePosition = pygame.mouse.get_pos()
        elapsedTime = time.time() - startTime

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == targetEvent:
                x = random.randint(targetPadding, Width - targetPadding)
                y = random.randint(targetPadding + topBarHeight, Height - targetPadding)
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True 
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            # * breaks the tuple and sends each thing in it as a indiviual parameter
            if click and target.collison(*mousePosition):
                targets.remove(target)
                targetPressed += 1

        if misses >= lives:
            endScreen(Window,elapsedTime,targetPressed,clicks) 

        drawingTargets(Window, targets)
        drawTopBar(Window , elapsedTime, targetPressed, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()










