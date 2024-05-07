from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    delivery_order = fields.Date(string='Date')
    # , domain = "[('salesperson_id', '!=', id)]"
    
    def action_confirm(self):
        super(SaleOrder, self).action_confirm()