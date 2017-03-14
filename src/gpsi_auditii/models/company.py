# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Company(models.Model):
    _inherit = 'res.company'

    is_gaudit = fields.Boolean('GAudit', default=False)
    cust_audit_task_ids = fields.Many2many('project.task', 'gpsi_aii_company_audit_task_rel', 'company_id', 'task_id', 'Customer Audits', 
        domain="[('is_supplier_audit','=',True)]")

    @api.model
    def create_gaudit(self, name, email):
        """
        Crea una compania GAudit
        """
        Currency = self.env['res.currency'].sudo()
        return self.sudo().create({
            'is_gaudit': True,
            'name': name,
            'rml_header1': False,
            'email': email,
            'currency_id': Currency.search([('name','=','USD')]).id
        })

    @api.model
    def create(self, vals):
        res = super(Company, self).create(vals)

        if not res.partner_id.gstd_partner_id:
            res._create_gstd_partner()

        if res.is_gaudit:
            Project = self.env['project.project']
            Project.create_supplier_audit_project(res.name, res.partner_id.gstd_partner_id.id)

        return res

    @api.model
    def find_supplier_audit_project(self):
        """
        Regresa el proyecto de auditoría asociado a esta compañia
        """
        Project = self.env['project.project'].sudo()
        return Project.search([('is_supplier_audit','=',True), ('partner_id','=',self.partner_id.gstd_partner_id.id)])

    def add_customer_audit(self, audit_task):
        if audit_task:
            self.write({
                'cust_audit_task_ids': [(4, audit_task.id, 0)]
            })

    @api.multi
    def action_open_suppliers(self):
        self.ensure_one()
        return {
            "type": 'ir.actions.act_window',
            "res_model": 'res.partner',
            "views": [(False, 'tree'), (self.env.ref('gpsi_auditii.supplier_view_form').id, 'form')],
            "domain": [('company_id', '=', self.id), ('parent_id','=',False), ('supplier','=',True)],
            "context": {'default_company_id': self.id, 'default_supplier': True, 'default_customer': False, 'default_company_type': 'company'},
            "name": "Suppliers"
        }

    @api.multi
    def action_open_audits(self):
        self.ensure_one()
        project = self.find_supplier_audit_project()
        return {
            "type": 'ir.actions.act_window',
            "res_model": 'project.task',
            "views": [[False, 'tree'], [self.env.ref('gpsi_staff.supplier_audit_task_view_form').id, 'form']],
            "domain": [('is_supplier_audit', '=', True), ('partner_id','=',self.partner_id.gstd_partner_id.id)],
            "context": {'default_project_id': project.id, 'default_partner_id': self.partner_id.gstd_partner_id.id, 'default_is_supplier_audit': True},
            "name": "Audits"
        }

    @api.multi
    def action_open_cust_audits(self):
        """
        Abre las auditorías solicitadas por los clientes
        """
        self.ensure_one()
        return {
            "type": 'ir.actions.act_window',
            "res_model": 'project.task',
            "views": [[False, 'tree'], [False, 'form']],
            "domain": [('id', 'in', self.cust_audit_task_ids.ids)],
            "context": {},
            "name": "Customer Audits"
        }

    def _create_gstd_partner(self):
        """
        Crea el partner de GlobalSTD asociado a esta compania
        """
        gstd_partner = self.partner_id.copy({
            'name': self.partner_id.name,
            'company_type': 'company',
            'customer': True,
            'supplier': False,
            'company_id': 1,
            'gaudit_partner_id': self.partner_id.id
        })

        self.partner_id.write({
            'gstd_partner_id': gstd_partner.id
        })
