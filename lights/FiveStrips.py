import time
import board
import neopixel
import adafruit_dht

# --- SENSOR SETUP ---
dhtDevice = adafruit_dht.DHT22(board.D4)  # Using GPIO4 for DHT22

# --- LED SETUP ---
pixels = [
    neopixel.NeoPixel(board.D18, 30, brightness=0.8, auto_write=False),
    neopixel.NeoPixel(board.D12, 30, brightness=0.8, auto_write=False),
    neopixel.NeoPixel(board.D13, 30, brightness=0.8, auto_write=False),
    neopixel.NeoPixel(board.D21, 30, brightness=0.8, auto_write=False),
    neopixel.NeoPixel(board.D19, 30, brightness=0.8, auto_write=False)
]

# --- HELPER FUNCTIONS ---
def fill_all(color):
    for strip in pixels:
        strip.fill(color)
        strip.show()

def water_flow(level):
    """Light up terraces based on 'level' (0–5)."""
    fill_all((0,0,0))  # turn everything off first
    for i in range(level):
        pixels[i].fill((0, 100, 255))
        pixels[i].show()

# --- MAIN LOOP ---
try:
    while True:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print(f"Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")

            # Simple logic: higher humidity → more terraces lit
            if humidity < 40:
                level = 1
            elif humidity < 60:
                level = 2
            elif humidity < 75:
                level = 3
            elif humidity < 85:
                level = 4
            else:
                level = 5

            # Optionally: use temperature to tint color
            color = (0, int(255 - (temperature * 3)), 255)
            for i in range(level):
                pixels[i].fill(color)
                pixels[i].show()

            print(f"Lighting up {level} terraces\n")
            time.sleep(5)

        except RuntimeError as e:
            # DHT sensors sometimes time out; just retry
            print("Sensor read error:", e)
            time.sleep(2)

except KeyboardInterrupt:
    print("Shutting down...")
    fill_all((0, 0, 0))
