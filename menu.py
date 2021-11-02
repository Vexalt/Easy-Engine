import pygame,sys
from opensimplex import OpenSimplex

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP,MOUSEBUTTONDOWN])
pygame.display.set_caption("Easy Engine Version 4")

WINDOW_SIZE = (1000,800)

screen = pygame.display.set_mode(WINDOW_SIZE,RESIZABLE|DOUBLEBUF)

display = screen.copy()

font = pygame.font.Font('data/fonts/font.ttf',50)

click = False

def draw_text(text,font,color,surface,x,y):
    textobj = font.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)

def WINDOW_RESIZED(screen_size,WINDOW_SIZE):
    if screen_size[0] / WINDOW_SIZE[0] > screen_size[1] / WINDOW_SIZE[1]:
        factor = screen_size[1] / WINDOW_SIZE[1]
        display_size = (WINDOW_SIZE[0]*factor,WINDOW_SIZE[1]*factor)
        display_y = 0
        display_x = (screen_size[0]-WINDOW_SIZE[0]*factor)/2
    else:
        factor = screen_size[0] / WINDOW_SIZE[0]
        display_size = (WINDOW_SIZE[0]*factor,WINDOW_SIZE[1]*factor)
        display_x = 0
        display_y = (screen_size[1]-WINDOW_SIZE[1]*factor)/2

    return display_size,(display_x,display_y),pygame.Rect((display_x,display_y),display_size)

import libs.engine as e
import random

def generate_chunk(CHUNK_SIZE,noise,x,y):
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

from PIL import Image, ImageFilter
def draw_tile():
    map_data = {}
    TILE_SIZE = 24
    CHUNK_SIZE = 7
    SEED = random.randint(-999999,999999)
    noise = OpenSimplex(SEED)
    tile_database = e.load_images(TILE_SIZE)
    img = pygame.Surface(WINDOW_SIZE)
    light_display = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    tile_light = []
    for y in range(6):
        for x in range(7):
            target_x = x - 1 + int(round(0/(CHUNK_SIZE*TILE_SIZE)))
            target_y = y - 1 + int(round(-200/(CHUNK_SIZE*TILE_SIZE)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in map_data:
                map_data[target_chunk] = generate_chunk(CHUNK_SIZE,noise,target_x,target_y)
            for tile in map_data[target_chunk]:
                pos_x = tile[0]*TILE_SIZE
                pos_y = tile[1]*TILE_SIZE+200
                tile_data = map_data[target_chunk][tile]
                img.blit(tile_database[tile_data["type"]],(pos_x,pos_y))
                if tile_data["type"] == "torch":
                    tile_light.append(((pos_x+10,pos_y+7),0.4))
    light_display.fill((0,0,0))
    light_display.set_alpha(150)
    for distance in reversed(range(10)):
        for light in tile_light:
            pygame.draw.circle(light_display,(0,0,0,distance*25),light[0],int(light[1]*distance*10)*distance*0.2,int(light[1]//10))
    img.blit(light_display,(0,0))
    #Pil Blurred
    pil_string_image = pygame.image.tostring(img,"RGBA",False)
    im = Image.frombytes("RGBA",WINDOW_SIZE,pil_string_image)
    im = im.filter(ImageFilter.GaussianBlur(radius=2))
    data = im.tobytes()
    surface = pygame.image.fromstring(data, im.size, im.mode)
    return surface

def main_menu():
    display_size = WINDOW_SIZE
    display_pos = (0,0)
    display_rect = pygame.Rect(display_pos,display_size)

    screen.fill((0,0,0))

    background = draw_tile()

    while 1:
        display.blit(background,(0,0))
        draw_text("Main Menu",font,(255,255,255),display,400,100)

        mx,my = pygame.mouse.get_pos()

        pygame.draw.polygon(display,(100,100,100),((100,100),(80,140),(200,140),(220,100)))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == WINDOWRESIZED:
                display_size,display_pos,display_rect = WINDOW_RESIZED(screen.get_size(),WINDOW_SIZE)
                screen.fill((0,0,0))
                pygame.display.update()

        screen.blit(pygame.transform.scale(display,display_size),display_pos)
        pygame.display.update(display_rect)
        mainClock.tick(60)

main_menu()