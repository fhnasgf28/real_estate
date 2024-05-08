from odoo import models, fields, api, _

class ResUsers(models.Model):
    _inherit = 'res.users'
    _description = 'Res User'

    property_ids = fields.One2many('estate.property', 'salesperson_id', string='Properties')
    # , domain = "[('salesperson_id', '!=', id)]"
