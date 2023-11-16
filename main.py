# dit spel is gemaakt door:
# - Daan van Middendorp

from typing import Any
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # call the __init__ function of the Sprite class
        player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha() # load the image player_walk_1.png with transparency
        player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha() # load the image player_walk_1.png with transparency
        self.player_walk = [player_walk1, player_walk2] # create a list with the player_walk1 and player_walk2 surf
        self.player_index = 0 # create a variable to store the player index
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha() # load the image jump.png with transparency

        self.image = self.player_walk[self.player_index] # create a variable to store the player surf
        self.rect = self.image.get_rect(midbottom = (80, 300)) # create a rectangle around the player surf
        self.gravity = 0 # create a variable to store the gravity value

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3") # load the sound jump.mp3
        self.jump_sound.set_volume(0.5) # set the volume of the sound to 0.5

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300: 
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly": # if the type is fly
            fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else: # if the type is snail
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        self.animation_index = 0 # create a variable to store the animation index
        self.image = self.frames[self.animation_index] # create a variable to store the obstacle surf
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos)) # create a rectangle around the obstacle surf
    
    def animation_state(self):
        self.animation_index += 0.1  # increase the animation_index value
        if self.animation_index >= len(self.frames): self.animation_index = 0 # if the animation_index is bigger than the length of the frames list set the animation_index to 0
        self.image = self.frames[int(self.animation_index)] # create a variable to store the obstacle surf

    def update(self):
        self.animation_state()
        self.rect.x -= 6 # move the obstacle to the left
        self.destroy() # call the destroy function
    
    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time # calculate the current time / 1000 to get the seconds
    score_surf = score_font.render(f'Score: {current_time}', False, (64,64,64)) # create a surf with text on it
    score_rect = score_surf.get_rect(center = (400, 50)) # create a rectangle around the text surf
    screen.blit(score_surf, score_rect) # draw the text surf on the screen
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list: # if the obstacle_list is not empty
        for obstacle_rect in obstacle_list: # loop through the obstacle_list
            obstacle_rect.x -= 5 # move the obstacle to the left

            if obstacle_rect.bottom == 300: # if the obstacle is a snail
                screen.blit(snail_surf, obstacle_rect) # draw the snail surf on the screen
            else: # if the obstacle is a fly
                screen.blit(fly_surf, obstacle_rect) # draw the fly surf on the screen
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # remove the obstacle from the list if it is off the screen

        return obstacle_list # return the obstacle_list
    else: # if the obstacle_list is empty
        return [] # return an empty list

def collissions(player, obstacles):
    if obstacles: # if the obstacles list is not empty
        for obstacle_rect in obstacles: # loop through the obstacles list
            if player.colliderect(obstacle_rect): # if the player collides with an obstacle
                return False # return False to end the game and chage game state
    return True # return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): # if the player collides with an obstacle
        obstacle_group.empty() # empty the obstacle_group sprite group
        return False # return False to end the game and chage game state
    else: # if the player does not collide with an obstacle
        return True # return True

def player_animation():
    global player_surf, player_index # make the player_surf and player_index variables global

    if player_rect.bottom < 300: # if the player is not on the ground
        player_surf = player_jump # set the player_surf to the player_jump surf
    else: # if the player is on the ground
        player_index += 0.1 # increase the player_index value
        if player_index >= len(player_walk): # if the player_index is bigger than the length of the player_walk list
            player_index = 0 # set the player_index to 0
        player_surf = player_walk[int(player_index)] # set the player_surf to the player_walk surf with the player_index as index

    # player_surf = player_walk[player_index] # set the player_surf to the player_walk surf with the player_index as index


pygame.init() # initialize pygame
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner") # set the title of the window
clock = pygame.time.Clock() # create a clock object
score_font = pygame.font.Font("font/Pixeltype.ttf", 50) # create a font object
game_active = True # create a variable to store if the game is active or not
start_time = 0 # create a variable to store the start time
score = 0 # create a variable to store the score
background_music = pygame.mixer.Sound("audio/music.wav") # load the sound music.wav
background_music.play(loops = -1) # play the sound infinite times
background_music.set_volume(0.5) # set the volume of the sound to 0.5

# groups
player = pygame.sprite.GroupSingle() # create a sprite group for the player
player.add(Player()) # add the player to the sprite group

obstacle_group = pygame.sprite.Group() # create a sprite group for the obstacles

sky_surf = pygame.image.load("graphics/Sky.png").convert() # load the image
ground_surf = pygame.image.load("graphics/ground.png").convert() # load the image

# obstacles
#snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha() # load the image snail1.png with transparency
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha() # load the image snail2.png with transparency
snail_frames = [snail_frame_1, snail_frame_2] # create a list with the snail_frame_1 and snail_frame_2 surf
snail_frame_index = 0 # create a variable to store the snail frame index
snail_surf = snail_frames[snail_frame_index] # create a variable to store the snail surf

#fly
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha() # load the image Fly1.png with transparency
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha() # load the image Fly2.png with transparency
fly_frames = [fly_frame_1, fly_frame_2] # create a list with the fly_frame_1 and fly_frame_2 surf
fly_frame_index = 0 # create a variable to store the fly frame index
fly_surf = fly_frames[fly_frame_index] # create a variable to store the fly surf

obstacle_rect_list = [] # create a list to store the obstacles

player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha() # load the image player_walk_1.png with transparency
player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha() # load the image player_walk_1.png with transparency
player_walk = [player_walk1, player_walk2] # create a list with the player_walk1 and player_walk2 surf
player_index = 0 # create a variable to store the player index
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha() # load the image jump.png with transparency

player_surf = player_walk[player_index] # create a variable to store the player surf
player_rect = player_surf.get_rect(midbottom = (80, 300)) # create a rectangle around the player surf
player_gravity = 0 # create a variable to store the gravity value

# game over screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha() # load the image player_stand.png with transparency
player_stand = pygame.transform.rotozoom(player_stand, 0,2) # scale the image up 2 times no rotation
player_stand_rect = player_stand.get_rect(center = (400, 200)) # create a rectangle around the player_stand surf

game_name = score_font.render("Pixel Runner", False, (111,196,169)) # create a surf with text on it
game_name_rect = game_name.get_rect(center = (400, 80)) # create a rectangle around the text surf

game_message = score_font.render("Press space to run", False, (111,196,169)) # create a surf with text on it
game_message_rect = game_message.get_rect(center = (400, 330)) # create a rectangle around the text surf

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    # draw all our ellements
    # update all our ellements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active: # if the game is active
            if event.type == pygame.MOUSEBUTTONDOWN: # if the mouse button is down
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300: # if the mouse is on the player
                    player_gravity = -20 # set the gravity value to -20

            if event.type == pygame.KEYDOWN: # if a key is down
                if event.key == pygame.K_SPACE and player_rect.bottom == 300: # if the key is the space bar
                    player_gravity = -20 # set the gravity value to -20
        else: # if the game is not active
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True # set the game to active
                start_time = int(pygame.time.get_ticks() / 1000)  # set the start time / 1000 to get the seconds
               # score = 0 # set the score to 0

        if game_active:
            if event.type == obstacle_timer :
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail']))) # add a fly to the obstacle_group
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300))) # add a snail to the obstacle_rect_list
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210))) # add a snail to the obstacle_rect_list

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
        

    #game part
    if game_active: # if the game is active
        # draw all our ellements
        screen.blit(sky_surf, (0, 0)) # draw the sky surf on the screen
        screen.blit(ground_surf, (0, 300)) # draw the ground surf on the screen
        score = display_score()

        player.draw(screen) # draw the player sprite on the screen
        player.update() # update the player sprite

        obstacle_group.draw(screen) # draw the obstacle_group on the screen
        obstacle_group.update()

        #obstacles movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list) # call the obstacle_movement function and store the return value in the obstacle_rect_list variable

        # collision
        game_active = collision_sprite()
        #game_active = collissions(player_rect, obstacle_rect_list) # call the collissions function and store the return value in the game_active variable


    #start/menu
    else:
        screen.fill((94,129,162)) # fill the screen with a color
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = score_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
        
    
    pygame.display.update() # Update the screen
    clock.tick(60) # 60 frames per second loop cant go faster than 60 frames per second