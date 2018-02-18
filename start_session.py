#!/usr/bin/env python3

from datetime import timedelta

import config
import fs_storage
import session
import time_utils
import notify

def read_from_config():
    conf = config.load()
    return conf['base_dir'], conf['me'], timedelta(seconds=int(conf['time_box_seconds']))

if __name__ == "__main__":
    base_dir, me, time_box = read_from_config()

    fs_session_storage = fs_storage.FileSystemSessionStorage(base_dir)
    session_manager = session.SessionManager(fs_session_storage, time_utils.TimeProvider())

    print('Starting session for user %s ...' % me)
    publisher_handle = session_manager.create_session(me, time_box)

    timer = time_utils.Timer()
    print('Starting timer (%s). End time: %s' % (time_box, publisher_handle.get_end_time()))
    timer.start(publisher_handle.get_end_time())
    print('Session done.')

    requests = publisher_handle.get_requests()
    if len(requests):
        print('Requests available: %s' % str(requests))
        notify.show_message('Teamtimer session done.', 'Requests: %s' % str(requests))
    else:
        print('No requests filed.')
        notify.show_message('Teamtimer session done.', 'No requests filed.')

    print('Finishing session...')
    publisher_handle.stop()
