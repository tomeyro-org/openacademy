# -*- coding: utf-8 -*-

from openerp import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(default=False)

    session_ids = fields.Many2many(
        'openacademy.session',
        string='Attended sessions',
        readonly=True
    )
