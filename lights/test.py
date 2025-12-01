import time
import board
import neopixel

# 5 terraces (bottom → top)
print("Initializing LED strips...")

try:
    pixels = [
        neopixel.NeoPixel(board.D18, 200, brightness=0.8, auto_write=True),  # Level 1
        neopixel.NeoPixel(board.D12, 200, brightness=0.8, auto_write=True),  # Level 2
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

def turn_all_blue():
    """Turn all terraces blue simultaneously."""
    print("Turning on all LEDs to blue...")
    for i, strip in enumerate(pixels):
        print(f"Setting Level {i+1} to blue...")
        strip.fill(BLUE)
    print("All levels are now BLUE")

def turn_all_off():
    """Turn off all LEDs on all levels."""
    print("Turning off all LEDs...")
    for i, strip in enumerate(pixels):
        print(f"Turning off Level {i+1}...")
        strip.fill(OFF)
    print("All lights are now OFF")

try:
    turn_all_blue()
    print("All lights are on. Press Ctrl+C to turn off.")
    
    # Keep lights on until interrupted
    while True:
        time.sleep(1)

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
