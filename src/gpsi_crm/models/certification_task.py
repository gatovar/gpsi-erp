# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    gpsi_is_cert_project = fields.Boolean('Certification Project', compute='_compute_gpsi_is_cert_project', help='Certification Sales Opportunity Project')
    gpsi_sales_team_id = fields.Many2one('crm.team', 'Sales Team')

    @api.depends()
    def _compute_gpsi_is_cert_project(self):
        cert_project = self.env.ref('gpsi_crm.project_certification_sales_opportunities')
        for project in self:
            project.gpsi_is_cert_project = project.id == cert_project.id


class ProjectTask(models.Model):
    _inherit = 'project.task'

    gpsi_is_cert_task = fields.Boolean('Certification Task', compute='_compute_gpsi_is_cert_task', help='Certification Sales Opportunity Task')
    gpsi_opportunity_id = fields.Many2one('crm.lead', 'Opportunity')


    @api.depends()
    def _compute_gpsi_is_cert_task(self):
        cert_project = self.env.ref('gpsi_crm.project_certification_sales_opportunities')
        for task in self:
            task.gpsi_is_cert_task = task.project_id and task.project_id.id == cert_project.id

    def _validate_cert_wkf(self):
        pass
