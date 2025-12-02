import board
import neopixel

# Initialize LED strips
pixels = [
    neopixel.NeoPixel(board.D18, 50, brightness=0.8, auto_write=True),  # Level 1 
    neopixel.NeoPixel(board.D12, 50, brightness=0.8, auto_write=True),  # Level 2
    neopixel.NeoPixel(board.D13, 50, brightness=0.8, auto_write=True),  # Level 3
    neopixel.NeoPixel(board.D19, 100, brightness=0.8, auto_write=True),  # Level 4
    neopixel.NeoPixel(board.D21, 50, brightness=0.8, auto_write=True)   # Level 5
]

BLUE = (0, 0, 255)
OFF = (0, 0, 0)

# ===== LEVEL 5 =====
for i in range(0, 0):  # Pixels 1-49 (0, 48)
    pixels[4][i] = BLUE

# ===== LEVEL 4 =====
for i in range(0, 79):  # Pixels 1-93 (0, 93)
    pixels[3][i] = BLUE

# ===== LEVEL 3 =====
for i in range(0, 0):  # Pixels 0-0 (0, 0)
    pixels[2][i] = BLUE

# ===== LEVEL 2 =====
for i in range(0, 0):  # Pixels 0-0 (0, 0)
    pixels[1][i] = BLUE

# ===== LEVEL 1 =====
for i in range(0, 0):  # Pixels 0-0 (0, 0)
    pixels[0][i] = BLUE
