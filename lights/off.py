import board
import neopixel

# Initialize LED strips with same settings as your other scripts
pixels = [
    neopixel.NeoPixel(board.D18, 200, brightness=0.0, auto_write=True),  # Level 1 
    neopixel.NeoPixel(board.D12, 200, brightness=0.0, auto_write=True),  # Level 2
    neopixel.NeoPixel(board.D13, 200, brightness=0.0, auto_write=True),  # Level 3
    neopixel.NeoPixel(board.D19, 200, brightness=0.0, auto_write=True),  # Level 4
    neopixel.NeoPixel(board.D21, 200, brightness=0.0, auto_write=True)   # Level 5
]

OFF = (0, 0, 0)

print("Turning off all LED pixels...")

# Turn off all LEDs on all levels
for strip in pixels:
    strip.fill(OFF)
    
print("All LED pixels are now OFF")