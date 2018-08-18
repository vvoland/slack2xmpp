import logging

from ..gateway import Gateway
from ..message import Message

class SlackConversation(Gateway):
    def __init__(self, client, conversation_id):
        super(SlackConversation, self).__init__(client)
        self.conversation_id = conversation_id
        client.on_connected.register(self._on_connected)
        self._log = logging.getLogger(__name__)

    def send_message(self, message):
        slack = self._client
        conversation_id = self.conversation_id
        try:
            conversation_name = slack.conversations[conversation_id]["name"]
        except KeyError:
            self._log.error("Unknown conversation name %s",
                            conversation_name)
            return
        body = message.body
        slack.send_message(conversation_id, body)

    def _on_connected(self):
        conversations = self._client.conversations
        if self.conversation_id not in conversations:
            raise RuntimeError("Unknown conversation id {0}".format(
                            self.conversation_id))
        on_message = self._client.on_message_received
        on_message.register(self._on_message)
        name = conversations[self.conversation_id]["name"]
        self._log.info("Processing conversation %s id %s",
                       name, self.conversation_id)

    def _on_message(self, event):
        slack = self._client
        conversation_id = event["channel"]
        try:
            conversation = slack.conversations[conversation_id]
            conversation_name = conversation["name"]
        except KeyError:
            self._log.error("No conversation with id %s",
                            conversation_id)
            return

        if self.conversation_id != conversation_id:
            self._log.debug("Omitting message to conversation %s",
                           conversation_name)
            return

        user_id = event["user"]

        if user_id == slack.me:
            self._log.debug("Message from myself, dont care")
            return
        try:
            user = slack.users[user_id]
        except KeyError:
            self._log.error("No user with id %s",
                            user_id)

        message = Message()
        message.body = event["text"]
        message.sender = user["name"]
        message.to = conversation_name

        self.on_message_received.notify(message)
