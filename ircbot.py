#! /usr/bin/env python
#
# Example program using irc.bot.
#
# Joel Rosdahl <joel@rosdahl.net>

"""A simple example bot.

This is an example bot that uses the SingleServerIRCBot class from
irc.bot.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.
It also responds to DCC CHAT invitations and echos data sent in such
sessions.

The known commands are:

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.

    dcc -- Let the bot invite you to a DCC CHAT connection.
"""


# coding=utf-8
import logging
import sys
import os

#logging init
logger = logging.getLogger("irclog")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)-15s %(message)s')
formatter_short = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s', "%M:%S")
# filehandler

dirPath = os.path.join("var", 'log')
if not os.path.exists(dirPath):
    logger.info("creating log directory")
    try:
        os.makedirs(dirPath)
    except:
        pass

name = "log"#+datetime.now().strftime("%Y_%m_%d")
hdlr = logging.FileHandler(os.path.join(dirPath, name))

hdlr.setFormatter(formatter)
hdlr.setLevel(logging.CRITICAL)
logger.addHandler(hdlr)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter_short)
logger.addHandler(ch)

def log_uncaught_exceptions(*exc_info): 
    logging.critical('Unhandled exception:', exc_info=exc_info) 
sys.excepthook = log_uncaught_exceptions













import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad
#, ip_quad_to_numstr
import irc_handler
from irc.buffer import LineBuffer

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.connection.buffer_class = LineBuffer
        # I couldn't find any place where the flood limit is specified - I've read 3/5 (3 messages in 5 seconds)
        self.connection.set_rate_limit(1)

    def on_nicknameinuse(self, c, e):
        print "nickname in use"
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        print "welcome"
        c.join(self.channel)

    def on_privmsg(self, c, e):
        print "privmsg"
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        print "pubmsg"
        self.do_command(e, e.arguments[0])

    def on_dccmsg(self, c, e):
        print "dccmsg"
        c.privmsg("You said: " + e.arguments[0])

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        nick = e.source.nick
        if e.type == "privmsg":
            # normally this sould be logged in another file
            pass
        elif e.type == "pubmsg":
            logger.critical("[ %s ]: %s" % (nick, cmd))

        reload(irc_handler)
        irc_handler.handle_command(self.connection, e, cmd)

        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die()
        #elif cmd == "stats":
        #    for chname, chobj in self.channels.items():
        #        c.notice(nick, "--- Channel statistics ---")
        #        c.notice(nick, "Channel: " + chname)
        #        users = chobj.users()
        #        users.sort()
        #        c.notice(nick, "Users: " + ", ".join(users))
        #        opers = chobj.opers()
        #        opers.sort()
        #        c.notice(nick, "Opers: " + ", ".join(opers))
        #        voiced = chobj.voiced()
        #        voiced.sort()
        #        c.notice(nick, "Voiced: " + ", ".join(voiced))
        #elif cmd == "dcc":
        #    dcc = self.dcc_listen()
        #    c.ctcp("DCC", nick, "CHAT chat %s %d" % (
        #        ip_quad_to_numstr(dcc.localaddress),
        #        dcc.localport))
        #else:
        #    c.notice(nick, "Not understood: " + cmd)

def main():
    import sys
    print sys.argv
    if len(sys.argv) != 4:
        print "Usage: testbot <server[:port]> <channel> <nickname>"
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print "Error: Erroneous port."
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = TestBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
