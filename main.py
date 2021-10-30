#coding: UTF-8
#pipreqs

import pygame, sys, random
import libs.engine as e
from libs import tick
from opensimplex import OpenSimplex
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

VERSION = "3.0"

pygame.display.set_caption('Easy Engine Version '+VERSION)
pygame.display.set_icon(pygame.image.load("icon.png"))

WINDOW_SIZE = (600,400)
MONITOR_RESOLUTION = (pygame.display.Info().current_w,pygame.display.Info().current_h)

screen = pygame.display.set_mode(WINDOW_SIZE,RESIZABLE|DOUBLEBUF|SCALED) # initiate the window

display = pygame.Surface(WINDOW_SIZE) # used as the surface for rendering, which is scaled
display_pos = (0,0)
display_rect = pygame.Rect(0,0,600,400)

light_display = pygame.Surface((700,500), pygame.SRCALPHA)

player = e.Player((100,100,5,13))

true_scroll = [0,0]

CHUNK_SIZE = 6

SEED = random.randint(-999999,999999)
noise = OpenSimplex(SEED)
random.seed(SEED)

def generate_chunk(x,y):
    scale = 10

    chunk_data = {}
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            value = int(noise.noise2d(target_x*0.1,0)*scale)

            tile_type = "air"
            attribute = {}
            if target_y > 8 - value: tile_type="dirt"

            elif target_y == 8 - value:
                tile_type="grass"

            elif target_y == 8 - value -1:
                if random.randint(1,5) > 1:
                    tile_type="plant"
                elif random.randint(1,3) == 1: 
                    tile_type="torch"

            chunk_data[target_x,target_y] = {"type":tile_type,"attribute":attribute}
    return chunk_data

game_map = {}

TILE_SIZE = 20
tile_database = e.load_images(TILE_SIZE)
tile_blockstates = e.load_blockstates()

TICK = 0

myfont = pygame.font.Font('data/fonts/font.ttf', 10)

ambiant_music = pygame.mixer.music.load("data/sounds/musics/ambiant.mp3")
pygame.mixer.music.play(-1)

fullscreen = False
#background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

while True: # game loop

    true_scroll[0] += (player.rect.x-true_scroll[0]-225)/20
    true_scroll[1] += (player.rect.y-true_scroll[1]-150)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    player_pos_x  = player.rect.x-scroll[0]
    player_pos_y  = player.rect.y-scroll[1]

    #pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    #for background_object in background_objects:
        #obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        #if background_object[0] == 0.5:
            #pygame.draw.rect(display,(20,170,150),obj_rect)
        #else:
            #pygame.draw.rect(display,(15,76,73),obj_rect)

    tile_light = [((player_pos_x,player_pos_y),0.7,(0,0,0))]
    tile_rects = []
    for y in range(5):
        for x in range(7):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*TILE_SIZE)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*TILE_SIZE)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in game_map[target_chunk]:
                pos_x = tile[0]*TILE_SIZE-scroll[0]
                pos_y = tile[1]*TILE_SIZE-scroll[1]
                tile_data = game_map[target_chunk][tile]
                if pos_x > -16 and pos_x < 600 and pos_y > -16 and pos_y < 400:
                    display.blit(tile_database[tile_data["type"]],(pos_x,pos_y))

                if tile_blockstates[tile_data["type"]]["collision"] == True:
                    if pos_x > player_pos_x-TILE_SIZE-10 and pos_x < player_pos_x+TILE_SIZE and pos_y > player_pos_y-TILE_SIZE-10 and pos_y < player_pos_y+TILE_SIZE:
                        tile_rects.append(pygame.Rect(tile[0]*TILE_SIZE,tile[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))
                        #pygame.draw.rect(display,(200,200,200),(pos_x,pos_y,TILE_SIZE,TILE_SIZE))

                if tile_data["type"] == "torch":
                    tile_light.append(((pos_x+10,pos_y+7),0.4,(243, 156, 18 )))
                if TICK == 0:
                    tick.Tick(CHUNK_SIZE,game_map,tile,tile_data,tile_blockstates)

    TICK +=1
    if TICK == 5:
        TICK = 0

    if player.movement[0] == 0:
        player.change_action(player.action,player.frame,'idle')
    if player.movement[0] > 0:
        player.flip = False
        player.change_action(player.action,player.frame,'run')
    if player.movement[0] < 0:
        player.flip = True
        player.change_action(player.action,player.frame,'run')

    player.move(tile_rects)

    display.blit(player.get_image(),(player_pos_x,player_pos_y))

    light_display.fill((0,0,0))

    for distance in reversed(range(10)):
        for light in tile_light:
            pygame.draw.circle(light_display,(0,0,0,distance*25),light[0],int(light[1]*distance*10)*distance*0.2,int(light[1]//10))

    display.blit(light_display,(0,0),display_rect)

    display.blit(myfont.render("Easy Engine Version 3.0 - "+str(round(clock.get_fps())),False, (255,255,255)),(0,0))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.moving_right = True
            if event.key == K_LEFT:
                player.moving_left = True
            if event.key == K_UP:
                if player.air_timer < 6:
                    player.vertical_momentum = -5

            if event.key == K_F11:
                if not fullscreen:
                    screen = pygame.display.set_mode(WINDOW_SIZE,FULLSCREEN|HWSURFACE|DOUBLEBUF|SCALED)
                    screen.fill((0,0,0))
                    fullscreen = True
                    pygame.display.update()
                else:
                    screen = pygame.display.set_mode(WINDOW_SIZE,RESIZABLE|DOUBLEBUF|SCALED)
                    screen = pygame.display.set_mode(WINDOW_SIZE,RESIZABLE|DOUBLEBUF|SCALED)
                    fullscreen = False
                    screen.fill((0,0,0))
                    pygame.display.update()


        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.moving_right = False
            if event.key == K_LEFT:
                player.moving_left = False

        #Window Resize Event
        if event.type == WINDOWRESIZED:
            screen.fill((0,0,0))
            s = pygame.display.get_window_size()
            print(s[0]//2,s[1]//2)
            pygame.display.update()
        
    screen.blit(display,(0,0))
    pygame.display.update()
    clock.tick(80)
