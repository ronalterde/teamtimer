#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import os
import time

def session_to_file_name(session):
    return session['owner'] + '_' + session['end_time'].strftime('%Y-%m-%dT%H:%M:%S')

def session_to_file_content(session):
    if 'requests' in session:
        return "\n".join(str(i) for i in session['requests'])
    else:
        return ''

def file_to_session(file_name, content):
    if file_name == '':
        raise ValueError
    owner = file_name.split('_')[0]
    end_time = file_name.split('_')[1]
    session = { 'owner' : owner,
                'end_time' : datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S') } 

    if content != '':
        session['requests'] = content.split()
    return session 

def append_request_to_session(session, request):
    new_session = dict(session)

    if 'requests' in new_session:
        new_session['requests'].append(request)
        return new_session
    else:
        new_session['requests'] = [ request ]
        return new_session

# This takes care of the concrete file and directory handling:
class FsSessionDirectory:
    def __init__(self, base_path):
        self.base_path = base_path

    def add_session(self, session):
        f = open(self.base_path + '/' + session_to_file_name(session), 'x')

    def remove_sessions_owned_by(self, owner):
        dir_content = os.listdir(self.base_path)
        matching_files = [f for f in dir_content if owner in f]
        for f in matching_files:
            os.remove(self.base_path + '/' + f)

    def update_session(self, session):
        with open(self.base_path + '/' + session_to_file_name(session), 'w') as session_file:
            session_file.write(session_to_file_content(session))

    def list_sessions(self):
        files = os.listdir(self.base_path)
        sessions = []
        for f in files:
            with open(self.base_path + '/' + f, 'r') as session_file:
                lines = session_file.readlines()
            sessions.append(file_to_session(f, ''.join(i for i in lines)))
        return sessions

if __name__ == "__main__":
    fs_session_directory = FsSessionDirectory('./test')
    fs_session_directory.add_session({'owner' : 'A', 'end_time' : datetime.now() + timedelta(minutes=30)})
    sessions = fs_session_directory.list_sessions()
    print(sessions)
    time.sleep(10)
    modified_session = dict(sessions[0])
    modified_session = append_request_to_session(modified_session, 'User A')
    modified_session = append_request_to_session(modified_session, 'User B')
    modified_session = append_request_to_session(modified_session, 'User C')
    fs_session_directory.update_session(modified_session)
    sessions = fs_session_directory.list_sessions()
    print(sessions)
    time.sleep(20)
    fs_session_directory.remove_sessions_owned_by('A')
