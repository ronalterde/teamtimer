#!/usr/bin/env python3

from datetime import timedelta
import storage

class SessionHandle:
    def get_end_time(self):
        sessions = self.session_storage.list_sessions()
        my_sessions = [x for x in sessions if x['owner'] == self.owner]
        return my_sessions[0]['end_time']

class PublisherSessionHandle(SessionHandle):
    def __init__(self, session_storage, owner):
        self.session_storage = session_storage
        self.owner = owner

    def stop(self):
        self.session_storage.remove_sessions_owned_by(self.owner)

    def get_requests(self):
        session = self._get_my_session()
        if 'requests' in session:
            return session['requests']
        else:
            return []

    def _get_my_session(self):
        """TODO: Storage should ensure there's only one session per user."""
        sessions = self.session_storage.list_sessions()
        my_sessions = [x for x in sessions if x['owner'] == self.owner]
        return my_sessions[0]

class ObserverSessionHandle(SessionHandle):
    def __init__(self, session_storage, owner):
        self.session_storage = session_storage
        self.owner = owner

    def make_request(self, me):
        sessions = self.session_storage.list_sessions()
        matching_sessions = [x for x in sessions if x['owner'] == self.owner]
        modified_session = dict(matching_sessions[0])
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

    def get_running_sessions(self):
        sessions = self.session_storage.list_sessions()
        handlers = []
        for i in sessions:
            handlers.append(ObserverSessionHandle(self.session_storage, i['owner']))
        return handlers
