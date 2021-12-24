import selectors


class Reactor:
    def __init__(self):
        self._selector = selectors.DefaultSelector()

    def register_read(self, sock, callback):
        self._selector.register(sock, selectors.EVENT_READ, callback)

    def unregister(self, fd):
        self._selector.unregister(fd)

    def run(self):
        while True:
            events = self._selector.select()
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)


