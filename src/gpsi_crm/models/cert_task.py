# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CertTask(models.Model):
    '''
    '''
    _inherit = 'project.task'

    gpsi_is_cert_task = fields.Boolean()
    gpsi_opportunity = fields.Many2one()
    gpsi_application_card = fields.Many2one()


    @api.model
    def state_changed(self, state):
        pass

    def _start_unassigned_cert_wkf(self):
        pass

    @api.model
    def task_completed(self):
        pass
        