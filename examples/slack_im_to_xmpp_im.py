#!/usr/bin/env python3
"""
Bridge slack direct message conversation with ID D12345678
with XMPP conversation with user me@xmppserver.example.
Any message sent by the other side of the slack conversation
will be sent to xmpp user me@xmppserver.example from xmpp
account provided via environment variable.
"""
import os

from slack2xmpp import main_loop, Bridge
from slack2xmpp.xmpp import XmppClient, XmppMuc
from slack2xmpp.slack import SlackClient, SlackConversation


def main():
    slack_token = os.environ["SLACK2XMPP_SLACK_TOKEN"]
    xmpp_user = os.environ["SLACK2XMPP_XMPP_USER"]
    xmpp_pass = os.environ["SLACK2XMPP_XMPP_PASSWORD"]

    xmpp_client = XmppClient(xmpp_user, xmpp_pass)
    slack_client = SlackClient(slack_token)

    xmpp_me = XmppIm(xmpp_client, "me@xmppserver.example")
    slack_direct_message = SlackConversation(slack_client, "D12345678")
    # You can obtain conversation ID from URL
    # https://workspace.slack.com/messages/G1234ASDF/
    # You can also use channel or private message ID

    bridge = Bridge()
    bridge.connect_gateway(slack_direct_message)
    bridge.connect_gateway(xmpp_me)

    main_loop([slack_client, xmpp_client])


if __name__ == "__main__":
    main()
