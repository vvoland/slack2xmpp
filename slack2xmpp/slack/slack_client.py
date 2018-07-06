import slackclient
import time
import logging

from ..client import Client


class SlackClient(Client):
    def __init__(self, token):
        super(SlackClient, self).__init__()
        self._log = logging.getLogger(__name__)
        self.users = dict()
        self.conversations = dict()
        self.sleep_time = 0.33
        self._notify_on_hello = True
        self._run = True
        self._token = token
        self._slack = slackclient.SlackClient(self._token)

    def connect(self):
        slack = self._slack
        self._run = True
        self._log.info("Connecting to Slack...")
        while self._run:
            if slack.rtm_connect(auto_reconnect=True):
                self._connection_loop()
            else:
                raise RuntimeError("Failed to connect to slack")

    def _connection_loop(self):
        while self._run:
            try:
                events = self._slack.rtm_read()
            except ConnectionResetError:
                # https://github.com/slackapi/python-slackclient/issues/101
                self._log.info("Connection reset. Reconnecting...")
                return
            for event in events:
                self._on_event(event)
            time.sleep(self.sleep_time)

    def send_message(self, channel, body):
        self._slack.rtm_send_message(channel, body)

    def close(self):
        self._log.info("Closing...")
        self._run = False
        time.sleep(1)

    def fetch_users(self):
        response = self._slack.api_call("users.list")
        if not response["ok"]:
            self._log.error("fetch_users failed, %s",
                            response["error"])
            return

        self.users = dict()
        for user in response["members"]:
            id = user["id"]
            name = user["name"]
            self.users[id] = {
                "id": id,
                "name": name
            }

    def fetch_conversations(self):
        response = self._slack.api_call(
            "conversations.list",
            types="public_channel,private_channel,im")

        if not response["ok"]:
            self._log.error("fetch_conversations failed, %s",
                            response["error"])
            return

        self.conversations = dict()
        for conv in response["channels"]:
            c_type = None
            c_name = None
            c_id = conv["id"]

            if self._exists_and_true(conv, "is_im"):
                c_type = "im"
                c_name = self._get_im_name(conv)
            elif self._exists_and_true(conv, "is_group"):
                c_type = "group"
                c_name = conv["name"]
            elif self._exists_and_true(conv, "is_channel"):
                c_type = "channel"
                c_name = conv["name"]

            self._log.debug("Slack %s %s %s", c_type, c_id, c_name)
            if c_type is not None:
                self.conversations[c_id] = {
                    "id": c_id,
                    "name": c_name,
                    "type": c_type
                }

    def _get_im_name(self, conversation):
        user_id = conversation["user"]
        name = user_id
        retry = True
        while True:
            try:
                user = self.users[user_id]
                name = user["name"]
            except KeyError:
                if retry:
                    self.fetch_users()
                    retry = False
                    continue
                self._log.error("Failed to get %s user name",
                                user_id)
            break
        return name

    def _exists_and_true(self, dictionary, key):
        try:
            return dictionary[key]
        except KeyError:
            return False

    def _on_connected(self):
        self._log.info("Connected to Slack!")
        self.fetch_users()
        self.fetch_conversations()
        self.on_connected.notify()

    def _on_event(self, event):
        try:
            event_type = event["type"]
        except KeyError:
            return

        if event_type == "hello":
            if self._notify_on_hello:
                self._notify_on_hello = False
                self._on_connected()
            return
        elif event_type == "message":
            try:
                conversation_id = event["channel"]
                sender_user_id = event["user"]
            except KeyError:
                self._log.error("Could not process message event %s",
                                event)
                return

            if sender_user_id not in self.users:
                self._log.info("Sender not in users, fetching")
                self.fetch_users()
            if conversation_id not in self.conversations:
                self._log.info("Conversation not known, fetching")
                self.fetch_users()
                self.fetch_conversations()
            self.on_message_received.notify(event)
