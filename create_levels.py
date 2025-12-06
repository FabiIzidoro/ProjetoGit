import csv

ROWS = 16
COLS = 150

# Tile constants
GRASS_L = 0
GRASS_M = 1
GRASS_R = 2
DIRT_L = 3
DIRT_M = 4
DIRT_R = 5
CRATE = 8
WATER = 9
DECO_GRASS = 14
PLAYER = 15
ENEMY = 16
AMMO = 17
GRENADE = 18
HEALTH = 19
EXIT = 20

def create_empty_level():
    return [[-1] * COLS for _ in range(ROWS)]

def add_floor(level, start, end, y):
    # y is the top surface of the floor
    for x in range(start, end):
        if x == start:
            level[y][x] = GRASS_L
        elif x == end - 1:
            level[y][x] = GRASS_R
        else:
            level[y][x] = GRASS_M
        
        # Fill below with dirt
        for dy in range(y + 1, ROWS):
            if x == start:
                level[dy][x] = DIRT_L
            elif x == end - 1:
                level[dy][x] = DIRT_R
            else:
                level[dy][x] = DIRT_M

def add_platform(level, x, y, width):
    for i in range(width):
        tile = GRASS_M
        if i == 0: tile = GRASS_L
        elif i == width - 1: tile = GRASS_R
        level[y][x+i] = tile

def save_level(level, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(level)

# --- Level 1 ---
lvl1 = create_empty_level()
ground_y = ROWS - 2 # 14

# Main Ground
add_floor(lvl1, 0, 150, ground_y)

# Water Gaps (3 blocks wide)
for x in range(30, 33):
    # Clear floor and dirt
    for dy in range(ground_y, ROWS):
        lvl1[dy][x] = -1
    # Add water at bottom
    lvl1[ROWS-1][x] = WATER

for x in range(70, 73):
    for dy in range(ground_y, ROWS):
        lvl1[dy][x] = -1
    lvl1[ROWS-1][x] = WATER

# Platforms - Height Rule: 2 blocks difference
# Ground is at 14.
add_platform(lvl1, 10, 12, 3) # 2 blocks high
add_platform(lvl1, 20, 12, 3) 
add_platform(lvl1, 35, 10, 3) # 2 blocks higher than 12
add_platform(lvl1, 45, 12, 3) 
add_platform(lvl1, 60, 10, 4) 
add_platform(lvl1, 80, 12, 5) 

# Player
lvl1[ground_y-3][5] = PLAYER

# Enemies
lvl1[ground_y-3][25] = ENEMY
lvl1[ground_y-3][42] = ENEMY
lvl1[ground_y-3][62] = ENEMY
lvl1[ground_y-3][90] = ENEMY

# Items
lvl1[11][11] = AMMO # On platform at 12
lvl1[9][36] = GRENADE # On platform at 10
lvl1[11][46] = HEALTH # On platform at 12

# Exit - Must be on a block
# Ground at 14. Sign at 13.
lvl1[ground_y-1][145] = EXIT

save_level(lvl1, 'nivel1_data.csv')

# --- Level 2 ---
lvl2 = create_empty_level()

# Stepped Terrain
# Section 1: Ground level (14)
add_floor(lvl2, 0, 30, 14)

# Section 2: Up 2 blocks (12)
# Gap of 2 blocks: 30-32
add_floor(lvl2, 32, 60, 12)

# Section 3: Up 2 blocks (10)
# Gap of 2 blocks: 60-62
add_floor(lvl2, 62, 90, 10)

# Section 4: Down 2 blocks (12)
# Gap 2 blocks: 90-92
add_floor(lvl2, 92, 120, 12)

# Section 5: Ground level (14)
# Gap 2 blocks: 120-122
add_floor(lvl2, 122, 150, 14)

# Water in gaps
for x in range(30, 32):
    lvl2[ROWS-1][x] = WATER
for x in range(60, 62):
    lvl2[ROWS-1][x] = WATER
for x in range(90, 92):
    lvl2[ROWS-1][x] = WATER
for x in range(120, 122):
    lvl2[ROWS-1][x] = WATER

# Platforms
add_platform(lvl2, 15, 11, 3) # 3 blocks high (reachable with high jump)
add_platform(lvl2, 75, 7, 3) # 3 blocks higher than section 3 (10)

# Player
lvl2[11][5] = PLAYER

# Enemies
lvl2[11][20] = ENEMY
lvl2[9][40] = ENEMY # Ground at 12
lvl2[7][70] = ENEMY # Ground at 10
lvl2[9][100] = ENEMY # Ground at 12
lvl2[11][130] = ENEMY # Ground at 14

# Items
lvl2[10][16] = AMMO
lvl2[6][76] = GRENADE
lvl2[10][110] = HEALTH

# Exit
# Ground at 14. Sign at 13.
lvl2[13][145] = EXIT

save_level(lvl2, 'nivel2_data.csv')
