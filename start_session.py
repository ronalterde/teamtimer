#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import time

from fs_storage import *
from session import Session
from session import SessionManager
from session import PublisherSessionHandle
import config
import tkgui

class Timer:
    def start(self, end_time):
        while datetime.now() < end_time:
            print('Time left: ' + str((end_time - datetime.now())).split('.')[0] + '\r', sep=' ', end='', flush=True)
            time.sleep(1)

class TimeProvider:
    def get_current_time(self):
        return datetime.now()

if __name__ == "__main__":
    conf = config.load()
    base_dir = conf['base_dir']
    me = conf['me']
    time_box = timedelta(seconds=int(conf['time_box_seconds']))

    fs_session_storage = FileSystemSessionStorage(base_dir)
    session_manager = SessionManager(fs_session_storage, TimeProvider())

    print('Starting session for user %s ...' % me)
    publisher_handle = session_manager.create_session(me, time_box)

    timer = Timer()
    print('Starting timer (%s). End time: %s' % (time_box, publisher_handle.get_end_time()))
    timer.start(publisher_handle.get_end_time())
    print('Session done.')

    sessions = fs_session_storage.list_sessions()
    my_sessions = [x for x in sessions if x['owner'] == me]

    requests = []
    if 'requests' in my_sessions[0]:
        requests = my_sessions[0]['requests']
        print('Requests available: %s' % str(requests))
    else:
        print('No requests filed.')

    print('Removing session...')
    publisher_handle.stop()

    tkgui.show_message('Session done.', 'Requests: %s' % str(requests))
