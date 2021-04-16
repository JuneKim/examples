import pygame

pygame.init() # shoud be called

#set size of display
screen_width = 480
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))

# title of screen
pygame.display.set_caption("my game")

#fps
clock = pygame.time.Clock()

background = pygame.image.load("/home/mj/workplaces/MyApp/pygame_basic/background.png")

# call sprite
character = pygame.image.load("/home/mj/workplaces/MyApp/pygame_basic/character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height - character_height

# pos to move
to_x = 0
to_y = 0

# moving speed
character_speed = 0.6

# enermy
enemy = pygame.image.load("/home/mj/workplaces/MyApp/pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = screen_width/2 - enemy_width/2
enemy_y_pos = screen_height/2 - enemy_height/2


# check 
running = True
while running:
    dt = clock.tick(60) # fps
     
    print ("fps: " + str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN: # check if key is pushed
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed
        if event.type == pygame.KEYUP: # key is up
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt
               
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height
     
    # collision control
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # check collision
    if character_rect.colliderect(enemy_rect):
        running = False

    screen.blit(background, (0,0)) # draw bg
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    
    #screen.fill((0, 0, 255))
    pygame.display.update() # should be called to update screen
    
# pygame end
pygame.quit()