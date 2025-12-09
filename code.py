# ============================================================

import time
import board
import busio

import math
import neopixel
import adafruit_adxl34x
import random


# -------------------------------
#  STATES
# -------------------------------
STATE_INTRO = 0
STATE_SELECT_CHAR = 1
STATE_SELECT_LEVEL = 2
STATE_PLAYING = 3
STATE_GAME_OVER = 4

LEVELS = 10
OPED = True
game_state = STATE_INTRO

# ------------------------------------------------------
#   === imports other files ===
# ------------------------------------------------------

import oled_renderer
from oled_renderer import *
from character import CharacterManager
from input_manager import KnobController, Accelerator
from game_manager import GameManager
from score_manager import ScoreManager

from utils import *

# setup

displayio.release_displays()        
i2c = busio.I2C(board.SCL, board.SDA)
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)  
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

pixels = neopixel.NeoPixel(board.D10, 4, brightness=0.3, auto_write=True)

accel = adafruit_adxl34x.ADXL345(i2c)

char_manager = CharacterManager()
knob = KnobController()
game_manager = GameManager()
acc = Accelerator(accel)
score_manager = ScoreManager()

# -------------------------------
#   Intro 
# -------------------------------
def play_intro():

    print("Intro: WELCOME")
    clear_display(display)
    draw_text_block(
        display,
        ["WELCOME"],
        align="center"
    )
    
    if OPED: play_melody(open_melody)
    time.sleep(1)


# -------------------------------
#   Character
# -------------------------------
def select_character():
    print("Select Character")
    
    
    render_character_select(display, char_manager)
    
    t = 0
    while True:
        
        role_color = char_manager.get_color()
        
        pixels[0] = breathing_color(role_color, t)
        pixels.show()
        t += 0.08
        
        event = knob.check()
        
        if event:
            etype, value = event

            if etype == "turn":
                if value > 0:
                    char_manager.next()
                    render_character_select(display, char_manager)
                else:
                    char_manager.prev()
                    render_character_select(display, char_manager)

            elif etype == "press":
                print("Select", char_manager.current()["name"])
                clear_display(display)
                draw_text_block(
                    display,
                    ["< Selected >", "["+char_manager.current()["name"]+"]"],
                    align="center"
                )
                time.sleep(1)
                break
            
        time.sleep(0.01)
    


# -------------------------------
#   Difficulty
# -------------------------------
def select_level():
    print("Select Level")
    # Easy / Medium / Hard
    render_difficulty_select(display, game_manager)
    while True:
        
        event = knob.check()
        
        if event:
            etype, value = event

            if etype == "turn":
                    game_manager.next_difficulty()
                    render_difficulty_select(display, game_manager)

            elif etype == "press":
                print("Select", game_manager.current_difficulty())
                clear_display(display)
                draw_text_block(
                    display,
                    ["< Selected >", "["+game_manager.current_difficulty()["name"]+"]"],
                    align="center"
                )
                time.sleep(1)
                break  
            
        time.sleep(0.01)
    
    time.sleep(1)

    level_index = 0
    return level_index


# -------------------------------
#   Game loop
# -------------------------------
def game_loop():
    print("Game Loop Started")
    
    difficulty = game_manager.current_difficulty()
    time.sleep(0.5)
    
    total_score = 0
    
    HP = 3
    HP_show(HP,pixels)
    
    for game_level in range(1,LEVELS+1):
        
        grid = game_manager.generate_map()
        
        # player pos
        player_col = 2
        

        offset = game_manager.get_offset()
        last_move = time.monotonic()
        score = game_manager.get_score()
        while True:

            now = time.monotonic()
            step_time = game_manager.get_step_time()
            offset = game_manager.get_offset()
        
            # every step_time move forward 1 row
            if now - last_move >= step_time:
                game_manager.update_offset(1)
                last_move = now
                game_manager.update_score(10)
                char_manager.add_charge(5)
                
                offset = game_manager.get_offset()
                print(offset)
            
            # left/right -> player_col
            
            left, right, shake = acc.update()
        
            if left:
                player_col = max(0, player_col - 1)

            if right:
                player_col = min(4, player_col + 1)
                
                
            # shake → skill
            if shake:
                char_manager.try_use_skill(game_manager, grid, offset, player_col)
                print("+++"+ str(offset))
                visible_rows = draw_map(display, grid, player_col, offset)
                screen = ["Lv."+str(game_level)+"    "+ str(char_manager.get_charge()) +"%    "+str(score)]
                screen.extend(visible_rows)
                draw_text_block(display, screen, align="center", start_pos=(0, 10), line_spacing=10)
                play_melody(skill_sound)
            
            
            if game_manager.check_collision(grid, offset, player_col):
                print("!!!")
                game_manager.update_score(-50)
                play_melody(hurt_sound)
                grid[offset + 4][player_col] = " "
                
            
            score = game_manager.get_score()
            visible_rows = draw_map(display, grid, player_col, offset)
            screen = ["Lv."+str(game_level)+"    "+ str(char_manager.get_charge()) +"%    "+str(score)]
            screen.extend(visible_rows)
            draw_text_block(display, screen, align="center", start_pos=(0, 10), line_spacing=10)
            
            time.sleep(0.1)
            
            # level pass
            if offset == 0:
                clear_display(display)
                draw_text_block(
                    display,
                    ["Congrats!","Lv."+str(game_level)+" PASSED","Score:"+str(score)],
                    align="center"
                )
                play_melody(pass_sound)
                time.sleep(1)
                break
            
        total_score += score
        
        if score < 0:
            HP -= 1
            HP_show(HP,pixels)
            
        # Game over
        if HP == 0:
            clear_display(display)
            draw_text_block(
                display,
                ["GAME OVER"],
                align="center"
            )
            time.sleep(1)
            game_result = "LOSE"
            return game_result,total_score
            
    # Survived
    game_result = "WIN"
    return game_result,total_score


# -------------------------------
#   Game Over
# -------------------------------
def play_ending(result,total_score):
    print("Game Over! Result =", result)
    
    clear_display(display)
    draw_text_block(
        display,
        ["CONGRATS!","Total:"+str(total_score)],
        align="center"
    )
    time.sleep(1)
    
    # New High Score?
    name = char_manager.current()["name"]
    is_new_high = score_manager.add_score(name, total_score)

    if is_new_high:
        draw_text_block(
        display,
        ["New High Score!"],
        align="center"
    )
    time.sleep(1)
    
    high_scores = score_manager.get_highscore_display()
    
    # Show High Scores

    render_high_score_board(display, high_scores)

    if OPED: play_melody(end_melody)
    time.sleep(5)
    


# ============================================================
#               Main loop
# ============================================================

print("Game Booting...")

while True:
    if game_state == STATE_INTRO:
        play_intro()
        game_state = STATE_SELECT_CHAR

    elif game_state == STATE_SELECT_CHAR:
        chosen_char = select_character()
        game_state = STATE_SELECT_LEVEL

    elif game_state == STATE_SELECT_LEVEL:
        chosen_level = select_level()
        game_state = STATE_PLAYING

    elif game_state == STATE_PLAYING:
        result,total_score = game_loop()
        game_state = STATE_GAME_OVER

    elif game_state == STATE_GAME_OVER:
        play_ending(result,total_score)
        # back to character
        game_state = STATE_SELECT_CHAR

