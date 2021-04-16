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

# check 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0,0)) # draw bg
    screen.blit(character, (character_x_pos, character_y_pos))
    #screen.fill((0, 0, 255))
    pygame.display.update() # should be called to update screen
    
# pygame end
pygame.quit()