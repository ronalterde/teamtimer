#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import time

class Timer:
    def start(self, end_time):
        while datetime.now() < end_time:
            print('Time left: ' + str((end_time - datetime.now())).split('.')[0] + '\r', sep=' ', end='', flush=True)
            time.sleep(1)

class TimeProvider:
    def get_current_time(self):
        return datetime.now()
