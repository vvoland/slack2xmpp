class Bridge(object):
    def __init__(self):
        self.gateways = []

    def connect_gateway(self, gateway):
        for other in self.gateways:
            self._connect(other, gateway)
        self.gateways.append(gateway)

    def _connect(self, gateway1, gateway2):
        gateway1.on_message_received.register(gateway2.send_message)
        gateway2.on_message_received.register(gateway1.send_message)
