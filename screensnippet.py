#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import signal
import logging
import subprocess
from PyQt4 import QtGui, QtCore, uic

log = logging.getLogger('byzanz-gui')
APP_DIR = os.path.dirname(os.path.realpath(__file__))

class byzanz_gui(QtGui.QMainWindow):

    def __init__(self):
        super(byzanz_gui, self).__init__()
        uic.loadUi(os.path.join(APP_DIR, 'byzanz_gui.ui'), self)

        self.setWindowTitle("byzanz-gui")
        self.pb_record.clicked.connect(self.on_pbRecord_clicked)

        self._dimensions = None
        self._playback_label = None
        self._countdown = None

        self._sys_icon = QtGui.QSystemTrayIcon()
        # self._sys_icon.setIcon(QtGui.QIcon.fromTheme("document-save"))
        self._sys_icon.setVisible(True)

        self.setAutoFillBackground(False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.Tool)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.on_timer_timeout)

        # self.statusBar().setSizeGripEnabled(True)

    def on_timer_timeout(self):
        self._countdown -= 1
        if self._countdown > 0:
            self._sys_icon.showMessage('get ready!', '%d' % self._countdown)
        else:
            self._timer.stop()
            self._sys_icon.setVisible(False)
            self.setVisible(False)
            _filename = str(self.le_filename.text())
            _cmd = ['byzanz-record', '--cursor', '--delay=%d' % 0, '--verbose',
                    '--duration=%d' % self.sb_duration.value(),
                    '--x=%d' % self._dimensions[0], '--y=%d' % self._dimensions[1],
                    '--width=%d' % self._dimensions[2], '--height=%d' % self._dimensions[3],
                    _filename]

            print("run: ", ' '.join(_cmd))
            _process = subprocess.Popen(_cmd)
            _process.wait()
            self.setVisible(True)
            self.display(_filename)

    def on_pbRecord_clicked(self):
        self._countdown = 6
        self._timer.start()

    def moveEvent(self, _):
        self.update_size_info()

    def resizeEvent(self, _):
        self.update_size_info()

    def update_size_info(self):
        _geom = self.geometry()
        self._dimensions = _geom.x(), _geom.y(), _geom.width(), _geom.height()
        print("update", self._dimensions)
        self.setWindowTitle("%s - byzanz-gui" % (self._dimensions, ))

    def display(self, filename):
        self._playback_label = QtGui.QLabel()
        movie = QtGui.QMovie(filename)
        self._playback_label.setMovie(movie)
        self._playback_label.show()
        movie.start()
        self._playback_label.adjustSize()


def sigint_handler(*_):
    sys.stderr.write('\r')
    QtGui.QApplication.quit()

def main():
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s:  %(message)s",
        datefmt="%y%m%d-%H%M%S",
        level=logging.INFO)
    log.info("%s %s",
             '.'.join((str(e) for e in sys.version_info)),
             sys.executable)

    app = QtGui.QApplication(sys.argv)

    ex = byzanz_gui()
    ex.show()

    for _signal in (signal.SIGABRT, signal.SIGINT, signal.SIGTERM):
        signal.signal(_signal, lambda signr, frame: sigint_handler(signr, ex))

    # catch the interpreter every now and then to be able to catch signals
    timer = QtCore.QTimer()
    timer.start(200)
    timer.timeout.connect(lambda: None)

    log.info('run Qt application')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

