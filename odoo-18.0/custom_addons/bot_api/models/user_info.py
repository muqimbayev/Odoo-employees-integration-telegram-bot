from odoo import http
from odoo.http import request, Response
import json

class InfoApi(http.Controller):

    @http.route('/api/user/info/<int:telegram_id>', type="http", auth="public", methods=["GET"], csrf=False)
    def get_user_info(self, telegram_id):
        employee = request.env['hr.employee'].sudo().search([('telegram_id', '=', telegram_id)], limit=1)
        if employee:
            return Response(
                json.dumps({
                    "id": employee.id,
                    "name": employee.name,
                    "birth_date": str(employee.birthday) if employee.birthday else None,
                    "work_days": employee.work_days or 0,
                    "position": employee.job_id.name if employee.job_id else None,
                    "department": employee.department_id.name if employee.department_id else None,
                    "department_head": employee.department_id.manager_id.name if employee.department_id else None,
                    "contract_date": str(employee.contract_id.date_start) if employee.contract_id else None,
                    "phone": employee.phone or None,

                }),
                status=200,
                content_type="application/json"
            )
        else:
            return Response(
                json.dumps({"error": "Foydalanuvchi topilmadi!"}),
                status=404,
                content_type="application/json"
            )

