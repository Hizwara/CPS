import time
import board
import neopixel

# 5 terraces (bottom → top)
print("Initializing LED strips...")

try:
    pixels = [
        neopixel.NeoPixel(board.D18, 100, brightness=0.8, auto_write=True),  # Level 1 
        neopixel.NeoPixel(board.D12, 100, brightness=0.8, auto_write=True),  # Level 2
        neopixel.NeoPixel(board.D13, 100, brightness=0.8, auto_write=True),  # Level 3
        neopixel.NeoPixel(board.D19, 100, brightness=0.8, auto_write=True),  # Level 4
        neopixel.NeoPixel(board.D21, 100, brightness=0.8, auto_write=True)   # Level 5
    ]
    print("LED strips initialized successfully!")
except Exception as e:
    print(f"Error initializing LED strips: {e}")
    exit(1)

BLUE = (0, 0, 255)
OFF = (0, 0, 0)

def flowing_water():
    """Simulate water flowing from top (Level 5) to bottom (Level 1) with accumulation."""
    print("Starting water flow animation...")
    
    # Turn all LEDs off first
    for strip in pixels:
        strip.fill(OFF)
    
    # Flow from Level 5 down to Level 1 (water accumulates)
    for i in range(4, -1, -1):  # Start from index 4 (Level 5) down to 0 (Level 1)
        pixels[i].fill(BLUE)  # Turn on current level
        print(f"Water reaches Level {i+1}")
        time.sleep(1)  # Each level lights for 1 second
    
    print("Water flow complete - all levels filled!")

def turn_all_off():
    """Turn off all LEDs on all levels."""
    print("Turning off all LEDs...")
    for i, strip in enumerate(pixels):
        strip.fill(OFF)
    print("All lights are now OFF")

try:
    print("Water flow animation started. Press Ctrl+C to stop.")
    
    while True:
        flowing_water()  # 5 seconds total (5 levels × 1 second each)
        print("Waiting 3 seconds before next flow cycle...")
        time.sleep(3)  # Wait 3 seconds before repeating

except KeyboardInterrupt:
    print("\nReceived Ctrl+C, shutting down safely...")
    turn_all_off()
    print("Program terminated successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Turning off all lights as safety measure...")
    turn_all_off()
finally:
    print("Cleanup complete.")
