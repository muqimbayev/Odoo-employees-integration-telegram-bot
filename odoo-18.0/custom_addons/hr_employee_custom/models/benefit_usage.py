from odoo import fields, models, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class HrEmployeeBenefitUsage(models.Model):
    _name = 'hr.employee.benefit.usage'
    _description = 'Employee Benefit Usage'

    def _compute_display_name(self):
        for record in self:
            if record.employee_id and record.state:
                record.display_name = f"{record.employee_id.name} ({record.state})"
            else:
                record.display_name = record.employee_id.name or super()._compute_display_name()

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    benefit_id = fields.Many2one('hr.employee.benefit', string="Benefit", required=True)
    date_requested = fields.Datetime(string="Request Date", default=fields.Datetime.now())
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('stoped', 'Stoped'),
        ("no_confirmation_required", "No confirmation required")
    ], string="Status", default='draft', tracking=True, required=True)
    stoped_date = fields.Datetime(string="Stoped Date", compute="_compute_stoped_date")
    approved_by = fields.Many2one('res.users', string="Approved By", default=lambda self: self.env.user.id)
    approved_date = fields.Datetime(string="Approved Date", default=fields.Datetime.now())
    rejection_reason = fields.Text(string="Rejection Reason")
    approved_message = fields.Text(string="Approved Message")

    @api.onchange("benefit_id")
    def _onchange_benefit_id(self):
        if self.benefit_id and not self.approved_message:
            self.approved_message = self.benefit_id.approved_message

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('state') == 'rejected' and not vals.get('rejection_reason'):
                raise ValidationError("Rejection Reason cannot be empty")
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            new_state = vals.get("state", record.state)
            new_reason = vals.get("rejection_reason", record.rejection_reason)
            if new_state == "rejected" and not new_reason:
                raise ValidationError("Rejection Reason cannot be empty")
        return super().write(vals)
