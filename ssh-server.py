#!/usr/bin/env python

from twisted.cred.portal import Portal
from twisted.conch.ssh.factory import SSHFactory
from twisted.internet import reactor
from twisted.conch.ssh.keys import Key
from twisted.cred.checkers import FilePasswordDB
from twisted.conch.interfaces import IConchUser
from twisted.conch.avatar import ConchUser
from twisted.conch.ssh.channel import SSHChannel
from twisted.conch.ssh.session import parseRequest_pty_req
from twisted.internet.protocol import Protocol
from twisted.conch.ssh.session import SSHSession, SSHSessionProcessProtocol, wrapProtocol

from twisted.python import log
import sys
log.startLogging(sys.stderr)

with open('id_rsa') as privateBlobFile:
    privateBlob = privateBlobFile.read()
    privateKey  = Key.fromString(data=privateBlob)

with open('id_rsa.pub') as publicBlobFile:
    publicBlob = publicBlobFile.read()
    publicKey  = Key.fromString(data=publicBlob)

class EchoProtocol(Protocol):
    def connectionMade(self):
        self.transport.write("Echo protocol connected\r\n")

    def dataReceived(self, bytes):
        self.transport.write("echo: " + repr(bytes) + "\r\n")

    def connectionLost(self, reason):
        print 'Connection lost', reason

def nothing():
    pass

class SimpleSession(SSHChannel):
    name = 'session'

    def dataReceived(self, bytes):
        self.write("echo: " + repr(bytes) + "\r\n")
        
    def request_shell(self, data):
        protocol  = EchoProtocol()
        transport = SSHSessionProcessProtocol(self)
        protocol.makeConnection(transport)
        transport.makeConnection(wrapProtocol(protocol))
        self.client = transport
        return True

    def request_pty_req(self, data):
         return True

    def eofReceived(self):
        print 'eofReceived'

    def closed(self):
        print 'closed'

    def closeReceived(self):
        print 'closeReceived'

class SimpleRealm(object):
    def requestAvatar(self, avatarId, mind, *interfaces):
        user = ConchUser()
        user.channelLookup['session'] = SimpleSession
        return IConchUser, user, nothing

factory = SSHFactory()
factory.privateKeys = { 'ssh-rsa': privateKey }
factory.publicKeys  = { 'ssh-rsa': publicKey  }

factory.portal = Portal(SimpleRealm())
factory.portal.registerChecker(FilePasswordDB("ssh-passwords"))

reactor.listenTCP(2022, factory)
reactor.run()

