#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import sys
import time

from fs_dir import *
import config

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('usage: %s <target user>' % sys.argv[0])
        exit(1)

    target_user = sys.argv[1]
    conf = config.load()
    base_dir = conf['base_dir']
    me = conf['me']

    fs_session_directory = FsSessionDirectory(base_dir)
    sessions = fs_session_directory.list_sessions()
    matching_sessions = [x for x in sessions if x['owner'] == target_user]

    if len(matching_sessions) == 1:
        print('Session for user %s running. Scheduled end time: %s' % (target_user, matching_sessions[0]['end_time']))
        print('Filing request...')
        modified_session = dict(matching_sessions[0])
        modified_session = append_request_to_session(modified_session, me)
        fs_session_directory.update_session(modified_session)
    else:
        print('No session for user %s running.' % target_user)


