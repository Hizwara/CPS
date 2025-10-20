import time
import board
import neopixel
import adafruit_dht

# --- SENSOR SETUP ---
# Connect your DHT22 sensor data pin to GPIO4 (physical pin 7)
dhtDevice = adafruit_dht.DHT22(board.D4)

# --- LED STRIPS SETUP ---
# Each terrace has its own LED strip connected to a GPIO pin
# Adjust LED counts according to your setup
pixels1 = neopixel.NeoPixel(board.D18, 30, brightness=0.8, auto_write=False)
pixels2 = neopixel.NeoPixel(board.D21, 30, brightness=0.8, auto_write=False)
pixels3 = neopixel.NeoPixel(board.D22, 30, brightness=0.8, auto_write=False)

terraces = [pixels1, pixels2, pixels3]

# --- HELPER FUNCTIONS ---A
def fill_all(color):
    """Set all strips to a specific color."""
    for strip in terraces:
        strip.fill(color)
        strip.show()

def show_water_level(level, color=(0, 100, 255)):
    """Light up terraces according to the humidity level (1–3)."""
    fill_all((0, 0, 0))  # Turn off all first
    for i in range(level):
        terraces[i].fill(color)
        terraces[i].show()

# --- MAIN LOOP ---
try:
    while True:
        try:
            # Read from DHT22
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print(f"🌤 Temp: {temperature:.1f}°C | 💧 Humidity: {humidity:.1f}%")

            # --- DECISION LOGIC ---
            # Determine water level based on humidity percentage
            if humidity < 50:
                level = 1   # Dry season – top terrace only
            elif humidity < 75:
                level = 2   # Normal moisture – top 2 terraces filled
            else:
                level = 3   # Rainy / high humidity – all terraces filled

            # Optionally adjust color based on temperature (hotter = less blue)
            blue_value = max(0, min(255, int(255 - (temperature * 3))))
            color = (0, 100, blue_value)

            # Display LED pattern
            show_water_level(level, color)
            print(f"💡 Lighting up {level} terraces\n")

            time.sleep(5)  # Wait before next read

        except RuntimeError as e:
            # DHT22 often throws read errors; just retry
            print("Sensor read error:", e.args)
            time.sleep(2)

except KeyboardInterrupt:
    print("🛑 Shutting down system...")
    fill_all((0, 0, 0))
