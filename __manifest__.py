# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

{
    'name': 'OpenEduCat Discipline',
    'version': '13.0',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Discipline Rules',
    'complexity': "easy",
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': [
        'account',
        'product',
        'openeducat_core_enterprise',
        'openeducat_student_progress_enterprise',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'data/fine_product_demo.xml',
        'data/discipline_mail_template_data.xml',
        'wizard/take_action_wizard_view.xml',
        'wizard/progression_discipline_wizard_view.xml',
        'views/misbehaviour_category_view.xml',
        'wizard/take_action_wizard_view.xml',
        'views/discipline_record_view.xml',
        'views/suspended_student_view.xml',
        'views/student_view.xml',
        'views/school_offences_view.xml',
        'views/elearning_rules_view.xml',
        'views/openeducat_discipline_portal.xml',
        'views/openeducat_progression_discipline.xml',
        'views/student_progression_discipline_portal.xml',
        'wizard/misbehaviour_type_wizard_view.xml',
        'wizard/student_wise_wizard_view.xml',
        'report/misbehaviour_type_report.xml',
        'report/student_wise_report.xml',
        'report/report_menu.xml',
        'report/discipline_progression_report.xml',
        'menus/op_menu.xml',
        'views/assets.xml',
    ],
    'demo': [
        'demo/misbehave_category_demo.xml',
        'demo/discipline_record_demo.xml',
        'demo/suspended_students_demo.xml',
        'demo/progression_discipline_demo.xml'
    ],
    'images': [
        'static/description/openeducat_discipline_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 150,
    'currency': 'EUR',
    'license': 'OPL-1',
    'live_test_url': 'https://www.openeducat.org/plans'
}
