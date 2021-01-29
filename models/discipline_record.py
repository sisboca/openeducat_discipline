# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

from odoo.exceptions import ValidationError

from odoo import models, fields, api, _


class OpDiscipline(models.Model):
    _name = "op.discipline"
    _inherit = "mail.thread"
    _description = "Discipline Record Details"
    _rec_name = "student_id"

    @api.depends('student_id')
    def _compute_get_student_class(self):
        for record in self:
            if record.student_id:
                student_search = self.env['op.student']. \
                    search([('id', '=', record.student_id.id)])
                if student_search and student_search.course_detail_ids:
                    record.course_id = \
                        student_search.course_detail_ids[0].course_id

    student_id = fields.Many2one('op.student', 'Student', required=True)

    progression_id = fields.Many2one('op.student.progression',
                                     string="Progression No")

    date = fields.Date('Date', copy=False, default=fields.Date.today())
    course_id = fields.Many2one(
        'op.course', 'Course',
        compute='_compute_get_student_class', store=True)
    discipline_master = fields.Many2one(
        'res.users', string='Created By',
        default=lambda self: self.env.user, readonly=True)
    priority = fields.Selection(
        [('0', 'Low'), ('1', 'Normal'), ('2', 'High')],
        string='Priority')
    misbehaviour_type = fields.Selection(
        [('major', 'Major'), ('minor', 'Minor')],
        'Misbehaviour Type', required=True)

    misbehaviour_category_id = fields.Many2one(
        'op.misbehaviour.category', 'Misbehaviour Category', required=True)
    misbehaviour_action = fields.Char('Action To Be Taken', required=True)
    meeting_datetime = fields.Datetime('Meeting Date Time')
    meeting_remark = fields.Text('Remark For Meeting')
    master_comment = fields.Text('Comment By Discipline Master')
    parent_comment = fields.Text(
        'Comment By Discipline Master (Meeting With Parents)')
    state = fields.Selection(
        [('draft', 'Draft'), ('email_sent', 'Email Sent'),
         ('awaiting_letter', 'Awaiting Letter'),
         ('action_taken', 'Action Taken'),
         ('awaiting_meeting', 'Awaiting Meeting'),
         ('suspended', 'Suspended'), ('done', 'Done')],
        'State', default='draft', track_visibility='onchange')
    company_id = fields.Many2one(
        'res.company', 'Company', required=True,
        default=lambda self: self.env.user.company_id)
    note = fields.Text(string="Note")
    recipients_ids = fields.Many2many('res.partner', 'recipients_id')
    active = fields.Boolean(default=True)
    merit_points = fields.Float(string='Merit Points')
    demerit_points = fields.Float(string='Demerit Points')

    @api.onchange('student_id')
    def onchange_student_discipline_progrssion(self):
        if self.student_id:
            student = self.env['op.student.progression'].search(
                [('student_id', '=', self.student_id.id)])
            self.progression_id = student.id
            sequence = student.name
            student.write({'name': sequence})

    @api.constrains('meeting_datetime')
    def check_dates(self):
        for record in self:
            today_date = fields.Datetime.from_string(fields.Datetime.now())
            meeting_datetime = \
                fields.Datetime.from_string(record.meeting_datetime)
            if meeting_datetime < today_date:
                raise ValidationError(
                    _("Meeting Date cannot be set before Today."))

    def _composer_format(self, res_model, res_id, template):
        compose_form = self.env.ref(
            'mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model=res_model,
            default_res_id=res_id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            misbehaviour_report_as_sent=True,
            force_email=True
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def send_email(self):
        self.ensure_one()
        template = self.misbehaviour_category_id.misbehaviour_template_id
        return self._composer_format(res_model='op.discipline',
                                     res_id=self.id,
                                     template=template)

    def apologies_letter(self):
        self.state = 'awaiting_letter'

    def meeting_awaiting(self):
        self.state = 'awaiting_meeting'

    def submit_apology_letter(self):
        self.ensure_one()
        template = self.env.ref(
            'openeducat_discipline.email_student_apology_letter_template',
            False)
        self.state = 'awaiting_letter'
        return self._composer_format(res_model='op.student',
                                     res_id=self.id,
                                     template=template)


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def send_mail(self, auto_commit=False):
        res = super(MailComposeMessage, self).send_mail(
            auto_commit=auto_commit)
        context = self._context
        if context.get('default_model') == 'op.discipline' and \
                context.get('default_res_id') and \
                context.get('misbehaviour_report_as_sent'):
            discipline_id = self.env['op.discipline'].browse(
                context['default_res_id'])
            discipline_id.state = 'email_sent'
        return res


class OpStudent(models.Model):
    _inherit = "op.student"

    discipline_ids = fields.One2many('op.discipline', 'student_id',
                                     'Discipline Details')
    
    discipline_score = fields.Integer("Discipline Score", compute="change_discipline_point")

    @api.onchange('discipline_ids')
    def change_discipline_point(self):
        points = 0
        for discipline in self.discipline_ids:
            points += discipline.misbehaviour_category_id.point
        self.discipline_score = 40-points