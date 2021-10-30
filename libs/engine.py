#coding: UTF-8

import pygame
from json import load
from os import listdir

def load_blockstates():
    tile_blockstates = {}
    for json_file in listdir("data/blockstates"):
        json = open("data/blockstates/"+json_file)
        json_text = load(json)
        json.close()

        tile_blockstates[json_text["name"]] = json_text

    return tile_blockstates


def load_images(TILE_SIZE):
    tile_database = {}

    images = listdir("data/images")
    for image in images:
        original_image = pygame.transform.smoothscale(pygame.image.load("data/images/"+image).convert_alpha(),(TILE_SIZE,TILE_SIZE))
        background = pygame.Surface((TILE_SIZE,TILE_SIZE))
        background.fill((93, 173, 226))
        background.blit(original_image,(0,0))

        tile_database[image.split(".png")[0]] = background.convert()

    #The load Function create the "air" block
    temp_img =pygame.Surface((TILE_SIZE,TILE_SIZE))
    temp_img.fill((93, 173, 226))
    tile_database["air"] = temp_img

    return tile_database

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

    def move(self,tile_rects):
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
