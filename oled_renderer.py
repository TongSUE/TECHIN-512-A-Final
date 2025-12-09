# ============================================================
#   OLED Rendering Helper for SSD1306 (128x64)
# ============================================================

import displayio
import terminalio
from adafruit_display_text import label
import i2cdisplaybus
import adafruit_displayio_ssd1306

from character import CharacterManager

# ------------------------------------------------------------
#   CLEAR
# ------------------------------------------------------------

def clear_display(display):
    display.root_group = displayio.Group()


# ------------------------------------------------------------
#   SHOW TEXT
# ------------------------------------------------------------

def draw_text_block(display, text_lines,
                    align="left",
                    start_pos=None,
                    line_spacing=14):

    group = displayio.Group()

    # cal y -> center
    if start_pos is None:
        total_height = len(text_lines) * line_spacing
        start_y = 32 - total_height // 2  
        start_x = 0
    else:
        start_x, start_y = start_pos

    y = start_y
    for t in text_lines:
        if align == "left":
            x = start_x
        else:  # center
            text_width = len(t) * 6
            x = (128 - text_width) // 2

        txt = label.Label(
            terminalio.FONT,
            text=t,
            color=0xFFFFFF,
            x=x,
            y=y
        )
        group.append(txt)
        y += line_spacing

    display.root_group = group
    
    
def draw_title(display, title_text):
    draw_text_block(
        display,
        [title_text],
        align="center",
        start_pos=(0, 10)
    )
    
# Character Shapes

WHITE = 0xFFFFFF


def _palette():
    p = displayio.Palette(2)
    p[0] = 0x000000
    p[1] = WHITE
    return p


def draw_shape(group, shape_name, cx=100, cy=30):

    if shape_name == "circle":
        _draw_circle(group, cx, cy)

    elif shape_name == "square":
        _draw_square(group, cx, cy)

    elif shape_name == "diamond":
        _draw_diamond(group, cx, cy)

    elif shape_name == "triangle":
        _draw_triangle(group, cx, cy)

    elif shape_name == "flower":
        _draw_flower(group, cx, cy)


def _draw_circle(group, cx, cy):
    palette = _palette()
    r = 8
    for dy in range(-r, r + 1):
        w = int((r*r - dy*dy)**0.5)
        bmp = displayio.Bitmap(w*2, 1, 2)
        for x in range(w*2):
            bmp[x, 0] = 1
        group.append(displayio.TileGrid(bmp, pixel_shader=palette, x=cx-w, y=cy+dy))


def _draw_square(group, cx, cy):
    palette = _palette()
    bmp = displayio.Bitmap(14, 14, 2)
    for x in range(14):
        for y in range(14):
            bmp[x, y] = 1
    group.append(displayio.TileGrid(bmp, pixel_shader=palette, x=cx-7, y=cy-7))


def _draw_diamond(group, cx, cy):
    palette = _palette()
    for dy in range(-9, 9):
        w = 9 - abs(dy)
        bmp = displayio.Bitmap(w*2, 1, 2)
        for x in range(w*2):
            bmp[x, 0] = 1
        group.append(displayio.TileGrid(bmp, pixel_shader=palette, x=cx-w, y=cy+dy))


def _draw_triangle(group, cx, cy):
    palette = _palette()
    side = 17
    h = int(side * 0.9)
    top_y = cy - h//2 - 2
    for row in range(h):
        span = int((row/(h-1)) * (side/2))
        bmp = displayio.Bitmap(span*2, 1, 2)
        for x in range(span*2):
            bmp[x, 0] = 1
        group.append(displayio.TileGrid(bmp, pixel_shader=palette, x=cx-span, y=top_y+row))


def _draw_flower(group, cx, cy):
    palette = _palette()
    r = 4
    offsets = [(0,-5),(5,-1),(0,-1),(-5,-1),(3,4),(-3,4)]
    for ox, oy in offsets:
        for dy in range(-r, r+1):
            w = int((r*r - dy*dy)**0.5)
            if w <= 0:
                continue
            bmp = displayio.Bitmap(w*2, 1, 2)
            for x in range(w*2):
                bmp[x, 0] = 1
            group.append(displayio.TileGrid(bmp, pixel_shader=palette, x=cx+ox-w, y=cy+oy+dy))


# Select Character UI

def render_character_select(display, char_manager):

    clear_display(display)

    role = char_manager.current()
    name = role["name"]
    skill = role["skill"]
    shape = role["shape"]

    group = displayio.Group()

    # title
    title = label.Label(
        terminalio.FONT,
        text="< Character Select >",
        color=0xFFFFFF,
        x=10,
        y=8
    )
    group.append(title)

    # name
    t_name = label.Label(
        terminalio.FONT,
        text="[" + name + "]",
        color=0xFFFFFF,
        x=5,
        y=30
    )
    group.append(t_name)

    # skill
    t_skill = label.Label(
        terminalio.FONT,
        text=skill,
        color=0xFFFFFF,
        x=5,
        y=55
    )
    group.append(t_skill)

    # shape
    draw_shape(group, shape)

    # frame

    frx = 80
    fry = 20
    f1 = label.Label(terminalio.FONT, text="-----", color=0xFFFFFF, x=frx+5, y=fry-5)
    f2 = label.Label(terminalio.FONT, text="|", color=0xFFFFFF, x=frx+2, y=fry)
    f3 = label.Label(terminalio.FONT, text="|", color=0xFFFFFF, x=frx+2, y=fry+10)
    f4 = label.Label(terminalio.FONT, text="|", color=0xFFFFFF, x=frx+2, y=fry+20)
    f5 = label.Label(terminalio.FONT, text="|", color=0xFFFFFF, x=frx+32, y=fry)
    f6 = label.Label(terminalio.FONT, text="|", color=0xFFFFFF, x=frx+32, y=fry+10)
    f7 = label.Label(terminalio.FONT, text="|", color=0xFFFFFF, x=frx+32, y=fry+20)
    f8 = label.Label(terminalio.FONT, text="-----", color=0xFFFFFF, x=frx+5, y=fry+24)
    for f in [f1,f2,f3,f4,f5,f6,f7,f8]:
        group.append(f)

    # show
    display.root_group = group
    
    
# Difficulty level


def render_difficulty_select(display, game_manager):

    clear_display(display)

    diff = game_manager.current_difficulty()
    name = diff["name"]
    speed = diff["speed"]
    density = diff["density"]

    group = displayio.Group()

    # title
    title = label.Label(
        terminalio.FONT,
        text="< Difficulty >",
        color=0xFFFFFF,
        x=20,
        y=10
    )
    group.append(title)

    # name
    t_name = label.Label(
        terminalio.FONT,
        text="[" + name + "]",
        color=0xFFFFFF,
        x=10,
        y=25
    )
    group.append(t_name)

    # tips
    t_speed = label.Label(
        terminalio.FONT,
        text="Speed: " + str(speed),
        color=0xFFFFFF,
        x=10,
        y=45
    )
    group.append(t_speed)

    t_density = label.Label(
        terminalio.FONT,
        text="Obstacle: " + str(density),
        color=0xFFFFFF,
        x=10,
        y=55
    )
    group.append(t_density)

    display.root_group = group
    
    
# Game

def draw_map(display, map_data, player_col, offset):

    visible_rows = []

    # OLED 5 rows
    for i in range(5):
        map_row_index = offset + i

        if map_row_index < len(map_data):
            row = map_data[map_row_index].copy()
        else:

            row = [" "] * 5

        # plyaer
        if i == 4:
            row[player_col] = "O"

        # | 
        line = " | ".join(row)
        line = " " + line + " "
        visible_rows.append(line)

    return visible_rows
    

def render_high_score_board(display, scores):
    lines = ["< High Score >"]

    # empty）
    if len(scores) == 0:
        lines.append("-----")
        lines.append("-----")
        lines.append("-----")
    else:
        for i in range(3):
            if i < len(scores):
                lines.append(scores[i])
            else:
                lines.append("-----")

    draw_text_block(display, lines, align="center")


