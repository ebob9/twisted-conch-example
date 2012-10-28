#!/usr/bin/env python

from twisted.cred.portal import Portal
from twisted.conch.ssh.factory import SSHFactory
from twisted.internet import reactor
from twisted.conch.ssh.keys import Key

with open('id_rsa') as privateBlobFile:
    privateBlob = privateBlobFile.read()
    privateKey  = Key.fromString(data=privateBlob)

with open('id_rsa.pub') as publicBlobFile:
    publicBlob = publicBlobFile.read()
    publicKey  = Key.fromString(data=publicBlob)

factory = SSHFactory()
factory.privateKeys = { 'ssh-rsa': privateKey }
factory.publicKeys  = { 'ssh-rsa': publicKey  }
factory.portal = Portal(None)

reactor.listenTCP(2022, factory)
reactor.run()
