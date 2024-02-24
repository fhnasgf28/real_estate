from odoo import models, fields, api


class Estate(models.Model):
    _name = 'estate.property'
    _description = 'Real estate property'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode', required=True, copy=False)
    date_availability = fields.Date(string='Date Availability')
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(string='Selling price')
    bedroom = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('N', 'North'),
        ('S', 'South'),
        ('E', 'East'),
        ('W', 'West'),
    ], help='Orientation of the garden on the property')
