slack2xmpp
==========

WARNING
=======
**If for some reason you choose to use slack2xmpp, bear in mind that it is made purely for personal use, it is not documented nor tested enough for stable usage. It works for me. I will try to improve it whenever I can, but I can not promise you anything.**

Contributions (as well as issues) are welcome :)

What the hell is this?
----------------------
slack2xmpp allows you to bridge Slack's channels, groups and direct messages to XMPP multi-user conference or regular conversation. 

For XMPP MUC it can dynamically change bot's sender nick to match the Slack's message sender username, so that messages appear as sent by different people, even though they are posted from the same XMPP account.

Only Slack and XMPP are supported, although more protocols could be added. (maybe in future?)

How do I configure it?
----------------------
For now there is no configuration file, you need to write a simple wire-up python script. For examples, see **examples** directory.
