# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead']

    gs_is_cert = fields.Boolean('Certification')
    gs_cert_card_id = fields.Many2one('gpsi.crm.cert.card', 'Certification Card')


class CertificationCard(models.Model):
    '''
    Model para la aplicación de certificado.
    '''

    _name = 'gpsi.crm.cert.card'
    _description = 'Certification Card'
    _inherit = 'mail.thread'

    name = fields.Char('Name')
    facility_ids = fields.One2many('gpsi.crm.cert.card.site', 'cert_card_id', 'Facilities')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=24, change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    country_id = fields.Many2one('res.country', 'Country', ondelete='restrict')
    email = fields.Char('Email')
    phone1 = fields.Char('Phone 1')
    phone2 = fields.Char('Phone 2')
    website = fields.Char('Website', help='Website of Partner or Company')
    rfc = fields.Char('RFC')
    fiscal_address = fields.Char('Fiscal Address')
    contact_name = fields.Char('Name')
    contact_position = fields.Char('Job Position')
    contact_email1 = fields.Char('Email 1')
    contact_email2 = fields.Char('Email 2')
    standard_id = fields.Selection(selection=[('iso_9001:2008', 'ISO 9001:2008'), ('iso_9001:2015', 'ISO 9001:2015')], string='Standard')
    co_profile = fields.Selection(
        selection=[
            ('manufacture', 'Manufacture'),
            ('education', 'Education'),
            ('service', 'Service'),
            ('other', 'Other')], default='manufacture', string='Profile')
    co_profile_desc = fields.Text('Description')
    scope = fields.Text('Scope')
    apply_design = fields.Boolean('Apply Design')
    exclusions = fields.Text('Exclusions')
    certified = fields.Boolean('Certified')
    certified_desc = fields.Text('Certified Description')
    audit_type = fields.Selection(
        selection=[
            ('separated', 'Separated'), 
            ('combined', 'Combined'), 
            ('integrated', 'Integrated'), 
            ('mixed', 'Mixed')], default='separated', string='Audit Type')
    customers = fields.Char('Customers')
    suppliers = fields.Char('Suppliers')
    has_external_proc = fields.Boolean('External Process')
    external_proc = fields.Char('Name')
    external_proc_outsource = fields.Char('Outsourcing Name')
    has_consultant = fields.Boolean('Consultant')
    consultant_name = fields.Char('Name')
    consultant_phone = fields.Char('Phone')
    language = fields.Char('Language')
    good_practices = fields.Char('Good Practices')
    technologies = fields.Char('Technologies')
    company_know = fields.Char('Company Know')
    has_internal_audits = fields.Boolean('Internal Audits')
    has_management_reviews = fields.Boolean('Management Reviews')
    has_quality_manual = fields.Boolean('Quality Manual')
    preaudit_date = fields.Date('Pre-Audit Date')
    audit_stage1_date = fields.Date('Document Review Date')
    audit_stage2_date = fields.Date('Certification Audit')
    audit_surveillance1_date = fields.Date('Surveillance 1')
    audit_surveillance2_date = fields.Date('Surveillance 2')


class CertificationCardSite(models.Model):
    '''
    Sitio de certificación.
    '''
    
    _name = 'gpsi.crm.cert.card.site'
    _description = 'Site'

    cert_card_id = fields.Many2one('gpsi.crm.cert.card', 'Certification Card', ondelete="cascade")
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=24, change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    country_id = fields.Many2one('res.country', 'Country', ondelete='restrict')
    shift1 = fields.Integer('Shift 1')
    shift2 = fields.Integer('Shift 2')
    shift3 = fields.Integer('Shift 3')
    shift4 = fields.Integer('Shift 4')
    description = fields.Text('Description')
    