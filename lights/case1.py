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

# Color definitions
OFF = (0, 0, 0)
YELLOW = (255, 255, 0)      # Drought <50%
LIGHT_BLUE = (173, 216, 230)  # 50-75%
DARK_BLUE = (0, 0, 139)     # 75-100%
RED = (255, 0, 0)           # Overflow >100%

# Water system parameters (MODIFY THESE FOR DIFFERENT SCENARIOS)
NORMAL_SPRING_RATE = 3.0    # Normal water input (L/s)
HEAVY_RAIN_RATE = 10.0      # Heavy rain water input (L/s) - MODIFY THIS
current_spring_rate = NORMAL_SPRING_RATE

# Blockage parameters
LEVEL_4_NORMAL_FLOW = 2.0   # Normal Level 4 flow rate
LEVEL_4_BLOCKED_FLOW = 0.3  # Blocked Level 4 flow rate (partially blocked) - MODIFY THIS

# Water capacities for each level in litres (larger for lower levels)
water_capacities = [400, 300, 250, 200, 150]  # Level 1 to Level 5

# Flow rates for each level in L/s (Level 4 will be modified during blockage)
flow_rates = [4.0, 3.0, 2.5, LEVEL_4_NORMAL_FLOW, 1.5]  # Level 1 to Level 5 (L/s)

# Current water levels in litres (start at 50% capacity)
current_water_levels = [200.0, 150.0, 125.0, 100.0, 75.0]  # Level 1 to Level 5

# Simulation control flags
level_4_blocked = False     # Set to True to trigger Level 4 blockage - MANUAL TRIGGER
heavy_rain_active = False   # Set to True to trigger heavy rain - MANUAL TRIGGER

def get_color_for_level(level_index):
    """Get LED color based on water level percentage"""
    water_percentage = (current_water_levels[level_index] / water_capacities[level_index]) * 100
    
    if water_percentage < 50:
        return YELLOW
    elif water_percentage < 75:
        return LIGHT_BLUE
    elif water_percentage <= 100:
        return DARK_BLUE
    else:
        return RED

def update_water_system():
    """Update water levels with blockage and heavy rain scenarios"""
    global current_water_levels, current_spring_rate, flow_rates
    
    # Time step (1 second per update cycle)
    time_step = 1.0
    
    # Update spring rate based on heavy rain status
    if heavy_rain_active:
        current_spring_rate = HEAVY_RAIN_RATE
    else:
        current_spring_rate = NORMAL_SPRING_RATE
    
    # Update Level 4 flow rate based on blockage status
    if level_4_blocked:
        flow_rates[3] = LEVEL_4_BLOCKED_FLOW  # Level 4 (index 3) is blocked
    else:
        flow_rates[3] = LEVEL_4_NORMAL_FLOW   # Level 4 normal flow
    
    # Add water to Level 5 from water spring
    water_input = current_spring_rate * time_step
    current_water_levels[4] += water_input
    
    # Water flows from higher levels to lower levels when overflowing
    # Process from Level 5 down to Level 2
    for i in range(4, 0, -1):  # Level 5 (index 4) down to Level 2 (index 1)
        if current_water_levels[i] > water_capacities[i]:
            # Calculate overflow
            overflow = current_water_levels[i] - water_capacities[i]
            
            # Calculate actual transfer rate (limited by level's flow rate)
            actual_transfer = min(overflow, flow_rates[i] * time_step)
            
            # Transfer water to next lower level
            current_water_levels[i] -= actual_transfer
            current_water_levels[i-1] += actual_transfer
    
    # Level 1 outflow (water disappears from system)
    if current_water_levels[0] > 0:
        outflow = min(current_water_levels[0], flow_rates[0] * time_step)
        current_water_levels[0] -= outflow

def display_water_status():
    """Display current water status with blockage and rain indicators"""
    print("\n" + "="*70)
    print("FLOOD SIMULATION - WATER SYSTEM STATUS")
    print("="*70)
    
    # Display current conditions
    rain_status = "HEAVY RAIN" if heavy_rain_active else "NORMAL"
    blockage_status = "BLOCKED" if level_4_blocked else "NORMAL"
    
    print(f"Weather: {rain_status} | Water Input: {current_spring_rate} L/s")
    print(f"Level 4 Flow: {blockage_status} ({flow_rates[3]} L/s)")
    print("-"*70)
    
    flood_levels = 0  # Count levels in flood state
    
    for i in range(5):
        level_num = i + 1
        water_pct = (current_water_levels[i] / water_capacities[i]) * 100
        capacity = water_capacities[i]
        current = current_water_levels[i]
        flow_rate = flow_rates[i]
        
        if water_pct < 50:
            status = "DROUGHT"
        elif water_pct < 75:
            status = "NORMAL"
        elif water_pct <= 100:
            status = "FULL"
        else:
            status = "⚠️  FLOOD ⚠️"
            flood_levels += 1
        
        # Add blockage indicator for Level 4
        blockage_indicator = " [BLOCKED]" if level_4_blocked and i == 3 else ""
        
        print(f"Level {level_num}: {current:6.1f}L/{capacity}L ({water_pct:5.1f}%) | Flow: {flow_rate} L/s | {status}{blockage_indicator}")
    
    # Calculate system throughput
    total_input = current_spring_rate
    total_output = min(current_water_levels[0], flow_rates[0]) if current_water_levels[0] > 0 else 0
    print("-"*70)
    print(f"System Input: {total_input} L/s | System Output: {total_output:.1f} L/s")
    
    if flood_levels > 0:
        print(f"⚠️  FLOOD ALERT: {flood_levels} levels in flood state! ⚠️")
    
    print("="*70)

def blink_blocked_level(level_index, pixel_range):
    """Special red blinking for blocked level"""
    # Red ON
    for i in range(pixel_range[0], pixel_range[1]):
        pixels[level_index][i] = RED
    pixels[level_index].show()
    
    time.sleep(0.5)  # Red ON for 0.5 seconds
    
    # Turn OFF
    for i in range(pixel_range[0], pixel_range[1]):
        pixels[level_index][i] = OFF
    pixels[level_index].show()
    
    time.sleep(0.5)  # OFF for 0.5 seconds

def keep_other_levels_colored(current_level, level_ranges):
    """Keep all other levels at their water capacity colors while one level blinks"""
    for i in range(5):
        if i != current_level:  # Keep all other levels at capacity color
            color = get_color_for_level(i)
            for j in range(level_ranges[i][0], level_ranges[i][1]):
                pixels[i][j] = color
            pixels[i].show()

def blink_level(level_index, pixel_range, level_ranges):
    """Blink a specific level with special handling for blocked Level 4"""
    print(f"Blinking Level {level_index + 1}...")
    
    # Special red blinking for blocked Level 4
    if level_index == 3 and level_4_blocked:  # Level 4 is index 3
        print("⚠️  Level 4 BLOCKED - Red blinking!")
        keep_other_levels_colored(level_index, level_ranges)
        blink_blocked_level(level_index, pixel_range)
        return
    
    # Normal blinking for other levels
    level_color = get_color_for_level(level_index)
    
    # Ensure all other levels show their capacity colors
    keep_other_levels_colored(level_index, level_ranges)
    
    # Turn OFF the current level
    for i in range(pixel_range[0], pixel_range[1]):
        pixels[level_index][i] = OFF
    pixels[level_index].show()
    
    time.sleep(0.5)  # OFF for 0.5 seconds
    
    # Turn ON the current level with capacity color
    for i in range(pixel_range[0], pixel_range[1]):
        pixels[level_index][i] = level_color
    pixels[level_index].show()
    
    time.sleep(0.5)  # ON for 0.5 seconds

def flowing_water_animation():
    """Water animation with flood scenario simulation"""
    # Define pixel ranges for each level [start, end]
    level_ranges = [
        [0, 60],   # Level 1: pixels 0-59
        [0, 40],   # Level 2: pixels 0-39
        [0, 30],   # Level 3: pixels 0-29
        [0, 79],   # Level 4: pixels 0-78
        [0, 50]    # Level 5: pixels 0-49
    ]
    
    # Update water system
    update_water_system()
    
    # Display status every 5 cycles
    cycle_count = getattr(flowing_water_animation, 'cycle_count', 0)
    flowing_water_animation.cycle_count = cycle_count + 1
    
    if cycle_count % 5 == 0:
        display_water_status()
    
    # Blink from Level 5 down to Level 1
    for level in range(4, -1, -1):  # 4,3,2,1,0 (Level 5 down to Level 1)
        blink_level(level, level_ranges[level], level_ranges)

# Initial setup
print("Setting up flood simulation scenario...")
print(f"Normal Spring Rate: {NORMAL_SPRING_RATE} L/s")
print(f"Heavy Rain Rate: {HEAVY_RAIN_RATE} L/s")
print(f"Level 4 Normal Flow: {LEVEL_4_NORMAL_FLOW} L/s")
print(f"Level 4 Blocked Flow: {LEVEL_4_BLOCKED_FLOW} L/s")
print("\n" + "="*50)
print("MANUAL TRIGGERS (Modify these variables):")
print("level_4_blocked = False  # Set to True to block Level 4")
print("heavy_rain_active = False  # Set to True for heavy rain")
print("="*50)

for i in range(5):
    color = get_color_for_level(i)
    pixels[i].fill(color)
    pixels[i].show()

time.sleep(3)
display_water_status()

print("\nStarting flood simulation...")
print("Modify 'level_4_blocked' and 'heavy_rain_active' variables to trigger scenarios")
print("Press Ctrl+C to stop")

try:
    while True:
        flowing_water_animation()

except KeyboardInterrupt:
    print("\nStopping flood simulation...")
    for strip in pixels:
        strip.fill(OFF)
        strip.show()
    print("Flood simulation ended.")