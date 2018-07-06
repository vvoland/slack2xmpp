#!/usr/bin/env python3
"""
Bridge slack channel with ID G1234ASDF with XMPP MUC
room@muc.xmppserver.example. Any message posted to
either of them will be reflected on the other.
"""
import os

from slack2xmpp import main_loop, Bridge
from slack2xmpp.xmpp import XmppClient, XmppMuc
from slack2xmpp.slack import SlackClient, SlackConversation


def main():
    slack_token = os.environ["SLACK2XMPP_SLACK_TOKEN"]
    xmpp_muc_user = os.environ["SLACK2XMPP_XMPP_MUC_USER"]
    xmpp_muc_pass = os.environ["SLACK2XMPP_XMPP_MUC_PASSWORD"]

    xmpp_client = XmppClient(xmpp_muc_user, xmpp_muc_pass)
    slack_client = SlackClient(slack_token)

    xmpp_my_muc = XmppMuc(xmpp_client, "room@muc.xmppserver.example", "bot_nick")
    # By default, before sending message, bot changes
    # its nick to the nick of the message sender.
    # To turn this off and have every message prefixed
    # with <sender_nick> uncomment line below.
    # xmpp_my_muc.dynamic_nick = False

    slack_my_channel = SlackConversation(slack_client, "G1234ASDF")
    # You can obtain conversation ID from URL
    # https://workspace.slack.com/messages/G1234ASDF/
    # You can also use channel or private message ID

    bridge = Bridge()
    bridge.connect_gateway(slack_my_channel)
    bridge.connect_gateway(xmpp_my_muc)

    main_loop([slack_client, xmpp_client])


if __name__ == "__main__":
    main()
