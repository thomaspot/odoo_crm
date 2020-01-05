# Copyright 2013-2020 Open2Bizz <info@open2bizz.nl>
# License LGPL-3

from odoo import _, api, exceptions, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    planned_revenue_hours = fields.float(string='Planned revenue in Hours')
    planned_revenue_product = fields.Many2many(
        comodel_name='product.product', string="Hour rate",
        domain="[('type', '=', 'service')]")

    planned_revenue_amount = fields.float(
        compute='_compute_planned_revenue_amount',
    )

    @api.multi
    def _compute_planned_revenue_amount(self):
        """Calculate amount based on hours."""
        for lead in self:
	    hourly_rate = lead.planned_revenue_product.list_price
            lead.planned_revenue_amount = lead.planned_revenue_hours * hourly_rate
