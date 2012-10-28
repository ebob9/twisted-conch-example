#!/usr/bin/env python

from twisted.cred.portal import Portal
from twisted.conch.ssh.factory import SSHFactory
from twisted.internet import reactor
from twisted.conch.ssh.keys import Key
from twisted.cred.checkers import FilePasswordDB
from twisted.conch.interfaces import IConchUser
from twisted.conch.avatar import ConchUser
from twisted.conch.ssh.channel import SSHChannel

from twisted.python import log
import sys
log.startLogging(sys.stderr)

with open('id_rsa') as privateBlobFile:
    privateBlob = privateBlobFile.read()
    privateKey  = Key.fromString(data=privateBlob)

with open('id_rsa.pub') as publicBlobFile:
    publicBlob = publicBlobFile.read()
    publicKey  = Key.fromString(data=publicBlob)

def nothing():
    pass

class SimpleSession(SSHChannel):
    name = 'session'

    def request_shell(self, data):
        self.write("This session is very simple. Good bye!\r\n")
        self.loseConnection()
        return True

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

