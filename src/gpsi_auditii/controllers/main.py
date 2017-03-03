import logging
import werkzeug
import openerp

from openerp import http
from openerp.http import request
from openerp.tools import safe_eval
from openerp.addons.web.controllers.main import Home

_logger = logging.getLogger(__name__)


class AuditiiController(http.Controller):
    @http.route('/ga/admin/signin', type='http', auth="none")
    def sign_in(self, redirect=None, **kw):
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate('demo', request.params['login'], request.params['password'])
            if uid is not False:
                request.params['login_success'] = True
                if not redirect:
                    redirect = '/ga/admin'
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
        return request.render('gpsi_auditii.admin/login', values)

    @http.route('/ga/admin/signup', type='http', methods=['POST'], auth="none")
    def sign_up(self, redirect=None, **kw):
        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None
        
        company = request.env['res.company'].sudo().create({
            'name': request.params['company'],
            'rml_header1': False,
            'email': request.params['email'],
            'currency_id': request.env['res.currency'].sudo().search([('name','=','USD')]).id
        })

        user = request.env['res.users'].sudo().create({
            'name': request.params['username'],
            'login': request.params['email'],
            'password': request.params['password'],
            'company_id': company.id,
            'company_ids': [(4, company.id, False)]
        })

        uid = request.session.authenticate('demo', request.params['email'], request.params['password'])
        if uid is not False:
            request.params['login_success'] = True
            if not redirect:
                redirect = '/ga/admin'
            return http.redirect_with_hash(redirect)

        return request.render('gpsi_auditii.admin/login', values)

    @http.route('/ga/admin/logout', type='http', auth="user")
    def logout(self):
        request.session.logout(keep_db=True)
        return werkzeug.utils.redirect('/ga/admin/signin', 303)

    @http.route('/ga/admin', type='http', auth="user")
    def dashboard(self, **kw):
        return request.render('gpsi_auditii.admin/dashboard')

    @http.route('/ga/admin/ca/contracts', type='http', auth="user")
    def ca_contracts(self, **kw):
        return request.render('gpsi_auditii.admin/ca/contracts')

    @http.route('/ga/admin/ca/contracts/<int:contract_id>', type='http', auth="user")
    def ca_contract(self, contract_id, **kw):
        return request.render('gpsi_auditii.admin/ca/contract')

    @http.route('/ga/admin/ca/events', type='http', auth="user")
    def ca_events(self, **kw):
        return request.render('gpsi_auditii.admin/ca/events')

    @http.route('/ga/admin/ca/events/<int:event_id>', type='http', auth="user")
    def ca_event(self, event_id, **kw):
        return request.render('gpsi_auditii.admin/ca/event')
