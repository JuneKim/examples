import pygame
import random

# 0. Mandatory for pygame
########################################################################
pygame.init() # shoud be called

#set size of display
screen_width = 480
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))

# title of screen
pygame.display.set_caption("Quiz")

#fps
clock = pygame.time.Clock()
########################################################################


# 1. Init of User game such as BG, game image, position, speed, font so on
background = pygame.image.load("/home/mj/workplaces/MyApp/pygame_basic/background.png")

#create character
character =  pygame.image.load("/home/mj/workplaces/MyApp/pygame_basic/character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height
character_speed = 10

ddong = pygame.image.load("/home/mj/workplaces/MyApp/pygame_basic/enemy.png")
ddong_size = ddong.get_rect().size
ddong_width = ddong_size[0]
ddong_height = ddong_size[1]
ddong_x_pos = random.randint(0, screen_width - ddong_width)
ddong_y_pos = 0
ddong_speed = 10

to_x =  0
# check 
running = True
while running:
    dt = clock.tick(30) # fps
     
    # 2. Event Control (keyboard, mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
                
    # 3. Define the position of game character
    character_x_pos += to_x
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        
    ddong_y_pos += ddong_speed
    
    if ddong_y_pos > screen_height:
        ddong_y_pos = 0
        ddong_x_pos = random.randint(0, screen_width - ddong_width)

    # 4. collision control and check
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    ddong_rect = ddong.get_rect()
    ddong_rect.left = ddong_x_pos
    ddong_rect.top = ddong_y_pos
    
    if character_rect.colliderect(ddong_rect):
        running = False

    # 5. Draw on the screen
    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(ddong, (ddong_x_pos, ddong_y_pos))
    
    pygame.display.update() # should be called to update screen
    
pygame.time.delay(2000)

# pygame end
pygame.quit()