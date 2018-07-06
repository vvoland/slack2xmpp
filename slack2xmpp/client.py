from .observable import Observable


class Client(object):
    def __init__(self):
        self.on_message_received = Observable()
        self.on_connected = Observable()

    def connect(self):
        raise NotImplementedError("Client.connect not implemented")

    def close(self):
        raise NotImplementedError("Client.close not implemented")
