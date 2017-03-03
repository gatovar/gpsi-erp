# -*- coding: utf-8 -*-

import logging
import werkzeug
import openerp

from openerp import http
from openerp.http import request

_logger = logging.getLogger(__name__)


class AuditController(http.Controller):
    @http.route('/gpsi/staff/audits/<int:audit_id>/assessment', type='http', auth="user")
    def edit_assessment(self, audit_id, **kw):
        if request.httprequest.method == 'POST':
            Line = request.env['gpsi.staff.audit.chk.line']
            Field = request.env['gpsi.staff.audit.chk.field']
            for key in kw:
                if 'field$$' in key:
                    field = Field.search([('id','=',int(key[7:]))])
                    if field.typ == 'boolean':
                        field.write({'b_value': bool(kw[key])})
                    elif field.typ == 'char':
                        field.write({'c_value': kw[key]})
                    elif field.typ == 'int':
                        field.write({'i_value': int(kw[key])})
                    elif field.typ == 'float':
                        field.write({'f_value': float(kw[key])})
                    elif field.typ == 'date':
                        field.d_value = False
                    elif field.typ == 'text':
                        field.write({'t_value': kw[key]})
                    elif field.typ == 'html':
                        field.write({'h_value': kw[key]})
                if 'line_score_id$$' in key:
                    line = Line.search([('id','=',int(key[15:]))])
                    line.write({'score_id': int(kw[key])})

        audit = request.env['gpsi.staff.audit'].sudo().search([('id','=',audit_id)])
        qcontext = {
            'audit': audit,
            'assessment': audit.asst_id
        }
        return request.render(audit.asst_id.view_id.xml_id, qcontext)
