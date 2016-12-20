# -*- coding: utf-8 -*-

'''
Global tests for open academy session
'''

from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger
from openerp.exceptions import ValidationError


class GlobalTestOpenAcademySession(TransactionCase):
    '''
    Global tests for open academy courses
    '''

    # Pseudo-constructor
    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']

    # Class methods (not tests)

    def create_session(self, name, course_id, **kwargs):
        '''
        Create a session and return its id
        '''
        kwargs['name'] = name
        kwargs['course_id'] = course_id
        session_id = self.session.create(kwargs)
        return session_id

    def get_example_course(self):
        '''
        Return an example course
        '''
        return self.env.ref('openacademy.course0')

    def get_example_partner(self, ref='base.partner_root'):
        '''
        Return an example partner
        '''
        return self.env.ref(ref)

    # Test methods

    def test_10_instructor_is_attendee(self):
        '''
        Create a course with instructor as attendee.
        It should raise a validation error.
        '''
        course = self.get_example_course()
        partner = self.get_example_partner()
        with self.assertRaisesRegexp(
            ValidationError,
            "A session's instructor can't be an attendee"
        ):
            self.create_session(
                'test',
                course.id,
                instructor_id=partner.id,
                seats=10,
                attendee_ids=[(4, partner.id)]
            )

    @mute_logger('openerp.sql_db')
    def test_20_empty_instructor(self):
        '''
        Create a course without and instructor.
        It should raise an integrity error.
        '''
        with self.assertRaisesRegexp(
            IntegrityError,
            'null value in column "course_id" violates not-null constraint'
        ):
            self.create_session('test', None)

    def test_30_workflow(self):
        '''
        Create a session and test its workflow.
        1. It should start in 'draft'
        2. After 'button_confirm' signal it should be 'confirmed'
        3. After 'button_done' signal it should be 'done'
        4. After 'button_draft' signal it should go back to 'draft'
        5. After adding a new attendee it should go to 'confirmed'
        6. After 'button_draft' it should remain in 'confirmed'
        7. After removing an anttendee and signaling 'button_draft' again it
        should go back to 'draft'
        '''
        session = self.create_session(
            'test',
            self.get_example_course().id,
            seats=3,
            attendee_ids=[(4, self.get_example_partner().id)]
        )
        # 1
        self.assertEqual(
            session.state, 'draft',
            'Initial state should be "draft"'
        )
        # 2
        session.signal_workflow('button_confirm')
        self.assertEqual(
            session.state, 'confirmed',
            'After signal "button_confirm" state should be "confirmed"'
        )
        # 3
        session.signal_workflow('button_done')
        self.assertEqual(
            session.state, 'done',
            'After signal "button_done" state should be "done"'
        )
        # 4
        session.signal_workflow('button_draft')
        self.assertEqual(
            session.state, 'draft',
            'After signal "button_draft" (from "done") state should be "draft"'
        )
        # 5
        session.write({
            'attendee_ids': [
                (4, self.get_example_partner('base.res_partner_23').id)
            ]
        })
        self.assertEqual(
            session.state, 'confirmed',
            'After adding a new attendee the state should be "confirmed"'
        )
        # 6
        session.signal_workflow('button_draft')
        self.assertEqual(
            session.state, 'confirmed',
            'After signal "button_draft" (from "confirmed" with 2 attendees) '
            'state should remain in "draft"'
        )
        # 7
        session.write({
            'attendee_ids': [(3, self.get_example_partner().id)]
        })
        session.signal_workflow('button_draft')
        self.assertEqual(
            session.state, 'draft',
            'After signal "button_draft" (from "confirmed" with 1 attendee) '
            'state should be "draft"'
        )
