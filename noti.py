#!/usr/bin/python

import socket
import struct
import time
import threading
import bluetooth
import led_control
import buzzer_control

uuid="00001101-0000-1000-8000-00805F9B34FB"
size = 1024

HEADER_MESSAGE = "BB"
HEADER_MESSAGE_SIZE = struct.calcsize(HEADER_MESSAGE)
colors = {
    1: led_control.COLOR_RED,
    2: led_control.COLOR_GREEN,
    3: led_control.COLOR_BLUE,
}


def handle_message(message):
    print("New Message: ", list(message))
    if len(message) != HEADER_MESSAGE_SIZE:
        return

    color_index, call_flicker = struct.unpack(HEADER_MESSAGE, message)
    if call_flicker:
        alert_thread = threading.Thread(target=buzzer_control.alert)
        alert_thread.start()
        led_control.flicker_led(colors[color_index], led_control.FLICKER_INTERVAL_SHORT, led_control.FLICKER_TIME_LONG)
    else:
        led_control.flicker_led(colors[color_index])


def main():
    led_control.flicker_led(led_control.COLOR_BLUE)
    
    port = bluetooth.PORT_ANY
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.bind(("",port))

    s.listen(1)
    bluetooth.advertise_service(s, "SampleServer", service_id = uuid,
                                service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                                profiles = [ bluetooth.SERIAL_PORT_PROFILE ]) 
    while True:
        print("Listening for client connection...")
        client_sock, address = s.accept()
        print("new client:", address)

        # Handle new client
        try:
            data, addr = client_sock.recvfrom(size)
            while data:
                handle_message(data.decode("UTF-8"))
                data, addr = client_sock.recvfrom(size)
        except bluetooth.BluetoothError as e:
            print(e)
            continue


if __name__ == "__main__":
    main()

