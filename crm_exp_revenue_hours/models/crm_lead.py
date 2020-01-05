# Copyright 2013-2020 Open2Bizz <info@open2bizz.nl>
# License LGPL-3

from odoo import _, api, exceptions, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    planned_revenue_hours = fields.Float(string='Planned revenue in Hours',track_visibility='onchange')
    planned_revenue_product = fields.Many2one(
        comodel_name='product.product', string="Hour rate",
        domain="[('type', '=', 'service')]")

    planned_revenue_amount = fields.Monetary(
        compute='_compute_planned_revenue_amount', currency_field='company_currency',
    )

    @api.multi
    def _compute_planned_revenue_amount(self):
        """Calculate amount based on hours."""
        for lead in self:
            hourly_rate = lead.planned_revenue_product.list_price
            lead.planned_revenue_amount = lead.planned_revenue_hours * hourly_rate

    @api.onchange('planned_revenue_hours')
    def onchange_planned_revenue_hours(self):    
        for lead in self:
            if lead.planned_revenue_hours > 0:
                if lead.planned_revenue_product:
                    hourly_rate = lead.planned_revenue_product.list_price
                    lead.planned_revenue = lead.planned_revenue_hours * hourly_rate 
