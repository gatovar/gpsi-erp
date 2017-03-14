# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError

CERT_TYPES = [
    ('initial', 'Initial'),
    ('recert', 'Recertification'),
    ('takeover', 'Takeover')]

SCHEME_TYPES = [
    ('annual', 'Annual'),
    ('biannual', 'Biannual')]

RISK_LVL_TYPES = [
    ('low', 'Low'),
    ('normal', 'Normal'),
    ('high', 'High'),
    ('vhigh', 'Very High')]

DURATION_TYPES = [
    ('1', '1 Year'), 
    ('2', '2 Years'),
    ('3', '3 Years')]


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    is_cert_order = fields.Boolean('Certification Order')
    cert_contract_id = fields.Many2one('gpsi.sale.contract', 'Contract')


class Contract(models.Model):
    _name = 'gpsi.sale.contract'
    _description = 'Contract'

    cert_type = fields.Selection(CERT_TYPES, 'Certification Type', CAR_STAGES[0][0])
    standard = fields.Many2one('gpsi.sale.contract.standard', 'Standard')
    empl_count = fields.Integer('Employees')
    risk_lvl = fields.Selection(RISK_LVL_TYPES, 'Risk Level', RISK_LVL_TYPES[0][0])
    apply_dsgn = fields.Boolean('Apply Design')
    multisite = fields.Boolean('Multisite')
    multilocate = fields.Boolean('Multilocate')
    bil_auditor = fields.Boolean('Bilingual Auditor')
    scheme = fields.Selection(SCHEME_TYPES, 'Scheme', SCHEME_TYPES[0][0])
    duration = fields.Selection(DURATION_TYPES, 'Duration', DURATION_TYPES[0][0])
    site_ids = fields.Many2many('gpsi.sale.contract.site', 'gpsi_sale_contract_site_rel', 'contract_id', 'site_id', 'Sites')
    notes = fields.Html('Notes')


class ContractSite(models.Model):
    _name = 'gpsi.sale.contract.site'
    _description = 'Site'

    partner_id = fields.Many2one('res.partner', 'Contact', domain=[('parent_id','!=',False)])
    empl_count = fields.Integer('Employees')


class ContractStandard(models.Model):
    _name = 'gpsi.sale.contract.standard'
    _description = 'Standard'

    name = fields.Char('Code')
    desc = fields.Char('Description')
