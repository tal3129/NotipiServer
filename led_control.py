import time
from gpiozero import RGBLED



FLICKER_TIME = 3
FLICKER_TIME_LONG = 8


FLICKER_INTERVAL = 0.3
FLICKER_INTERVAL_SHORT = 0.1

COLOR_OFF = (0,0,0)
COLOR_RED = (1,0,0)
COLOR_GREEN = (0,1,0)
COLOR_BLUE = (0,0,1)

red_gpio = 2
green_gpio = 3
blue_gpio = 4

led = RGBLED(red_gpio, green_gpio, blue_gpio, active_high=False)


def flicker_led(flicker_color, flicker_interval=FLICKER_INTERVAL, flicker_time=FLICKER_TIME):
    current_flicker_timer = flicker_time
    while current_flicker_timer > 0:
        led.color = flicker_color
        time.sleep(flicker_interval)
        led.off()
        time.sleep(flicker_interval)
        current_flicker_timer -= flicker_interval * 2

