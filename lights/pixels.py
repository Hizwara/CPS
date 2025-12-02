import board
import neopixel

# Initialize LED strips
pixels = [
    neopixel.NeoPixel(board.D18, 50, brightness=0.8, auto_write=True),  # Level 1 
    neopixel.NeoPixel(board.D12, 50, brightness=0.8, auto_write=True),  # Level 2
    neopixel.NeoPixel(board.D13, 50, brightness=0.8, auto_write=True),  # Level 3
    neopixel.NeoPixel(board.D19, 50, brightness=0.8, auto_write=True),  # Level 4
    neopixel.NeoPixel(board.D21, 50, brightness=0.8, auto_write=True)   # Level 5
]

BLUE = (0, 0, 255)
OFF = (0, 0, 0)

# Turn off all LEDs first
for strip in pixels:
    strip.fill(OFF)

# ===== LEVEL 5 =====
for i in range(0, 48):  # Pixels 1-10 (modify this range)
    pixels[4][i] = BLUE

# ===== LEVEL 4 =====
for i in range(0, 0):  # Pixels 11-20 (modify this range)
    pixels[3][i] = BLUE

# ===== LEVEL 3 =====
for i in range(0, 0):  # Pixels 21-30 (modify this range)
    pixels[2][i] = BLUE

# ===== LEVEL 2 =====
for i in range(0, 0):  # Pixels 31-40 (modify this range)
    pixels[1][i] = BLUE

# ===== LEVEL 1 =====
for i in range(0, 0):  # Pixels 41-50 (modify this range)
    pixels[0][i] = BLUE