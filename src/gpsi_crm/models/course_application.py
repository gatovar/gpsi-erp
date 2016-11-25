# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class CourseParticipant(models.Model):
    """
    Modelo para el registro de participantes de un curso.
    """

    _name = 'gpsi.sale.application.course.participant'
    _description = 'Participant Course'

    course_id = fields.Many2one('gpsi.sale.application.course', 'Course', ondelete='restrict')
    email = fields.Char('Email')
    name = fields.Char('Name')
    position = fields.Char('Position')

    
class CourseApplication(models.Model):
    """
    Modelo para la aplicación de un curso.
    """
    _name = 'gpsi.sale.application.course'
    _description = 'Application Course'
    
    apartment_number = fields.Integer('Apartment Number')
    attention_to = fields.Char('Attention To')
    billing_phone = fields.Char('Billing Phone')
    billing_street = fields.Char('Street')
    billing_postal_code = fields.Char('Billing Postal Code')
    business_name = fields.Char('Business Name')
    city = fields.Char('City')
    shipping_city = fields.Char('Shipping City')
    billing_street2 = fields.Char('Billing Neighborhood')
    shipping_street2 = fields.Char('Shipping Neighborhood')
    company = fields.Char('Company')
    confirmation_date = fields.Date('Confirmation Date')
    confirmation_name = fields.Date('Confirmation Name')
    shipping_country_id = fields.Many2one("res.country", 'Country', ondelete='restrict')
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
    billing_location = fields.Char('Billing Location')
    billing_email = fields.Char('Billing Email')
    main_contact = fields.Char('Main Contact')
    name = fields.Char('Course Name')
    participant_ids = fields.One2many('gpsi.sale.application.course.participant', 'course_id', 'Participant')
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
    billing_state = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    shipping_state = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    billing_street_address = fields.Char('Billing Street Address')
    billing_township = fields.Char('BIlling Township')
    translator_needed = fields.Boolean('Translator Needed')
    applies_v = fields.Boolean('Applies')
    website_published = fields.Boolean('Website Published')
    zip_code = fields.Char('Zip Code')








