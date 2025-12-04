#!/usr/bin/env python3
# pigpio_neopixel_compatible.py
# Minimal-change replacement for Adafruit NeoPixel usage using pigpio.
# Requires pigpio daemon (sudo systemctl enable --now pigpiod)

import pigpio
import time
import atexit
from threading import Lock

# -----------------------------
# Minimal Multi-strip pigpio NeoPixel implementation
# (keeps API similar: pixels = [Strip(...), ...]; pixels[i][j] = (r,g,b); auto_write option)
# -----------------------------

# WS2812 timing values (microseconds)
T1H_US = 800  # high time for '1' (approx 0.8us)
T1L_US = 450  # low time for '1'
T0H_US = 400  # high time for '0'
T0L_US = 850  # low time for '0'
RESET_US = 60  # Reset time in microseconds (>50us)

# Helper: clamp color
def clamp_color(c):
    return (int(max(0, min(255, c[0]))),
            int(max(0, min(255, c[1]))),
            int(max(0, min(255, c[2]))))

class PigpioMulti:
    """
    Combines multiple strips and builds a single pigpio wave for a show() call.
    This class is intentionally minimal to keep your original code simple.
    """
    def __init__(self, pi, strips, brightness=1.0):
        """
        pi: pigpio.pi() instance
        strips: list of tuples (gpio_pin, led_count)
        brightness: 0.0..1.0
        """
        self.pi = pi
        self.pins = [s[0] for s in strips]
        self.counts = [s[1] for s in strips]
        self.brightness = float(brightness)
        self.lock = Lock()

        # pixel buffers per strip (r,g,b tuples)
        self.pixels = [ [(0,0,0)] * c for c in self.counts ]

        # init pins
        for p in self.pins:
            self.pi.set_mode(p, pigpio.OUTPUT)
            self.pi.write(p, 0)

        atexit.register(self._cleanup)
        self._last_wave = None

    def set_pixel(self, strip_index, pixel_index, color):
        self.pixels[strip_index][pixel_index] = clamp_color(color)

    def fill_strip(self, strip_index, color):
        color = clamp_color(color)
        for i in range(self.counts[strip_index]):
            self.pixels[strip_index][i] = color

    def show(self):
        """
        Build a pigpio wave combining all strips and send it once.
        This constructs per-bit pulses so each GPIO gets the correct timing for its bit.
        """
        with self.lock:
            # delete previous wave
            try:
                if self._last_wave is not None:
                    self.pi.wave_delete(self._last_wave)
            except Exception:
                pass
            self._last_wave = None

            max_pixels = max(self.counts)
            # build bitstreams per strip: MSB-first GRB per LED
            bitstreams = []
            for s_idx in range(len(self.pins)):
                bs = []
                for i in range(max_pixels):
                    if i < self.counts[s_idx]:
                        r,g,b = self.pixels[s_idx][i]
                        # apply brightness
                        r = int(r * self.brightness)
                        g = int(g * self.brightness)
                        b = int(b * self.brightness)
                        grb = (g & 0xFF, r & 0xFF, b & 0xFF)
                    else:
                        grb = (0,0,0)
                    for byte in grb:
                        for bit in range(7, -1, -1):
                            bs.append(1 if (byte >> bit) & 1 else 0)
                bitstreams.append(bs)

            total_bits = len(bitstreams[0])
            pulses = []

            # For efficiency, precompute GPIO bit masks
            gpio_masks = [1 << pin for pin in self.pins]

            for bit_index in range(total_bits):
                # determine which pins require '1' for this bit
                want1_mask = 0
                for i_pin, mask in enumerate(gpio_masks):
                    if bitstreams[i_pin][bit_index]:
                        want1_mask |= mask

                # The sequence for WS2812: set '1' pins high. '0' pins should be high only for T0H_US.
                # We construct three pulses per bit where needed:
                # 1) set all '1' pins high (others low) for T0H_US
                # 2) after T0H_US, clear pins that are '0' (they were never set), keep '1' pins high for (T1H_US - T0H_US)
                # 3) clear remaining pins and wait T1L_US
                # Implementation with pigpio.pulse(on_mask, off_mask, delay)
                # Step 1:
                if want1_mask:
                    # set want1 pins high; ensure other pins are low
                    pulses.append(pigpio.pulse(want1_mask, 0, T0H_US))
                    if T1H_US > T0H_US:
                        pulses.append(pigpio.pulse(0,0, T1H_US - T0H_US))
                    # then clear want1 pins and wait T1L_US
                    pulses.append(pigpio.pulse(0, want1_mask, T1L_US))
                else:
                    # all zeros: no pins high for entire T0H + T0L (we still need timing)
                    pulses.append(pigpio.pulse(0,0, T0H_US + T0L_US))

            # Reset pulse
            pulses.append(pigpio.pulse(0,0, RESET_US))

            # load and send wave
            try:
                self.pi.wave_clear()
                self.pi.wave_add_generic(pulses)
                wid = self.pi.wave_create()
                if wid >= 0:
                    self._last_wave = wid
                    self.pi.wave_send_once(wid)
                    # wait until finished
                    while self.pi.wave_tx_busy():
                        time.sleep(0.001)
                else:
                    raise RuntimeError("Failed to create pigpio wave")
            except Exception as e:
                print("Error sending wave:", e)

    def _cleanup(self):
        try:
            if self._last_wave is not None:
                self.pi.wave_delete(self._last_wave)
        except Exception:
            pass
        for gpio in self.pins:
            try:
                self.pi.write(gpio, 0)
            except Exception:
                pass

# -----------------------------
# Small wrapper so code can use pixels[i][j] style like neopixel.NeoPixel
# -----------------------------
class StripProxy:
    def __init__(self, multi, idx, auto_write=True):
        self._multi = multi
        self._idx = idx
        self.auto_write = auto_write
        self.length = self._multi.counts[idx]

    def __setitem__(self, key, color):
        # allow setting item or slice not implemented; keep simple
        self._multi.set_pixel(self._idx, key, color)
        if self.auto_write:
            self._multi.show()

    def __getitem__(self, key):
        return self._multi.pixels[self._idx][key]

    def __len__(self):
        return self.length

# -----------------------------
# === Your original code adapted ===
# minimal changes: replace neopixel.NeoPixel(...) with StripProxy objects backed by PigpioMulti
# -----------------------------
if __name__ == "__main__":
    # Connect to pigpio
    pi = pigpio.pi()
    if not pi.connected:
        raise SystemExit("pigpio daemon not running. Start with: sudo systemctl start pigpiod")

    # Define strips as (BCM_pin, length) matching your original board.Dxx usage:
    # board.D18 -> BCM 18, D12->12, D13->13, D19->19, D21->21
    strip_defs = [
        (18, 50),   # Level 1
        (12, 50),   # Level 2
        (13, 50),   # Level 3
        (19, 100),  # Level 4
        (21, 50)    # Level 5
    ]

    multi = PigpioMulti(pi, strip_defs, brightness=0.8)

    # create "pixels" list of proxies to mimic neopixel.NeoPixel behavior (auto_write=True keeps original behavior)
    pixels = [StripProxy(multi, i, auto_write=True) for i in range(len(strip_defs))]

    BLUE = (0, 0, 255)
    OFF = (0, 0, 0)

    # ===== LEVEL 5 =====
    for i in range(0, 0):  # Pixels 1-49 (0, 48)
        pixels[4][i] = BLUE

    # ===== LEVEL 4 =====
    for i in range(0, 79):  # Pixels 1-93 (0, 93)
        pixels[3][i] = BLUE

    # ===== LEVEL 3 =====
    for i in range(0, 0):  # Pixels 0-0 (0, 0)
        pixels[2][i] = BLUE

    # ===== LEVEL 2 =====
    for i in range(0, 0):  # Pixels 0-0 (0, 0)
        pixels[1][i] = BLUE

    # ===== LEVEL 1 =====
    for i in range(0, 0):  # Pixels 0-0 (0, 0)
        pixels[0][i] = BLUE

    # keep script alive briefly so you can see results (adjust or remove as you want)
    time.sleep(1)

    # cleanup
    pi.stop()