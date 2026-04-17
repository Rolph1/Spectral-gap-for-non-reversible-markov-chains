# import pygame package
import pygame

# initializing imported module
pygame.init()

# displaying a window of height
# 500 and width 400
screen = pygame.display.set_mode((1600, 1600))
color = (255, 255, 255)
black = (0, 0, 0)
# creating a bool value which checks
# if game is running
running = True

# keep game running till running is true
while running:
    
    # Check for event if user has pushed
    # any event in queue
    for event in pygame.event.get():
        screen.fill(black)
        pygame.draw.rect(screen, color, pygame.Rect(30, 30, 60, 60),  2)
        pygame.display.flip()
        # if event is of type quit then 
        # set running bool to false
        if event.type == pygame.QUIT:
            running = False