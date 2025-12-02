import time
import board
import neopixel
import busio
import adafruit_am2320

# Initialize AM2320 sensor on I2C (SDA/SCL pins)
i2c = busio.I2C(board.SCL, board.SDA)
am2320 = adafruit_am2320.AM2320(i2c)

# Initialize LED strips
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

# Color definitions
YELLOW = (255, 255, 0)      # Drought <50%
LIGHT_BLUE = (173, 216, 230)  # 50-75%
DARK_BLUE = (0, 0, 139)     # 75-100%
RED = (255, 0, 0)           # Overflow >100%
OFF = (0, 0, 0)

# Water capacity for each level (0-100%)
water_levels = [50.0, 50.0, 50.0, 50.0, 50.0]  # Start at 50% for all levels

def read_sensor():
    """Read temperature and humidity from AM2320"""
    try:
        temperature = am2320.temperature
        humidity = am2320.relative_humidity
        if temperature is not None and humidity is not None:
            return temperature, humidity
        else:
            return None, None
    except Exception as e:
        print(f"Sensor error: {e}")
        return None, None

def calculate_flow_rate(temperature, humidity):
    """Calculate water flow rate based on weather conditions"""
    if temperature is None or humidity is None:
        return 1.0  # Default flow rate
    
    # Higher humidity = more water input
    # Lower temperature = more water retention (less evaporation)
    humidity_factor = humidity / 100.0  # 0-1 scale
    temp_factor = max(0.1, (40 - temperature) / 30.0)  # Inverse temperature effect
    
    flow_rate = (humidity_factor * 2) + (temp_factor * 1.5)
    return min(5.0, max(0.1, flow_rate))  # Clamp between 0.1 and 5.0

def get_color_for_level(water_percentage):
    """Get LED color based on water level percentage"""
    if water_percentage < 50:
        return YELLOW
    elif water_percentage < 75:
        return LIGHT_BLUE
    elif water_percentage <= 100:
        return DARK_BLUE
    else:
        return RED

def update_water_system(flow_rate):
    """Update water levels in connected system (Level 5 → 1)"""
    global water_levels
    
    # Add water to Level 5 based on weather (rain input)
    water_input = flow_rate * 2  # Rain input to top level
    water_levels[4] += water_input
    
    # Water flows from higher levels to lower levels
    overflow_rate = flow_rate * 1.5  # How fast water moves between levels
    
    # Process overflow from Level 5 down to Level 1
    for i in range(4, 0, -1):  # Level 5 (index 4) down to Level 2 (index 1)
        if water_levels[i] > 100:
            overflow = (water_levels[i] - 100) * (overflow_rate / 10)
            water_levels[i] -= overflow
            water_levels[i-1] += overflow
    
    # Simulate evaporation/drainage
    evaporation_rate = 0.5
    for i in range(5):
        water_levels[i] = max(0, water_levels[i] - evaporation_rate)

def update_leds():
    """Update LED colors based on water levels"""
    for i in range(5):
        color = get_color_for_level(water_levels[i])
        pixels[i].fill(color)

def display_status(temperature, humidity, flow_rate):
    """Display current system status"""
    print(f"\n--- Water System Status ---")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Flow Rate: {flow_rate:.2f}")
    for i in range(5):
        level_num = i + 1
        water_pct = water_levels[i]
        if water_pct < 50:
            status = "DROUGHT"
        elif water_pct < 75:
            status = "NORMAL"
        elif water_pct <= 100:
            status = "FULL"
        else:
            status = "OVERFLOW"
        print(f"Level {level_num}: {water_pct:.1f}% - {status}")

def turn_all_off():
    """Turn off all LEDs"""
    for strip in pixels:
        strip.fill(OFF)

try:
    print("Water management system started. Press Ctrl+C to stop.")
    
    while True:
        # Read sensor data
        temperature, humidity = read_sensor()
        
        if temperature is not None and humidity is not None:
            # Calculate flow rate based on weather
            flow_rate = calculate_flow_rate(temperature, humidity)
            
            # Update water system
            update_water_system(flow_rate)
            
            # Update LED display
            update_leds()
            
            # Display status every 10 cycles
            if int(time.time()) % 10 == 0:
                display_status(temperature, humidity, flow_rate)
        
        time.sleep(2)  # Update every 2 seconds

except KeyboardInterrupt:
    print("\nShutting down water management system...")
    turn_all_off()
    print("System terminated successfully.")
except Exception as e:
    print(f"System error: {e}")
    turn_all_off()
finally:
    print("Cleanup complete.")
