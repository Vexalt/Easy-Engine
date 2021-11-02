true_scroll[0] += (player_rect.x-scroll[0]-(WINDOW_SIZE[0]/4))/20 #20 is the time for the camera follow the movement
    true_scroll[1] += (player_rect.y-scroll[1]-(WINDOW_SIZE[1]/4))/20
    scroll = true_scroll.copy()