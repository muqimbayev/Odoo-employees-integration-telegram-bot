from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    benefit_ids = fields.One2many(
        'hr.employee.benefit.usage',
        'employee_id',
        string="Benefits"
    )
    telegram_id = fields.Integer(string="Telegram ID", unique=True)
    months_worked = fields.Integer(string="Months Worked", compute='_compute_months_worked')
    appropriate_benefit_ids = fields.Many2many('hr.employee.benefit', compute='_compute_appropriate_benefit_ids')
    work_days = fields.Integer(string="Work days", compute='_compute_work_days')
    @api.depends()
    def _compute_months_worked(self):
        for employee in self:
            contract = self.env['hr.contract'].search([('employee_id', '=', employee.id), ('state', '=', 'open')])
            contract_date = contract.date_start
            today = fields.Date.today()
            if contract_date:
                months = (today.year - contract_date.year) * 12 + (today.month - contract_date.month)
                employee.months_worked = months
            else:
                employee.months_worked = 0

    
    @api.depends("months_worked")
    def _compute_appropriate_benefit_ids(self):
        for record in self:
            benefits = self.env["hr.employee.benefit"].search([("is_active", "=", True)])
            appropriate_benefits = []
            for b in benefits:
                count = self.env["hr.employee.benefit.usage"].search_count([
                    ("employee_id", "=", record.id),
                    ("benefit_id", "=", b.id),
                    ("state", "!=", "rejected"),
                ])

                eligibility_ok = (
                    (b.eligibility_start <= record.months_worked and b.eligibility_end >= record.months_worked)
                    or (b.eligibility_start <= record.months_worked and b.eligibility_end == 0)
                    or (b.eligibility_start == 0 and b.eligibility_end == 0)
                    or (b.eligibility_start == 0 and b.eligibility_end >= record.months_worked)
                )
                department_ok = not b.department_ids or record.department_id.id in b.department_ids.ids
                company_ok = not b.company_ids or record.company_id.id in b.company_ids.ids

                max_amount_ok = not b.max_amount or count < b.max_amount

                if eligibility_ok and department_ok and company_ok and max_amount_ok:
                    appropriate_benefits.append(b.id)

            record.appropriate_benefit_ids = [(6, 0, appropriate_benefits)]

    @api.depends()
    def _compute_work_days(self):
        today = fields.Date.today()
        for employee in self:
            contract = self.env['hr.contract'].search(
                [('employee_id', '=', employee.id), ('state', '=', 'open')],
                limit=1
            )
            if contract and contract.date_start:
                employee.work_days = (today - contract.date_start).days
            else:
                employee.work_days = 0