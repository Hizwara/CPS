import board
import neopixel
import time

# Initialize LED strips
pixels = [
    neopixel.NeoPixel(board.D18, 200, brightness=0.8, auto_write=True),  # Level 1 
    neopixel.NeoPixel(board.D12, 200, brightness=0.8, auto_write=True),  # Level 2
    neopixel.NeoPixel(board.D13, 200, brightness=0.8, auto_write=True),  # Level 3
    neopixel.NeoPixel(board.D19, 200, brightness=0.8, auto_write=True),  # Level 4
    neopixel.NeoPixel(board.D21, 200, brightness=0.8, auto_write=True)   # Level 5
]

BLUE = (0, 0, 255)
OFF = (0, 0, 0)

# Turn off all LEDs first
for strip in pixels:
    strip.fill(OFF)

print("Testing LED pixels by level...")

# ===== LEVEL 5 =====
print("LEVEL 5:")
pixels[4].fill(OFF)  # Turn off all first
# Modify the pixel range below (start_pixel-1 to end_pixel-1 because of 0-indexing)
for i in range(0, 10):  # Pixels 1-10
    pixels[4][i] = BLUE
time.sleep(2)

# ===== LEVEL 4 =====
print("LEVEL 4:")
pixels[3].fill(OFF)  # Turn off all first
# Modify the pixel range below
for i in range(10, 20):  # Pixels 11-20
    pixels[3][i] = BLUE
time.sleep(2)

# ===== LEVEL 3 =====
print("LEVEL 3:")
pixels[2].fill(OFF)  # Turn off all first
# Modify the pixel range below
for i in range(20, 30):  # Pixels 21-30
    pixels[2][i] = BLUE
time.sleep(2)

# ===== LEVEL 2 =====
print("LEVEL 2:")
pixels[1].fill(OFF)  # Turn off all first
# Modify the pixel range below
for i in range(30, 40):  # Pixels 31-40
    pixels[1][i] = BLUE
time.sleep(2)

# ===== LEVEL 1 =====
print("LEVEL 1:")
pixels[0].fill(OFF)  # Turn off all first
# Modify the pixel range below
for i in range(40, 50):  # Pixels 41-50
    pixels[0][i] = BLUE
time.sleep(2)

print("Test complete!")

# Keep LEDs on until Ctrl+C
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    for strip in pixels:
        strip.fill(OFF)
    print("All LEDs turned off.")