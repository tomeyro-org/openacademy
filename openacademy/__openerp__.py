# -*- coding: utf-8 -*-

{
    'name': "Open Academy",

    'summary': """Manage trainings""",

    'author': "tomas@vauxoo.com",
    'website': "http://www.vauxoo.com",

    'category': "Test",
    'version': "0.1",

    'depends': ["base"],

    'data': [
        'view/openacademy_course_view.xml',
        'view/openacademy_session_view.xml',
        'view/openacademy_session_workflow.xml',
        'view/partner_view.xml',
    ],
    'demo': [
        'demo/openacademy_course_demo.xml',
    ],

    'installable': True,
    'auto_install': False,
}
