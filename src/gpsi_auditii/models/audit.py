# -*- coding: utf-8 -*-
"""Control de auditoría de certificación
"""

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class AuditTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create_supplier_audit():
        pass
        
    @api.model
    def search_supplier_audits():
        """Busca las auditorías de proveedor solicitadas por el usuario actual.
        """
        result = self.search([('partner_id','=',None), ('is_supplier_audit','=',True)])

    @api.model
    def search_cert_audits():
        """Busca las auditorías de certificación solicitadas por el usuario actual.
        """
        pass
