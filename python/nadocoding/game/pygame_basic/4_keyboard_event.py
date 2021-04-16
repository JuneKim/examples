import pygame

pygame.init() # shoud be called

#set size of display
screen_width = 480
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))

# title of screen
pygame.display.set_caption("my game")

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

# check 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN: # check if key is pushed
            if event.key == pygame.K_LEFT:
                to_x -= 5
            elif event.key == pygame.K_RIGHT:
                to_x += 5
            elif event.key == pygame.K_UP:
                to_y -= 5
            elif event.key == pygame.K_DOWN:
                to_y += 5
        if event.type == pygame.KEYUP: # key is up
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
    character_x_pos += to_x
    character_y_pos += to_y
               
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height
     
    screen.blit(background, (0,0)) # draw bg
    screen.blit(character, (character_x_pos, character_y_pos))
    #screen.fill((0, 0, 255))
    pygame.display.update() # should be called to update screen
    
# pygame end
pygame.quit()