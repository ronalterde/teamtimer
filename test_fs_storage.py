#!/usr/bin/env python3

from fs_storage import *

import unittest

class TestSessionString(unittest.TestCase):

    def test_session_to_file_name(self):
        self.assertEqual(session_to_file_name(
            { 'owner' : 'A', 'end_time' : datetime(2018, 1, 1, 20, 15) }), 'A_2018-01-01T20:15:00')
        self.assertEqual(session_to_file_name(
            { 'owner' : 'B', 'end_time' : datetime(2018, 1, 1, 20, 15) }), 'B_2018-01-01T20:15:00')
        self.assertEqual(session_to_file_name(
            { 'owner' : 'A', 'end_time' : datetime(1999, 1, 1, 20, 15) }), 'A_1999-01-01T20:15:00')

    def test_session_to_file_content(self):
        self.assertEqual(session_to_file_content({ }), '')
        self.assertEqual(session_to_file_content({ 'requests' : [ 'A' ]}), 'A')
        self.assertEqual(session_to_file_content({ 'requests' : [ 'A', 'B' ]}), 'A\nB')
        self.assertEqual(session_to_file_content({
            'owner' : 'A',
            'end_time' : datetime(1999, 1, 1, 20, 15),
            'requests' : [ 'A', 'B' ] }), 'A\nB')

    def test_file_to_session(self):
        self.assertRaises(ValueError, file_to_session, '', '')

        self.assertEqual(file_to_session('A_2018-01-01T20:15:00', ''),
                { 'owner' : 'A', 'end_time' : datetime(2018, 1, 1, 20, 15) })
        self.assertEqual(file_to_session('B_2018-01-01T20:15:00', ''),
                { 'owner' : 'B', 'end_time' : datetime(2018, 1, 1, 20, 15) })
        self.assertEqual(file_to_session('UserFoo_2018-01-01T20:15:00', ''),
                { 'owner' : 'UserFoo', 'end_time' : datetime(2018, 1, 1, 20, 15) })

        self.assertEqual(file_to_session('A_2018-01-01T20:15:00', 'A'),
                { 'owner' : 'A', 'end_time' : datetime(2018, 1, 1, 20, 15), 'requests' : [ 'A' ] })
        self.assertEqual(file_to_session('A_2018-01-01T20:15:00', 'A\nB'),
                { 'owner' : 'A', 'end_time' : datetime(2018, 1, 1, 20, 15), 'requests' : [ 'A', 'B' ] })

    def test_append_request_to_session(self):
        new_session = append_request_to_session({ 'owner' : 'A', 'end_time' : datetime(2018, 1, 1, 20, 15) }, 'A')
        self.assertTrue('requests' in new_session)
        self.assertEqual(new_session['requests'], [ 'A' ])

        new_session2 = append_request_to_session(new_session, 'B')
        self.assertEqual(new_session['requests'], [ 'A', 'B' ])

        self.assertEqual(new_session2, { 'owner' : 'A', 'end_time' : datetime(2018, 1, 1, 20, 15), 'requests' : [ 'A', 'B' ]})

