# -*- coding: utf-8 -*-
"""Control de auditoría de certificación
"""

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class AuditProject(models.Model):
    _inherit = 'project.project'

    @api.model
    def create_supplier_audit_project(self, name, partner_id):
        """
        Crea proyecto de auditorías de vendedor
        """
        return self.sudo().create({
            'name': name,
            'is_supplier_audit': True,
            'partner_id': partner_id
        })

    @api.model
    def find_audit_project(self):
        """
        Busca el proyecto de auditoría asociado al usuario actual
        """
        return self.sudo().search([('is_supplier_audit','=',True), ('partner_id','=',self.env.user.company_id.partner_id.gstd_partner_id.id)])

    @api.model
    def request_audit(self, supplier_id, chk_id, date, notes):
        """
        Llamar este método para solicitar nueva auditoría a GlobalSTD
        """

        Task = self.env['project.task']
        Partner = self.env['res.partner']
        Audit = self.env['gpsi.staff.audit']
        AuditInvitation = self.env['gpsi.auditii.audit.invitation']

        project = self.find_audit_project()
        auditee = Partner.search([('id','=',supplier_id)])
        if not auditee.gstd_partner_id:
            raise ValidationError(_('Supplier dont have gstd partner'))

        audit = Audit.sudo().create({
            'chk_id': chk_id,
            'auditee_id': auditee.gstd_partner_id.id,
            'execution_date': date,
            'notes': notes
        })

        audit_task = Task.sudo().create({
            'name': auditee.name,
            'project_id': project.id,
            'company_id': 1,
            'audit_id': audit.id,
            'user_id': 1
        })
        
        if auditee.aii_company_id:
            auditee.sudo().aii_company_id.add_customer_audit(audit_task)
        else:
            AuditInvitation.send_invitation(auditee, audit_task.id)

        return audit_task

    @api.model
    def find_supplier_audits(self):
        """
        Busca todas las auditorías de vendedor asociadas a este proyecto y el usuario 
        actual
        """
        gstd_partner = self.env.user.company_id.partner_id.gstd_partner_id
        project = self.sudo().search([('is_supplier_audit','=',True), ('partner_id','=',gstd_partner.id)])
        return self.env['project.task'].sudo().search([('project_id','=',project.id)], order='create_date desc')


class AuditTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        res = super(AuditTask, self).create(vals)
        return res
