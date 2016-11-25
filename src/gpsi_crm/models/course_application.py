# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class CourseParticipant(models.Model):
    """
    Modelo para el registro de participantes de un curso.
    """

    _name = 'gpsi.crm.application.course.participant'
    _description = 'Participant Course'

    course_id = fields.Many2one('gpsi.crm.application.course', 'Course', ondelete='restrict')
    email = fields.Char('Email')
    name = fields.Char('Name')
    position = fields.Char('Position')

    
class CourseApplication(models.Model):
    """
    Modelo para la aplicación de un curso.
    """
    
    _name = 'gpsi.crm.application.course'
    _description = 'Application Course'
    
    apartment_number = fields.Integer('Apartment Number')
    attention_to = fields.Char('Attention To')
    business_name = fields.Char('Business Name')
    city = fields.Char('City')
    company = fields.Char('Company')
    confirmation_date = fields.Date('Confirmation Date')
    confirmation_name = fields.Date('Confirmation Name')
    course_date = fields.Date('Course Date')
    course_fee = fields.Float('Course Fee')
    currency = fields.Selection(
        selection=[
            ('usd','USD'),
            ('mxn','MXN')], default='usd', string='Currency')
    customer_email = fields.Char('Customer Email')
    customer_organization = fields.Char('Customer Organization')
    customer_phone = fields.Char('Customer Phone')
    customer_position = fields.Char('Customer Position')
    disability_applies = fields.Boolean('Disability Applies')
    food_applies = fields.Boolean('Food Applies')
    impartition_location_site = fields.Char('Impartition Location Site')
    main_contact = fields.Char('Main Contact')
    name = fields.Char('Course Name')
    participant_ids = fields.One2many('gpsi.crm.application.course.participant', 'course_id', 'Participant')
    payment_type = fields.Selection(
        selection=[
            ('cash','Cash'),
            ('cheque','Cheque'),
            ('credit_card','Credit Card ( Master / Visa )'),
            ('wire_transfer','Wire Transfer'),
            ('bank_deposit','Bank Deposit')], default='cash', string='Payment Type')
    previous_information = fields.Boolean('It has pre-course information')
    purchase_order = fields.Char('Purchase Order')
    rfc = fields.Char('RFC')
    shipping_position = fields.Char('Shipping Position')
    shipping_state_id = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    shipping_city = fields.Char('Shipping City')
    shipping_street = fields.Char('Shipping Street')
    shipping_street2 = fields.Char('Shipping Street2')
    shipping_phone = fields.Char('Shipping Phone')
    shipping_country_id = fields.Many2one("res.country", 'Country', ondelete='restrict')
    shipping_zip_code = fields.Char('Shipping Zip Code')
    billing_phone = fields.Char('Billing Phone')
    billing_street = fields.Char('Billing Street')
    billing_street2 = fields.Char('Billing Street2')
    billing_township = fields.Char('BIlling Township')
    billing_location = fields.Char('Billing Location')
    billing_email = fields.Char('Billing Email')
    billing_state_id = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    billing_zip_code = fields.Char('Billing Zip Code')
    translator_needed = fields.Boolean('Translator Needed')
    travel_expenses_applies = fields.Boolean('Travel Expenses Applies')
    website_published = fields.Boolean('Website Published')
