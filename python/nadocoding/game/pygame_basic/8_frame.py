import pygame

# 0. Mandatory for pygame
########################################################################
pygame.init() # shoud be called

#set size of display
screen_width = 480
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))

# title of screen
pygame.display.set_caption("my game")

#fps
clock = pygame.time.Clock()
########################################################################


# 1. Init of User game such as BG, game image, position, speed, font so on


# check 
running = True
while running:
    dt = clock.tick(30) # fps
     
    # 2. Event Control (keyboard, mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # 3. Define the position of game character

    # 4. collision control and check

    # 5. Draw on the screen

    pygame.display.update() # should be called to update screen
    
pygame.time.delay(2000)

# pygame end
pygame.quit()