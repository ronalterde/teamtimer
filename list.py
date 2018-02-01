#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import sys
import time

from fs_dir import *
import config

if __name__ == "__main__":
    conf = config.load()
    base_dir = conf['base_dir']

    fs_session_directory = FsSessionDirectory(base_dir)
    sessions = fs_session_directory.list_sessions()
    print('currently running sessions: ')
    print(sessions)
