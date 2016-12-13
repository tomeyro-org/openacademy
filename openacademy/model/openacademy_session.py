from openerp import models, fields


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string='Title', required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
