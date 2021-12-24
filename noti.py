#!/usr/bin/python
from reactor import Reactor
import struct
from threading import Thread
import bluetooth
import led_control
import lcd_control
import buzzer_control

uuid="00001101-0000-1000-8000-00805F9B34FB"
MESSAGE_BUFFER_SIZE = 1024

MESSAGE_HEADER = "BBH"
HEADER_MESSAGE_SIZE = struct.calcsize(MESSAGE_HEADER)
colors = {
    1: led_control.COLOR_RED,
    2: led_control.COLOR_GREEN,
    3: led_control.COLOR_BLUE,
}


class NotipiServer():
    def __init__(self):
        self.reactor = Reactor()
        Thread(target=led_control.flicker_led, args=[led_control.COLOR_RED]).start()

    def run(self):
        port = bluetooth.PORT_ANY
        server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server.bind(("",port))
        server.listen(1)
        bluetooth.advertise_service(server, "SampleServer", service_id = uuid,
                                    service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                                    profiles = [ bluetooth.SERIAL_PORT_PROFILE ])
        self.reactor.register_read(server, self.server_handler)

    def server_handler(self, server):
        client_sock, address = server.accept()
        Thread(target=led_control.flicker_led, args=[led_control.COLOR_RED], kwargs={"flicker_time": 1}).start()
        print("New client:", address)
        self.reactor.register_read(client_sock, self.client_handler)

    def client_handler(self, client_sock):
        try:
            data, _ = client_sock.recvfrom(MESSAGE_BUFFER_SIZE)
            if data:
                self.handle_message(data)
                return
        except bluetooth.BluetoothError as e:
            print(e)
        # On error or empty buffer
        print(f"Client disconnected")
        self.reactor.unregister(client_sock)

    def handle_message(self, message):
        print(f"New Message: {list(message[:HEADER_MESSAGE_SIZE])}...")
        if len(message) < HEADER_MESSAGE_SIZE:
            return

        color_index, is_call, payload_length = struct.unpack(MESSAGE_HEADER, message[:HEADER_MESSAGE_SIZE])
        payload = message[HEADER_MESSAGE_SIZE:HEADER_MESSAGE_SIZE + payload_length].decode("utf-8")
        print(payload)

        # Write to LCD
        lcd_control.clear_screen()
        lcd_control.write(payload)

        # Flicker led and start buzzer on call
        if is_call:
            Thread(target=buzzer_control.alert).start()
            Thread(target=led_control.flicker_led, args=[colors[color_index], led_control.FLICKER_INTERVAL_SHORT, led_control.FLICKER_TIME_LONG]).start()
        else:
            Thread(target=led_control.flicker_led, args=[colors[color_index]]).start()


if __name__ == "__main__":
    NotipiServer().run()

