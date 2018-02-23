#!/usr/bin/env python3

from datetime import timedelta
import storage

class SessionHandle:
    def get_end_time(self):
        my_session = self.session_storage.get_session_owned_by(self.owner)
        return my_session['end_time']

class PublisherSessionHandle(SessionHandle):
    def __init__(self, session_storage, owner):
        self.session_storage = session_storage
        self.owner = owner

    def stop(self):
        self.session_storage.remove_sessions_owned_by(self.owner)

    def get_requests(self):
        """TODO: Storage should ensure there's only one session per user."""
        session = self.session_storage.get_session_owned_by(self.owner)
        if 'requests' in session:
            return session['requests']
        else:
            return []

class ObserverSessionHandle(SessionHandle):
    def __init__(self, session_storage, owner):
        self.session_storage = session_storage
        self.owner = owner

    def make_request(self, me):
        session = self.session_storage.get_session_owned_by(self.owner)
        modified_session = dict(session)
        modified_session = storage.append_request_to_session(modified_session, me)
        self.session_storage.update_session(modified_session)

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

        return PublisherSessionHandle(self.session_storage, username)

    def _calculate_end_time(self, duration):
        return self.time_provider.get_current_time() + duration

    def get_running_session(self, owner):
        session = self.session_storage.get_session_owned_by(owner)
        if session == None:
            return None
        return ObserverSessionHandle(self.session_storage, session['owner'])
