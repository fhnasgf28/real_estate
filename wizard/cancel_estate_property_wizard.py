from odoo import models, fields, api


class EstatePropertyTag(models.TransientModel):
    _name = 'cancel.estate.property.wizard'
    _description = 'Real estate property tag'

    selling_price = fields.Float(string='Selling price')
    bedroom = fields.Integer(string='Bedrooms', default=2)