# TECHIN-512-A-Final
Yutong Luo

---

# Project Overview

## **Magical Runner — A Motion-Controlled OLED Mini Game Console**

**Magical Runner** is a fully self-contained handheld game console built with CircuitPython, featuring a 0.96" OLED display, accelerometer-based motion controls, rotary encoder UI navigation, a buzzer for sound effects, and NeoPixel feedback.
Everything — from character abilities to map generation, scoring, and high-score persistence — runs on a custom-designed hardware platform powered by the ESP32-C3.

The console offers 5 playable characters inspired by *Puella Magi Madoka Magica* (also known simply as *Madoka Magica*). Each character has unique abilities, enhancing replayability and strategic movement.
Players tilt the device left or right to dodge obstacles, flick the device vertically to jump, and perform a shake gesture to activate their ultimate skill.

The entire system is designed to feel like a tiny, physical arcade cabinet you can hold in your hands.

---

## **Key Features**

* **Motion-controlled gameplay** powered by ADXL345 accelerometer
* **Procedurally generated maps** with difficulty scaling
* **Six unique characters**, each with personalized stats and skills
* **Real-time OLED rendering** optimized for 128×64 SSD1306 screens
* **Persistent high-score system** stored in internal flash
* **Modular architecture**, where each logical component lives in its own file
* **Mix of physical and digital UI**: rotary encoder for menus, gesture input for gameplay
* **Device feedback system** using NeoPixel colors + buzzer sound effects

---

## **Code Structure**

```
/ (root)
│
├── code.py              # Main program, auto-runs on boot
├── character.py         # Character definitions, abilities, stats
├── game_manager.py      # Game flow, difficulty, map generation
├── input_manager.py     # Accelerometer + rotary encoder handling
├── oled_renderer.py     # All OLED rendering utilities
├── score_manager.py     # High-score reading, writing, sorting
├── scores.txt           # Local high-score data
├── utils.py             # Buzzer, NeoPixel, audio, misc helpers
└── README.md            # Project documentation
```

---

## **Hardware Used**

* **Xiao ESP323C Microcontroller**
* **SSD1306 128×64 OLED**
* **ADXL345 accelerometer** for tilt and shake detection
* **Rotary encoder + button** for menu navigation
* **Buzzer** for audio effects
* **4 NeoPixel RGB LED** for player feedback(1 for Character, 3 for HP display)
* **Switch** for power switch on/off
* **LiPo Battery** for power supply

* **Custom-designed enclosure** (See below)

---

# **Gameplay**

## **Basic Controls**

The map is procedurally generated based on difficulty.
Different difficulties modify the scrolling speed and obstacle density.
The character always stays on the bottom row while the map scrolls downward at a fixed speed.
There are 5 lanes, and players move between them using motion controls.

Controls:

* **Tilt left**: Move the character one lane to the left
* **Tilt right**: Move the character one lane to the right
* **Fast shaking**: Activate the character’s ultimate skill (only when energy reaches 100%)

Energy starts at 0%.
Each step forward restores **5% energy**, and energy **carries over between stages**.

---

## **Character Skills**

Each character has a unique ultimate skill.
The skill is triggered by shaking and can only be used when energy is at **100%**.

* **Madoka**: Clears all obstacles in a 5×5 area of the screen
* **Homura**: Slows down time dramatically, making the map scroll extremely slowly for the rest of the stage
* **Sayaka**: Restores 200 HP (HP is also used as score)
* **Mami**: Clears all obstacles in the player’s current lane for the next 10 rows upward
* **Kyoko**: Dashes forward 3 rows instantly

Skill effects last for the duration of the stage, and energy persists across stages.

---

## **HP and Failure Conditions**

* The player has a maximum of **3 HP** for the entire run
* At the start of each stage, the stage score resets to **0**
* **Moving forward +1 row awards 10 points**
* **Colliding with obstacles deducts 50 points**

At the end of each stage:

* If the stage score is **below 0**, the player loses **1 HP**
* If HP reaches **0**, the entire game ends

After Game Over, the total score and the High Score list are displayed.
If the player reaches the top 3, the game will show **“New High Score!”**.

---

# **Enclosure and Interaction Design**

## **Enclosure Concept**

The enclosure follows the form of a compact game controller, inspired by the ergonomics of endless-runner games.
The goal was to create a device that feels intuitive to grip, simple to assemble, and friendly for rapid iteration during development.

The central body is printed in white PLA, while the two side handles are printed in translucent PLA.
The handles double as structural locks for the upper and lower shells, making the assembly easy to open and re-close without additional hardware.
A USB-C port is placed on the left side and is normally hidden under the handle during use.

This design keeps the device lightweight, durable, and highly serviceable.

---

## **UI Layout**

The OLED display is positioned at the center of the front panel, forming the primary gameplay interface.

* **Left side**: Power switch and buzzer
* **Right side**: Rotary encoder for menu navigation and difficulty/character selection
* **Bottom edge**: Four indicator LEDs

  * Three LEDs on the left represent player HP and turn off one by one as HP decreases
  * One LED on the right represents the currently selected character or character state

The UI is designed for glanceability during fast gameplay and supports clear feedback through both visuals and sound.

---

## **Interactions**

When the player is selecting a character, the OLED displays the character’s icon while the LEDs cycle through that character’s signature color in a soft breathing pattern.

Once a character is locked in, the breathing effect stops and the LED stays at a steady glow in the assigned color.

---

## **Sound Design**

Audio cues are used to strengthen the game’s personality and responsiveness.

* The opening and ending themes are simple tone sequences referencing the original series’ TV-animation opening and the movie ending theme
* Unique sound cues play when the player activates their ultimate skill or takes damage

These light musical elements give the device a sense of charm while keeping the audio system minimal and hardware-friendly.

---