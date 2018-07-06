class Message(object):
    def __init__(self, sender=None, to=None, body=None):
        self.sender = sender
        self.to = to
        self.body = body
