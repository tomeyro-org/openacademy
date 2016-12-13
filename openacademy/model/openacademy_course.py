# -*- coding: utf-8 -*-

from openerp import models, fields


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()

    responsible_id = fields.Many2one(
        'res.users',
        ondelete='set null',
        string='Responsible',
        index=True
    )
    session_ids = fields.One2many(
        'openacademy.session',
        'course_id',
        string='Sessions'
    )
