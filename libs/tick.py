from libs.engine import get_tile_info,Item,Particule
import random
#This value is used for avoid spam Tick Function
TICK = 0

def Tick(CHUNK_SIZE,game_map,tile,tile_data,blockstates,Entity,tile_items):
    if TICK == 0:
        if blockstates[tile_data["type"]]["on_ground"]:
            info = get_tile_info(CHUNK_SIZE,game_map,tile[0],tile[1])
            if info["bottom"] is not None and blockstates[info["bottom"]["type"]]["collision"] == False:
                    Entity.add(Item(tile[0]*16,tile[1]*16,tile_items[tile_data["type"]]))
                    tile_data["break"] = blockstates["air"]["hardness"]
                    tile_data["type"] = "air"

        if tile_data["type"] == "torch":
            for particule in range(random.randint(1,3)):
                Entity.add(Particule(tile[0]*16,tile[1]*16,(244, 208, 63),random.randint(15,25)))
            for particule in range(random.randint(1,3)):
                Entity.add(Particule(tile[0]*16,tile[1]*16,(230, 126, 34),random.randint(15,25)))

def add_tick():
    global TICK
    TICK +=1
    if TICK == 20:
        TICK = 0
