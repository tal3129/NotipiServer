import time
from string import printable
import serial
from threading import Lock

LCD_MAX_LEN = 32

lcd_connection = serial.Serial(
        port='/dev/serial0', 
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
)


def clear_screen():
    lcd_connection.write(b"\xFE\x01")

def write(message: str):
    message = ''.join(filter(lambda x: x in printable, message))
    message = ' '.join(message.split())
    if len(message) > LCD_MAX_LEN:
        message = message[:LCD_MAX_LEN - 3] + "..."
    lcd_connection.write(message.encode("utf-8"))


