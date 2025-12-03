import time
import board
import neopixel

# 5 terraces (bottom → top)
print("Initializing LED strips...")

try:
    pixels = [
        neopixel.NeoPixel(board.D18, 150, brightness=0.8, auto_write=False),  # Level 1 
        neopixel.NeoPixel(board.D12, 150, brightness=0.8, auto_write=False),  # Level 2
        neopixel.NeoPixel(board.D13, 150, brightness=0.8, auto_write=False),  # Level 3
        neopixel.NeoPixel(board.D19, 100, brightness=0.8, auto_write=False),  # Level 4
        neopixel.NeoPixel(board.D21, 100, brightness=0.8, auto_write=False)   # Level 5
    ]
    print("LED strips initialized successfully!")
except Exception as e:
    print(f"Error initializing LED strips: {e}")
    exit(1)

OFF = (0, 0, 0)
BLUE = (0, 0, 255)
BRIGHT_BLUE = (0, 100, 255)

def setup_level_ranges():
    """Set up the pixel ranges for each level"""
    # Turn off all LEDs first
    for strip in pixels:
        strip.fill(OFF)
        strip.show()

def blink_level(level_index, pixel_range):
    """Blink a specific level for 1 second"""
    print(f"Blinking Level {level_index + 1}...")
    
    # Turn ON the level
    for i in range(pixel_range[0], pixel_range[1]):
        pixels[level_index][i] = BLUE
    pixels[level_index].show()
    
    time.sleep(0.5)  # ON for 0.5 seconds
    
    # Turn OFF the level
    for i in range(pixel_range[0], pixel_range[1]):
        pixels[level_index][i] = OFF
    pixels[level_index].show()
    
    time.sleep(0.5)  # OFF for 0.5 seconds

def flowing_water_animation():
    """Continuous flowing water animation from Level 5 to Level 1"""
    # Define pixel ranges for each level [start, end]
    level_ranges = [
        [0, 60],   # Level 1: pixels 0-59
        [0, 40],   # Level 2: pixels 0-39
        [0, 30],   # Level 3: pixels 0-29
        [0, 79],   # Level 4: pixels 0-78
        [0, 50]    # Level 5: pixels 0-49
    ]
    
    # Blink from Level 5 down to Level 1
    for level in range(4, -1, -1):  # 4,3,2,1,0 (Level 5 down to Level 1)
        blink_level(level, level_ranges[level])

# Initial setup
setup_level_ranges()
print("Starting continuous flowing water animation...")
print("Press Ctrl+C to stop")

try:
    while True:
        flowing_water_animation()

except KeyboardInterrupt:
    print("\nStopping animation...")
    for strip in pixels:
        strip.fill(OFF)
        strip.show()
    print("All LEDs turned off.")
