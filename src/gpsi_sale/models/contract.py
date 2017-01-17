# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Standard(models.Model):
    _name = 'gpsi.sale.contract.standard'
    
    name = fields.Char('Name')
    

class Contract(models.Model):
    _inherit = 'sale.order'

    gs_is_contract = fields.Boolean('Is Contract', help='Indica que esta orden es un contrato GlobalSTD')
    gs_cycle = fields.Integer('Cycle')
    gs_standard_id = fields.Many2one('gpsi.sale.contract.standard', 'Standard')
    gs_code = fields.Char('Code')
    gs_apply_design = fields.Boolean('Apply Design')
    gs_is_multisite = fields.Boolean('Multisite')
    gs_is_multilocate = fields.Boolean('Multilocate')
    gs_block_contract = fields.Boolean('Block Contract')
    gs_need_bilingual_auditor = fields.Boolean('Bilingual Auditor')
    gs_risk_level = fields.Selection([('low','Low'), ('medium','Medium'), ('high','High'), ('lim','Lim')], 'Risk Level')
    gs_certification_type = fields.Selection([('initial', 'Initial')], 'Certification Type')
    gs_scheme = fields.Selection([('mixed', 'Mixed'), ('annual', 'Annual')], 'Scheme')
    gs_duration = fields.Selection([('1year', '1 Year'), ('2year', '2 Year'), ('3year', '3 Year')], 'Duration')
    gs_scope = fields.Text('Scope')
    gs_expiration_date = fields.Date('Expiration Date')
    gs_certificate_status = fields.Selection([('active', 'Active'), ('expired', 'Expired'), ('suspended', 'Suspended'), ('canceled', 'Canceled')], 
        'Certificate Status')
    
    gs_responsible_id = fields.Many2one('res.partner', 'Responsible')
    gs_notes = fields.Text(default='Nota 1: Cuando aplique, adicional a estos costos serán facturados al cliente los eventos de auditorías especiales y cierre de “No Conformidades en sitio” (instalaciones de cliente) conforme a los términos y condiciones pactados en este contrato. \n Nota 2: Cuando aplique, adicional a estos costos serán facturados al cliente los viáticos relacionados con la ejecución de los eventos de auditoría.', string='Notes')
    gs_special_conditions = fields.Text('Special Conditions')
    gs_approval_date = fields.Date('Approval Date')

    gs_audit_date = fields.Date('Audit Date')

