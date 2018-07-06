from ..message import Message
from ..gateway import Gateway

import logging

class XmppGateway(Gateway):
    def __init__(self, client):
        super(XmppGateway, self).__init__(client)
        client.on_message_received.register(self._on_message_received)
        client.on_connected.register(self._on_connected)
        self._log = logging.getLogger(__name__)

    def send_message(self, message):
        raise NotImplementedError("send_message")

    def _on_connected(self):
        pass

    def _on_message_received(self, message_data):
        raise NotImplementedError("_on_message_received")

    def _pass_message(self, sender_nick, body, to):
        self._log.info("Message from %s", sender_nick)
        message = Message()
        message.sender = sender_nick
        message.body = body
        message.to = to
        self.on_message_received.notify(message)
