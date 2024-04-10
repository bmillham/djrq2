#!/usr/bin/python

try:
    import irc.client as client
except:
    print('Unable to import irc.clients/irc.events')
    client = None
    events = None
from time import sleep
import sys

class IRC(object):
    def __init__(self, server=None, port=6667, channel=None, nick=None, no_irc=False):
        self.server = server
        self.port = int(port)
        self.channel = channel
        self.nick = nick
        self.no_irc = no_irc
        self._joined = False
        self.client = None
        self.reactor = None
        if client is None:
            self.no_irc = True

    def on_connect(self, connection, event):
        for a in event.arguments:
            print(f"IRC: {a}")
        if client.is_channel(self.channel):
            connection.join(self.channel)
        print('IRC: Joined IRC without a target')

    def on_join(self, connection, event):
        print(f'IRC: Joined {event.target}')
        self._joined = True

    def connect(self):
        if self.no_irc:
            print('Will not update IRC')
            return

        print(f'Connecting to IRC server: {self.nick}@{self.server}/{self.port}')
        self.reactor = client.Reactor()
        try:
            self.client = self.reactor.server().connect(self.server, self.port, self.nick)
        except client.ServerConnectionError:
            print(sys.exc_info()[1])
            return

        print(f'Connected: Joining {self.channel}')
        self.client.add_global_handler("welcome", self.on_connect)
        self.client.add_global_handler("join", self.on_join)
        print(f'Waiting to join {self.channel}')
        while not self._joined:
            self.reactor.process_once()
            sleep(.1)
        print(f'Joined {self.channel}')
        self.send(message="is on the job!", send_now=True, action=True)

    def send(self, message=None, bold=False, send_now=False, action=False):
        if type(message) == list:
            print(" ".join(message))
            if bold:
                message[0] = f"\x02{message[0]}\x0F"
            message = " ".join(message)
        elif message is not None:
            print(message)
            if bold and message is not None:
                message = f"\x02{message}\x0F"
        if self.no_irc:
            return
        if self.client is not None and message is not None:
            if action:
                self.client.action(self.channel, message)
            else:
                self.client.privmsg(self.channel, message)
        if send_now and self.reactor is not None:
            self.reactor.process_once()
