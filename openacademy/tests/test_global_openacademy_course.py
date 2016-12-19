# -*- coding: utf-8 -*-

'''
Global tests for open academy courses
'''

from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger


class GlobalTestOpenAcademyCourse(TransactionCase):
    '''
    Global tests for open academy courses
    '''

    # Pseudo-constructor
    def setUp(self):
        super(GlobalTestOpenAcademyCourse, self).setUp()
        # Define global variables
        self.course = self.env['openacademy.course']

    # Class methods (not tests)

    def create_course(self, name, description, responsible_id=None):
        '''
        Create a course and return its id
        '''
        course_id = self.course.create({
            'name': name,
            'description': description,
            'responsible_id': responsible_id
        })
        return course_id

    # Test methods

    @mute_logger('openerp.sql_db')
    def test_01_same_name_description(self):
        '''
        Create course with same name and description
        to test constraint that forces them to be different
        '''
        with self.assertRaisesRegexp(
            IntegrityError,
            'new row for relation "openacademy_course" violates check'
            ' constraint "openacademy_course_name_description_check"'
        ):
            self.create_course('test', 'test')
