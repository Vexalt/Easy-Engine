#coding: UTF-8
#~~~----Easy-Engine-Code----~~~#

VERSION = "4.0"
DEBUG_MODE = False

#Libs Importation
import random, os
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
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP,MOUSEBUTTONDOWN,MOUSEBUTTONUP])

#Caption and Icon Setup
pygame.display.set_caption('Easy Engine Version '+VERSION)
pygame.display.set_icon(pygame.image.load("icon.png"))

#Default Monitor Size
WINDOW_SIZE = (600,400)
MONITOR_RESOLUTION = (pygame.display.Info().current_w,pygame.display.Info().current_h)
fullscreen = False
mousedown = False

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
CHUNK_SIZE = 8

#Load All tile from data/blockstates
TILE_SIZE = 16
tile_database,tile_blockstates,tile_items = e.load_images(TILE_SIZE)

#Load Break Database
break_database = []
for break_image in reversed(range(1,11)):
    img = pygame.image.load("data/menu/break/dig"+str(break_image)+".png").convert_alpha()
    pygame.draw.rect(img,(255,255,255,0),(0,0,82,82),1)
    break_database.append(pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE)))

REGENERATE_DAMAGE_BLOCK_TIME = 0.1
Break_Speed = 1

#Create The Light Value used for render light with animation
light_velocity = -1

#Selector Number
Toolbar = 0

#Entity List
Entity = pygame.sprite.Group()

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
                    tile_blockstates = e.load_images(TILE_SIZE)[1]
                    #-----------TEMP-CODE-------------#

            #Change Toolbar Selecte
            elif event.scancode in [30,31,32,33,34,35,36,37,38,39]:
                Toolbar = [30,31,32,33,34,35,36,37,38,39].index(event.scancode)

            #Fullscreen Mode
            elif event.key == K_F11:
                if not fullscreen:
                    screen = pygame.display.set_mode(WINDOW_SIZE,FULLSCREEN|HWSURFACE|DOUBLEBUF|SCALED)
                else:
                    screen = pygame.display.set_mode(WINDOW_SIZE,DOUBLEBUF|SCALED)
                    screen = pygame.display.set_mode(WINDOW_SIZE,RESIZABLE|DOUBLEBUF|SCALED)
                fullscreen = not fullscreen
                screen.fill((0,0,0))
                pygame.display.update()
                    
        #Button Event Listener
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                player.moving_right = False
            if event.key == K_LEFT:
                player.moving_left = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1: mousedown = True
        elif event.type == MOUSEBUTTONUP:
            mousedown = False

    #Position Calculator
    true_scroll[0] += (player.rect.x-true_scroll[0]-225)/20
    true_scroll[1] += (player.rect.y-true_scroll[1]-150)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #Calculate Player Position
    player_pos_x  = player.rect.x-scroll[0]
    player_pos_y  = player.rect.y-scroll[1]

    #Tile_light is a list of all tile that produce light
    tile_light = [((player_pos_x,player_pos_y),0.7,(0,0,0))]
    #Tile_rects is a list of all tile that have collision
    tile_rects = []
    #Tile_blit is a list of all tile that was blit on the Player
    tile_blit = []

    #Render Distance Default Value (5,7)
    for y in range(5):
        for x in range(7):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*TILE_SIZE)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*TILE_SIZE)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = gen.generate_chunk(CHUNK_SIZE,target_x,target_y,tile_blockstates)
            for tile in game_map[target_chunk]:
                pos_x = tile[0]*TILE_SIZE-scroll[0]
                pos_y = tile[1]*TILE_SIZE-scroll[1]
                tile_data = game_map[target_chunk][tile]

                if pos_x > -16 and pos_x < 600 and pos_y > -16 and pos_y < 400: #Be sure that The tile is on the Screen
                    if tile_blockstates[tile_data["type"]]["special_blit"] == True:

            #~~~~-------------------Special Blit Code-------------------~~~~#
                        if tile_data["type"] == "plant":
                            attribute = tile_data["attribute"]
                            display.blit(tile_database["plant"],(pos_x,pos_y))
                            for plant in range(len(attribute["type"])):
                                img = tile_database[attribute["type"][plant]]
                                tile_blit.append((img,(pos_x+attribute["pos"][plant],pos_y)))
                                if tick.TICK % 20 ==  0:
                                    if attribute["type"][plant] == "plant_0":
                                        tile_data["attribute"]["type"][plant] = "plant_2"
                                    elif attribute["type"][plant] == "plant_1":
                                        tile_data["attribute"]["type"][plant] = "plant_3"
                                    elif attribute["type"][plant] == "plant_3":
                                        tile_data["attribute"]["type"][plant] = "plant_1"
                                    elif attribute["type"][plant] == "plant_2":
                                        tile_data["attribute"]["type"][plant] = "plant_0"
            #~~~~-------------------Special Blit Code-------------------~~~~#

                    else:
                        display.blit(tile_database[tile_data["type"]],(pos_x,pos_y)) #Blit the tile with type
                    
                    #If the Block have damage
                    hardness = tile_blockstates[tile_data["type"]]["hardness"]
                    if tile_data["break"] != hardness:
                        rect = tile_blockstates[tile_data["type"]]["collision_rect"]
                        display.blit(break_database[int(tile_data["break"]/hardness*10)],(pos_x+rect[2],pos_y+rect[3]),(rect[2],rect[3],rect[0],rect[1]))
                        
                        #Regenerate the Block with Time
                        tile_data["break"] += REGENERATE_DAMAGE_BLOCK_TIME
                        if tile_data["break"] > float(hardness):
                            tile_data["break"] = hardness

                if tile_blockstates[tile_data["type"]]["collision"] == True: #If collision
                    if pos_x > player_pos_x-TILE_SIZE-10 and pos_x < player_pos_x+TILE_SIZE and pos_y > player_pos_y-TILE_SIZE-10 and pos_y < player_pos_y+TILE_SIZE: #Check if the tile is nearby of the player 
                        rect = tile_blockstates[tile_data["type"]]["collision_rect"] #Get the Collision Size
                        tile_rects.append(pygame.Rect(tile[0]*TILE_SIZE+rect[2],tile[1]*TILE_SIZE+rect[3],rect[0],rect[1]))
                        
                        if DEBUG_MODE: #Color in Red the Collision Rect of the Tile
                            pygame.draw.rect(display,(169, 50, 38),(pos_x+rect[2],pos_y+rect[3],rect[0],rect[1]),2)


                if tile_data["type"] == "torch":
                    tile_light.append(((pos_x+10,pos_y+7),0.4,(243, 156, 18 )))

                #TICK Function
                tick.Tick(CHUNK_SIZE,game_map,tile,tile_data,tile_blockstates,Entity,tile_items)

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

    for tile in tile_blit:
        display.blit(tile[0],tile[1])

    #Entity And Item Engine
    true_player_rect = (player_pos_x,player_pos_y,player.rect.width,player.rect.height)

    if DEBUG_MODE:
        pygame.draw.rect(display,(31, 97, 141 ),true_player_rect,1)

    #Entity Engine
    Entity.update(game_map,CHUNK_SIZE,TILE_SIZE,scroll,player.rect,true_player_rect)
    Entity.draw(display)

    #Light Engine
    light_display.fill((0,0,0))

    #Used For an Slow Animation of the Light
    light_effect = (light_velocity**3-light_velocity)*10
    light_velocity += 0.02
    if light_velocity >= 1:
        light_velocity = -1

    for distance in reversed(range(10)):
        for light in tile_light:
            pygame.draw.circle(light_display,(0,0,0,distance*25),light[0],int(light[1]*distance*10)*distance*0.15+light_effect,int(light[1]//10))
    
    display.blit(light_display,(0,0),display_rect)
    
    #Cursor Engine
    pygame_pos = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
    original_pos = ((pygame_pos[0]+scroll[0])//TILE_SIZE , (pygame_pos[1]+scroll[1])//TILE_SIZE)
    pos = (original_pos[0]*TILE_SIZE-scroll[0],original_pos[1]*TILE_SIZE-scroll[1])

    #Get Tile rect
    info = e.get_tile_with_pos(CHUNK_SIZE,game_map,original_pos[0],original_pos[1])
    rect = tile_blockstates[info["type"]]["collision_rect"]
    pygame.draw.rect(display,(255,255,255),(pos[0]+rect[2],pos[1]+rect[3],rect[0]+1,rect[1]),1)
    
    #On Right Click = Destroy
    if mousedown and info["type"] != "air":

        #Get Tile
        tile = e.get_tile_with_pos(CHUNK_SIZE,game_map,original_pos[0],original_pos[1])
        #Try to Break the Block
        if info["break"] > 0:
            tile["break"] -= Break_Speed
        else:
            Entity.add(e.Item(original_pos[0]*TILE_SIZE,original_pos[1]*TILE_SIZE,tile_items[info["type"]]))
            tile["break"] = tile_blockstates["air"]["hardness"]
            tile["type"] = "air"

    #Toolbar
    try: tool_image = tool_image,tool_image_focus = tool_image_focus
    except:
        tool_image = pygame.image.load("data/menu/toolbar.png").convert_alpha()
        tool_image_focus = pygame.image.load("data/menu/toolbar_focus.png").convert_alpha()

    start = (WINDOW_SIZE[0] - (tool_image.get_width() * 10))//2
    for tool in range(10):
        if tool == Toolbar:display.blit(tool_image_focus,(start+tool*tool_image.get_width(),365))
        else:display.blit(tool_image,(start+tool*tool_image.get_width(),365))

    #Text Blitting
    display.blit(myfont.render("Easy Engine Version 4.0 - "+str(round(clock.get_fps())),False, (255,255,255)),(0,0))

    #Pygame End
    screen.blit(display,(0,0))
    pygame.display.update()
    clock.tick(80)