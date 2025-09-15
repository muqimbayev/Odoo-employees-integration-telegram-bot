from odoo import http
from odoo.http import request, Response
import json

class BenefitKeyboard(http.Controller):

    @http.route('/api/user/benefits/<int:telegram_id>', type="http", auth="public", methods=["GET"], csrf=False)
    def get_benefits_info(self, telegram_id):
        employee = request.env['hr.employee'].sudo().search([('telegram_id', '=', telegram_id)], limit=1)
        if employee:
            benefits = employee.appropriate_benefit_ids
            benefits_list = []
            for benefit in benefits:
                benefits_list.append({"id": benefit.id,
                                       "name": benefit.name,})
            return Response(
                json.dumps({"benefits": benefits_list}),
                status=200,
                content_type="application/json"
            )
        else:
            return Response(
                json.dumps({"error": "Foydalanuvchi topilmadi!"}),
                status=404,
                content_type="application/json"
            )

    @http.route('/api/user/benefit/<int:telegram_id>/<int:benefit_id>', type="http", auth="public", methods=["GET"], csrf=False)
    def get_benefit_info(self, telegram_id, benefit_id):
        employee = request.env['hr.employee'].sudo().search([('telegram_id', '=', telegram_id)], limit=1)
        if employee:
            benefit = employee.appropriate_benefit_ids.filtered(lambda b: b.id == benefit_id)
            if benefit:
                benefit = benefit[0]  
                data = {
                    "id": benefit.id,
                    "name": benefit.name,
                    "note": benefit.notes,
                    "type": benefit.benefit_type,
                    "max_amount": benefit.max_amount,
                    "period_use": dict(benefit._fields['period_use'].selection).get(benefit.period_use),
                    "period_days": benefit.period_use_days,
                    "requires_approval": benefit.requires_approval
                }
                return Response(
                    json.dumps(data, ensure_ascii=False),
                    status=200,
                    content_type="application/json"
                )
            else:
                return Response(
                    json.dumps({"error": "Imtiyoz topilmadi!"}),
                    status=404,
                    content_type="application/json"
                )
        else:
            return Response(
                json.dumps({"error": "Foydalanuvchi topilmadi!"}),
                status=404,
                content_type="application/json"
            )

    @http.route('/api/user/benefit/approved/<int:telegram_id>', type='http', methods=['GET'], auth='public', csrf=False)
    def benefit_approved(self, telegram_id):
        user = request.env['hr.employee'].sudo().search([('telegram_id', '=', telegram_id)])
        benefits = request.env['hr.employee.benefit.usage'].sudo().search([('employee_id', '=', user.id), ('state', '=', 'approved')])
        data = []
        for benefit in benefits:
            data.append({
                'id': benefit.id,
                'name': benefit.benefit_id.name,
                'date_requested': benefit.date_requested.strftime('%Y-%m-%d %H:%M:%S') if benefit.date_requested else None,
                'approved_date': benefit.approved_date.strftime('%Y-%m-%d %H:%M:%S') if benefit.approved_date else None,
                'type': benefit.benefit_id.benefit_type
            })
        return Response((json.dumps({"data": data})), status=200, content_type='application/json')
            
    @http.route('/api/user/benefit/petition/<int:telegram_id>', type='http', methods=['GET'], auth='public', csrf=False)
    def benefit_petition(self, telegram_id):
        user = request.env['hr.employee'].sudo().search([('telegram_id', '=', telegram_id)])
        benefits = request.env['hr.employee.benefit.usage'].sudo().search([('employee_id', '=', user.id), ('state', 'in', ['rejected' ,'approved', 'submitted'])])
        data = []
        for benefit in benefits:
            data.append({
                'id': benefit.id,
                'name': benefit.benefit_id.name,
                'state': benefit.state,
                'date_requested': benefit.date_requested.strftime('%Y-%m-%d %H:%M:%S') if benefit.date_requested else None,
                'rejection_reason': benefit.rejection_reason,
                'approved_date': benefit.approved_date.strftime('%Y-%m-%d %H:%M:%S') if benefit.approved_date else None,
            })
        return Response((json.dumps({"data": data})), status=200, content_type='application/json')
            
