#!/usr/bin/env python3

from datetime import timedelta

class Session:
    def __init__(self, directory, time_provider, username):
        self.directory = directory
        self.time_provider = time_provider
        self.username = username
    
    def start(self, duration):
        if duration.total_seconds() == 0:
            return
        if self.username == '':
            return

        self.directory.remove_sessions_owned_by(self.username)
        self.directory.add_session({'end_time' : self.end_time(duration), 'owner' : self.username })
        return self.end_time(duration)

    def end_time(self, duration):
        return self.time_provider.get_current_time() + duration
