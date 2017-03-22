import logging
import werkzeug
import openerp

from ..models.exception import AuditiiException

from openerp import http
from openerp.http import request
from openerp.exceptions import ValidationError
from openerp.tools import safe_eval
from openerp.addons.web.controllers.main import Home

_logger = logging.getLogger(__name__)


class AuditiiApiController(http.Controller):
    @http.route('/ga/api/logout', type='http', methods=['GET'], auth="user")
    def logout(self):
        request.session.logout(keep_db=True)
        return werkzeug.wrappers.Response(status=200)

    @http.route('/ga/api/settings/users', type='json', methods=['POST'], auth="none")
    def get_users(self, **kw):
        users = request.env['res.users'].sudo().search_read([('company_id','=',1)])
        return {
            'length': len(users),
            'records': users
        }

    @http.route('/ga/api/va/suppliers', type='json', methods=['GET'], auth="none")
    def get_va_suppliers(self, **kw):
        users = request.env['res.users'].sudo().search_read([('company_id','=',1)])
        return {
            'length': len(users),
            'records': users
        }

    @http.route('/ga/api/va/suppliers', type='json', methods=['PUT'], auth="none")
    def get_va_new_supplier(self, **kw):
        users = request.env['res.users'].sudo().search_read([('company_id','=',1)])
        return {
            'length': len(users),
            'records': users
        }
