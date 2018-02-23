#!/usr/bin/env python3

import unittest
from session import *
from datetime import datetime
from datetime import timedelta

class TestSessionStorage:
    def __init__(self):
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def remove_sessions_owned_by(self, owner):
        self.sessions = [s for s in self.sessions if s['owner'] != owner]

    def update_session(self, session):
        self.remove_sessions_owned_by(session['owner'])
        self.sessions.append(session)

    def get_session_owned_by(self, owner):
        matching_sessions = [s for s in self.sessions if s['owner'] == owner]
        if len(matching_sessions) == 0:
            return None
        return matching_sessions[0]

class TestTimeProvider:
    def __init__(self):
        self.current = datetime.now()
            
    def get_current_time(self):
        return self.current

class SessionManagerTest(unittest.TestCase):
    def setUp(self):
        self.session_storage = TestSessionStorage()
        self.time_provider = TestTimeProvider()
        self.manager = SessionManager(self.session_storage, self.time_provider)

    def test_create_session_puts_session_data_into_storage(self):
        self.manager.create_session('Franz', timedelta(seconds=10))
        self.assertEqual(len(self.session_storage.sessions), 1)

    def test_create_session_doesnt_put_if_duration_zero(self):
        self.manager.create_session('Franz', timedelta(seconds=0))
        self.assertEqual(len(self.session_storage.sessions), 0)

    def test_create_session_doesnt_put_if_username_empty(self):
        self.manager.create_session('', timedelta(seconds=10))
        self.assertEqual(len(self.session_storage.sessions), 0)

    def test_create_session_sets_end_time(self):
        self.manager.create_session('Franz', timedelta(seconds=10))

        expected_end_time = self.time_provider.current + timedelta(seconds=10)
        self.assertEqual(self.session_storage.sessions[0]['end_time'], expected_end_time)

    def test_create_session_sets_owner(self):
        self.manager.create_session('Franz', timedelta(seconds=10))
        self.assertEqual(self.session_storage.sessions[0]['owner'], 'Franz')

        self.manager.create_session('Helmut', timedelta(seconds=10))
        self.assertEqual(self.session_storage.sessions[1]['owner'], 'Helmut')

    def test_create_session_removes_all_previous_sessions_of_this_user(self):
        for i in range(0, 100):
            self.manager.create_session('Franz', timedelta(seconds=10))

        self.assertEqual(len(self.session_storage.sessions), 1)

    def test_create_session_doesnt_remove_sessions_of_other_users(self):
        self.manager.create_session('Friedhelm', timedelta(seconds=10))
        self.manager.create_session('Helmut', timedelta(seconds=10))
        self.manager.create_session('Franz', timedelta(seconds=10))

        self.assertEqual(len(self.session_storage.sessions), 3)

    def test_create_session_returns_handle(self):
        handle = self.manager.create_session('Franz', timedelta(seconds=10))
        self.assertTrue(isinstance(handle, PublisherSessionHandle))

    def test_create_session_passes_owner_to_handle(self):
        handle = self.manager.create_session('Franz', timedelta(seconds=10))
        self.assertEqual(handle.owner, 'Franz')

        handle = self.manager.create_session('Helmut', timedelta(seconds=10))
        self.assertEqual(handle.owner, 'Helmut')

    def test_get_running_session_returns_none(self):
        self.assertEqual(self.manager.get_running_session('NotExistingOwner'), None)

    def test_get_running_session_returns_observer_handle(self):
        self.manager.create_session('Franz', timedelta(seconds=10))
        self.assertTrue(isinstance(self.manager.get_running_session('Franz'), ObserverSessionHandle))

    def test_get_running_session_puts_owner_into_handle(self):
        self.manager.create_session('Franz', timedelta(seconds=10))
        self.manager.create_session('Helmut', timedelta(seconds=10))
        self.assertEqual(self.manager.get_running_session('Franz').owner, 'Franz')
        self.assertEqual(self.manager.get_running_session('Helmut').owner, 'Helmut')

class PublisherSessionHandleTest(unittest.TestCase):
    def setUp(self):
        self.session_storage = TestSessionStorage()
        self.time_provider = TestTimeProvider()
        self.manager = SessionManager(self.session_storage, self.time_provider)

    # def test_stop_throws_if_no_session_in_storage(self):
    #     self.assertRaises(Exception, self.handle.stop())

    def test_stop_removes_session_from_storage(self):
        handle = self.manager.create_session('Franz', timedelta(seconds=10))
        self.assertEqual(len(self.session_storage.sessions), 1)
        handle.stop()
        self.assertEqual(len(self.session_storage.sessions), 0)

    def test_get_end_time_returns_time_from_storage(self):
        self.manager.create_session('Helmut', timedelta(seconds=10))
        self.session_storage.sessions[0]['end_time'] = datetime(2018, 10, 11, 5, 12, 23, 1)

        handle = self.manager.create_session('Franz', timedelta(seconds=10))
        self.assertEqual(self.session_storage.sessions[1]['end_time'], handle.get_end_time())

    def test_get_requests(self):
        handle = self.manager.create_session('Franz', timedelta(seconds=10))
        
        self.assertEqual(handle.get_requests(), [])

        self.session_storage.sessions[0]['requests'] = [ 'Hans' ]
        self.assertEqual(handle.get_requests(), ['Hans'])

        self.session_storage.sessions[0]['requests'] = [ 'Hans', 'Lenz' ]
        self.assertEqual(handle.get_requests(), ['Hans', 'Lenz'])

class ObserverSessionHandleTest(unittest.TestCase):
    def setUp(self):
        self.session_storage = TestSessionStorage()
        self.time_provider = TestTimeProvider()
        self.manager = SessionManager(self.session_storage, self.time_provider)

    def test_request_goes_into_storage(self):
        self.manager.create_session('Franz', timedelta(seconds=10))
        handle = self.manager.get_running_session('Franz')
        handle.make_request('Hans')
        self.assertEqual(self.session_storage.sessions[0]['requests'], ['Hans'])

    def test_get_end_time_is_from_base_class(self):
        self.manager.create_session('Franz', timedelta(seconds=10))
        handle = self.manager.get_running_session('Franz')
        handle.get_end_time()
