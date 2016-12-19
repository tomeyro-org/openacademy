# -*- coding: utf-8 -*-

"""
" Web service tests
"""

import functools
import xmlrpclib
import time

HOST = 'localhost'
PORT = 8069
DB = 'odoo_course'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# 1: Login

uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
print "Logged in as %s (uid: %d)" % (USER, uid)

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS
)

# 2: Read the sessions

sessions = call('openacademy.session', 'search_read', [], [
    'name', 'seats', 'taken_seats'
])
for session in sessions:
    print "Session %s (%s seats : %s%% taken)" % (
        session['name'], session['seats'], session['taken_seats']
    )

# 3: Create new session

course_ids = call('openacademy.course', 'search', [('name', '=', 'WS Course')])
if len(course_ids) > 0:
    course_id = course_ids[0]
else:
    course_id = call('openacademy.course', 'create', {
        'name': 'WS Course',
        'responsible_id': uid
    })

session_id = call('openacademy.session', 'create', {
    'name': 'WS Session ' + time.strftime('%Y-%m-%d %H:%M:%S'),
    'course_id': course_id
})
print "Session created (uid: %d)" % (session_id)
