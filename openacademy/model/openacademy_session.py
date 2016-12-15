# -*- coding: utf-8 -*-

from datetime import timedelta
from openerp import models, fields, api, exceptions


class Session(models.Model):
    _name = 'openacademy.session'

    _sql_constraints = [
        ('check_end_gte_start',
         'CHECK(end_date >= start_date)',
         "The end date must be greater than the start date"),

        ('check_duration_gte_zero',
         'CHECK(duration >= 0)',
         "The duration must be positive"),
    ]

    name = fields.Char(string='Title', required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(
        digits=(6, 2),
        string="Duration in days",
        help="Duration in days"
    )
    end_date = fields.Date(
        store=True,
        compute="_get_end_date",
        inverse="_set_end_date"
    )
    hours = fields.Float(
        string="Duration in hours",
        compute="_get_hours",
        inverse="_set_hours"
    )
    seats = fields.Integer(string="Number of seats")
    taken_seats = fields.Float(compute="_taken_seats", default=0.0)
    active = fields.Boolean(default=True)
    color = fields.Integer()
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
    attendees_count = fields.Integer(
        store=True,
        compute='_get_attendees_count'
    )
    state = fields.Selection(
        [
            ('draft', "Draft"),
            ('confirmed', "Confirmed"),
            ('done', "Done"),
        ]
    )

    @api.one
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        if not (self.start_date and self.duration):
            self.end_date = self.start_date
        else:
            # Add duration to start_date, but: Mon + 5 days = Sat, so
            # subtract one second to get on Fri instead
            start = fields.Datetime.from_string(self.start_date)
            duration = timedelta(days=self.duration, seconds=-1)
            self.end_date = start + duration

    def _set_end_date(self):
        if self.start_date and self.end_date:
            # Compute the difference between dates, but: Fri - Mon = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(self.start_date)
            end_date = fields.Datetime.from_string(self.end_date)
            self.duration = (end_date - start_date).days + 1

    @api.one
    @api.depends('duration')
    def _get_hours(self):
        self.hours = self.duration * 24

    def _set_hours(self):
        self.duration = self.hours / 24

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if self.seats:
            self.taken_seats = 100 * len(self.attendee_ids) / self.seats
        else:
            self.taken_seats = 0

    @api.one
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        self.attendees_count = len(self.attendee_ids)

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not "
                               "be negative",
                }
            }
        if len(self.attendee_ids) > self.seats:
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                }
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError("A session's instructor can't be "
                                             "an attendee")

    @api.multi
    def action_draft(self):
        self.ensure_one()
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.ensure_one()
        self.state = 'done'
