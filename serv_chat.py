#!/usr/bin/env python3

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor

MAX_USERS = 100
MAX_MSG_LENGTH = 255
MAX_USER_LENGTH = 16
PORT = 8000

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        
        with open('forbidden.txt') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
        
        self.forbidden = lines
        self.timer = None

    def connectionMade(self):
        if len(self.factory.users) == MAX_USERS:
            self.sendLine("-1".encode())
            self.transport.loseConnection()
        else:
            self.sendLine("FTR0 1 1 0".encode())
            users = "USR"
            for key in self.factory.users.keys():
                users += self.factory.users[key].name + " "
            self.sendLine(users.encode())

    def connectionLost(self, reason):
        if self.name != None:
            del self.factory.users[self.name]
            
            message = "OUT" + self.name
            for user in self.factory.users.values():
                    user.sendLine(message.encode())
    
    def lineReceived(self, line):
        line = line.decode()
        if line.startswith("NME") and not self.name:
            name = line[3:]
            if " " in name:
                self.sendLine("-2".encode())
                self.transport.loseConnection()
            elif len(name) > MAX_USER_LENGTH:
                self.sendLine("-3".encode())
            elif name in self.factory.users.keys():
                self.sendLine("-4".encode())
            else:
                self.timer = reactor.callLater(10,self.notMessage)
                self.name = name
                self.factory.users[self.name] = self
                message = "INN" + self.name
                for user in self.factory.users.values():
                    if user != self:
                        user.sendLine(message.encode())
                
        
        elif line.startswith("MSG") and self.name:
            message = line[3:]
            if len(message) > MAX_MSG_LENGTH:
                self.sendLine("-5".encode)
            else:
                for word in self.forbidden:
                    message = message.replace(word, "#" * len(word))
                message = "MSG{} {}".format(self.name,message)
                for user in self.factory.users.values():
                    if user != self:
                        user.sendLine(message.encode())
                self.sendLine("+".encode())
        elif line.startswith("WRT"):
            message = line + self.name
            for user in self.factory.users.values():
                if user != self:
                    user.sendLine(message.encode())
        else:
            self.sendLine("-0".encode())
            
    def notMessage(self):
        self.sendLine(b'NOP')
        self.timer = reactor.callLater(10, self.notMessage)

class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)

if __name__ == "__main__":
	reactor.listenTCP(PORT, ChatFactory())
	reactor.run()
