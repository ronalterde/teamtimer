#!/usr/bin/env python3

import unittest
from session import Session
from datetime import datetime
from datetime import timedelta

class TestSessionDirectory:
    def __init__(self):
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def remove_sessions_owned_by(self, owner):
        self.sessions = [s for s in self.sessions if s['owner'] != owner]

    def update_session(self, session):
        pass

    def list_sessions(self):
        pass

class TestTimeProvider:
    def __init__(self):
        self.current = datetime.now()
            
    def get_current_time(self):
        return self.current

class TestSession(unittest.TestCase):

    def setUp(self):
        self.valid_duration = timedelta(seconds=10)
        self.directory = TestSessionDirectory()
        self.time_provider = TestTimeProvider()

    def test_start_puts_session_data_into_directory(self):
        session = Session(self.directory, self.time_provider, 'Franz')
        session.start(duration=self.valid_duration)
        self.assertEqual(len(self.directory.sessions), 1)

    def test_start_doesnt_put_if_duration_zero(self):
        session = Session(self.directory, self.time_provider, 'Franz')
        session.start(timedelta(seconds=0))
        self.assertEqual(len(self.directory.sessions), 0)

    def test_start_doesnt_put_if_username_empty(self):
        session = Session(self.directory, self.time_provider, '')
        session.start(duration=self.valid_duration)
        self.assertEqual(len(self.directory.sessions), 0)

    def test_start_sets_end_time_and_returns_it(self):
        expected_end_time = self.time_provider.current + self.valid_duration
        session = Session(self.directory, self.time_provider, 'Franz')

        end_time = session.start(duration=self.valid_duration)

        self.assertEqual(self.directory.sessions[0]['end_time'], expected_end_time)
        self.assertEqual(end_time, expected_end_time)

    def test_start_sets_owner(self):
        session = Session(self.directory, self.time_provider, 'Franz')
        session.start(duration=self.valid_duration)
        self.assertEqual(self.directory.sessions[0]['owner'], 'Franz')

        session = Session(self.directory, self.time_provider, 'Helmut')
        session.start(duration=self.valid_duration)
        self.assertEqual(self.directory.sessions[1]['owner'], 'Helmut')

    def test_start_removes_all_previous_sessions_of_this_user(self):
        session = Session(self.directory, self.time_provider, 'Franz')
        for i in range(0, 100):
            session.start(duration=self.valid_duration)

        session = Session(self.directory, self.time_provider, 'Franz')
        session.start(duration=self.valid_duration)

        self.assertEqual(len(self.directory.sessions), 1)

    def test_start_doesnt_remove_sessions_of_other_users(self):
        Session(self.directory, self.time_provider, 'Helmut').start(self.valid_duration)
        Session(self.directory, self.time_provider, 'Wilhelm').start(self.valid_duration)
        Session(self.directory, self.time_provider, 'Friedbert').start(self.valid_duration)
        self.assertEqual(len(self.directory.sessions), 3)

        Session(self.directory, self.time_provider, 'Franz').start(duration=self.valid_duration)

        self.assertEqual(len(self.directory.sessions), 4)

    def test_stop_returns_filed_requests(self):
        session = Session(self.directory, self.time_provider, 'Franz')
        session.start(duration=self.valid_duration)
        requests = session.stop()
        self.assertTrue(isinstance(requests, list))

    def test_stop_removes_session_from_directory(self):
        pass
