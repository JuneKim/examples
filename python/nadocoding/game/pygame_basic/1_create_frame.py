import pygame

pygame.init() # shoud be called

#set size of display
screen_width = 480
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))

# title of screen
pygame.display.set_caption("my game")

# check 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# pygame end
pygame.quit()
