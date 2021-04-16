import pygame
import os

# 0. Mandatory for pygame
########################################################################
pygame.init() # shoud be called

#set size of display
screen_width = 640
screen_height = 480

screen = pygame.display.set_mode((screen_width, screen_height))

# title of screen
pygame.display.set_caption("my Pang")

#fps
clock = pygame.time.Clock()
########################################################################


# 1. Init of User game such as BG, game image, position, speed, font so on
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

background = pygame.image.load(os.path.join(image_path, "background_640x480.png"))

stage = pygame.image.load(os.path.join(image_path, "stage_640x50.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

character = pygame.image.load(os.path.join(image_path, "character_33x60.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

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
    screen.blit(background, (0,0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update() # should be called to update screen
    
pygame.time.delay(2000)

# pygame end
pygame.quit()