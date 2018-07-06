import sleekxmpp
import logging

from sleekxmpp.xmlstream import ET
from ..client import Client


class XmppClient(Client):
    def __init__(self, jid, password):
        Client.__init__(self)
        self.log = logging.getLogger(__name__)
        self.jid = jid
        self._xmpp = sleekxmpp.ClientXMPP(jid, password)
        self._init_xmpp()

    def connect(self):
        if self._xmpp.connect():
            self._xmpp.process(block=True)
        else:
            raise RuntimeError("XMPP connection {0} failed".format(self.jid))

    def close(self):
        self._xmpp.disconnect()

    def join_muc(self, room, nick, password=None):
        if password is None:
            password = ''
        plugin = self._xmpp.plugin["xep_0045"]
        plugin.joinMUC(room, nick, password=password, wait=True)

    def change_nick(self, room, old_nick, nick):
        plugin = self._xmpp.plugin["xep_0045"]
        pto = "{0}/{1}".format(room, nick)
        pfrom = "{0}/{1}".format(self.jid, old_nick)
        stanza = plugin.xmpp.make_presence(pto=pto, pfrom=pfrom)
        expect = ET.Element("{%s}presence" % plugin.xmpp.default_ns, {'from':"%s/%s" % (room, nick)})
        plugin.xmpp.send(stanza, expect)
        plugin.ourNicks[room] = nick

    def send(self, msg_type, recipient, body, nick=None):
        valid_types = ("chat", "groupchat")
        if msg_type not in valid_types:
            raise ValueError("type must be one of: {0}".format(valid_types))
        self._xmpp.send_message(recipient, body,
                                mtype=msg_type, mnick=nick)

    def _init_xmpp(self):
        xmpp = self._xmpp
        xmpp.register_plugin("xep_0030")  # Disco
        xmpp.register_plugin("xep_0045")  # MUC
        xmpp.register_plugin("xep_0203")  # Delayed Delivery
        xmpp.register_plugin("xep_0280")  # Message Carbons
        xmpp.register_plugin("xep_0199")  # Ping (is it needed?)

        xmpp.add_event_handler("session_start", self._on_start)
        xmpp.add_event_handler("message", self._on_message)

    def _on_start(self, event):
        self._xmpp.send_presence()
        self._xmpp.get_roster()
        self.log.info("[%s] connected!", self.jid)
        self.on_connected.notify()

    def _on_message(self, msg):
        self.on_message_received.notify(msg)
