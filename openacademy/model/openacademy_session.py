# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string='Title', required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")

    taken_seats = fields.Float(compute="_taken_seats", default=0.0)

    instructor_id = fields.Many2one(
        'res.partner',
        string='Instructor',
        domain=[
            '|',
            ('instructor', '=', True),
            ('category_id', 'ilike', 'Teacher'),
        ]
    )
    course_id = fields.Many2one(
        'openacademy.course',
        ondelete='cascade',
        string='Course',
        required=True
    )
    attendee_ids = fields.Many2many('res.partner', string='Attendees')

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if self.seats:
            self.taken_seats = 100 * len(self.attendee_ids) / self.seats
        else:
            self.taken_seats = 0
