#coding: UTF-8
#~~~----Easy-Engine-Code----~~~#

VERSION = "4.0"
DEBUG_MODE = False

#Libs Importation
import pygame, sys
import libs.engine as e
import libs.tick as tick
import libs.generation as gen
clock = pygame.time.Clock()

#Pygame Init
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

#Prevent Spam Event
pygame.event.set_blocked(None)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

#Caption and Icon Setup
pygame.display.set_caption('Easy Engine Version '+VERSION)
pygame.display.set_icon(pygame.image.load("icon.png"))

#Default Monitor Size
WINDOW_SIZE = (600,400)
MONITOR_RESOLUTION = (pygame.display.Info().current_w,pygame.display.Info().current_h)
fullscreen = False

#Initiate the window
screen = pygame.display.set_mode(WINDOW_SIZE,RESIZABLE|DOUBLEBUF|SCALED)

#Used as the surface for rendering, which is scaled
display = pygame.Surface(WINDOW_SIZE)
display_pos = (0,0)
display_rect = pygame.Rect(0,0,600,400)

#The equivalent of display but for light render
light_display = pygame.Surface((700,500), pygame.SRCALPHA)

#Setup Player
player = e.Player((100,100,5,13))

#Set the Coordinate of the Player
true_scroll = [0,0]

#Setup Map Dict and Chunk Size
game_map = {}
CHUNK_SIZE = 6

#Load All tile from data/blockstates
TILE_SIZE = 20
tile_database,tile_blockstates = e.load_images(TILE_SIZE)

#Create The Light Value used for render light with animation
light_velocity = -1

#--------------------------------TEMP CODE------------------------------------#
myfont = pygame.font.Font('data/fonts/font.ttf', 10)

ambiant_music = pygame.mixer.music.load("data/sounds/musics/ambiant.mp3")
pygame.mixer.music.play(-1)
#-------------------------------TEMP CODE END---------------------------------#

#Game Loop
while 1:

    #Event Loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.moving_right = True
            elif event.key == K_LEFT:
                player.moving_left = True
            elif event.key == K_UP:
                if player.air_timer < 6:
                    player.vertical_momentum = -5
            elif event.key == K_d:
                DEBUG_MODE = not DEBUG_MODE
                if DEBUG_MODE:
                    #-----------TEMP-CODE-------------#
                    tile_database,tile_blockstates = e.load_images(TILE_SIZE)
                    #-----------TEMP-CODE-------------#
            elif event.key == K_F11:
                if not fullscreen:
                    screen = pygame.display.set_mode(WINDOW_SIZE,FULLSCREEN|HWSURFACE|DOUBLEBUF|SCALED)
                    screen.fill((0,0,0))
                    fullscreen = True
                    pygame.display.update()
                else:
                    screen = pygame.display.set_mode(WINDOW_SIZE,DOUBLEBUF|SCALED)
                    screen = pygame.display.set_mode(WINDOW_SIZE,RESIZABLE|DOUBLEBUF|SCALED)
                    fullscreen = False
                    screen.fill((0,0,0))
                    pygame.display.update()
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                player.moving_right = False
            if event.key == K_LEFT:
                player.moving_left = False
        #Be Sure That the screen is dark
        elif event.type == WINDOWRESIZED:
            screen.fill((0,0,0))

    #Position Calculator
    true_scroll[0] += (player.rect.x-true_scroll[0]-225)/20
    true_scroll[1] += (player.rect.y-true_scroll[1]-150)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    player_pos_x  = player.rect.x-scroll[0]
    player_pos_y  = player.rect.y-scroll[1]

    #Tile_light is a list of all tile that produce light
    tile_light = [((player_pos_x,player_pos_y),0.7,(0,0,0))]

    #Tile_rects is a list of all tile that have collision
    tile_rects = []

    #Render Distance Default Value (5,7)
    for y in range(5):
        for x in range(7):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*TILE_SIZE)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*TILE_SIZE)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = gen.generate_chunk(CHUNK_SIZE,target_x,target_y)
            for tile in game_map[target_chunk]:
                pos_x = tile[0]*TILE_SIZE-scroll[0]
                pos_y = tile[1]*TILE_SIZE-scroll[1]
                tile_data = game_map[target_chunk][tile]
                if pos_x > -16 and pos_x < 600 and pos_y > -16 and pos_y < 400: #Be sure that The tile is on the Screen
                    display.blit(tile_database[tile_data["type"]],(pos_x,pos_y)) #Blit the tile with type
                if tile_blockstates[tile_data["type"]]["collision"] == True: #If collision
                    if pos_x > player_pos_x-TILE_SIZE-10 and pos_x < player_pos_x+TILE_SIZE and pos_y > player_pos_y-TILE_SIZE-10 and pos_y < player_pos_y+TILE_SIZE: #Check if the tile is nearby of the player 
                        rect = tile_blockstates[tile_data["type"]]["collision_rect"] #Get the Collision Size
                        tile_rects.append(pygame.Rect(tile[0]*TILE_SIZE+rect[2],tile[1]*TILE_SIZE+rect[3],rect[0],rect[1]))
                        
                        if DEBUG_MODE: #Color in Red the Collision Rect of the Tile
                            pygame.draw.rect(display,(169, 50, 38),(pos_x+rect[2],pos_y+rect[3],rect[0],rect[1]),2)


                if tile_data["type"] == "torch":
                    tile_light.append(((pos_x+10,pos_y+7),0.4,(243, 156, 18 )))

                #TICK Function
                tick.Tick(CHUNK_SIZE,game_map,tile,tile_data,tile_blockstates)

    #Add A tick
    tick.add_tick()

    #Update Movement Animation Of the Player
    if player.movement[0] == 0:
        player.change_action(player.action,player.frame,'idle')
    if player.movement[0] > 0:
        player.flip = False
        player.change_action(player.action,player.frame,'run')
    if player.movement[0] < 0:
        player.flip = True
        player.change_action(player.action,player.frame,'run')

    #Change Pos of the Player
    player.move(tile_rects)
    display.blit(player.get_image(),(player_pos_x,player_pos_y))

    light_display.fill((0,0,0))

    #Used For an Slow Animation of the Light
    light_effect = (light_velocity**3-light_velocity)*5
    light_velocity += 0.02
    if light_velocity >= 1:
        light_velocity = -1

    for distance in reversed(range(10)):
        for light in tile_light:
            pygame.draw.circle(light_display,(0,0,0,distance*25),light[0],int(light[1]*distance*10)*distance*0.15+light_effect,int(light[1]//10))

    display.blit(light_display,(0,0),display_rect)

    display.blit(myfont.render("Easy Engine Version 3.0 - "+str(round(clock.get_fps())),False, (255,255,255)),(0,0))
        
    screen.blit(display,(0,0))
    pygame.display.update()
    clock.tick(80)

