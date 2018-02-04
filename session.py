#!/usr/bin/env python3

from datetime import timedelta

class SessionManager:
    def __init__(self, session_storage, time_provider):
        self.session_storage = session_storage
        self.time_provider = time_provider

    def create_session(self, username, duration):
        if duration.total_seconds() == 0:
            return
        if username == '':
            return

        self.session_storage.remove_sessions_owned_by(username)
        self.session_storage.add_session({
            'end_time' : self._calculate_end_time(duration),
            'owner' : username
        })

    def _calculate_end_time(self, duration):
        return self.time_provider.get_current_time() + duration

class Session:
    def __init__(self, session_storage, time_provider, username):
        self.session_storage = session_storage
        self.time_provider = time_provider
        self.username = username
    
    def start(self, duration):
        if duration.total_seconds() == 0:
            return
        if self.username == '':
            return

        self.session_storage.remove_sessions_owned_by(self.username)
        self.session_storage.add_session({'end_time' : self.end_time(duration), 'owner' : self.username })
        return self.end_time(duration)

    def stop(self):
        return []

    def end_time(self, duration):
        return self.time_provider.get_current_time() + duration
