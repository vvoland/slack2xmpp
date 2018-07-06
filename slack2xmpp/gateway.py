from .observable import Observable


class Gateway(object):
    def __init__(self, client):
        self._client = client
        self.on_message_received = Observable()

    def send_message(self, message):
        raise NotImplementedError("send_message")
