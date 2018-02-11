#!/usr/bin/env python3

from datetime import datetime
import storage
import unittest

def test_append_request_to_session(self):
    new_session = append_request_to_session({ 'owner' : 'A', 'end_time' : datetime(2018, 1, 1, 20, 15) }, 'A')
    self.assertTrue('requests' in new_session)
    self.assertEqual(new_session['requests'], [ 'A' ])

    new_session2 = append_request_to_session(new_session, 'B')
    self.assertEqual(new_session['requests'], [ 'A', 'B' ])

    self.assertEqual(new_session2, { 'owner' : 'A', 'end_time' : datetime(2018, 1, 1, 20, 15), 'requests' : [ 'A', 'B' ]})
