import requests
import time
import board
import neopixel

# --- Initialize LEDs as before ---
led_pins = [board.D18, board.D21, board.D12]
led_lengths = [30, 30, 30]
led_strips = [neopixel.NeoPixel(pin, length, brightness=0.5, auto_write=True)
              for pin, length in zip(led_pins, led_lengths)]

API_KEY = "YOUR_API_KEY"
CITY = "Ubud,id"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def map_weather_to_led(temp, humidity, rain):
    if rain > 5:  # mm
        level = 3
        color = (0, 0, 255)
    elif humidity > 80:
        level = 2
        color = (0, 128, 255)
    elif humidity > 60:
        level = 1
        color = (0, 255, 150)
    else:
        level = 0
        color = (0, 0, 0)
    return level, color

while True:
    response = requests.get(URL)
    data = response.json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rain = data.get("rain", {}).get("1h", 0)  # mm of rain last hour

    print(f"Ubud Weather: {temp}°C, {humidity}%, rain: {rain}mm")

    level, color = map_weather_to_led(temp, humidity, rain)
    for i, strip in enumerate(led_strips):
        if i < level:
            strip.fill(color)
        else:
            strip.fill((0, 0, 0))

    time.sleep(600)  # update every 10 minutes
