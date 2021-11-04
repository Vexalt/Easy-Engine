#coding: UTF-8

from random import randint, uniform
import pygame, math
from json import load
from os import listdir

#Inventory
global Inventory
Inventory = [{},{},{},{},{},{},{},{},{},{}]

def load_images(TILE_SIZE):
    tile_blockstates = {}
    images = {}
    for json_file in listdir("data/blockstates"):
        json = open("data/blockstates/"+json_file)
        json_text = load(json)
        json.close()

        for tile in json_text:
            #Default Collision Rect
            
            json_text[tile].setdefault("collision_rect",[TILE_SIZE,TILE_SIZE,0,0])
            json_text[tile].setdefault("special_blit",False)
            json_text[tile].setdefault("background",True)
            json_text[tile].setdefault("item",None)
            json_text[tile].setdefault("on_ground",False)
            json_text[tile].setdefault("on_himself",False)
            json_text[tile].setdefault("reward",tile)

            tile_blockstates[tile] = json_text[tile]
            images[tile] = json_text[tile]["path"]

    tile_database = {}
    for image_name in images.keys():
        if images[image_name] is not None:
            original_image = pygame.transform.smoothscale(pygame.image.load("data/images/"+images[image_name]).convert_alpha(),(TILE_SIZE,TILE_SIZE))
            if tile_blockstates[image_name]["background"] is True:
                background = pygame.Surface((TILE_SIZE,TILE_SIZE))
                background.fill((93, 173, 226))
                background.blit(original_image,(0,0))

                tile_database[image_name] = background.convert()
            else: tile_database[image_name] = original_image

        else:
            #The load Function an invisible "air" block
            temp_img =pygame.Surface((TILE_SIZE,TILE_SIZE))
            temp_img.fill((93, 173, 226))
            tile_database[image_name] = temp_img.convert()

    #Load Tile Items with Tile_blockstates
    tile_items = {}
    for item in tile_blockstates.keys():
        if tile_blockstates[item]["item"] is None:
            tile_items[item] = tile_database[item]
        else:
            tile_items[item] = pygame.transform.smoothscale(pygame.image.load("data/items/"+tile_blockstates[item]["item"]).convert_alpha(),(TILE_SIZE,TILE_SIZE))

    return tile_database,tile_blockstates,tile_items

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move_function(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
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
    return rect, collision_types

def get_tile_info(CHUNK_SIZE,game_map,tile_x,tile_y):
    info = {'top':None,'bottom':None,'right':None,'left':None}
    try:info["left"] = game_map[str((tile_x+1)//CHUNK_SIZE)+";"+str(tile_y//CHUNK_SIZE)][(tile_x+1,tile_y)]
    except:pass
    try:info["right"] = game_map[str((tile_x-1)//CHUNK_SIZE)+";"+str(tile_y//CHUNK_SIZE)][(tile_x-1,tile_y)]
    except:pass
    try:info["top"] = game_map[str(tile_x//CHUNK_SIZE)+";"+str((tile_y-1)//CHUNK_SIZE)][(tile_x,tile_y-1)]
    except:pass
    try:info["bottom"] = game_map[str(tile_x//CHUNK_SIZE)+";"+str((tile_y+1)//CHUNK_SIZE)][(tile_x,tile_y+1)]
    except:pass

    return info

def get_tile_with_pos(CHUNK_SIZE,game_map,tile_x,tile_y):
    return game_map[str((tile_x)//CHUNK_SIZE)+";"+str(tile_y//CHUNK_SIZE)][(tile_x,tile_y)]

class Player():
    def __init__(self,rect):
        #Movement Player Setup
        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0

        self.movement = [0,0]

        self.speed_x = 2
        self.speed_y = 0.2

        #Load animation from json file
        self.animation_frames = {}
        json_animations_file = open('data/player/animations/animations.json');json_text = load(json_animations_file);json_animations_file.close()
        self.animation_database = {}
        for action in json_text.keys():
            self.animation_database[action] = self.load_animation(json_text[action]["path"],json_text[action]["time"])

        #Animation Value
        self.action = 'idle'
        self.frame = 0
        self.flip = False

        self.rect = pygame.Rect(rect)

        #Sound Setup
        self.sound_database = {}

        self.light = 3

    def change_action(self,action_var,frame,new_value):
        if action_var != new_value:
            action_var = new_value
            frame = 0
        self.action = action_var
        self.frame = frame

    def move(self,tile_rects,):
        self.movement = [0,0]
        if self.moving_right == True:
            self.movement[0] += self.speed_x
        if self.moving_left == True:
            self.movement[0] -= self.speed_x
        self.movement[1] += self.vertical_momentum
        self.vertical_momentum += self.speed_y
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3

        self.rect,collisions = move_function(self.rect,self.movement,tile_rects)

        if collisions['bottom'] == True:
            self.air_timer = 0
            self.vertical_momentum = 0
        elif collisions['top'] == True:
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1

        self.new_frame()


    def new_frame(self):
        self.frame += 1
        if self.frame >= len(self.animation_database[self.action]):
            self.frame = 0

    def load_animation(self,path,frame_durations):
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + '_' + str(n)
            img_loc = path + '/' + animation_frame_id + '.png'
            # player_animations/idle/idle_0.png
            animation_image = pygame.image.load(img_loc).convert()
            animation_image.set_colorkey((255,255,255))
            self.animation_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data

    def get_image(self):
        player_img_id = self.animation_database[self.action][self.frame]
        player_img = self.animation_frames[player_img_id]
        return pygame.transform.flip(player_img,self.flip,False)

    def add_sound(self,path,name):
        self.sound_database[name] = pygame.mixer.Sound(path)

    def get_sound(self,name):
        return self.sound_database[name]

class Item(pygame.sprite.Sprite):
    def __init__(self,tile_x,tile_y,type,img):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = pygame.transform.scale(img,(8,8))
        self.rect = self.image.get_rect()

        #For a Natural Effect
        self.rect.x = tile_x+ randint(0,8)
        self.rect.y = tile_y+ randint(0,8)

        self.x = self.rect.x
        self.y = self.rect.y
        self.movement = -1

        self.time = 2100 #30 Seconds

    def update(self,game_map,CHUNK_SIZE,TILE_SIZE,scroll,player_pos,player_rect,tile_blockstates):
        pos_x  = self.x-scroll[0]
        pos_y  = self.y-scroll[1]

        effect = (self.movement**3-self.movement)*5
        self.movement += 0.02
        if self.movement >= 0:
            self.movement = -1
        self.rect.x= pos_x
        self.rect.y= pos_y + effect

        #Collision Engine
        self.tile_x,self.tile_y = ((self.rect.x+scroll[0])//TILE_SIZE , (self.rect.y+8+scroll[1])//TILE_SIZE)
        info = get_tile_with_pos(CHUNK_SIZE,game_map,self.tile_x,self.tile_y)
        if tile_blockstates[info["type"]]["collision"] == False:
            self.y += 1
        
        #Pythagore
        total_distance = ((((player_pos[0] - self.x )**2) + ((player_pos[1] - self.y)**2) )**0.5)
        if total_distance < 25:
            self.x += (player_pos[0] - self.x)/16
            self.y += (player_pos[1] - self.y)/16

        self.time -= 1

        #Item Despawn
        if self.time == 0:
            self.kill()
            self.remove()

        if self.rect.colliderect(player_rect):
            self.kill()
            self.remove()
            
            for slot in range(10):
                if Inventory[slot] != {}:
                    if Inventory[slot]["type"] == self.type and Inventory[slot]["number"] < 64:
                            Inventory[slot]["number"] +=1
                            break
                if slot == 9:
                    for slot in range(10):
                        if Inventory[slot] == {}:
                            Inventory[slot] = {"type":self.type,"number":1}
                            break

class Particule(pygame.sprite.Sprite):
    def __init__(self,tile_x,tile_y,color,time,mode="normal"):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((2,2),pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill(color)

        #For a Natural Effect
        if mode=="normal":
            self.rect.x = tile_x+ randint(0,14)
            self.rect.y = tile_y+ randint(0,14)
            self.movement = [0,0.1]
        elif mode=="Explosion":
            self.rect.x = tile_x
            self.rect.y = tile_y
            self.movement = [uniform(-0.5,0.5),uniform(-0.5,0.5)]

        self.x = self.rect.x
        self.y = self.rect.y
        
        self.max_time = time
        self.time = time

    def update(self,game_map,CHUNK_SIZE,TILE_SIZE,scroll,player_pos,player_rect,tile_blockstates):
        pos_x  = self.x-scroll[0]
        pos_y  = self.y-scroll[1]

        self.rect.x= pos_x
        self.rect.y= pos_y

        self.x += self.movement[0]
        self.y += self.movement[1]

        self.time -= 1
        self.image.set_alpha((self.time*255)//self.max_time)

        if self.time == 0:
            self.kill()
            self.remove()
    