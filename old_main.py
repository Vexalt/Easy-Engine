#coding: UTF-8
#============================Main.py=====================================#
# auto-py-to-exe
from typing import Generator
import pygame
from sys import exit
from random import randint, choice, seed
from pygame.locals import *
from opensimplex import OpenSimplex #noise

if __name__ != '__main__':
    exit()

#Global Value
WINDOW_SIZE = (1200,800)
CHUNK_SIZE = 9
TILE_SIZE = 16
CURSOR_SIZE = 18
RENDER_DISTANCE = 6
SEED = randint(-999999,999999)
TIME = 15
TICK = 12
noise = OpenSimplex(seed=SEED)
print("SEED : "+ str(SEED))
seed(SEED)

global animation_frames
animation_frames = {}

#Initiation of library
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.mixer.set_num_channels(64)
pygame.display.set_caption('Infinity Game')
screen = pygame.display.set_mode(WINDOW_SIZE,RESIZABLE|HWSURFACE| DOUBLEBUF)


#Importation of data
Data_feature = {"grass": {"colision":True , "rotation":False,"flip":True,"size":False,"ground":False,"special":False,"background":False},
    "grass_left": {"colision":True , "rotation":False,"flip":False,"size":False,"ground":False,"special":False,"background":False},
    "grass_right": {"colision":True , "rotation":False,"flip":False,"size":False,"ground":False,"special":False,"background":False},
    "dirt_corner_left": {"colision":True , "rotation":False,"flip":False,"size":False,"ground":False,"special":False,"background":False},
    "dirt_corner_right": {"colision":True , "rotation":False,"flip":False,"size":False,"ground":False,"special":False,"background":False},
    "dirt_corner_middle": {"colision":True , "rotation":False,"flip":False,"size":False,"ground":False,"special":False,"background":False},
    "grass_middle": {"colision":True , "rotation":False,"flip":False,"size":False,"ground":False,"special":False,"background":False},


    "dirt": {"colision":True , "rotation":True,"flip":False,"size":False,"ground":False,"special":False,"background":False},
    "air": {"colision":False , "rotation":False,"flip":False,"size":False,"ground":False,"special":True,"background":False},
    "stone": {"colision":True , "rotation":True,"flip":False,"size":False,"ground":False,"special":False,"background":False},
    "leaves": {"colision":False , "rotation":True,"flip":False,"size":False,"ground":False,"special":False,"background":False},
    
    
    #Plant Group
    "plant": {"colision":False , "rotation":False,"flip":False,"size":True,"ground":True,"special":True,"background":False},
    "plant_0": {"colision":False , "rotation":False,"flip":False,"size":True,"ground":True,"special":True,"background":False},
    "plant_1": {"colision":False , "rotation":False,"flip":False,"size":True,"ground":True,"special":True,"background":False},
    "plant_2": {"colision":False , "rotation":False,"flip":False,"size":True,"ground":True,"special":True,"background":False},
    "plant_3": {"colision":False , "rotation":False,"flip":False,"size":True,"ground":True,"special":True,"background":False},
    }

Data_image = {}
Temp_value = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
def Initialisation(images):
    Data_image["air"] = []
    for alpha in reversed(Temp_value):
        temp_rect = pygame.Surface((TILE_SIZE,TILE_SIZE))
        temp_rect.fill((0,0,0))
        temp_rect.set_alpha((alpha*220)/16)
        Data_image["air"].append(temp_rect)

    for image_name in images:
        Data_image[image_name] = []
        try:images[image_name] = pygame.image.load(images[image_name]).convert_alpha()
        except: print(image_name)
        images[image_name] = pygame.transform.smoothscale(images[image_name],(TILE_SIZE,TILE_SIZE))
        
        #Initialisation all possible image with light
        for alpha in range(16):
                temp_img = images[image_name].copy()
                alpha_color = (alpha*255)//15
                temp_img.fill((alpha_color,alpha_color,alpha_color), special_flags=pygame.BLEND_RGBA_MULT)#BLEND_RGB_ADD
                Data_image[image_name].append([])

                if Data_feature[image_name]["background"] is True:
                    temp_rect = pygame.Surface((TILE_SIZE,TILE_SIZE), pygame.SRCALPHA)
                    temp_rect.fill((0,0,0,(list(reversed(Temp_value))[alpha]*220)/16))
                    temp_rect.blit(temp_img,(0,0), special_flags=pygame.BLEND_RGBA_ADD)
                    temp_img = temp_rect.copy()
                if Data_feature[image_name]["rotation"] is True:
                    for rot in range(4):
                        Data_image[image_name][alpha].append(pygame.transform.rotate(temp_img, rot * 90))
                
                elif Data_feature[image_name]["flip"] is True:
                    Data_image[image_name][alpha].append(pygame.transform.flip(temp_img,True,False))
                    Data_image[image_name][alpha].append(pygame.transform.flip(temp_img,True,False))
                    Data_image[image_name][alpha].append(temp_img)
                    Data_image[image_name][alpha].append(temp_img)
                elif Data_feature[image_name]["size"] is True:
                    Data_image[image_name][alpha].append(temp_img)
                    Data_image[image_name][alpha].append(temp_img)
                    Data_image[image_name][alpha].append(pygame.transform.smoothscale(temp_img,(TILE_SIZE-5,TILE_SIZE)))
                    Data_image[image_name][alpha].append(pygame.transform.smoothscale(temp_img,(TILE_SIZE-5,TILE_SIZE)))
                else:
                    for i in range(4):
                        Data_image[image_name][alpha].append(temp_img)

Data_sound = {"jump" : pygame.mixer.Sound('musics/jump.wav'),
    "grass_sounds" : (pygame.mixer.Sound('musics/grass_0.wav'), pygame.mixer.Sound('musics/grass_1.wav')),
    }

#Initialisation of data
Initialisation({
    #Grass Group
    "grass":"data/grass/grass.png",
    "grass_left":"data/grass/grass_left.png",
    "grass_right":"data/grass/grass_right.png",
    "dirt_corner_left":"data/grass/grass_corner_left.png",
    "dirt_corner_right":"data/grass/grass_corner_right.png",
    "dirt_corner_middle":"data/grass/grass_corner_middle.png",
    "grass_middle":"data/grass/grass_middle.png",


    "dirt":"data/dirt.png",
    "stone":"data/stone.png",

    #Plant Group
    "plant_0":"data/plants/plant_0.png",
    "plant_1":"data/plants/plant_1.png",
    "plant_2":"data/plants/plant_2.png",
    "plant_3":"data/plants/plant_3.png",
})

#Default Value
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
display = pygame.Surface((600,400))

game_map = {}
grass_sound_timer = 0

cursor_pos = (0,0)
size = 1
center = WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2
mousepress = False

Cursor = pygame.image.load('data/cursor.png').convert_alpha()
Cursor = pygame.transform.smoothscale(Cursor,(CURSOR_SIZE,CURSOR_SIZE))

Data_sound["grass_sounds"][0].set_volume(0.2)
Data_sound["grass_sounds"][1].set_volume(0.2)

#Ambiant Music
pygame.mixer.music.load('musics/music.wav')
########################################################pygame.mixer.music.play(-1)

#Generation Value
scale = 5

#Function
def generate_chunk(x,y):
    chunk_data = {}

    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos 
            tile_type = "air" # nothing
            value = int(noise.noise2d(target_x*0.1,0)*scale)
            if target_y > 11 - value: tile_type="stone"
            elif target_y > 8 - value: tile_type="dirt"

            elif target_y == 8 - value: tile_type="grass"

            elif target_y == 8 - value -1:
                if randint(1,5) > 1: tile_type="plant"

            elif target_y < 8 - value -1: tile_type= "sky_air"

            if tile_type == "sky_air": chunk_data[(target_x,target_y)] = ["air",16,0]

            elif tile_type == "plant": chunk_data[(target_x,target_y)] = ["plant",0,{}]

            elif tile_type == "grass" or tile_type == "dirt" : chunk_data[(target_x,target_y)] = ["grass",0,randint(0,3),[False,False,False,False]]


            else: chunk_data[(target_x,target_y)] = [tile_type,0,randint(0,3)]
                #chunk_data.append([[target_x,target_y],tile_type,randint(0,15),randint(0,3)])
    return chunk_data

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert_alpha()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text

#Animation Setup
animation_database = {}

animation_database['run'] = load_animation('player_animations/run',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[7,7,40])

player_action = 'idle'
player_frame = 0
player_flip = False

#Movement Function
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile): hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right' : False, 'left' : False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect , collision_types , hit_list

#Movement Setup
moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

scroll = [0,0]
true_scroll = [0,0]

player_rect = pygame.Rect(100,100,5,13)

#Background Objects
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

#Reduce Lag
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
save_size = 0
original_pos = 0,0

tick_delay = 0
pos_height = 0

Possible_Action = ["x+1","x-1","y-1","y+1","reset"]
#Tick_Action = Possible_Action[0]
Tick_Action = "reset"

#Light Code
def Get_info(chunk_x,chunk_y,x,y,type):
    try: return game_map[str(chunk_x) + ';' + str(chunk_y)][(x,y)]
    except KeyError:
        #chunk_x = int(str(x / CHUNK_SIZE)[:str(x / CHUNK_SIZE).find('.')])
        #chunk_y = int(str(y / CHUNK_SIZE)[:str(y / CHUNK_SIZE).find('.')])
        temp_chunk = None
        if type =="x+1": temp_chunk = str(chunk_x+1) + ';' + str(chunk_y)
        elif type == "x-1": temp_chunk = str(chunk_x-1) + ';' + str(chunk_y)
        elif type == "y+1": temp_chunk = str(chunk_x) + ';' + str(chunk_y+1)
        elif type == "y-1": temp_chunk = str(chunk_x) + ';' + str(chunk_y-1)

        try:
            if (x,y) in game_map[temp_chunk].keys(): return game_map[temp_chunk][(x,y)]
        except:
            pass
        
        return "error"

def Light_Tick():
    if value[1] != 16: value[1] = 0

    info = Get_info(target_x,target_y,tile[0],tile[1]-1,"y-1") #Up
    if not info == "error":
        if value[1] == 16 and info[1] != 16: value[1] = 15

        if Data_feature[info[0]]["colision"] == False:
            if info[1]-1 > value[1]: value[1] = info[1]-2
            if info[1] != 16 and value[1] == 16: value[1] == 15
            if value[0][:5] == "grass": value[3][2] = True
            #elif value[0][:4] == "dirt": value[3][2] = "air"
                
        else:
            if info[1]-3 > value[1]: value[1] = info[1]-3
            if value[0][:5] == "grass": value[3][2] = False
            #elif value[0][:4] == "dirt": value[3][2] = info[0]
        
    info = Get_info(target_x,target_y,tile[0]+1,tile[1],"x+1") #Right
    if not info == "error":
        if Data_feature[info[0]]["colision"] == False:
            if info[1]-1 > value[1]: value[1] = info[1]-2
            if value[0][:5] == "grass": value[3][0] = True
            #elif value[0][:4] == "dirt": value[3][0] = "air"    
        else:
            if info[1]-3 > value[1]: value[1] = info[1]-3
            if value[0][:5] == "grass": value[3][0] = False
            #elif value[0][:4] == "dirt": value[3][0] = info[0]

    info = Get_info(target_x,target_y,tile[0]-1,tile[1],"x-1") #Left
    if not info == "error":
        if Data_feature[info[0]]["colision"] == False:
            if info[1]-1 > value[1]: value[1] = info[1]-2
            if value[0][:5] == "grass": value[3][1] = True
            #elif value[0][:4] == "dirt": value[3][1] = "air"
                
        else:
            if info[1]-3 > value[1]: value[1] = info[1]-3
            if value[0][:5] == "grass": value[3][1] = False
            #elif value[0][:4] == "dirt": value[3][1] = info[0]

    info = Get_info(target_x,target_y,tile[0],tile[1]+1,"y+1") #Down
    if info != "error":  

        if Data_feature[info[0]]["colision"] == False:
            if value[1] == 16: info[1] = 16
            if info[1]-1 > value[1]: value[1] = info[1]-2
            if value[0][:5] == "grass": value[3][3] = True
            #if value[0][:5] == "wood_" and info[0][:5] != "wood_" and value[0][:11] == "wood_branch": value[0] = "air"
                
        else:
            if info[1]-3 > value[1]: value[1] = info[1]-3
            if value[0][:5] == "grass": value[3][3] = False

        if Data_feature[value[0]]['ground'] == True and Data_feature[info[0]]["colision"] == False: value[0] = "air"

    if value[0][:5] == "grass":
        if value[3][0] == True and value[3][1] == True: value[0] = "grass_middle"
        elif value[3][0] == True: value[0] = "grass_right"
        elif value[3][1] == True: value[0] = "grass_left"
        else: value[0] = "grass"
        if value[3][2] == False:
            value[0] = "dirt"
            value[3] = ["air","air","air","air"]
        if value[3][3] == True: value[0] = "grass"
    """if value[0][:4] == "dirt":
        if value[3][2] == "grass_middle": value[0] = "dirt_corner_middle"
        elif value[3][2] == "grass_right": value[0] = "dirt_corner_right"
        elif value[3][2] == "grass_left": value[0] = "dirt_corner_left"
        elif value[3][2][:5] != "grass": value[0] = "dirt"
        if value[0] == "dirt":
            if value[3][0][:5] == "grass" or value[3][1][:5] == "grass":
                if randint(0,50) == 50 and value[3][2] == "air": value[0] = "grass"
            if value[3][0][:5] == "dirt_" or value[3][1][:5] == "dirt_":
                if randint(0,50) == 50 and value[3][2] == "air": value[0] = "grass"""

def Change(chunk_x,chunk_y,x,y,block):
    try:
        game_map[str(chunk_x) + ';' + str(chunk_y)][(x,y)][0] = block
        game_map[str(chunk_x) + ';' + str(chunk_y)][(x,y)][2] = randint(0,3)
    except KeyError:
        temp_chunk = []
        temp_chunk.append((chunk_x-1 , chunk_y))
        temp_chunk.append((chunk_x , chunk_y+1))
        temp_chunk.append((chunk_x-1 , chunk_y+1))
        temp_chunk.append((chunk_x-1 , chunk_y-1))
        temp_chunk.append((chunk_x+1 , chunk_y))
        temp_chunk.append((chunk_x , chunk_y-1))
        temp_chunk.append((chunk_x+1 , chunk_y+1))
        temp_chunk.append((chunk_x+1 , chunk_y-1))
        temp_value = False
        for chunk in temp_chunk:
            try:
                if (x,y) in game_map[str(chunk[0]) + ";"+str(chunk[1])]: pass
            except KeyError:
                game_map[str(chunk[0]) + ";"+str(chunk[1])] = generate_chunk(chunk[0],chunk[1])
            if (x,y) in game_map[str(chunk[0]) + ";"+str(chunk[1])]:
                game_map[str(chunk[0]) + ";"+str(chunk[1])][(x,y)][0] = block
                game_map[str(chunk[0]) + ";"+str(chunk[1])][(x,y)][2] = randint(0,3)
                break

#Running Game
while 1:
    display.fill((146,244,255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (player_rect.x-scroll[0]-(WINDOW_SIZE[0]/4))/20 #20 is the time for the camera follow the movement
    true_scroll[1] += (player_rect.y-scroll[1]-(WINDOW_SIZE[1]/4))/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    #for background_object in background_objects:
        #obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        #if background_object[0] == 0.5:
            #pygame.draw.rect(display,(14,222,150),obj_rect)
        #else:
            #pygame.draw.rect(display,(9,91,85),obj_rect)

    tile_rects = []
    for y in range(RENDER_DISTANCE):
        for x in range(RENDER_DISTANCE):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*TILE_SIZE)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*TILE_SIZE)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)

            for tile, value in game_map[target_chunk].items():

                if value[0] == "tree":
                    value[0] = "wood_ground"
                    for i in range(randint(10,15)):
                        if i != 0:
                            if randint(0,3) == 3:
                                if randint(0,1) == 0:
                                    Change(target_x,target_y,tile[0],tile[1]-i,"wood_branch_right")
                                    Change(target_x,target_y,tile[0]+1,tile[1]-i,"wood_branch_right_0")
                                    Change(target_x,target_y,tile[0]+2,tile[1]-i,"wood_branch_right_1")
                                    Change(target_x,target_y,tile[0]+3,tile[1]-i,"wood_branch_right_leaves")

                                else:
                                    Change(target_x,target_y,tile[0],tile[1]-i,"wood_branch_left")
                            else:
                                Change(target_x,target_y,tile[0],tile[1]-i,"wood_"+str(randint(0,4)))

                #Do Tick Event
                if tick_delay == 0: Light_Tick()

                #Render Tile
                coordinate = (tile[0]*TILE_SIZE-scroll[0],tile[1]*TILE_SIZE-scroll[1])
                if mousepress and tile[0] == original_pos[0] and tile[1] == original_pos[1]:
                        value[0] = "dirt"
                        if value[1] == 16: value[1] = 15
                        value[2] = randint(0,3)
                if Data_feature[value[0]]["special"] == False:
                    rect = pygame.Rect(tile[0]*TILE_SIZE,tile[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE)
                    if not value[1] == 16: display.blit(Data_image[value[0]][value[1]][value[2]],coordinate)
                    else: display.blit(Data_image[value[0]][15][value[2]],coordinate)
                    if Data_feature[value[0]]["colision"] is True and x > 1 and x < 5 and y > 0 and y < 4: tile_rects.append(rect)
                else:
                    if value[0] == "air":
                        if value[1] != 16: display.blit(Data_image["air"][value[1]],coordinate)

                    elif value[0] == "plant":    
                            if len(value[2]) == 0:
                                value[2] = []
                                for i in range(6): value[2].append(["plant_"+str(randint(0,3)),i*(16/6)-2,randint(0,3),randint(0,5),0.5])
                                
                            
                            for plant_value in value[2]:
                                plant_value[3] += plant_value[4]
                                if plant_value[3] > 10: plant_value[4] =  -0.5
                                if plant_value[3] < 0: plant_value[4] =  0.5
                                if value[1] == 16: temp_img = pygame.transform.rotate(Data_image[plant_value[0]][15][plant_value[2]],plant_value[3])
                                else: temp_img = pygame.transform.rotate(Data_image[plant_value[0]][value[1]][plant_value[2]],plant_value[3])
                                display.blit(temp_img,(coordinate[0]+plant_value[1],coordinate[1]))
                            
                            if value[1] != 16: display.blit(Data_image["air"][value[1]],coordinate)

    #Tick Delay Code
    tick_delay += 1
    if tick_delay == TICK:
        tick_delay = 0

    #Player movement Code
    player_movement = [0,0]
    if moving_right:
        player_movement[0] += 3
    if moving_left:
        player_movement[0] -= 3
    player_movement[1] += player_y_momentum
    player_y_momentum +=0.3
    if player_y_momentum > 3:
        player_y_momentum = 3

    #Player Animation change
    if player_movement[0] > 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = False
    if player_movement[0] == 0: player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] < 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = True

    #Colision Code
    player_rect, collisions, hit_list = move(player_rect,player_movement,tile_rects)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer =0
        if player_movement[0] != 0:
            if grass_sound_timer ==0:
                grass_sound_timer =30
                choice(Data_sound['grass_sounds']).play()
    elif collisions['top']:
        player_y_momentum = 0
        air_timer =0
    else: air_timer += 1
        

    #Animation frame Code
    player_frame += 1
    if player_frame >= len(animation_database[player_action]): player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x -scroll[0], player_rect.y-scroll[1]))

    #Mouse
    pygame_pos = pygame.mouse.get_pos()[0]-center[0],pygame.mouse.get_pos()[1]-center[1]
    original_pos = ((pygame_pos[0]/(2*size)+scroll[0])//TILE_SIZE , (pygame_pos[1]/(2*size)+scroll[1])//TILE_SIZE)
    mouse_pos = (original_pos[0]*TILE_SIZE-scroll[0],original_pos[1]*TILE_SIZE-scroll[1])
    display.blit(Cursor,(mouse_pos[0]-1,mouse_pos[1]-1))
    
    #Pygame loop event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT: moving_right = True
            if event.key == K_w: pygame.mixer.music.fadeout(1000)
            if event.key == K_e:
                pygame.mixer.music.play(-1)
                print(game_map)
                exit()
            if event.key == K_LEFT: moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    Data_sound['jump'].play()
                    player_y_momentum = -5

        if event.type == MOUSEBUTTONDOWN: mousepress = True
        if event.type == MOUSEBUTTONUP: mousepress = False

        if event.type == KEYUP:
            if event.key == K_RIGHT: moving_right = False
            if event.key == K_LEFT: moving_left = False

    #Windows Resize
    if screen.get_size() != save_size:
        save_size = screen.get_size() 
        if  screen.get_size()[0] / WINDOW_SIZE[0] > screen.get_size()[1] / WINDOW_SIZE[1]: size = screen.get_size()[0] / WINDOW_SIZE[0]
        else: size = screen.get_size()[1] / WINDOW_SIZE[1]
        surf = pygame.transform.scale(display, (int(WINDOW_SIZE[0]*size),int(WINDOW_SIZE[1]*size)))
        center = screen.get_rect().center[0] - surf.get_rect().center[0], screen.get_rect().center[1] - surf.get_rect().center[1]

    #Render Game
    surf = pygame.transform.scale(display, (int(WINDOW_SIZE[0]*size),int(WINDOW_SIZE[1]*size)))
    screen.blit(surf, center)
    screen.blit(update_fps(), (10,0))
    #light.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
    pygame.display.update(surf.get_rect())

    #Maximum Fps for the game is 60 fps
    clock.tick(60)