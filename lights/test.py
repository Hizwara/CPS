import time
import board
import neopixel

# 5 terraces (bottom → top)
print("Initializing LED strips...")

try:
    pixels = [
        neopixel.NeoPixel(board.D18, 150, brightness=0.8, auto_write=True),  # Level 1 
        neopixel.NeoPixel(board.D12, 150, brightness=0.8, auto_write=True),  # Level 2
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
    """Turn all levels blue initially."""
    print("Turning all levels blue...")
    for strip in pixels:
        strip.fill(BLUE)
    print("All levels are blue!")

def flowing_water():
    """Simulate water flowing with beeping effect (OFF→ON) while keeping all levels blue."""
    print("Starting water flow animation...")
    
    # Flow from Level 5 down to Level 1 (beep each level)
    for i in range(4, -1, -1):  # Start from index 4 (Level 5) down to 0 (Level 1)
        # Beeping effect: turn OFF then ON again
        pixels[i].fill(OFF)  # Turn OFF
        print(f"Level {i+1} beeps - OFF")
        time.sleep(0.5)  # OFF for 0.5 seconds
        pixels[i].fill(BLUE)  # Turn ON again
        print(f"Level {i+1} beeps - ON")
        time.sleep(0.5)  # ON for 0.5 seconds
    
    print("Water flow animation complete!")

def turn_all_off():
    """Turn off all LEDs on all levels."""
    print("Turning off all LEDs...")
    for i, strip in enumerate(pixels):
        strip.fill(OFF)
    print("All lights are now OFF")

try:
    # Initially turn all lights blue
    turn_all_blue()
    print("Continuous water flow animation started. Press Ctrl+C to stop.")
    
    while True:
        flowing_water()  # Continuous flow without delay

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
