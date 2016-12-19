# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


class Course(models.Model):
    _name = 'openacademy.course'

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

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

    @api.multi
    def copy(self, default=None):
        copied_count = self.search_count(
            [('name', '=ilike', (_("Copy of {}") + "%").format(self.name))]
        )
        if not copied_count:
            new_name = _("Copy of {}").format(self.name)
        else:
            while True:
                duplicated_count = self.search_count(
                    [('name', '=ilike', _("Copy of {} ({})").format(
                        self.name, copied_count))]
                )
                if not duplicated_count:
                    break
                else:
                    copied_count += 1
            new_name = _("Copy of {} ({})").format(
                self.name, copied_count)
        default['name'] = new_name
        return super(Course, self).copy(default)
