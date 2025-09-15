from odoo import http, fields
from odoo.http import request, Response
import json

class APIInlineKeyboard(http.Controller):

    @http.route(
        '/api/user/benefit/<int:telegram_id>/<int:benefit_id>/confirm',
        type='http', auth='public', methods=['POST'], csrf=False
    )
    def benefit_confirm(self, telegram_id, benefit_id):
        user = request.env['hr.employee'].sudo().search([('telegram_id', '=', telegram_id)], limit=1)
        benefit_usage = request.env['hr.employee.benefit.usage'].sudo().search([('employee_id', '=', user.id), ('benefit_id', '=', benefit_id), ('state', '=', 'submitted')], order="id desc", limit=1)
        benefit_usage_count = len(benefit_usage)
        if benefit_usage_count>=1:
            return Response(json.dumps({"error": "Sizda yuborilgan ariza mavjud!", "id": benefit_usage.id}), content_type="application/json", status=400)
            
        if not user:
            return Response(json.dumps({"error": "Foydalanuvchi topilmadi"}), content_type="application/json", status=404)

        usage = request.env['hr.employee.benefit.usage'].sudo().create({
            "id": benefit_usage.id,
            "employee_id": user.id,
            "benefit_id": benefit_id,
            "date_requested": fields.Datetime.now(),
            "state": 'submitted'
        })
        return Response(json.dumps({
            "message": "Tasdiqlash so‘rovi yuborildi",
            "usage_id": usage.id
        }))

    @http.route("/api/user/benefit/<int:telegram_id>/<int:benefit_id>/use", type='http', auth='public', methods=['POST'], csrf=False)
    def benfit_use(self, telegram_id, benefit_id):
        user = request.env['hr.employee'].sudo().search([('telegram_id', '=', telegram_id)], limit=1)
        benefit = request.env['hr.employee.benefit'].sudo().search([('id', '=', benefit_id)])
        benefit_usage_count = request.env['hr.employee.benefit.usage'].sudo().search_count([('employee_id', '=', user.id), ('benefit_id', '=', benefit_id), ('state', '=', 'no_confirmation_required')])
        if benefit_usage_count>=1:
            return Response(json.dumps({"message": "Sizda bu bonus faol mavjud!", 'approved_message': benefit.approved_message}), content_type="application/json", status=400)
        if not user:
            return {"error": "Foydalanuvchi topilmadi"}

        usage = request.env['hr.employee.benefit.usage'].sudo().create({
            "employee_id": user.id,
            "benefit_id": benefit_id,
            "date_requested": fields.Datetime.now(),
            "state": 'no_confirmation_required'
        })
        return Response(json.dumps({
            "message": "Foydalanishingiz mumkin:",
            "usage_id": usage.id,
            'guide': benefit.approved_message
        }))