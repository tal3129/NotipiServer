import time
import random
import RPi.GPIO as gpio
from threading import Lock

BUZZER_GPIO = 14

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(BUZZER_GPIO, gpio.OUT)
buzz = gpio.PWM(BUZZER_GPIO, 1000)

DUTY_CYCLE = 20
FREQ_START = 200
FREQ_END = 2500
FREQ_STEP = 50
FREQ_PLAY_TIME = 0.05
ALERT_CYCLES = 2

RANDOM_PLAY_TIME = 1

buzzer_mutex = Lock()

def rising_buzz():
    for i in range(FREQ_START, FREQ_END, FREQ_STEP):
        buzz.ChangeFrequency(i)
        buzz.start(DUTY_CYCLE)
        time.sleep(FREQ_PLAY_TIME)
        buzz.stop()


def falling_buzz():
    for i in range(FREQ_END, FREQ_START, -FREQ_STEP):
        buzz.ChangeFrequency(i)
        buzz.start(DUTY_CYCLE)
        time.sleep(FREQ_PLAY_TIME)
        buzz.stop()


def random_buzz():
    for i in range(int(RANDOM_PLAY_TIME / FREQ_PLAY_TIME)):
        buzz.ChangeFrequency(random.randint(FREQ_START, FREQ_END))
        buzz.start(DUTY_CYCLE)
        time.sleep(FREQ_PLAY_TIME)
        buzz.stop()


def alert():
    buzzer_mutex.acquire()
    print("Alerting...")
    for i in range(ALERT_CYCLES):
        rising_buzz()
        falling_buzz()

    buzzer_mutex.release()

