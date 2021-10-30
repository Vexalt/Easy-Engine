from libs.engine import get_tile_info

def Tick(CHUNK_SIZE,game_map,tile,tile_data,blockstates):
    info = get_tile_info(CHUNK_SIZE,game_map,tile[0],tile[1])
    if tile_data["type"] == "grass":
        if info["left"] is not None:
            if blockstates[info["left"]["type"]]["collision"]:
                pass
