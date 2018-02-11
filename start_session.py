#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import time

from fs_storage import *
from session import Session
from session import SessionManager
from session import PublisherSessionHandle
import time_utils
import config
import tkgui

def read_from_config():
    conf = config.load()
    return conf['base_dir'], conf['me'], timedelta(seconds=int(conf['time_box_seconds']))

if __name__ == "__main__":
    base_dir, me, time_box = read_from_config()

    fs_session_storage = FileSystemSessionStorage(base_dir)
    session_manager = SessionManager(fs_session_storage, time_utils.TimeProvider())

    print('Starting session for user %s ...' % me)
    publisher_handle = session_manager.create_session(me, time_box)

    timer = time_utils.Timer()
    print('Starting timer (%s). End time: %s' % (time_box, publisher_handle.get_end_time()))
    timer.start(publisher_handle.get_end_time())
    print('Session done.')

    requests = publisher_handle.get_requests()
    if len(requests):
        print('Requests available: %s' % str(requests))
        tkgui.show_message('Session done.', 'Requests: %s' % str(requests))
    else:
        print('No requests filed.')
        tkgui.show_message('Session done.', 'No requests filed.')

    print('Finishing session...')
    publisher_handle.stop()
