#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import sys
import time

import fs_storage
import config
import session
import time_utils

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('usage: %s <target user>' % sys.argv[0])
        exit(1)

    target_user = sys.argv[1]
    conf = config.load()
    base_dir = conf['base_dir']
    me = conf['me']

    fs_session_storage = fs_storage.FileSystemSessionStorage(base_dir)
    session_manager = session.SessionManager(fs_session_storage, time_utils.TimeProvider())

    handlers = session_manager.get_running_sessions()
    matching_handles = [handle for handle in handlers if handle.owner == target_user]
    if len(matching_handles) > 1:
        print('Error: more than one handle for user %s found!' % target_user)
        exit(1)
    if len(matching_handles) == 1:
        print('Session for user %s running.' % (target_user))
        print('Session for user %s running. Scheduled end time: %s' % (target_user, matching_handles[0].get_end_time()))
        print('Filing request...')
        matching_handles[0].make_request(me)
    else:
        print('No session for user %s running.' % target_user)

