# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Supplier(models.Model):
    _inherit = 'res.partner'
    
    gstd_partner_id = fields.Many2one('res.partner', 'GStd Partner', help='GlobalSTD Partner')
    gaudit_partner_id = fields.Many2one('res.partner', 'GAudit Partner', help='GAudit Partner')
    aii_company_id = fields.Many2one('res.company', 'Auditii Company', help='Compañia auditii asociada con este proveedor')

    @api.model
    def create(self, vals):
        res = super(Supplier, self).create(vals)

        # Crea un partner asociado si este partner pertenece a una compañia GAudit
        if vals.get('create_gstd_partner', False) and res.company_id.is_gaudit and not res.gstd_partner_id:
            res._create_gstd_partner()
        return res

    def _create_gstd_partner(self):
        """
        Crea el partner de GlobalSTD asociado a este proveedor
        """
        partner = self.copy({
            'name': self.name,
            'company_type': 'company',
            'customer': True,
            'supplier': False,
            'gaudit_partner_id': self.id,
            'company_id': 1
        })

        self.write({
            'gstd_partner_id': partner.id
        })

    @api.model
    def find_gaudit_suppliers(self):
        return self.search([('parent_id','=',False), ('supplier','=',True), ('company_id','=', self.env.user.company_id.id)])
