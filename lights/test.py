import time
import board
import neopixel

# --- LED SETUP ---

# 5 terraces (bottom → top)
print("Initializing LED strips...")

try:
    pixels = [
    neopixel.NeoPixel(board.D18, 30, brightness=0.8, auto_write=True),  # Level 1
    neopixel.NeoPixel(board.D12, 30, brightness=0.8, auto_write=True),  # Level 2
    neopixel.NeoPixel(board.D13, 30, brightness=0.8, auto_write=True),  # Level 3
    neopixel.NeoPixel(board.D19, 30, brightness=0.8, auto_write=True),  # Level 4
    neopixel.NeoPixel(board.D21, 30, brightness=0.8, auto_write=True)   # Level 5
    ]
    print("LED strips initialized successfully!")
except Exception as e:
    print(f"Error initializing LED strips: {e}")
    exit(1)

BLUE = (0, 0, 255)
OFF = (0, 0, 0)

def test_leds():
    """Turn all terraces blue simultaneously."""
    print("Turning on all LEDs...")
    # Turn all LEDs on all levels to blue
    for i, strip in enumerate(pixels):
        print(f"Setting Level {i+1} to blue...")
        strip.fill(BLUE)
        time.sleep(0.1)  # Small delay to see each level turn on
    print("All levels should now be BLUE")

try:
    test_leds()
    print("Lights are on. Press Ctrl+C to turn off.")
    # Keep lights on until interrupted
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down safely...")
    for i, strip in enumerate(pixels):
        print(f"Turning off Level {i+1}...")
        strip.fill(OFF)
    print("All lights off.")
