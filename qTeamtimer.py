#!/usr/bin/env python3

import sys
import os.path
from datetime import datetime
from datetime import timedelta
import time

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QStringListModel, QUrl, QTimer, QObject, pyqtSlot

from fs_storage import *
import config
import session
import time_utils

def get_owners_from_session_list(sessions):
    owners = [session['owner'] for session in sessions]
    if len(owners) == 0:
        owners = ['none']
    return owners

def create_session_list_model(sessions):
    return QStringListModel(get_owners_from_session_list(sessions))

class SessionController(QObject):
    def __init__(self, session_storage, me, time_box):
        super(SessionController, self).__init__()
        self.session_manager = session.SessionManager(session_storage, time_utils.TimeProvider())
        self.me = me
        self.time_box = time_box

    @pyqtSlot()
    def start_session(self):
        def end():
            self.publisher_handle.stop()
            self.publisher_handle = None
        self.timer = QTimer.singleShot(self.time_box.total_seconds() * 1000, end)
        self.publisher_handle = self.session_manager.create_session(me, self.time_box)

    @pyqtSlot()
    def stop_session(self):
        self.publisher_handle.stop()
        self.publisher_handle = None
        # requests = publisher_handle.get_requests()

    @pyqtSlot(result=str)
    def get_remaining_time(self):
        if self.publisher_handle != None:
            return 'Time left: ' + str((self.publisher_handle.get_end_time() - datetime.now())).split('.')[0]
        else:
            return ''

def read_from_config():
    conf = config.load()
    return conf['base_dir'], conf['me'], timedelta(seconds=int(conf['time_box_seconds']))

if __name__ == "__main__":
    base_dir, me, time_box = read_from_config()
    fs_session_storage = FileSystemSessionStorage(base_dir)
    sessions = fs_session_storage.list_sessions()

    app = QGuiApplication(sys.argv)
    view = QQuickView()
    session_list_model = QStringListModel(get_owners_from_session_list(sessions))
    view.rootContext().setContextProperty('session_list_model', session_list_model)
    session_controller = SessionController(fs_session_storage, me, time_box)
    view.rootContext().setContextProperty('session_controller', session_controller)
    view.setSource(QUrl('main.qml'))
    view.show()

    def update_session_list():
        session_list_model.setStringList(get_owners_from_session_list(fs_session_storage.list_sessions()))

    timer = QTimer()
    timer.timeout.connect(update_session_list)
    timer.start(1000)

    sys.exit(app.exec_())
