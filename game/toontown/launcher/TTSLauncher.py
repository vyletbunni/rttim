from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
import os
import sys
import time

class LogAndOutput:
    def __init__(self, orig, log):
        self.orig = orig
        self.log = log

    def write(self, str):
        self.log.write(str)
        self.log.flush()
        self.orig.write(str)
        self.orig.flush()

    def flush(self):
        self.log.flush()
        self.orig.flush()

class TTSLauncher:
    notify = DirectNotifyGlobal.directNotify.newCategory('TTSLauncher')

    def __init__(self):
        self.http = HTTPClient()

        self.logPrefix = 'stride-'

        ltime = 1 and time.localtime()
        logSuffix = '%02d%02d%02d_%02d%02d%02d' % (ltime[0] - 2000,  ltime[1], ltime[2], ltime[3], ltime[4], ltime[5])

        if not os.path.exists('user/logs/'):
            os.mkdir('user/logs/')
            self.notify.info('Made new directory to save logs.')

        logfile = os.path.join('user/logs', self.logPrefix + logSuffix + '.log')

        log = open(logfile, 'a')
        logOut = LogAndOutput(sys.stdout, log)
        logErr = LogAndOutput(sys.stderr, log)
        sys.stdout = logOut
        sys.stderr = logErr

    def getPlayToken(self):
        return self.getValue('TTS_PLAYCOOKIE')

    def getGameServer(self):
        return self.getValue('TTS_GAMESERVER')

    def getValue(self, key, default = None):
        return os.environ.get(key, default)

    def setPandaErrorCode(self):
        pass

    def setDisconnectDetails(self, disconnectCode, disconnectMsg):
        self.disconnectCode = disconnectCode
        self.disconnectMsg = disconnectMsg

    def setDisconnectDetailsNormal(self):
        self.setDisconnectDetails(0, 'normal')
