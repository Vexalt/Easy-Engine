from opensimplex import OpenSimplex
import random

SEED = random.randint(-999999,999999)
noise = OpenSimplex(SEED)
random.seed(SEED)

def generate_chunk(CHUNK_SIZE,x,y):
    scale = 10

    chunk_data = {}
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos #The generation start at "-2" and not "0" for screen problem
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

def get_seed():
    return SEED