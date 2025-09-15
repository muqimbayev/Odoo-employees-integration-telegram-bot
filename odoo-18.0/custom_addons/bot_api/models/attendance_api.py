from odoo import http, fields
from odoo.http import Response, request
import json
from datetime import datetime, timedelta

class AttadenceApi(http.Controller):
    @http.route('/api/user/attendance/<int:telegram_id>', type='http', methods=['GET'], auth='public', csrf=False)
    def user_attandance_today(self, telegram_id):
        user = request.env['hr.employee'].sudo().search([('telegram_id', '=', telegram_id)])
        today = fields.Date.today()
        attendance = request.env['hr.attendance'].sudo().search([
                    ('employee_id', '=', user.id),
                    ('check_in', '>=', today),
                    ('check_in', '<', today + timedelta(days=1))
                ])
        return Response(json.dumps(
                 {
                    "id": attendance.id,
                    "check_in": attendance.check_in.strftime('%d.%m.%Y %H:%M') if attendance.check_in else None,
                    "check_out": attendance.check_out.strftime('%d.%m.%Y %H:%M') if attendance.check_out else None,
                    "expected_hours": round(float(attendance.expected_hours), 2) if hasattr(attendance, 'expected_hours') else 0.0,
                    "worked_hours": round(float(attendance.worked_hours), 2) if hasattr(attendance, 'worked_hours') else 0.0,
                }           
                ), status=200, content_type="application/json")
