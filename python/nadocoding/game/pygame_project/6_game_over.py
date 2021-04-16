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
character_speed = 5

weapon = pygame.image.load(os.path.join(image_path, "weapon_20x430.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]


ball_images = [
    pygame.image.load(os.path.join(image_path, "ball_160x160.png")),
    pygame.image.load(os.path.join(image_path, "ball_80x80.png")),
    pygame.image.load(os.path.join(image_path, "ball_40x40.png")),
    pygame.image.load(os.path.join(image_path, "ball_20x20.png"))]

ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3

balls = []
balls.append({
    "pos_x": 50,
    "pos_y": 50,
    "img_idx": 0,
    "to_x": 3,
    "to_y": -6,
    "init_speed_y": ball_speed_y[0]
})

weapon_to_remove = -1
ball_to_remove = -1

weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#multi weapons
weapons = []
weapon_speed = 10

to_x = 0

game_font  = pygame.font.Font(None, 40)
total_time = 10
start_tick = pygame.time.get_ticks()
game_result = "Game Over"

# check 
running = True
while running:
    dt = clock.tick(30) # fps
     
    # 2. Event Control (keyboard, mouse)total
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # 3. Define the position of game character
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed        
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width /2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    character_x_pos += to_x
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
    
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
    
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1
            
        if ball_pos_y > screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_speed_y"]
        else:
            ball_val["to_y"] += 0.5
            
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
            
    # 4. collision control and check
    character_rect = character.get_rect()
    character_rect.left = character_x_pos 
    character_rect.top = character_y_pos
    
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        if character_rect.colliderect(ball_rect):
            game_result = "You Lost"
            running = False
            break
        
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]
            
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx
                break
            
    if ball_to_remove > -1:
        if balls[ball_to_remove]["img_idx"] < 3:
            
            balls.append({
                "pos_x": balls[ball_to_remove]["pos_x"],
                "pos_y": balls[ball_to_remove]["pos_y"],
                "img_idx": balls[ball_to_remove]["img_idx"] + 1,
                "to_x": balls[ball_to_remove]["to_x"],
                "to_y": balls[ball_to_remove]["to_y"],
                "init_speed_y": ball_speed_y[0]
            })
            
            balls.append({
                "pos_x": balls[ball_to_remove]["pos_x"],
                "pos_y": balls[ball_to_remove]["pos_y"],
                "img_idx": balls[ball_to_remove]["img_idx"] + 1,
                "to_x": balls[ball_to_remove]["to_x"] * -1,
                "to_y": balls[ball_to_remove]["to_y"],
                "init_speed_y": ball_speed_y[0]
            })
        del balls[ball_to_remove]
        ball_to_remove = -1
        
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 5. Draw on the screen
    screen.blit(background, (0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
           
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    elasped_time = (pygame.time.get_ticks() - start_tick)/1000
    timer = game_font.render("Time: {}".format(str(int(total_time - elasped_time))), True,  (0, 0, 0))
    screen.blit(timer, (10, 10))
    
    if elasped_time > total_time:
        game_result = "Time Over"
        running = False
    elif len(balls) == 0:
        game_result = "Misson Completed"
        running = False
    
    pygame.display.update() # should be called to update screen

msg = game_font.render(game_result, True, (255, 0, 0))
msg_rect = msg.get_rect(center=(int(screen_width /2), int(screen_height/2)))
screen.blit(msg, msg_rect)
#screen.blit(msg, (screen_width / 2 - (msg.get_rect().size[0]/2), screen_height/2 - (msg.get_rect().size[1]/2) ))
pygame.display.update()
pygame.time.delay(2000)

# pygame end
pygame.quit()