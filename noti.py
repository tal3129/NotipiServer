#!/usr/bin/python

import threading
import socket
import struct
import time
from threading import Thread, Lock
import bluetooth
import led_control
import lcd_control
import buzzer_control

uuid="00001101-0000-1000-8000-00805F9B34FB"
size = 1024

MESSAGE_HEADER = "BBH"
HEADER_MESSAGE_SIZE = struct.calcsize(MESSAGE_HEADER)
colors = {
    1: led_control.COLOR_RED,
    2: led_control.COLOR_GREEN,
    3: led_control.COLOR_BLUE,
}


def handle_message(message):
    print("New Message: ", list(message))
    if len(message) < HEADER_MESSAGE_SIZE:
        return

    color_index, is_call, payload_length = struct.unpack(MESSAGE_HEADER, message[:HEADER_MESSAGE_SIZE])
    payload = message[HEADER_MESSAGE_SIZE:].decode("utf-8")
    print(payload)
    lcd_control.clear_screen()
    lcd_control.write(payload)
    
    if is_call:
        Thread(target=buzzer_control.alert).start()
        Thread(target=led_control.flicker_led, args=[colors[color_index], led_control.FLICKER_INTERVAL_SHORT, led_control.FLICKER_TIME_LONG]).start()
    else:
        Thread(target=led_control.flicker_led, args=[colors[color_index]]).start()

def handle_client(client_sock):
    try:
        while True:
            data, addr = client_sock.recvfrom(size)
            if not data:
                print("Client disconnected")
                return
            handle_message(data)
    except bluetooth.BluetoothError as e:
        print(e)
        return


def main():
    Thread(target=led_control.flicker_led, args=[led_control.COLOR_RED]).start()
    port = bluetooth.PORT_ANY
    server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server.bind(("",port))

    server.listen(1)
    bluetooth.advertise_service(server, "SampleServer", service_id = uuid,
                                service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                                profiles = [ bluetooth.SERIAL_PORT_PROFILE ])
    while True:
        print("Listening for client connection...")
        client_sock, address = server.accept()
        Thread(target=led_control.flicker_led, args=[led_control.COLOR_RED], kwargs={"flicker_time": 1}).start()
        print("New client:", address)

        # Handle new client
        threading.Thread(target=handle_client, args=[client_sock]).start()


if __name__ == "__main__":
    main()

