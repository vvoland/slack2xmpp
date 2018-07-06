from .xmpp_gateway import XmppGateway


class XmppMuc(XmppGateway):
    def __init__(self, client, muc_room, muc_nick, muc_password=None):
        super(XmppMuc, self).__init__(client)
        self.dynamic_nick = True
        self._room = muc_room
        self._nick = muc_nick
        self._password = muc_password

    def send_message(self, message):
        nick = self._nick
        body = message.body
        if self.dynamic_nick:
            nick = message.sender
            self._log.debug("Sending to %s message %s as %s",
                            self._room, message.body, nick)
            if nick != self._nick:
                self._join_as(nick)
        else:
            body = "<{0}> {1}".format(nick, body)
        self._client.send("groupchat", self._room, body, nick)

    def _on_connected(self):
        self._client.join_muc(self._room, self._nick, self._password)

    def _join_as(self, nick):
        self._client.change_nick(self._room, self._nick, nick)
        self._nick = nick

    def _on_message_received(self, message_data):
        from_ = message_data["from"]
        body = message_data["body"]
        room = from_.bare
        sender_nick = from_.resource

        # Only the room we are observing
        if room != self._room:
            return
        # Only for other user than this bot
        if sender_nick == self._nick:
            return
        self._pass_message(sender_nick, body, room)
