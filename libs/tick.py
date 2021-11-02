from libs.engine import get_tile_info
#This value is used for avoid spam Tick Function
TICK = 0

def Tick(CHUNK_SIZE,game_map,tile,tile_data,blockstates):
    if TICK == 0:
        info = get_tile_info(CHUNK_SIZE,game_map,tile[0],tile[1])
        if tile_data["type"] == "grass":
            if info["left"] is not None:
                if blockstates[info["left"]["type"]]["collision"]:
                    pass

def add_tick():
    global TICK
    TICK +=1
    if TICK == 5:
        TICK = 0
