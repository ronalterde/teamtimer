#!/usr/bin/env python3

from datetime import datetime

def append_request_to_session(session, request):
    new_session = dict(session)

    if 'requests' in new_session:
        new_session['requests'].append(request)
        return new_session
    else:
        new_session['requests'] = [ request ]
        return new_session
