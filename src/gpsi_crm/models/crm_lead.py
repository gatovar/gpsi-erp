# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead', 'gpsi.project.task.mixin']


class CrmLeadCertificationWorkflow(models.Model):
    _inherit = 'crm.lead'

    def stage_changed(self, stage_name):
        self.ensure_one()
    
        self._update_crm_stage(stage_name)
        self._update_task_stage()

        if stage_name == 'Unassigned':
            self._start_unassigned_cert_act()
        elif stage_name == 'Qualify':
            self._start_qualify_cert_act()
        elif stage_name == 'Proposition':
            self._start_proposition_cert_act()
        elif stage_name == 'Won':
            self._start_won_cert_act()
        elif stage_name == 'Lost':
            self._start_lost_cert_act()

    def _start_unassigned_cert_act(self):
        self.ensure_one()

        task = self.env['project.task'].create({
            'name': self.name,
            'project_id': self.team_id.bpm_project_id.id
        })

        task.write({
            'res_attachment_ids': [(0, False, {
                'task_id': task.id,
                'res_model': self._name,
                'res_id': self.id
            })]
        })

    def _start_qualify_cert_act(self):
        pass

    def _start_proposition_cert_act(self):
        pass

    def _start_won_cert_act(self):
        pass

    def _start_lost_cert_act(self):
        pass

    def task_completed(self):
        if not self._validate():
            raise ValidationError(_(''))

    def _validate(self):
        return False

    def _update_task_stage(self):
        stage = self._find_task_stage(self.stage_id.name)
        if stage != False:
            self.task_id.write({
                'stage_id': stage.id
            })

    def _find_task_stage(self, name):
        return self.env['project.task.type'].search([('name','=',name), ('project_ids','in',[self.team_id.bpm_project_id.id])])

    def _update_crm_stage(self, name):
        stage = self._find_crm_stage(name)
        self.write({
            'stage_id': stage.id
        })

    def _find_crm_stage(self, name):
        return self.env['crm.stage'].search([('name','=',name), ('team_id','=',self.team_id.id)])
