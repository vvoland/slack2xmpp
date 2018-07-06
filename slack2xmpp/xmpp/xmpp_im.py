from .xmpp_gateway import XmppGateway

class XmppIm(XmppGateway):
    def __init__(self, client, jid):
        super(XmppIm, self).__init__(client)
        self.jid = jid

    def send_message(self, message):
        to = self.jid
        body = message.body
        self._client.send("chat", to, body)

    def _on_message_received(self, message_data):
        from_ = message_data["from"]
        body = message_data["body"]
        sender_jid = from_.bare
        sender_name = from_.user
        to_name = self._client.jid
        try:
            index = to_name.index("@")
            to_name = to_name[:index]
        except ValueError:
            pass

        # Do not pass our own messages
        if sender_jid == self.jid:
            self._pass_message(sender_name, body, to_name)
