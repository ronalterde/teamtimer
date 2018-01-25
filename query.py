#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import sys
import time

from fs_dir import *
import config

TARGET_OWNER = sys.argv[1]

if __name__ == "__main__":
    conf = config.load()
    base_dir = conf['base_dir']
    me = conf['me']

    fs_session_directory = FsSessionDirectory(base_dir)
    sessions = fs_session_directory.list_sessions()
    matching_sessions = [x for x in sessions if x['owner'] == TARGET_OWNER]

    if len(matching_sessions) == 1:
        print('Session for user %s running. Scheduled end time: %s' % (TARGET_OWNER, matching_sessions[0]['end_time']))
        print('Filing request...')
        modified_session = dict(sessions[0])
        modified_session = append_request_to_session(modified_session, me)
        fs_session_directory.update_session(modified_session)
    else:
        print('No session for user %s running.' % TARGET_OWNER)


