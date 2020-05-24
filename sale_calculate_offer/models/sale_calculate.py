# Copyright 2020 Open2Bizz <info@open2bizz.nl>
from odoo import api, fields, models

class SaleOrderCalculate(models.Model):
    _name = "sale.order.calculate"
    _description = "Sale Order calculate"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char('Name', required=True, index=True)
    sale_id = fields.Many2one('sale.order', required=True, string='Sale Quotation', track_visibility='onchange', track_sequence=1, index=True,
        help="Linked Sale Order")
    partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='onchange', track_sequence=1, index=True, related='sale_id.partner_id'
        help="Linked partner (from sale order)", readonly=True)
    active = fields.Boolean('Active', default=True, track_visibility=True)    
    team_id = fields.Many2one('crm.team', string='Sales Team', default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(user_id=self.env.uid),
        index=True, track_visibility='onchange', help='When sending mails, the default email address is taken from the Sales Team.')
    stage_id = fields.Many2one('crm.stage', string='Stage', ondelete='restrict', track_visibility='onchange', index=True, copy=False,
        domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
        group_expand='_read_group_stage_ids', default=lambda self: self._default_stage_id())
    calculate_users = fields.Integer("Count Users", help="Number of users")
    calculate_enterprise = fields.Boolean("Enterprise?", help="Is it Enterprise version Odoo")
    calculate_saas = fields.Boolean("SaaS?", help="Is it SaaS version?")
    calculate_saas_support = fields.Integer("Support Hours (per month)", help="Nr of hours support per month")
    calculate_modules_ids = fields.One2many('sale.order.calculate.modules', 'calculate_id', string='Module Lines', readonly=True, copy=True)
    total_hours = fields.Float(string='Total', store=True, readonly=True, compute='_compute_total_hours')

    @api.multi
    def _compute_total_hours(self, calculate_modules_ids):
        total = 0
        for line in calculate_modules_ids:
           total -= line['calculate_hours']
        return total

class SaleOrderCalculateModules(models.Model):
    _name = "sale.order.calculate.modules"
    _description = "Sale Order calculate Modules"
    _order = "calculate_id,sequence,id"

    calculate_id = fields.Many2one('sale.order.calculate', string='Calculate Order', track_sequence=1, index=True, required=True)
    sequence = fields.Integer(default=10, help="Gives the sequence of this line when displaying the Calculation.")
    module_id = fields.Many2one('ir.module.module', domain="[('application', '=', True)]", required=True)
    calculate_method_id = fields.Many2one('sale.order.calculate.method', string='Calculate Method', required=True)
    calculate_extra_factor = fields.Float('Extra Factor") 
    calculate_users = fields.Integer("Count Users", help="Number of users", related='calculate_id.calculate_users', readonly=True) 
    calculate_hours = fields.Float('Hours")
    calculate_price_module = fields.Monetary('Hours")

class SaleOrderCalculateMethod(models.Model):
    _name = "sale.order.calculate.method"
    _description = "Sale Order calculate method"

    name = field.Char('Name', required=True)
    method = field.Char('Method', required=True)
    active = fields.Boolean('Active', default=True)

