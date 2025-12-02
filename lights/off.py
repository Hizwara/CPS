import board
import neopixel

# Initialize LED strips
pixels = [
    neopixel.NeoPixel(board.D18, 150, brightness=0.0, auto_write=True),  # Level 1 
    neopixel.NeoPixel(board.D12, 150, brightness=0.0, auto_write=True),  # Level 2
    neopixel.NeoPixel(board.D13, 100, brightness=0.0, auto_write=True),  # Level 3
    neopixel.NeoPixel(board.D19, 100, brightness=0.0, auto_write=True),  # Level 4
    neopixel.NeoPixel(board.D21, 100, brightness=0.0, auto_write=True)   # Level 5
]

# Turn off all LEDs
OFF = (0, 0, 0)
for strip in pixels:
    strip.fill(OFF)

print("All LEDs turned off.")