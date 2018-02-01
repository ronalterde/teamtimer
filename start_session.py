#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import time

from fs_dir import *
import config
import tkgui

class Timer:
    def start(self, end_time):
        while datetime.now() < end_time:
            print('Time left: ' + str((end_time - datetime.now())).split('.')[0] + '\r', sep=' ', end='', flush=True)
            time.sleep(1)

if __name__ == "__main__":
    conf = config.load()
    base_dir = conf['base_dir']
    me = conf['me']
    time_box = timedelta(seconds=int(conf['time_box_seconds']))

    print('Starting session for user %s ...' % me)
    fs_session_directory = FsSessionDirectory(base_dir)
    end_time = datetime.now() + time_box
    fs_session_directory.add_session({'owner' : me, 'end_time' : end_time})

    timer = Timer()
    print('Starting timer (%s). End time: %s' % (time_box, end_time))
    timer.start(end_time)
    print('Session done.')

    sessions = fs_session_directory.list_sessions()
    my_sessions = [x for x in sessions if x['owner'] == me]

    requests = []
    if 'requests' in my_sessions[0]:
        requests = my_sessions[0]['requests']
        print('Requests available: %s' % str(requests))
    else:
        print('No requests filed.')

    print('Removing session...')
    fs_session_directory.remove_sessions_owned_by(me)

    tkgui.show_message('Session done.', 'Requests: %s' % str(requests))
