# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class AuditProject(models.Model):
    _inherit = 'project.project'

    gs_is_cert_audit = fields.Boolean('Cert. Audit', help='Mark task like certification audit')
    gs_is_vendor_audit = fields.Boolean('Vendor Audit', help='Mark project like vendor audit')

    @api.model
    def create(self, vals):
        res = super(AuditProject, self).create(vals)
        res._gs_init_stages()
        return res

    def _gs_init_stages(self):
        if not self.gs_is_vendor_audit:
            return

        self.env.ref('gpsi_staff.vendor_audit_new_stage').write({'project_ids': [(4, self.id, False)]})
        self.env.ref('gpsi_staff.vendor_audit_scheduling_stage').write({'project_ids': [(4, self.id, False)]})
        self.env.ref('gpsi_staff.vendor_audit_execute_stage').write({'project_ids': [(4, self.id, False)]})
        self.env.ref('gpsi_staff.vendor_audit_review_stage').write({'project_ids': [(4, self.id, False)]})
        self.env.ref('gpsi_staff.vendor_audit_closed_stage').write({'project_ids': [(4, self.id, False)]})


class AuditTask(models.Model):
    _inherit = 'project.task'

    gs_checklist_id = fields.Many2one('gpsi.staff.checklist', 'Checklist', domain=[('is_template','=',True)])
    gs_assessment_id = fields.Many2one('gpsi.staff.checklist', 'Assessment')
    gs_audit_team_ids = fields.One2many('gpsi.staff.audit.team.member', 'task_id', 'Team')

    @api.model
    def create(self, vals):
        res = super(AuditTask, self).create(vals)
        res._gs_create_assessment()
        return res

    def _gs_create_assessment(self):
        if not self.project_id and not self.project_id.gs_is_vendor_audit:
            return

        assessment = self.gs_checklist_id.create_assessment()
        self.write({
            'gs_assessment_id': assessment.id
        })

    @api.multi
    def action_gs_edit_assessment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/ga/admin/va/events/{0}/assessment/edit'.format(self.id),
            'target': 'new'
        }
        

class AuditMember(models.Model):
    _name = 'gpsi.staff.audit.team.member'
    _description = 'Audit Member'

    task_id = fields.Many2one('project.task', 'Audit Task')
    user_id = fields.Many2one('res.users', 'User')
    role = fields.Selection([('lead', 'Lead'), ('observer', 'Observer'), ('witness', 'Witness')], 'Role')
