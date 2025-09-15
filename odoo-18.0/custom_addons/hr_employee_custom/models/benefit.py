from odoo import fields, models, api

class HrEmployeeBenefit(models.Model):
    _name = 'hr.employee.benefit'
    _description = 'HR Employee Benefit'

    name = fields.Char(string="Benefit name", required=True)
    department_ids = fields.Many2many('hr.department', string="Departments")
    benefit_type = fields.Selection([
        ('health', 'Health Insurance'),
        ('transport', 'Transport'),
        ('meal', 'Meal Allowance'),
        ('bonus', 'Bonus'),
    ], string="Benefit Type", required=True)
    eligibility_start = fields.Integer(string="Eligibility Start (Months)")
    eligibility_end = fields.Integer(string="Eligibility End (Months)")
    is_active = fields.Boolean(string="Is Active", default=True)
    notes = fields.Text(string="Description")
    company_ids = fields.Many2many(
        'res.company',
        string="Company / Branch",
    )
    requires_approval = fields.Boolean(
        string="Requires Approval",
        default=True,
        help="If checked, this benefit must be approved before being granted."
    )
    max_amount = fields.Float(
        string="Maximum Amount",
        help="Maximum benefit amount. Leave empty or zero for unlimited."
    )
    approved_message = fields.Text(
        string="Message After Approval",
        help="This message will be sent automatically after the record is approved."
    )
    period_use = fields.Selection([
        ("one_time", "One time"),
        ("one_month", "One month"),
        ("one_year", "One year"),
        ("other", "Other"),
    ],string="Period use", required=True, default='one_time')
    period_use_days = fields.Integer(string="Period use days")

    count_submitted = fields.Integer(string="Number of Submitted", compute='_compute_count_state', default=0)
    count_approved = fields.Integer(string="Number of Approved", compute='_compute_count_state', default=0)
    count_rejected = fields.Integer(string="Number of Rejected", compute='_compute_count_state', default=0)

    @api.depends()
    def _compute_count_state(self):
        self.count_submitted = self.env['hr.employee.benefit.usage'].search_count([('state', '=', 'submitted'), ("benefit_id", "=", self.id)])
        self.count_approved = self.env['hr.employee.benefit.usage'].search_count([("state", "in", ['approved', 'no_confirmation_required']), ("benefit_id", "=", self.id)])
        self.count_rejected = self.env['hr.employee.benefit.usage'].search_count([('state', '=', 'rejected'), ("benefit_id", "=", self.id)])

    def count_submitted_button(self):
        return {
            "name": "Tasdiqlanishi kerak",
            "type": "ir.actions.act_window",
            "res_model": "hr.employee.benefit.usage",
            "view_mode": "list,form",
            "domain": [("state", "=", "submitted"), ("benefit_id", '=', self.id)],
        }

    def count_approved_button(self):
        return {
            "name": "Tasdiqlangan",
            "type": "ir.actions.act_window",
            "res_model": "hr.employee.benefit.usage",
            "view_mode": "list,form",
            "domain": [("state", "in", ['approved', 'no_confirmation_required']), ("benefit_id", '=', self.id)],
        }

    def count_rejected_button(self):
        return {
            "name": "Rad etilgan",
            "type": "ir.actions.act_window",
            "res_model": "hr.employee.benefit.usage",
            "view_mode": "list,form",
            "domain": [("state", "=", "rejected"), ("benefit_id", '=', self.id)],
        }



