#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import sys
import time

from fs_storage import *
import config

if __name__ == "__main__":
    conf = config.load()
    base_dir = conf['base_dir']

    fs_session_storage = FileSystemSessionStorage(base_dir)
    sessions = fs_session_storage.list_sessions()
    print('currently running sessions: ')
    print(sessions)
