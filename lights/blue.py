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

def turn_all_blue():
    """Turn all LEDs to blue initially"""
    print("Turning all LEDs to blue...")
    for strip in pixels:
        strip.fill(BLUE)
        strip.show()
    print("All LEDs are now blue!")

def keep_other_levels_blue(current_level, level_ranges):
    """Keep all other levels blue while one level blinks"""
    for i in range(5):
        if i != current_level:  # Keep all other levels blue
            for j in range(level_ranges[i][0], level_ranges[i][1]):
                pixels[i][j] = BLUE
            pixels[i].show()

def blink_level(level_index, pixel_range, level_ranges):
    """Blink a specific level for 1 second while keeping others blue"""
    print(f"Blinking Level {level_index + 1}...")
    
    # Ensure all other levels stay blue
    keep_other_levels_blue(level_index, level_ranges)
    
    # Turn OFF the current level
    for i in range(pixel_range[0], pixel_range[1]):
        pixels[level_index][i] = OFF
    pixels[level_index].show()
    
    time.sleep(0.5)  # OFF for 0.5 seconds
    
    # Turn ON the current level (back to blue)
    for i in range(pixel_range[0], pixel_range[1]):
        pixels[level_index][i] = BLUE
    pixels[level_index].show()
    
    time.sleep(0.5)  # ON for 0.5 seconds

def flowing_water_animation():
    """Continuous flowing water animation from Level 5 to Level 1"""
    # Define pixel ranges for each level [start, end]
    level_ranges = [
        [0, 50],   # Level 1: pixels 0-59
        [0, 0,   # Level 2: pixels 0-39
        [0, 100],   # Level 3: pixels 0-29
        [0, 0],   # Level 4: pixels 0-78
        [0, 100]    # Level 5: pixels 0-49
    ]
    
    # Blink from Level 5 down to Level 1
    for level in range(4, -1, -1):  # 4,3,2,1,0 (Level 5 down to Level 1)
        blink_level(level, level_ranges[level], level_ranges)

# Initial setup - Turn all LEDs to blue first
turn_all_blue()
time.sleep(2)  # Keep all blue for 2 seconds

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
